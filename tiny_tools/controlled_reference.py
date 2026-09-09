from __future__ import annotations

import argparse
import csv
import json
import platform
import subprocess
import sys
from pathlib import Path

import numpy as np

from coffee_brain.actions import ACTION_NAMES, RoutineActions
from coffee_brain.config import ARCHITECTURE_VERSION
from coffee_brain.memory import shared_context_input
from coffee_brain.model import MODE_NAMES, RoutineMode, relationship_index
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario
from tiny_tools.simulate import STATE_KEYS, generate_truth, observe


DEFAULT_DAYS = 96
DEFAULT_PARTICLES = 1200
DEFAULT_SEED = 20260908
ACTION_GRAMMAR_VERSION = "1"

ACTION_GRAMMAR = {
    "ordinary-opt-in": RoutineActions(
        a_invite=1.0,
        a_deliver=1.0,
        a_notify=1.0,
        b_opt_in=1.0,
        b_acknowledge=1.0,
        b_closure=1.0,
    ),
    "callback-opt-in": RoutineActions(
        a_invite=1.0,
        a_deliver=1.0,
        a_notify=1.0,
        a_callback=1.0,
        b_opt_in=1.0,
        b_acknowledge=1.0,
        b_closure=1.0,
    ),
    "voluntary-pass": RoutineActions(
        a_invite=1.0,
        a_boundary_preserving=1.0,
        b_pass_choice=1.0,
        b_closure=1.0,
    ),
    "coordinated-exception": RoutineActions(
        a_notify=1.0,
        a_boundary_preserving=1.0,
        b_exception_sync=1.0,
    ),
    "recovery-return": RoutineActions(
        a_invite=1.0,
        a_deliver=1.0,
        a_notify=1.0,
        a_callback=1.0,
        b_opt_in=1.0,
        b_acknowledge=1.0,
        b_closure=1.0,
    ),
    "quiet": RoutineActions(),
}

ACTION_CYCLE = (
    "ordinary-opt-in",
    "ordinary-opt-in",
    "callback-opt-in",
    "voluntary-pass",
    "quiet",
    "coordinated-exception",
    "quiet",
    "recovery-return",
    "ordinary-opt-in",
    "callback-opt-in",
    "quiet",
    "ordinary-opt-in",
)


def build_action_schedule(days: int) -> tuple[list[str], list[RoutineActions]]:
    """Repeat one small generic action grammar without person-specific ontology. 🎮☕"""

    if days < 2:
        raise ValueError("🐾 Controlled reference needs at least two synthetic days.")
    labels = [ACTION_CYCLE[t % len(ACTION_CYCLE)] for t in range(days)]
    actions = [ACTION_GRAMMAR[label] for label in labels]
    return labels, actions


def controlled_observation(
    base: dict,
    actions: RoutineActions,
    phase: str,
) -> dict:
    """Keep overlapping protocol clues consistent with the declared known controls. 🧭☕

    The stochastic observation model still supplies the other clues. Scheduled actions
    only pin channels that would otherwise contradict the controlled experiment.
    """

    obs = dict(base)
    invite = int(actions.a_invite >= 0.5)
    opt_in = int(actions.b_opt_in >= 0.5)
    pass_event = int(actions.b_pass_choice >= 0.5)
    if opt_in and pass_event:
        raise ValueError("🐾 Controlled grammar cannot opt in and pass on the same step.")
    if (opt_in or pass_event) and not invite:
        raise ValueError("🐾 Controlled opt-in/pass needs a declared invitation.")

    obs["invite"] = invite
    obs["opt_in"] = opt_in
    obs["pass_event"] = pass_event
    obs["routine_maintenance"] = int(actions.a_deliver >= 0.5 and opt_in)

    scheduled_reply = any(
        value >= 0.5
        for value in (
            actions.b_opt_in,
            actions.b_pass_choice,
            actions.b_acknowledge,
            actions.b_exception_sync,
            actions.b_closure,
        )
    )
    if scheduled_reply:
        obs["text_reply"] = 1
    if actions.b_acknowledge >= 0.5:
        obs["reaction"] = 1
    if actions.b_exception_sync >= 0.5:
        obs["proactive_update"] = 1
    if phase == "recovery-return":
        obs["resume_signal"] = 1
    if not int(obs["text_reply"]):
        obs["response_delay_min"] = None

    return obs


