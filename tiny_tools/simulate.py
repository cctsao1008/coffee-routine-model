from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path
from typing import Sequence

import numpy as np

from coffee_brain.actions import RoutineActions, action_effect
from coffee_brain.memory import (
    DEFAULT_SHARED_CONTEXT_MEMORY,
    SharedContextMemoryConfig,
    shared_context_input,
    shared_context_step,
)
from coffee_brain.model import MODE_NAMES, RoutineMode, relationship_index
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import DEFAULT_SCENARIO, CoffeeScenario, get_scenario, scenario_names


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 365
DEFAULT_PARTICLES = 6000
STATE_KEYS = ("P", "M", "V", "C", "E", "F")
STATE_METRIC_NAMES = (
    "P_predictability",
    "M_mutuality",
    "V_voluntariness",
    "C_shared_context",
    "E_state_sharing",
    "F_friction",
)


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def _wiggle(logit: float, scenario: CoffeeScenario, rng: np.random.Generator) -> float:
    """Add scenario-specific observation wiggle without teaching the estimator the answer key. 🌪️🐣"""

    if scenario.logit_noise_sigma <= 0.0:
        return logit
    return float(logit + rng.normal(0.0, scenario.logit_noise_sigma))


def generate_truth(
    days: int,
    rng: np.random.Generator,
    scenario: CoffeeScenario,
    actions: Sequence[RoutineActions] | None = None,
    memory_config: SharedContextMemoryConfig = DEFAULT_SHARED_CONTEXT_MEMORY,
):
    """Grow one synthetic coffee timeline inside the selected tiny universe. ☕🌱

    When an action schedule is supplied, action ``t-1`` nudges the transition into
    state ``t``. Shared Context uses its own slow accumulation / decay law instead of
    behaving like a daily mood. With no schedule, the memory reservoir simply has a
    quiet day and decays gently. 🧠🌱
    """

    if actions is not None and len(actions) != days:
        raise ValueError("🎮🐾 Action schedule must have one tiny basket per synthetic day.")

    action_schedule = actions if actions is not None else [RoutineActions() for _ in range(days)]
    states = np.zeros((days, 6))
    modes = np.zeros(days, dtype=int)
    states[0] = [0.78, 0.68, 0.88, 0.70, 0.36, 0.14]

    for t in range(1, days):
        modes[t] = rng.choice(5, p=scenario.transition[modes[t - 1]])
        mode_effect = np.array(scenario.mode_effects[modes[t]], dtype=float, copy=True)
        mode_effect[3] = 0.0
        controlled_effect = action_effect(action_schedule[t - 1])
        process_noise = rng.normal(0.0, scenario.process_noise)
        process_noise[3] = 0.0

        mean_reversion = scenario.mean_reversion * (scenario.target - states[t - 1])
        mean_reversion[3] = 0.0
        proposal = states[t - 1] + mean_reversion + mode_effect + controlled_effect + process_noise
        proposal[3] = shared_context_step(
            states[t - 1, 3],
            shared_context_input(action_schedule[t - 1]),
            config=memory_config,
            noise=rng.normal(0.0, memory_config.process_noise),
        )
        states[t] = np.clip(proposal, 0.02, 0.98)

    return states, modes


def _validate_protocol_clues(observation: dict) -> None:
    """Keep the synthetic exam inside the observable protocol grammar. ☕🧭"""

    invite = int(observation["invite"])
    opt_in = int(observation["opt_in"])
    text_reply = int(observation["text_reply"])
    maintenance = int(observation["routine_maintenance"])
    pass_event = int(observation["pass_event"])

    if not invite and (opt_in or pass_event):
        raise ValueError("🐾 Synthetic opt-in/pass needs an invitation opportunity.")
    if opt_in and pass_event:
        raise ValueError("🐾 Synthetic opt-in and pass cannot be the same reply choice.")
    if (opt_in or pass_event) and not text_reply:
        raise ValueError("🐾 Synthetic opt-in/pass is itself an observed reply.")
    if maintenance and not opt_in:
        raise ValueError("🐾 Delivered-coffee maintenance needs an explicit synthetic opt-in.")


