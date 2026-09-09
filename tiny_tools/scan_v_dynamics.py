from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np

from coffee_brain.memory import DEFAULT_SHARED_CONTEXT_MEMORY, shared_context_step
from coffee_brain.model import MODE_NAMES, RoutineMode
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario
from tiny_tools.diagnose_v_compression import observation_loglik
from tiny_tools.excite_voluntariness import DEFAULT_HIGH_V, DEFAULT_LOW_V
from tiny_tools.simulate import observe


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 180
DEFAULT_PARTICLES = 800
DEFAULT_BASELINE_DIR = Path("examples/365-cute-days")
V_INDEX = 2


@dataclass(frozen=True)
class VPriorCandidate:
    name: str
    mean_reversion: float
    process_sigma: float
    role: str


CANDIDATES = (
    VPriorCandidate("default", 0.0350, 0.0110, "current-production-baseline"),
    VPriorCandidate("half-reversion", 0.0175, 0.0110, "bounded-diagnostic-comparator"),
    VPriorCandidate("double-noise", 0.0350, 0.0220, "bounded-diagnostic-comparator"),
    VPriorCandidate("half-reversion-1.5x-noise", 0.0175, 0.0165, "bounded-diagnostic-comparator"),
    VPriorCandidate("half-reversion-double-noise", 0.0175, 0.0220, "bounded-diagnostic-comparator"),
    VPriorCandidate("quarter-reversion-double-noise", 0.00875, 0.0220, "bounded-diagnostic-comparator"),
    VPriorCandidate("zero-reversion-high-noise", 0.0, 0.0350, "stress-extreme-comparator"),
)

SHAPES = ("ramp", "step", "triangle")
BINARY_KEYS = (
    "invite",
    "opt_in",
    "text_reply",
    "reaction",
    "state_share",
    "proactive_update",
    "routine_maintenance",
    "pass_event",
    "resume_signal",
)
STATE_KEYS = ("P", "M", "V", "C", "E", "F")
MODE_LOOKUP = {name: int(mode) for mode, name in MODE_NAMES.items()}


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


def build_v_shape(
    days: int,
    shape: str,
    *,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
) -> tuple[np.ndarray, np.ndarray]:
    """Build one focused V path without changing ordinary CSRDM truth dynamics. 🌿🧪"""

    if days < 60:
        raise ValueError("🌿 V prior scan needs at least 60 synthetic days.")
    if shape not in SHAPES:
        raise ValueError(f"🐾 Unknown V excitation shape '{shape}'.")
    if not 0.02 <= low_v < high_v <= 0.98:
        raise ValueError("🐾 V shape needs 0.02 <= low_v < high_v <= 0.98.")

    u = np.linspace(0.0, 1.0, days)
    if shape == "ramp":
        v_path = np.interp(
            u,
            [0.0, 0.20, 0.40, 0.60, 0.80, 1.0],
            [high_v, high_v, low_v, low_v, high_v, high_v],
        )
    elif shape == "step":
        v_path = np.where(u < 0.30, high_v, np.where(u < 0.68, low_v, high_v))
    else:  # triangle
        v_path = np.interp(u, [0.0, 0.50, 1.0], [high_v, low_v, high_v])

    states = np.tile(np.array([0.80, 0.72, high_v, 0.70, 0.42, 0.10], dtype=float), (days, 1))
    states[:, V_INDEX] = v_path
    for t in range(1, days):
        states[t, 3] = float(
            shared_context_step(
                states[t - 1, 3],
                0.0,
                config=DEFAULT_SHARED_CONTEXT_MEMORY,
                noise=0.0,
            )
        )
    modes = np.full(days, int(RoutineMode.NORMAL), dtype=int)
    return states, modes


def run_v_prior_candidate(
    observations: list[dict],
    truth: np.ndarray,
    modes: np.ndarray,
    candidate: VPriorCandidate,
    *,
    particles: int,
    seed: int,
) -> dict[str, float]:
    """Run an oracle-other-states 1-D V filter for one prior candidate. 🌿🐣

    This is a diagnostic isolator: P/M/C/E/F and mode come from synthetic truth.
    Only V remains uncertain. It is not the public CSRDM inference path.
    """

    if particles < 200:
        raise ValueError("🐣 V prior scan needs at least 200 particles.")

    rng = np.random.default_rng(seed)
    v = np.clip(0.80 + rng.normal(0.0, 0.09, particles), 0.02, 0.98)
    weights = np.ones(particles, dtype=float) / particles
    est = np.zeros(len(observations), dtype=float)
    low = np.zeros(len(observations), dtype=float)
    high = np.zeros(len(observations), dtype=float)

    for t, obs in enumerate(observations):
        if t > 0:
            v = np.clip(
                v
                + candidate.mean_reversion * (0.90 - v)
                + rng.normal(0.0, candidate.process_sigma, particles),
                0.02,
                0.98,
            )

        states = np.tile(truth[t], (particles, 1))
        states[:, V_INDEX] = v
        mode_array = np.full(particles, int(modes[t]), dtype=int)
        ll = observation_loglik(states, mode_array, obs)
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

    return _metrics(truth[:, V_INDEX], est, low, high)


