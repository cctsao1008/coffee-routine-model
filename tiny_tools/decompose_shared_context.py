from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.memory import DEFAULT_SHARED_CONTEXT_MEMORY, shared_context_step
from coffee_brain.model import MODE_LABELS, clip_state
from coffee_brain.particles import CoffeeParticleFilter


DEFAULT_BASELINE_DIR = Path("examples/365-cute-days")
DEFAULT_PARTICLES = 6000
DEFAULT_SEED = 20260908
DEFAULT_INITIAL_C_CENTER = 0.58
C_INDEX = 3
STATE_KEYS = ("P", "M", "V", "C", "E", "F")
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
MODE_LOOKUP = {name: index for index, name in enumerate(MODE_LABELS)}


@dataclass(frozen=True)
class CPriorCandidate:
    name: str
    requested_center: float | None
    role: str


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
    """Read the committed observation-only basket without inventing missing clues. 🧺🧠"""

    input_path = baseline_dir / "input.csv"
    output_path = baseline_dir / "output.csv"
    if not input_path.is_file() or not output_path.is_file():
        raise FileNotFoundError(f"🧺 Shared Context basket is missing input/output CSVs: {baseline_dir}")

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
        raise ValueError("🐾 Shared Context input/output rows do not line up.")
    return truth, mode_array, observations


def _centered_rmse(error: np.ndarray) -> float:
    centered = np.asarray(error, dtype=float) - float(np.mean(error))
    return float(np.sqrt(np.mean(centered * centered)))


def _safe_pearson(a: np.ndarray, b: np.ndarray) -> float:
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if np.std(a) <= 1e-12 or np.std(b) <= 1e-12:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _shift_initial_c(pf: CoffeeParticleFilter, requested_center: float | None) -> float:
    """Shift only C while preserving the existing particle offsets as much as possible. 🌱🧺

    The public filter API remains untouched. This is a diagnostic-only prior perturbation.
    """

    if requested_center is None:
        return float(np.mean(pf.particles[:, C_INDEX]))
    delta = float(requested_center) - DEFAULT_INITIAL_C_CENTER
    shifted = pf.particles[:, C_INDEX] + delta
    pf.particles[:, C_INDEX] = clip_state(shifted)
    return float(np.mean(pf.particles[:, C_INDEX]))


def quiet_bias_curve(initial_offset: float, days: int) -> np.ndarray:
    """Expected offset under the same no-input decay law used by inspect_memory. 🍂🧠"""

    config = DEFAULT_SHARED_CONTEXT_MEMORY
    high = 0.70
    low = high + float(initial_offset)
    curve = np.zeros(days, dtype=float)
    for t in range(days):
        curve[t] = low - high
        if t + 1 < days:
            high = float(shared_context_step(high, 0.0, config=config, noise=0.0))
            low = float(shared_context_step(low, 0.0, config=config, noise=0.0))
    return curve


def run_candidate(
    observations: list[dict],
    truth: np.ndarray,
    candidate: CPriorCandidate,
    *,
    particles: int,
    seed: int,
) -> tuple[dict[str, float | str], list[dict[str, object]]]:
    """Replay one observation basket with exactly one C-prior choice changed. 🧠🔬"""

    pf = CoffeeParticleFilter(particle_count=particles, seed=seed)
    prior_mean_c = _shift_initial_c(pf, candidate.requested_center)
    prior_offset = prior_mean_c - float(truth[0, C_INDEX])
    quiet_bias = quiet_bias_curve(prior_offset, len(observations))

    est = np.zeros(len(observations), dtype=float)
    low = np.zeros(len(observations), dtype=float)
    high = np.zeros(len(observations), dtype=float)
    rows: list[dict[str, object]] = []

    for t, obs in enumerate(observations):
        posterior = pf.update(obs)
        est[t] = posterior.mean[C_INDEX]
        low[t] = posterior.ci95_low[C_INDEX]
        high[t] = posterior.ci95_high[C_INDEX]
        rows.append(
            {
                "day": t + 1,
                "candidate": candidate.name,
                "true_C": truth[t, C_INDEX],
                "est_C": est[t],
                "error_C": est[t] - truth[t, C_INDEX],
                "quiet_bias_prediction": quiet_bias[t],
                "ci95_low_C": low[t],
                "ci95_high_C": high[t],
            }
        )

    error = est - truth[:, C_INDEX]
    bias = float(np.mean(error))
    rmse = float(np.sqrt(np.mean(error * error)))
    centered_rmse = _centered_rmse(error)
    quiet_residual = error - quiet_bias
    mse = rmse * rmse
    return (
        {
            "candidate": candidate.name,
            "role": candidate.role,
            "requested_center": "default" if candidate.requested_center is None else float(candidate.requested_center),
            "actual_prior_mean_C": prior_mean_c,
            "prior_offset_vs_truth_C0": prior_offset,
            "initial_posterior_error": float(error[0]),
            "final_posterior_error": float(error[-1]),
            "mean_bias": bias,
            "RMSE": rmse,
            "centered_RMSE": centered_rmse,
            "offset_MSE_fraction": float((bias * bias) / mse) if mse > 0.0 else 0.0,
            "Pearson_r": _safe_pearson(est, truth[:, C_INDEX]),
            "CI95_coverage": float(np.mean((truth[:, C_INDEX] >= low) & (truth[:, C_INDEX] <= high))),
            "quiet_predicted_mean_bias": float(np.mean(quiet_bias)),
            "mean_error_minus_quiet_prediction": float(np.mean(quiet_residual)),
            "RMSE_after_quiet_prediction": float(np.sqrt(np.mean(quiet_residual * quiet_residual))),
        },
        rows,
    )


