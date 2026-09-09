from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.model import RoutineMode
from coffee_brain.observation_model import (
    DEFAULT_OBSERVATION_MODEL,
    predict_binary_channels,
    predict_delay_log_mean,
    predict_warmth_mean,
)
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario
from tiny_tools.excite_voluntariness import (
    DEFAULT_DAYS,
    DEFAULT_HIGH_V,
    DEFAULT_LOW_V,
    DEFAULT_PARTICLES,
    DEFAULT_SEED,
    build_v_excitation_truth,
)
from tiny_tools.simulate import observe


V_INDEX = 2
NORMAL_MODE = int(RoutineMode.NORMAL)
NOMINAL_STATE = np.array([0.80, 0.72, 0.90, 0.70, 0.42, 0.10], dtype=float)
DEFAULT_V_TARGET = 0.90
DEFAULT_V_MEAN_REVERSION = 0.035
DEFAULT_V_PROCESS_SIGMA = 0.011
RELAXED_V_MEAN_REVERSION = 0.0
RELAXED_V_PROCESS_SIGMA = 0.035


def _bern_loglik(y: int, p: np.ndarray) -> np.ndarray:
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1.0 - 1e-6)
    return y * np.log(p) + (1 - y) * np.log(1 - p)


def observation_loglik(states: np.ndarray, modes: np.ndarray, obs: dict) -> np.ndarray:
    """Evaluate the current estimator likelihood without running state dynamics. 🌿🔍"""

    states = np.asarray(states, dtype=float)
    modes = np.asarray(modes, dtype=int)
    probabilities = predict_binary_channels(states, modes, DEFAULT_OBSERVATION_MODEL)
    ll = np.zeros(len(states), dtype=float)

    invite = obs.get("invite")
    response_opportunity = invite is None or int(invite) == 1
    for name in (
        "opt_in",
        "text_reply",
        "reaction",
        "state_share",
        "proactive_update",
        "routine_maintenance",
        "pass_event",
        "resume_signal",
    ):
        value = obs.get(name)
        if value is None:
            continue
        if name in ("opt_in", "pass_event") and not response_opportunity:
            continue
        ll += _bern_loglik(int(value), probabilities[name])

    warmth = obs.get("tone_warmth")
    if warmth is not None:
        mu = predict_warmth_mean(states, modes, DEFAULT_OBSERVATION_MODEL)
        sigma = DEFAULT_OBSERVATION_MODEL.tone_warmth.sigma
        ll += -0.5 * ((float(warmth) - mu) / sigma) ** 2

    delay = obs.get("response_delay_min")
    if delay is not None:
        mu = predict_delay_log_mean(states, modes, DEFAULT_OBSERVATION_MODEL)
        sigma = DEFAULT_OBSERVATION_MODEL.response_delay.sigma_log
        ll += -0.5 * ((math.log(max(float(delay), 0.2)) - mu) / sigma) ** 2

    return ll