def _parse_observation(row: dict[str, str]) -> dict:
    obs: dict[str, object] = {}
    for key in BINARY_KEYS:
        value = row.get(key, "")
        obs[key] = None if value == "" else int(value)
    warmth = row.get("tone_warmth", "")
    delay = row.get("response_delay_min", "")
    obs["tone_warmth"] = None if warmth == "" else float(warmth)
    obs["response_delay_min"] = None if delay == "" else float(delay)
    return obs


def load_committed_baseline(baseline_dir: Path) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    input_path = baseline_dir / "input.csv"
    output_path = baseline_dir / "output.csv"
    if not input_path.is_file() or not output_path.is_file():
        raise FileNotFoundError(f"🧺 Baseline basket is missing input/output CSVs: {baseline_dir}")

    with input_path.open(newline="", encoding="utf-8") as handle:
        observations = [_parse_observation(row) for row in csv.DictReader(handle)]

    truth_rows: list[list[float]] = []
    modes: list[int] = []
    with output_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            truth_rows.append([float(row[f"true_{key}"]) for key in STATE_KEYS])
            modes.append(MODE_LOOKUP[row["true_mode"]])

    truth = np.asarray(truth_rows, dtype=float)
    mode_array = np.asarray(modes, dtype=int)
    if len(observations) != len(truth):
        raise ValueError("🐾 Baseline input/output rows do not line up.")
    return truth, mode_array, observations


def _aggregate(candidate: VPriorCandidate, rows: list[dict[str, object]]) -> dict[str, object]:
    values = lambda key: np.asarray([float(row[key]) for row in rows], dtype=float)
    return {
        "candidate": candidate.name,
        "role": candidate.role,
        "mean_reversion": candidate.mean_reversion,
        "process_sigma": candidate.process_sigma,
        "stress_runs": len(rows),
        "stress_RMSE_mean": float(np.mean(values("RMSE"))),
        "stress_RMSE_worst": float(np.max(values("RMSE"))),
        "stress_Pearson_r_mean": float(np.mean(values("Pearson_r"))),
        "stress_Pearson_r_worst": float(np.min(values("Pearson_r"))),
        "stress_amplitude_ratio_mean": float(np.mean(values("amplitude_ratio"))),
        "stress_CI95_coverage_mean": float(np.mean(values("CI95_coverage"))),
    }