def observe(x, mode, rng, scenario: CoffeeScenario):
    """Turn one hidden synthetic state into tiny behavior-level clues. 👀☕

    The hidden-world Bernoulli recipes are intentionally approximate, but the final
    observable basket still obeys the public protocol grammar. The simulator may
    disagree with the estimator; it should not contradict itself. 🧭🐣
    """

    p, m, v, c, e, f = x
    invite = int(mode != RoutineMode.LEAVE and rng.random() < scenario.invite_probability)

    mode_opt = {0: 0.0, 1: -0.7, 2: -2.5, 3: 0.2, 4: 0.15}[int(mode)]
    opt_logit = _wiggle(
        -1.2 + 1.7 * m + 1.2 * v + 0.8 * p - 1.8 * f + mode_opt + scenario.opt_in_bias,
        scenario,
        rng,
    )
    opt_in = int(invite and rng.random() < sigmoid(opt_logit))

    text_logit = _wiggle(
        -0.7 + 1.1 * m + 0.6 * c + 0.3 * e - 0.8 * f
        + 0.2 * (mode == RoutineMode.SPECIAL) - 0.2 * (mode == RoutineMode.BUSY)
        + scenario.text_reply_bias,
        scenario,
        rng,
    )
    text_reply = int(rng.random() < sigmoid(text_logit))

    reaction_logit = _wiggle(
        -0.6 + 0.9 * m + 0.5 * p + 0.4 * v - 0.5 * f + scenario.reaction_bias,
        scenario,
        rng,
    )
    reaction = int(rng.random() < sigmoid(reaction_logit))

    share_logit = _wiggle(
        -2.2 + 2.0 * e + 0.8 * c + 0.3 * m - 0.3 * (mode == RoutineMode.BUSY)
        + scenario.state_share_bias,
        scenario,
        rng,
    )
    state_share = int(rng.random() < sigmoid(share_logit))

    update_logit = _wiggle(
        -1.8 + 1.3 * m + 0.8 * c + 0.5 * e - 0.6 * f
        + 0.45 * (mode in (RoutineMode.BUSY, RoutineMode.LEAVE))
        + scenario.proactive_update_bias,
        scenario,
        rng,
    )
    proactive_update = int(rng.random() < sigmoid(update_logit))

    mode_maint = {0: 0.0, 1: -0.3, 2: -1.4, 3: 0.3, 4: 0.6}[int(mode)]
    maint_logit = _wiggle(
        -1.1 + 1.5 * p + 1.4 * m + 0.9 * v + 0.7 * c - 1.4 * f
        + mode_maint + scenario.maintenance_bias,
        scenario,
        rng,
    )
    routine_maintenance = int(rng.random() < sigmoid(maint_logit))

    mode_pass = {0: -0.5, 1: 1.2, 2: 2.7, 3: -0.5, 4: -1.0}[int(mode)]
    pass_logit = _wiggle(
        -2.5 - 1.0 * m + 1.0 * f + mode_pass + scenario.pass_bias,
        scenario,
        rng,
    )
    pass_event = int(invite and rng.random() < sigmoid(pass_logit))

    # These clues come from separate structural Bernoulli recipes, then get reconciled
    # into one semantically possible protocol step. The reconciliation uses no extra
    # randomness, so a bug fix does not quietly reshuffle the rest of the RNG stream. ☕🧭
    if opt_in:
        pass_event = 0
    if opt_in or pass_event:
        text_reply = 1
    if not opt_in:
        routine_maintenance = 0

    mode_resume = {0: -0.8, 1: -0.5, 2: -1.0, 3: 0.0, 4: 2.8}[int(mode)]
    resume_logit = _wiggle(
        -3.0 + 1.0 * p + 0.6 * m + mode_resume + scenario.resume_bias,
        scenario,
        rng,
    )
    resume_signal = int(rng.random() < sigmoid(resume_logit))

    tone_warmth = float(
        np.clip(
            0.15 + 0.28 * m + 0.18 * v + 0.16 * c + 0.12 * e - 0.20 * f
            + scenario.warmth_bias + rng.normal(0.0, scenario.warmth_sigma),
            0,
            1,
        )
    )

    delay_base = scenario.delay_multiplier * (
        8 + 45 * (1 - p) + 30 * (1 - m)
        + 75 * (mode == RoutineMode.BUSY) + 110 * (mode == RoutineMode.LEAVE)
    )
    response_delay_min = float(
        np.clip(
            rng.lognormal(math.log(max(1.0, delay_base)), scenario.delay_sigma),
            0.2,
            360,
        )
    )

    observation = {
        "invite": invite,
        "opt_in": opt_in,
        "text_reply": text_reply,
        "reaction": reaction,
        "state_share": state_share,
        "proactive_update": proactive_update,
        "routine_maintenance": routine_maintenance,
        "pass_event": pass_event,
        "resume_signal": resume_signal,
        "tone_warmth": tone_warmth,
        "response_delay_min": response_delay_min,
    }
    _validate_protocol_clues(observation)
    return observation


def parse_args():
    parser = argparse.ArgumentParser(description="Simulate a tiny coffee routine with tiny weather. ☕🌦️🐣")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="number of synthetic days (default: 365)")
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES, help="particle count (default: 6000)")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="random seed")
    parser.add_argument(
        "--scenario",
        choices=scenario_names(),
        default=DEFAULT_SCENARIO,
        help=f"tiny coffee weather (default: {DEFAULT_SCENARIO})",
    )
    parser.add_argument("--out", type=Path, default=None, help="output directory")
    return parser.parse_args()