def _safe_pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _run_filter(
    observations: list[dict],
    actions: list[RoutineActions],
    *,
    particle_count: int,
    seed: int,
    action_aware: bool,
) -> dict[str, object]:
    pf = CoffeeParticleFilter(particle_count=particle_count, seed=seed)
    estimates: list[np.ndarray] = []
    low: list[np.ndarray] = []
    high: list[np.ndarray] = []
    modes: list[str] = []
    ess: list[float] = []

    for t, obs in enumerate(observations):
        # Temporal contract: action[t-1] moves the previous state into state[t].
        # The first update has no previous transition, so no control is supplied. 🎮⏱️
        transition_actions = actions[t - 1] if action_aware and t > 0 else None
        posterior = pf.update(obs, actions=transition_actions)
        estimates.append(posterior.mean)
        low.append(posterior.ci95_low)
        high.append(posterior.ci95_high)
        modes.append(posterior.mode)
        ess.append(posterior.ess)

    return {
        "estimates": np.asarray(estimates, dtype=float),
        "low": np.asarray(low, dtype=float),
        "high": np.asarray(high, dtype=float),
        "modes": modes,
        "ess": np.asarray(ess, dtype=float),
    }


def _score_rows(
    candidate: str,
    truth: np.ndarray,
    result: dict[str, object],
) -> list[dict[str, object]]:
    estimates = np.asarray(result["estimates"], dtype=float)
    low = np.asarray(result["low"], dtype=float)
    high = np.asarray(result["high"], dtype=float)
    rows: list[dict[str, object]] = []
    metric_names = (
        "P_predictability",
        "M_mutuality",
        "V_voluntariness",
        "C_shared_context",
        "E_state_sharing",
        "F_friction",
    )
    for j, name in enumerate(metric_names):
        error = estimates[:, j] - truth[:, j]
        rows.append(
            {
                "candidate": candidate,
                "metric_scope": name,
                "bias": float(np.mean(error)),
                "RMSE": float(np.sqrt(np.mean(error * error))),
                "MAE": float(np.mean(np.abs(error))),
                "Pearson_r": _safe_pearson(estimates[:, j], truth[:, j]),
                "CI95_coverage": float(np.mean((truth[:, j] >= low[:, j]) & (truth[:, j] <= high[:, j]))),
            }
        )
    return rows


