from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.config import ARCHITECTURE_VERSION
from coffee_brain.memory import DEFAULT_SHARED_CONTEXT_MEMORY, shared_context_step
from coffee_brain.model import RoutineMode
from coffee_brain.observation_model import DEFAULT_OBSERVATION_MODEL
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario
from tiny_tools.simulate import observe


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 180
DEFAULT_PARTICLES = 1200
DEFAULT_LOW_V = 0.58
DEFAULT_HIGH_V = 0.94
BASELINE_DIR = Path("examples/365-cute-days")


def _phase_labels(days: int) -> list[str]:
    u = np.linspace(0.0, 1.0, days)
    labels = []
    for value in u:
        if value < 0.20:
            labels.append("high-hold")
        elif value < 0.40:
            labels.append("ramp-down")
        elif value < 0.60:
            labels.append("low-hold")
        elif value < 0.80:
            labels.append("ramp-up")
        else:
            labels.append("high-return")
    return labels


def build_v_excitation_truth(
    days: int,
    *,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Build a focused synthetic truth path that deliberately excites V. 🌿🧪

    This is a diagnostic clamp, not ordinary CSRDM truth dynamics. P/M/E/F sit at
    estimator nominal targets, C follows its ordinary quiet-memory law, and only V
    is deliberately moved through a wide known range. That isolates the tracking
    question without changing the estimator or pretending the path is a human law.
    """

    if days < 40:
        raise ValueError("🌿 V excitation needs at least 40 days so every phase has room to breathe.")
    if not 0.02 <= low_v < high_v <= 0.98:
        raise ValueError("🐾 V excitation needs 0.02 <= low_v < high_v <= 0.98.")

    u = np.linspace(0.0, 1.0, days)
    v_path = np.interp(
        u,
        [0.0, 0.20, 0.40, 0.60, 0.80, 1.0],
        [high_v, high_v, low_v, low_v, high_v, high_v],
    )

    states = np.tile(np.array([0.80, 0.72, high_v, 0.70, 0.42, 0.10], dtype=float), (days, 1))
    states[:, 2] = v_path

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
    return states, modes, _phase_labels(days)


def _safe_pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def v_channel_sensitivity_rows(
    *,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
) -> list[dict[str, object]]:
    """Expose which current observation channels directly carry V information. 🎛️🌿"""

    base = np.array([0.80, 0.72, low_v, 0.70, 0.42, 0.10], dtype=float)
    high = base.copy()
    high[2] = high_v
    states = np.vstack([base, high])
    modes = np.array([int(RoutineMode.NORMAL), int(RoutineMode.NORMAL)], dtype=int)

    rows: list[dict[str, object]] = []
    for name, channel in DEFAULT_OBSERVATION_MODEL.binary_channels().items():
        probabilities = channel.probabilities(states, modes)
        rows.append(
            {
                "channel": name,
                "kind": "bernoulli",
                "direct_V_coefficient": float(channel.state_coefficients[2]),
                "low_V_expected": float(probabilities[0]),
                "high_V_expected": float(probabilities[1]),
                "high_minus_low": float(probabilities[1] - probabilities[0]),
                "epistemic_status": "Assumed structural observation relationship",
            }
        )

    warmth = DEFAULT_OBSERVATION_MODEL.tone_warmth
    warmth_mean = warmth.mean(states, modes)
    rows.append(
        {
            "channel": "tone_warmth",
            "kind": "gaussian-mean",
            "direct_V_coefficient": float(warmth.state_coefficients[2]),
            "low_V_expected": float(warmth_mean[0]),
            "high_V_expected": float(warmth_mean[1]),
            "high_minus_low": float(warmth_mean[1] - warmth_mean[0]),
            "epistemic_status": "Assumed structural observation relationship",
        }
    )

    delay = DEFAULT_OBSERVATION_MODEL.response_delay.log_mean(states, modes)
    rows.append(
        {
            "channel": "response_delay_log_mean",
            "kind": "continuous-log-mean",
            "direct_V_coefficient": 0.0,
            "low_V_expected": float(delay[0]),
            "high_V_expected": float(delay[1]),
            "high_minus_low": float(delay[1] - delay[0]),
            "epistemic_status": "Undefined outside the current direct model path; coefficient is zero here",
        }
    )
    return rows


def run_v_excitation(
    *,
    days: int = DEFAULT_DAYS,
    particles: int = DEFAULT_PARTICLES,
    seed: int = DEFAULT_SEED,
    low_v: float = DEFAULT_LOW_V,
    high_v: float = DEFAULT_HIGH_V,
):
    """Run the unchanged Particle Filter against one deliberately excited V path. 🐣🌿"""

    if particles < 100:
        raise ValueError("🐣 V excitation needs at least 100 particles.")

    scenario = get_scenario(DEFAULT_SCENARIO)
    truth, modes, phases = build_v_excitation_truth(days, low_v=low_v, high_v=high_v)
    obs_rng = np.random.default_rng(seed)
    observations = [
        observe(truth[t], RoutineMode(int(modes[t])), obs_rng, scenario)
        for t in range(days)
    ]

    pf = CoffeeParticleFilter(particle_count=particles, seed=seed + 1)
    est_v = np.zeros(days, dtype=float)
    ci_low = np.zeros(days, dtype=float)
    ci_high = np.zeros(days, dtype=float)

    for t, obs in enumerate(observations):
        posterior = pf.update(obs)
        est_v[t] = posterior.mean[2]
        ci_low[t] = posterior.ci95_low[2]
        ci_high[t] = posterior.ci95_high[2]

    true_v = truth[:, 2]
    metrics = {
        "truth_std": float(np.std(true_v)),
        "truth_span": float(np.ptp(true_v)),
        "estimate_std": float(np.std(est_v)),
        "RMSE": float(np.sqrt(np.mean((est_v - true_v) ** 2))),
        "MAE": float(np.mean(np.abs(est_v - true_v))),
        "Pearson_r": _safe_pearson(est_v, true_v),
        "CI95_coverage": float(np.mean((true_v >= ci_low) & (true_v <= ci_high))),
        "mean_estimate_minus_truth": float(np.mean(est_v - true_v)),
    }
    return truth, observations, phases, est_v, ci_low, ci_high, metrics


def _read_baseline_v(baseline_dir: Path) -> dict[str, float] | None:
    metrics_path = baseline_dir / "metrics.csv"
    excitation_path = baseline_dir / "state-excitation.csv"
    if not metrics_path.is_file() or not excitation_path.is_file():
        return None

    metric_row = None
    with metrics_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["metric_scope"] == "V_voluntariness":
                metric_row = row
                break
    excitation_row = None
    with excitation_path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row["state"] == "V":
                excitation_row = row
                break
    if metric_row is None or excitation_row is None:
        return None

    return {
        "truth_std": float(excitation_row["truth_std"]),
        "truth_span": float(excitation_row["truth_span"]),
        "estimate_std": float(excitation_row["estimate_std"]),
        "RMSE": float(metric_row["RMSE"]),
        "MAE": float(metric_row["MAE"]),
        "Pearson_r": float(metric_row["Pearson_r"]),
        "CI95_coverage": float(metric_row["CI95_coverage"]),
        "mean_estimate_minus_truth": float(excitation_row["mean_estimate_minus_truth"]),
    }


def _write_dict_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _paint(path: Path, true_v: np.ndarray, est_v: np.ndarray, low: np.ndarray, high: np.ndarray) -> None:
    days = np.arange(1, len(true_v) + 1)
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.plot(days, true_v, label="synthetic truth V")
    ax.plot(days, est_v, label="filtered estimate V")
    ax.fill_between(days, low, high, alpha=0.18, label="95% particle interval")
    ax.set_xlabel("synthetic day")
    ax.set_ylabel("V = Voluntariness")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("🌿 Deliberate Voluntariness excitation — tracking stress test")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Deliberately excite V before judging its tracking. 🌿☕")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--low-v", type=float, default=DEFAULT_LOW_V)
    parser.add_argument("--high-v", type=float, default=DEFAULT_HIGH_V)
    parser.add_argument("--baseline-dir", type=Path, default=BASELINE_DIR)
    parser.add_argument("--out", type=Path, default=Path("examples/v-excitation"))
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        truth, observations, phases, est_v, ci_low, ci_high, metrics = run_v_excitation(
            days=args.days,
            particles=args.particles,
            seed=args.seed,
            low_v=args.low_v,
            high_v=args.high_v,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    baseline = _read_baseline_v(args.baseline_dir)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    recipe = {
        "architecture_version": ARCHITECTURE_VERSION,
        "days": args.days,
        "high_v": args.high_v,
        "low_v": args.low_v,
        "observation_scenario": DEFAULT_SCENARIO,
        "observation_seed": args.seed,
        "particle_count": args.particles,
        "particle_filter_seed": args.seed + 1,
        "python_version": sys.version.split()[0],
        "numpy_version": np.__version__,
        "truth_construction": "focused V clamp; P/M/E/F nominal, C quiet-memory, Normal mode",
        "model_behavior_changed": False,
    }
    (out / "recipe.json").write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    summary_rows: list[dict[str, object]] = [{"experiment": "deliberate-v-excitation", **metrics}]
    if baseline is not None:
        summary_rows.append({"experiment": "365-observation-only-baseline", **baseline})
    _write_dict_rows(out / "summary.csv", summary_rows)

    track_rows = []
    for t in range(args.days):
        track_rows.append(
            {
                "day": t + 1,
                "phase": phases[t],
                "true_V": truth[t, 2],
                "est_V": est_v[t],
                "ci95_low_V": ci_low[t],
                "ci95_high_V": ci_high[t],
                "invite": observations[t]["invite"],
                "opt_in": observations[t]["opt_in"],
                "reaction": observations[t]["reaction"],
                "routine_maintenance": observations[t]["routine_maintenance"],
                "tone_warmth": observations[t]["tone_warmth"],
            }
        )
    _write_dict_rows(out / "v-track.csv", track_rows)
    _write_dict_rows(out / "channel-sensitivity.csv", v_channel_sensitivity_rows(low_v=args.low_v, high_v=args.high_v))
    _paint(out / "v-excitation.png", truth[:, 2], est_v, ci_low, ci_high)

    print(f"🌿 truth V std              : {metrics['truth_std']:.4f}")
    print(f"🌱 truth V span             : {metrics['truth_span']:.4f}")
    print(f"🐣 estimate V std           : {metrics['estimate_std']:.4f}")
    print(f"📏 V RMSE                   : {metrics['RMSE']:.4f}")
    print(f"📐 V MAE                    : {metrics['MAE']:.4f}")
    print(f"🧭 V Pearson r              : {metrics['Pearson_r']:.4f}")
    print(f"☂️ V 95% coverage           : {metrics['CI95_coverage']:.2%}")
    if baseline is not None:
        ratio = metrics["truth_std"] / baseline["truth_std"] if baseline["truth_std"] > 0 else float("nan")
        print(f"🔍 excitation std / baseline: {ratio:.2f}x")
        print(f"🧺 baseline V Pearson r      : {baseline['Pearson_r']:.4f}")
    print(f"☕ result basket             : {out}")


if __name__ == "__main__":
    main()