def default_output_path(days: int, scenario: CoffeeScenario) -> Path:
    """Keep the cozy baseline basket tidy and tuck alternate worlds into their own cubbies. 🧺🐾"""

    basket = Path(f"examples/{days}-cute-days")
    if scenario.slug != DEFAULT_SCENARIO:
        basket /= scenario.slug
    return basket


def main():
    args = parse_args()
    if args.days < 2:
        raise SystemExit("☕🐾 --days must be at least 2. Even a tiny routine needs a tomorrow.")
    if args.particles < 100:
        raise SystemExit("🐣 --particles must be at least 100. The tiny guess flock is too lonely.")

    scenario = get_scenario(args.scenario)
    out = args.out or default_output_path(args.days, scenario)
    rng = np.random.default_rng(args.seed)
    truth, true_modes = generate_truth(args.days, rng, scenario)
    observations = [observe(truth[t], true_modes[t], rng, scenario) for t in range(args.days)]

    pf = CoffeeParticleFilter(particle_count=args.particles, seed=args.seed)
    estimates = []
    estimated_modes = []
    ci95_low = []
    ci95_high = []
    ess = []

    for obs in observations:
        posterior = pf.update(obs)
        estimates.append(posterior.mean)
        estimated_modes.append(posterior.mode)
        ci95_low.append(posterior.ci95_low)
        ci95_high.append(posterior.ci95_high)
        ess.append(posterior.ess)

    estimates = np.asarray(estimates)
    ci95_low = np.asarray(ci95_low)
    ci95_high = np.asarray(ci95_high)
    ess = np.asarray(ess)

    # R keeps its legacy helper/CSV name for reproducibility, but it is only a
    # derived synthetic demo index — not a latent state or human score. ☕📏
    true_r = relationship_index(truth)
    est_r = relationship_index(estimates)

    rmse = np.sqrt(np.mean((estimates - truth) ** 2, axis=0))
    mae = np.mean(np.abs(estimates - truth), axis=0)
    correlation = np.array([np.corrcoef(estimates[:, i], truth[:, i])[0, 1] for i in range(6)])
    coverage = np.mean((truth >= ci95_low) & (truth <= ci95_high), axis=0)

    r_rmse = float(np.sqrt(np.mean((est_r - true_r) ** 2)))
    r_mae = float(np.mean(np.abs(est_r - true_r)))
    r_corr = float(np.corrcoef(est_r, true_r)[0, 1])
    mode_accuracy = float(np.mean([
        estimated_modes[t] == MODE_NAMES[RoutineMode(int(true_modes[t]))]
        for t in range(args.days)
    ]))

    out.mkdir(parents=True, exist_ok=True)

    with (out / "input.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sample_id", "scenario", *observations[0].keys()])
        writer.writeheader()
        for i, obs in enumerate(observations, 1):
            writer.writerow({"sample_id": i, "scenario": scenario.slug, **obs})

    with (out / "output.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["sample_id", "scenario", "true_mode", "estimated_mode", "ESS"]
        for name in STATE_KEYS:
            fieldnames += [f"true_{name}", f"est_{name}", f"ci95_low_{name}", f"ci95_high_{name}"]
        fieldnames += ["true_R", "est_R"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for t in range(args.days):
            row = {
                "sample_id": t + 1,
                "scenario": scenario.slug,
                "true_mode": MODE_NAMES[RoutineMode(int(true_modes[t]))],
                "estimated_mode": estimated_modes[t],
                "ESS": ess[t],
                "true_R": true_r[t],
                "est_R": est_r[t],
            }
            for j, name in enumerate(STATE_KEYS):
                row[f"true_{name}"] = truth[t, j]
                row[f"est_{name}"] = estimates[t, j]
                row[f"ci95_low_{name}"] = ci95_low[t, j]
                row[f"ci95_high_{name}"] = ci95_high[t, j]
            writer.writerow(row)

    with (out / "metrics.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric_scope", "RMSE", "MAE", "Pearson_r", "CI95_coverage"])
        for name, state_rmse, state_mae, state_r, state_coverage in zip(
            STATE_METRIC_NAMES, rmse, mae, correlation, coverage
        ):
            writer.writerow([name, state_rmse, state_mae, state_r, state_coverage])
        writer.writerow(["relationship_index_R", r_rmse, r_mae, r_corr, ""])
        writer.writerow(["mode_classification_accuracy", "", "", mode_accuracy, ""])

    print(f"{scenario.emoji} weather                 : {scenario.title}")
    print(f"🌱 tiny world              : {scenario.description}")
    print(f"☕ cute synthetic days     : {args.days}")
    print(f"🐣 particles               : {args.particles}")
    print(f"🌱 synthetic demo-index RMSE : {r_rmse:.4f}")
    print(f"✨ synthetic demo-index MAE  : {r_mae:.4f}")
    print(f"🧭 synthetic demo-index r    : {r_corr:.3f}")
    print(f"🎯 mode accuracy           : {mode_accuracy:.2%}")
    print(f"🧺 output                  : {out}")


if __name__ == "__main__":
    main()