def _source_revision() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        )
        return result.stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "unknown"


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_controlled_reference(
    *,
    days: int,
    particles: int,
    seed: int,
    scenario_slug: str,
    out: Path,
) -> dict[str, object]:
    scenario = get_scenario(scenario_slug)
    phases, actions = build_action_schedule(days)

    rng = np.random.default_rng(seed)
    truth, true_modes = generate_truth(days, rng, scenario, actions=actions)
    observations = [
        controlled_observation(observe(truth[t], true_modes[t], rng, scenario), actions[t], phases[t])
        for t in range(days)
    ]

    aware = _run_filter(
        observations,
        actions,
        particle_count=particles,
        seed=seed,
        action_aware=True,
    )
    blind = _run_filter(
        observations,
        actions,
        particle_count=particles,
        seed=seed,
        action_aware=False,
    )

    aware_est = np.asarray(aware["estimates"], dtype=float)
    blind_est = np.asarray(blind["estimates"], dtype=float)
    aware_r = relationship_index(aware_est)
    blind_r = relationship_index(blind_est)
    true_r = relationship_index(truth)

    score_rows = _score_rows("action-aware", truth, aware) + _score_rows("action-blind", truth, blind)

    excitation_rows: list[dict[str, object]] = []
    for j, name in enumerate(STATE_KEYS):
        excitation_rows.append(
            {
                "state": name,
                "truth_min": float(np.min(truth[:, j])),
                "truth_max": float(np.max(truth[:, j])),
                "truth_mean": float(np.mean(truth[:, j])),
                "truth_std": float(np.std(truth[:, j])),
                "truth_span": float(np.ptp(truth[:, j])),
                "action_aware_est_std": float(np.std(aware_est[:, j])),
                "action_blind_est_std": float(np.std(blind_est[:, j])),
            }
        )

    action_rows: list[dict[str, object]] = []
    for t, (phase, basket) in enumerate(zip(phases, actions), 1):
        row: dict[str, object] = {
            "day": t,
            "phase": phase,
            "shared_context_input": shared_context_input(basket),
        }
        row.update({name: float(getattr(basket, name)) for name in ACTION_NAMES})
        action_rows.append(row)

    input_rows = [
        {"day": t + 1, "phase": phases[t], **observations[t]}
        for t in range(days)
    ]

    output_rows: list[dict[str, object]] = []
    aware_low = np.asarray(aware["low"], dtype=float)
    aware_high = np.asarray(aware["high"], dtype=float)
    blind_low = np.asarray(blind["low"], dtype=float)
    blind_high = np.asarray(blind["high"], dtype=float)
    aware_ess = np.asarray(aware["ess"], dtype=float)
    blind_ess = np.asarray(blind["ess"], dtype=float)
    aware_modes = list(aware["modes"])
    blind_modes = list(blind["modes"])

    for t in range(days):
        row: dict[str, object] = {
            "day": t + 1,
            "phase": phases[t],
            "true_mode": MODE_NAMES[RoutineMode(int(true_modes[t]))],
            "action_aware_mode": aware_modes[t],
            "action_blind_mode": blind_modes[t],
            "action_aware_ESS": float(aware_ess[t]),
            "action_blind_ESS": float(blind_ess[t]),
            "true_R": float(true_r[t]),
            "action_aware_R": float(aware_r[t]),
            "action_blind_R": float(blind_r[t]),
        }
        for j, name in enumerate(STATE_KEYS):
            row[f"true_{name}"] = float(truth[t, j])
            row[f"action_aware_est_{name}"] = float(aware_est[t, j])
            row[f"action_aware_ci95_low_{name}"] = float(aware_low[t, j])
            row[f"action_aware_ci95_high_{name}"] = float(aware_high[t, j])
            row[f"action_blind_est_{name}"] = float(blind_est[t, j])
            row[f"action_blind_ci95_low_{name}"] = float(blind_low[t, j])
            row[f"action_blind_ci95_high_{name}"] = float(blind_high[t, j])
        output_rows.append(row)

    true_mode_names = [MODE_NAMES[RoutineMode(int(mode))] for mode in true_modes]
    summary_rows = []
    for candidate, result, candidate_r in (
        ("action-aware", aware, aware_r),
        ("action-blind", blind, blind_r),
    ):
        result_modes = list(result["modes"])
        summary_rows.append(
            {
                "candidate": candidate,
                "demo_index_RMSE": float(np.sqrt(np.mean((candidate_r - true_r) ** 2))),
                "demo_index_Pearson_r": _safe_pearson(candidate_r, true_r),
                "mode_accuracy": float(np.mean([a == b for a, b in zip(result_modes, true_mode_names)])),
                "mean_ESS": float(np.mean(np.asarray(result["ess"], dtype=float))),
            }
        )

    scope_rows = [
        {"key": "reference_scope", "value": "separate controlled action-aware synthetic reference"},
        {"key": "observation_only_baseline_mutated", "value": "false"},
        {"key": "truth_actions_supplied", "value": "true"},
        {"key": "particle_filter_actions_supplied", "value": "true"},
        {"key": "controlled_transition_path_exercised", "value": "true"},
        {"key": "shared_context_action_accumulation_exercised", "value": "true"},
        {"key": "temporal_alignment", "value": "action[t-1] drives transition into state[t]; first update gets no action"},
        {"key": "person_specific_ontology", "value": "false"},
        {"key": "human_validation_claim", "value": "false"},
    ]

    out.mkdir(parents=True, exist_ok=True)
    _write_rows(out / "action-schedule.csv", action_rows)
    _write_rows(out / "input.csv", input_rows)
    _write_rows(out / "output.csv", output_rows)
    _write_rows(out / "scorecard.csv", score_rows)
    _write_rows(out / "state-excitation.csv", excitation_rows)
    _write_rows(out / "summary.csv", summary_rows)
    _write_rows(out / "scope.csv", scope_rows)

    recipe = {
        "action_cycle": list(ACTION_CYCLE),
        "action_grammar_version": ACTION_GRAMMAR_VERSION,
        "architecture_version": ARCHITECTURE_VERSION,
        "days": days,
        "environment": {
            "numpy_version": np.__version__,
            "platform": platform.platform(),
            "python_implementation": platform.python_implementation(),
            "python_version": sys.version.split()[0],
        },
        "particle_count": particles,
        "reference_scope": "separate controlled action-aware synthetic reference",
        "scenario": scenario.slug,
        "seed": seed,
        "source_revision": _source_revision(),
        "temporal_alignment": "action[t-1] drives transition into state[t]; first update gets no action",
    }
    (out / "recipe.json").write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    c_aware = next(row for row in score_rows if row["candidate"] == "action-aware" and row["metric_scope"] == "C_shared_context")
    c_blind = next(row for row in score_rows if row["candidate"] == "action-blind" and row["metric_scope"] == "C_shared_context")
    c_excitation = next(row for row in excitation_rows if row["state"] == "C")
    memory_inputs = np.asarray([row["shared_context_input"] for row in action_rows], dtype=float)

    print("🎮☕ Controlled action-aware reference")
    print(f"🐣 synthetic days              : {days}")
    print(f"🎮 nonzero action days         : {sum(any(getattr(a, name) > 0 for name in ACTION_NAMES) for a in actions)}")
    print(f"🧠 mean Shared Context input   : {float(np.mean(memory_inputs)):.3f}")
    print(f"🌱 truth C span                : {float(c_excitation['truth_span']):.3f}")
    print(f"🎯 action-aware C RMSE / r     : {float(c_aware['RMSE']):.3f} / {float(c_aware['Pearson_r']):.3f}")
    print(f"🙈 action-blind C RMSE / r     : {float(c_blind['RMSE']):.3f} / {float(c_blind['Pearson_r']):.3f}")
    print(f"🧺 controlled reference basket : {out}")
    print("☕ Known controls exercise the transition path; they do not turn synthetic validation into human truth.")

    return {
        "scorecard": score_rows,
        "state_excitation": excitation_rows,
        "summary": summary_rows,
        "scope": scope_rows,
    }


def parse_args():
    parser = argparse.ArgumentParser(description="Run the separate controlled action-aware coffee reference. 🎮☕🐣")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--scenario", default=DEFAULT_SCENARIO)
    parser.add_argument("--out", type=Path, default=Path("examples/controlled-cute-days"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 2:
        raise SystemExit("🐾 Controlled reference needs at least two synthetic days.")
    if args.particles < 100:
        raise SystemExit("🐣 Controlled reference needs at least 100 particles.")
    run_controlled_reference(
        days=args.days,
        particles=args.particles,
        seed=args.seed,
        scenario_slug=args.scenario,
        out=args.out,
    )


if __name__ == "__main__":
    main()