def scan_v_dynamics(
    *,
    days: int = DEFAULT_DAYS,
    particles: int = DEFAULT_PARTICLES,
    seeds: Iterable[int] = (DEFAULT_SEED, DEFAULT_SEED + 1, DEFAULT_SEED + 2),
    shapes: Iterable[str] = SHAPES,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
    baseline_dir: Path | None = DEFAULT_BASELINE_DIR,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    seed_list = tuple(int(seed) for seed in seeds)
    shape_list = tuple(shapes)
    if not seed_list:
        raise ValueError("🌱 V prior scan needs at least one seed.")
    if not shape_list:
        raise ValueError("🌱 V prior scan needs at least one excitation shape.")

    scenario = get_scenario(DEFAULT_SCENARIO)
    stress_rows: list[dict[str, object]] = []

    for shape in shape_list:
        truth, modes = build_v_shape(days, shape, low_v=low_v, high_v=high_v)
        for seed in seed_list:
            obs_rng = np.random.default_rng(seed)
            observations = [
                observe(truth[t], RoutineMode(int(modes[t])), obs_rng, scenario)
                for t in range(days)
            ]
            for candidate in CANDIDATES:
                metrics = run_v_prior_candidate(
                    observations,
                    truth,
                    modes,
                    candidate,
                    particles=particles,
                    seed=seed + 1000,
                )
                stress_rows.append(
                    {
                        "shape": shape,
                        "seed": seed,
                        "candidate": candidate.name,
                        "mean_reversion": candidate.mean_reversion,
                        "process_sigma": candidate.process_sigma,
                        **metrics,
                    }
                )

    summary_rows = []
    for candidate in CANDIDATES:
        own_rows = [row for row in stress_rows if row["candidate"] == candidate.name]
        summary_rows.append(_aggregate(candidate, own_rows))

    baseline_rows: list[dict[str, object]] = []
    if baseline_dir is not None:
        truth, modes, observations = load_committed_baseline(baseline_dir)
        for candidate in CANDIDATES:
            metrics = run_v_prior_candidate(
                observations,
                truth,
                modes,
                candidate,
                particles=particles,
                seed=DEFAULT_SEED + 5000,
            )
            baseline_rows.append(
                {
                    "candidate": candidate.name,
                    "role": candidate.role,
                    "mean_reversion": candidate.mean_reversion,
                    "process_sigma": candidate.process_sigma,
                    **metrics,
                }
            )

        baseline_map = {row["candidate"]: row for row in baseline_rows}
        for summary in summary_rows:
            guard = baseline_map[summary["candidate"]]
            summary.update(
                {
                    "baseline_RMSE": guard["RMSE"],
                    "baseline_Pearson_r": guard["Pearson_r"],
                    "baseline_amplitude_ratio": guard["amplitude_ratio"],
                    "baseline_CI95_coverage": guard["CI95_coverage"],
                }
            )

    default_summary = next(row for row in summary_rows if row["candidate"] == "default")
    default_stress_rmse = float(default_summary["stress_RMSE_mean"])
    default_baseline_rmse = float(default_summary.get("baseline_RMSE", float("nan")))
    for summary in summary_rows:
        summary["stress_RMSE_change_vs_default_pct"] = 100.0 * (
            float(summary["stress_RMSE_mean"]) / default_stress_rmse - 1.0
        )
        if np.isfinite(default_baseline_rmse):
            summary["baseline_RMSE_change_vs_default_pct"] = 100.0 * (
                float(summary["baseline_RMSE"]) / default_baseline_rmse - 1.0
            )

    return summary_rows, stress_rows, baseline_rows


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _parse_seed_list(value: str) -> tuple[int, ...]:
    return tuple(int(item.strip()) for item in value.split(",") if item.strip())


def parse_args():
    parser = argparse.ArgumentParser(description="Scan bounded V dynamics priors before changing the model. 🌿🎛️")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES)
    parser.add_argument("--seeds", default="20260908,20260909,20260910")
    parser.add_argument("--low-v", type=float, default=DEFAULT_LOW_V)
    parser.add_argument("--high-v", type=float, default=DEFAULT_HIGH_V)
    parser.add_argument("--baseline-dir", type=Path, default=DEFAULT_BASELINE_DIR)
    parser.add_argument("--out", type=Path, default=Path("examples/v-dynamics-scan"))
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        seeds = _parse_seed_list(args.seeds)
        summary_rows, stress_rows, baseline_rows = scan_v_dynamics(
            days=args.days,
            particles=args.particles,
            seeds=seeds,
            low_v=args.low_v,
            high_v=args.high_v,
            baseline_dir=args.baseline_dir,
        )
    except (ValueError, FileNotFoundError) as exc:
        raise SystemExit(str(exc)) from exc

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    _write_rows(out / "candidate-summary.csv", summary_rows)
    _write_rows(out / "stress-runs.csv", stress_rows)
    _write_rows(out / "baseline-guard.csv", baseline_rows)
    (out / "recipe.json").write_text(
        json.dumps(
            {
                "days": args.days,
                "particles": args.particles,
                "seeds": list(seeds),
                "shapes": list(SHAPES),
                "low_v": args.low_v,
                "high_v": args.high_v,
                "baseline_dir": str(args.baseline_dir),
                "candidates": [candidate.__dict__ for candidate in CANDIDATES],
                "observation_coefficients_changed": False,
                "production_model_changed": False,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("🌿 bounded V dynamics scan")
    for row in summary_rows:
        print(
            f"🐣 {row['candidate']:<30} "
            f"stressRMSE={float(row['stress_RMSE_mean']):.3f}  "
            f"stressR={float(row['stress_Pearson_r_mean']):.3f}  "
            f"amp={float(row['stress_amplitude_ratio_mean']):.3f}  "
            f"cov={float(row['stress_CI95_coverage_mean']):.1%}  "
            f"baselineRMSE={float(row.get('baseline_RMSE', float('nan'))):.3f}"
        )
    print(f"☕ scan basket: {out}")


if __name__ == "__main__":
    main()