def time_bias_rows(track_rows: list[dict[str, object]], days: int) -> list[dict[str, object]]:
    windows = (
        ("day-001-030", 1, min(30, days)),
        ("day-031-090", 31, min(90, days)),
        ("day-091-180", 91, min(180, days)),
        ("day-181-end", 181, days),
    )
    out: list[dict[str, object]] = []
    candidates = sorted({str(row["candidate"]) for row in track_rows})
    for candidate in candidates:
        own = [row for row in track_rows if row["candidate"] == candidate]
        for label, start, end in windows:
            if start > end:
                continue
            errors = np.asarray(
                [float(row["error_C"]) for row in own if start <= int(row["day"]) <= end],
                dtype=float,
            )
            if not len(errors):
                continue
            out.append(
                {
                    "candidate": candidate,
                    "window": label,
                    "start_day": start,
                    "end_day": end,
                    "mean_bias": float(np.mean(errors)),
                    "RMSE": float(np.sqrt(np.mean(errors * errors))),
                    "centered_RMSE": _centered_rmse(errors),
                }
            )
    return out


def mode_bias_rows(
    track_rows: list[dict[str, object]],
    true_modes: np.ndarray,
) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    candidates = sorted({str(row["candidate"]) for row in track_rows})
    for candidate in candidates:
        own = [row for row in track_rows if row["candidate"] == candidate]
        errors = np.asarray([float(row["error_C"]) for row in own], dtype=float)
        for mode_index, mode_name in enumerate(MODE_LABELS):
            mask = true_modes == mode_index
            if not np.any(mask):
                continue
            selected = errors[mask]
            out.append(
                {
                    "candidate": candidate,
                    "mode": mode_name,
                    "days": int(np.sum(mask)),
                    "mean_bias": float(np.mean(selected)),
                    "RMSE": float(np.sqrt(np.mean(selected * selected))),
                    "centered_RMSE": _centered_rmse(selected),
                }
            )
    return out


def quiet_memory_rows(days: int) -> list[dict[str, float | int]]:
    config = DEFAULT_SHARED_CONTEXT_MEMORY
    rows: list[dict[str, float | int]] = []
    for horizon in (1, 30, 90, 180, days):
        if horizon < 1 or horizon > days:
            continue
        retention = quiet_bias_curve(1.0, horizon)[-1]
        rows.append(
            {
                "days": horizon,
                "offset_retention_ratio": retention,
                "accumulation_rate": config.accumulation_rate,
                "decay_rate": config.decay_rate,
                "process_noise": config.process_noise,
            }
        )
    return rows