def _safe_pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _weighted_interval(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    order = np.argsort(values)
    cdf = np.cumsum(weights[order])
    return float(values[order[np.searchsorted(cdf, q)]])


def _metrics(true_v: np.ndarray, est_v: np.ndarray, low: np.ndarray, high: np.ndarray) -> dict[str, float]:
    truth_std = float(np.std(true_v))
    estimate_std = float(np.std(est_v))
    return {
        "truth_std": truth_std,
        "estimate_std": estimate_std,
        "amplitude_ratio": estimate_std / truth_std if truth_std > 0.0 else float("nan"),
        "RMSE": float(np.sqrt(np.mean((est_v - true_v) ** 2))),
        "MAE": float(np.mean(np.abs(est_v - true_v))),
        "Pearson_r": _safe_pearson(est_v, true_v),
        "CI95_coverage": float(np.mean((true_v >= low) & (true_v <= high))),
        "mean_estimate_minus_truth": float(np.mean(est_v - true_v)),
    }


def likelihood_slice(
    *,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
    seed: int = DEFAULT_SEED,
    samples_per_level: int = 320,
    grid_points: int = 121,
) -> tuple[list[dict[str, float]], dict[str, float]]:
    """Ask whether the observation likelihood alone can separate low and high V. 🎛️🌿"""

    if samples_per_level < 40:
        raise ValueError("🌿 Likelihood slice needs at least 40 clue baskets per level.")
    if grid_points < 25:
        raise ValueError("🐾 V likelihood grid needs at least 25 points.")

    scenario = get_scenario(DEFAULT_SCENARIO)
    rng = np.random.default_rng(seed)
    grid = np.linspace(0.05, 0.98, grid_points)
    grid_states = np.tile(NOMINAL_STATE, (grid_points, 1))
    grid_states[:, V_INDEX] = grid
    grid_modes = np.full(grid_points, NORMAL_MODE, dtype=int)

    baskets: dict[str, list[dict]] = {}
    for label, value in (("low", low_v), ("high", high_v)):
        state = NOMINAL_STATE.copy()
        state[V_INDEX] = value
        baskets[label] = [observe(state, RoutineMode.NORMAL, rng, scenario) for _ in range(samples_per_level)]

    mean_ll: dict[str, np.ndarray] = {}
    for label, observations in baskets.items():
        total = np.zeros(grid_points, dtype=float)
        for obs in observations:
            total += observation_loglik(grid_states, grid_modes, obs)
        mean_ll[label] = total / len(observations)
        mean_ll[label] -= np.max(mean_ll[label])

    rows = [
        {
            "V": float(value),
            "low_basket_relative_mean_loglik": float(mean_ll["low"][i]),
            "high_basket_relative_mean_loglik": float(mean_ll["high"][i]),
        }
        for i, value in enumerate(grid)
    ]

    low_peak = float(grid[int(np.argmax(mean_ll["low"]))])
    high_peak = float(grid[int(np.argmax(mean_ll["high"]))])
    low_idx = int(np.argmin(np.abs(grid - low_v)))
    high_idx = int(np.argmin(np.abs(grid - high_v)))
    summary = {
        "low_peak_V": low_peak,
        "high_peak_V": high_peak,
        "peak_separation": high_peak - low_peak,
        "low_basket_preference_low_over_high": float(mean_ll["low"][low_idx] - mean_ll["low"][high_idx]),
        "high_basket_preference_high_over_low": float(mean_ll["high"][high_idx] - mean_ll["high"][low_idx]),
    }
    return rows, summary


def _normal_locked_transition() -> np.ndarray:
    """Almost-fix the diagnostic mode to Normal while satisfying positive-row guards. ☕🔒"""

    eps = 1e-12
    matrix = np.full((5, 5), eps, dtype=float)
    matrix[:, NORMAL_MODE] = 1.0 - 4.0 * eps
    return matrix


def _run_full_filter(
    observations: list[dict],
    true_v: np.ndarray,
    *,
    seed: int,
    particles: int,
    normal_locked: bool,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    pf = CoffeeParticleFilter(
        particle_count=particles,
        seed=seed,
        fixed_transition=_normal_locked_transition() if normal_locked else None,
    )
    est = np.zeros(len(observations), dtype=float)
    low = np.zeros(len(observations), dtype=float)
    high = np.zeros(len(observations), dtype=float)
    for t, obs in enumerate(observations):
        posterior = pf.update(obs)
        est[t] = posterior.mean[V_INDEX]
        low[t] = posterior.ci95_low[V_INDEX]
        high[t] = posterior.ci95_high[V_INDEX]
    return est, low, high, _metrics(true_v, est, low, high)


def _run_v_only_filter(
    observations: list[dict],
    truth: np.ndarray,
    *,
    seed: int,
    particles: int,
    mean_reversion: float,
    process_sigma: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, dict[str, float]]:
    """Diagnostic-only 1-D bootstrap filter: same likelihood, only V is uncertain. 🌿🐣"""

    rng = np.random.default_rng(seed)
    v = np.clip(0.80 + rng.normal(0.0, 0.09, particles), 0.02, 0.98)
    weights = np.ones(particles, dtype=float) / particles
    est = np.zeros(len(observations), dtype=float)
    low = np.zeros(len(observations), dtype=float)
    high = np.zeros(len(observations), dtype=float)

    for t, obs in enumerate(observations):
        if t > 0:
            v = np.clip(
                v + mean_reversion * (DEFAULT_V_TARGET - v) + rng.normal(0.0, process_sigma, particles),
                0.02,
                0.98,
            )

        states = np.tile(truth[t], (particles, 1))
        states[:, V_INDEX] = v
        modes = np.full(particles, NORMAL_MODE, dtype=int)
        ll = observation_loglik(states, modes, obs)
        ll -= np.max(ll)
        weights = np.exp(ll) * weights
        weights /= np.sum(weights)

        est[t] = float(np.sum(weights * v))
        low[t] = _weighted_interval(v, weights, 0.025)
        high[t] = _weighted_interval(v, weights, 0.975)

        ess = 1.0 / np.sum(weights * weights)
        if ess < 0.55 * particles:
            positions = (rng.random() + np.arange(particles)) / particles
            idx = np.searchsorted(np.cumsum(weights), positions)
            v = v[idx]
            weights = np.ones(particles, dtype=float) / particles

    return est, low, high, _metrics(truth[:, V_INDEX], est, low, high)


def run_compression_diagnostic(
    *,
    days: int = DEFAULT_DAYS,
    particles: int = DEFAULT_PARTICLES,
    seed: int = DEFAULT_SEED,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
) -> dict[str, object]:
    if days < 60:
        raise ValueError("🌿 V compression diagnostic needs at least 60 synthetic days.")
    if particles < 200:
        raise ValueError("🐣 V compression diagnostic needs at least 200 particles.")

    truth, modes, phases = build_v_excitation_truth(days, low_v=low_v, high_v=high_v)
    scenario = get_scenario(DEFAULT_SCENARIO)
    obs_rng = np.random.default_rng(seed)
    observations = [observe(truth[t], RoutineMode(int(modes[t])), obs_rng, scenario) for t in range(days)]
    true_v = truth[:, V_INDEX]

    full_hidden = _run_full_filter(
        observations,
        true_v,
        seed=seed + 1,
        particles=particles,
        normal_locked=False,
    )
    full_normal = _run_full_filter(
        observations,
        true_v,
        seed=seed + 1,
        particles=particles,
        normal_locked=True,
    )
    one_d_default = _run_v_only_filter(
        observations,
        truth,
        seed=seed + 2,
        particles=particles,
        mean_reversion=DEFAULT_V_MEAN_REVERSION,
        process_sigma=DEFAULT_V_PROCESS_SIGMA,
    )
    one_d_relaxed = _run_v_only_filter(
        observations,
        truth,
        seed=seed + 2,
        particles=particles,
        mean_reversion=RELAXED_V_MEAN_REVERSION,
        process_sigma=RELAXED_V_PROCESS_SIGMA,
    )

    slice_rows, slice_summary = likelihood_slice(low_v=low_v, high_v=high_v, seed=seed + 3)
    truth_step = np.diff(true_v)
    dynamics = {
        "default_target": DEFAULT_V_TARGET,
        "default_mean_reversion": DEFAULT_V_MEAN_REVERSION,
        "default_process_sigma": DEFAULT_V_PROCESS_SIGMA,
        "restoring_drift_at_low_V": DEFAULT_V_MEAN_REVERSION * (DEFAULT_V_TARGET - low_v),
        "restoring_drift_at_high_V": DEFAULT_V_MEAN_REVERSION * (DEFAULT_V_TARGET - high_v),
        "max_abs_truth_step": float(np.max(np.abs(truth_step))),
        "mean_abs_nonzero_truth_step": float(np.mean(np.abs(truth_step[np.abs(truth_step) > 1e-12]))),
    }

    variants = {
        "full-hidden-mode": full_hidden,
        "full-normal-locked": full_normal,
        "v-only-default-prior": one_d_default,
        "v-only-relaxed-prior": one_d_relaxed,
    }
    return {
        "truth": truth,
        "phases": phases,
        "observations": observations,
        "variants": variants,
        "likelihood_rows": slice_rows,
        "likelihood_summary": slice_summary,
        "dynamics": dynamics,
    }


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _paint(path: Path, truth: np.ndarray, phases: list[str], variants: dict[str, tuple]) -> None:
    days = np.arange(1, len(truth) + 1)
    fig, ax = plt.subplots(figsize=(11, 5.0))
    ax.plot(days, truth[:, V_INDEX], label="synthetic truth V")
    for name in ("full-hidden-mode", "full-normal-locked", "v-only-default-prior", "v-only-relaxed-prior"):
        ax.plot(days, variants[name][0], label=name)
    ax.set_xlabel("synthetic day")
    ax.set_ylabel("V = Voluntariness")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("V posterior compression diagnostic")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Separate the little causes of V posterior compression. 🌿🔬")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--low-v", type=float, default=DEFAULT_LOW_V)
    parser.add_argument("--high-v", type=float, default=DEFAULT_HIGH_V)
    parser.add_argument("--out", type=Path, default=Path("examples/v-compression-diagnostic"))
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        result = run_compression_diagnostic(
            days=args.days,
            particles=args.particles,
            seed=args.seed,
            low_v=args.low_v,
            high_v=args.high_v,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    comparison_rows = []
    for name, variant in result["variants"].items():
        comparison_rows.append({"variant": name, **variant[3]})
    _write_rows(out / "filter-comparison.csv", comparison_rows)
    _write_rows(out / "likelihood-slice.csv", result["likelihood_rows"])
    _write_rows(out / "likelihood-summary.csv", [{"diagnostic": "V-likelihood-slice", **result["likelihood_summary"]}])
    _write_rows(out / "dynamics-pressure.csv", [{"diagnostic": "V-default-dynamics", **result["dynamics"]}])

    recipe = {
        "days": args.days,
        "particle_count": args.particles,
        "seed": args.seed,
        "low_v": args.low_v,
        "high_v": args.high_v,
        "normal_mode_locked_diagnostic": True,
        "v_only_default_prior": {
            "target": DEFAULT_V_TARGET,
            "mean_reversion": DEFAULT_V_MEAN_REVERSION,
            "process_sigma": DEFAULT_V_PROCESS_SIGMA,
        },
        "v_only_relaxed_prior": {
            "target": DEFAULT_V_TARGET,
            "mean_reversion": RELAXED_V_MEAN_REVERSION,
            "process_sigma": RELAXED_V_PROCESS_SIGMA,
        },
        "model_behavior_changed": False,
    }
    (out / "recipe.json").write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    _paint(out / "v-compression.png", result["truth"], result["phases"], result["variants"])

    likelihood = result["likelihood_summary"]
    print(f"🌿 likelihood low-V peak       : {likelihood['low_peak_V']:.3f}")
    print(f"🌱 likelihood high-V peak      : {likelihood['high_peak_V']:.3f}")
    print(f"🔍 likelihood peak separation  : {likelihood['peak_separation']:.3f}")
    for row in comparison_rows:
        print(
            f"🐣 {row['variant']:<24} "
            f"amp={row['amplitude_ratio']:.3f}  r={row['Pearson_r']:.3f}  "
            f"RMSE={row['RMSE']:.3f}  coverage={row['CI95_coverage']:.1%}"
        )
    print(f"☕ diagnostic basket           : {out}")


if __name__ == "__main__":
    main()