def decompose_shared_context(
    baseline_dir: Path,
    *,
    particles: int = DEFAULT_PARTICLES,
    seed: int = DEFAULT_SEED,
) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    truth, true_modes, observations = load_committed_baseline(baseline_dir)
    truth_c0 = float(truth[0, C_INDEX])
    mirror_high = float(np.clip(2.0 * truth_c0 - DEFAULT_INITIAL_C_CENTER, 0.02, 0.98))
    candidates = (
        CPriorCandidate("default", None, "current-production-baseline"),
        CPriorCandidate("matched-truth-start", truth_c0, "diagnostic-matched-prior"),
        CPriorCandidate("mirror-high", mirror_high, "diagnostic-shifted-prior"),
    )

    summaries: list[dict[str, object]] = []
    tracks: list[dict[str, object]] = []
    for candidate in candidates:
        summary, rows = run_candidate(
            observations,
            truth,
            candidate,
            particles=particles,
            seed=seed,
        )
        summaries.append(summary)
        tracks.extend(rows)

    return (
        summaries,
        tracks,
        time_bias_rows(tracks, len(observations)),
        mode_bias_rows(tracks, true_modes),
        quiet_memory_rows(len(observations)),
    )


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _plot(path: Path, tracks: list[dict[str, object]]) -> None:
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    candidates = ("default", "matched-truth-start", "mirror-high")
    for candidate in candidates:
        rows = [row for row in tracks if row["candidate"] == candidate]
        day = np.asarray([row["day"] for row in rows], dtype=float)
        est = np.asarray([row["est_C"] for row in rows], dtype=float)
        err = np.asarray([row["error_C"] for row in rows], dtype=float)
        ax1.plot(day, est, label=candidate)
        ax2.plot(day, err, label=candidate)
    default_rows = [row for row in tracks if row["candidate"] == "default"]
    day = np.asarray([row["day"] for row in default_rows], dtype=float)
    truth = np.asarray([row["true_C"] for row in default_rows], dtype=float)
    quiet = np.asarray([row["quiet_bias_prediction"] for row in default_rows], dtype=float)
    ax1.plot(day, truth, linewidth=2.0, label="synthetic truth C")
    ax2.plot(day, quiet, linestyle="--", label="default quiet-law offset prediction")
    ax1.set_ylabel("Shared Context C")
    ax1.set_ylim(0.0, 1.0)
    ax1.set_title("🧠🌱 Shared Context: shape tracking versus prior offset")
    ax1.legend(ncol=2)
    ax2.axhline(0.0, linewidth=1.0)
    ax2.set_xlabel("synthetic day")
    ax2.set_ylabel("estimate - truth")
    ax2.legend(ncol=2)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Decompose Shared Context offset before touching its memory law. 🧠🌱🔬")
    parser.add_argument("--baseline-dir", type=Path, default=DEFAULT_BASELINE_DIR)
    parser.add_argument("--particles", type=int, default=DEFAULT_PARTICLES)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=Path("examples/shared-context-bias"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.particles < 200:
        raise SystemExit("🐣 Shared Context decomposition needs at least 200 particles.")

    summaries, tracks, by_time, by_mode, quiet = decompose_shared_context(
        args.baseline_dir,
        particles=args.particles,
        seed=args.seed,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    _write_rows(args.out / "prior-summary.csv", summaries)
    _write_rows(args.out / "error-track.csv", tracks)
    _write_rows(args.out / "time-bias.csv", by_time)
    _write_rows(args.out / "mode-bias.csv", by_mode)
    _write_rows(args.out / "quiet-memory.csv", quiet)
    _plot(args.out / "shared-context-bias.png", tracks)

    recipe = {
        "baseline_dir": str(args.baseline_dir),
        "particles": args.particles,
        "seed": args.seed,
        "memory_config": {
            "accumulation_rate": DEFAULT_SHARED_CONTEXT_MEMORY.accumulation_rate,
            "decay_rate": DEFAULT_SHARED_CONTEXT_MEMORY.decay_rate,
            "process_noise": DEFAULT_SHARED_CONTEXT_MEMORY.process_noise,
        },
        "note": "diagnostic-only prior perturbation; no production model change",
    }
    (args.out / "recipe.json").write_text(json.dumps(recipe, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    print("🧠🌱 Shared Context bias decomposition")
    for row in summaries:
        print(
            f"🐣 {row['candidate']:<20} "
            f"bias={float(row['mean_bias']):+.3f}  "
            f"RMSE={float(row['RMSE']):.3f}  "
            f"shapeRMSE={float(row['centered_RMSE']):.3f}  "
            f"r={float(row['Pearson_r']):.3f}  "
            f"coverage={100.0 * float(row['CI95_coverage']):.1f}%"
        )
    default = next(row for row in summaries if row["candidate"] == "default")
    print(f"🍂 default quiet-law mean bias : {float(default['quiet_predicted_mean_bias']):+.3f}")
    print(f"🧺 result basket               : {args.out}")
    print("☕ Shape tracking and offset are different questions. Tiny brain keeps both receipts.")


if __name__ == "__main__":
    main()
