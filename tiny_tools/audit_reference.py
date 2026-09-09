from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np


STATE_KEYS = ("P", "M", "V", "C", "E", "F")


def summarize_state_excitation(truth: np.ndarray, estimates: np.ndarray) -> list[dict[str, float | str]]:
    """Describe how much each synthetic truth state actually moved. 🔍🌱

    This is an excitation / scope receipt, not a second estimator scorecard. RMSE,
    correlation, and interval coverage stay owned by ``metrics.csv``. ☕📏
    """

    truth = np.asarray(truth, dtype=float)
    estimates = np.asarray(estimates, dtype=float)
    if truth.ndim != 2 or truth.shape[1] != 6 or estimates.shape != truth.shape:
        raise ValueError("🐾 Truth and estimate baskets must both have shape (days, 6).")
    if len(truth) < 2:
        raise ValueError("🌱 State excitation needs at least two synthetic days.")
    if not np.all(np.isfinite(truth)) or not np.all(np.isfinite(estimates)):
        raise ValueError("🐾 State excitation only accepts finite synthetic state values.")

    rows: list[dict[str, float | str]] = []
    for index, state in enumerate(STATE_KEYS):
        true_values = truth[:, index]
        est_values = estimates[:, index]
        rows.append(
            {
                "state": state,
                "truth_mean": float(np.mean(true_values)),
                "truth_std": float(np.std(true_values)),
                "truth_min": float(np.min(true_values)),
                "truth_max": float(np.max(true_values)),
                "truth_span": float(np.ptp(true_values)),
                "estimate_std": float(np.std(est_values)),
                "mean_estimate_minus_truth": float(np.mean(est_values - true_values)),
                "initial_estimate_minus_truth": float(est_values[0] - true_values[0]),
            }
        )
    return rows


def read_state_arrays(path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Read the six truth / estimate columns from one reference output basket. 🧺"""

    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise ValueError("🐣 The reference output basket is empty.")

    truth = np.array([[float(row[f"true_{state}"]) for state in STATE_KEYS] for row in rows])
    estimates = np.array([[float(row[f"est_{state}"]) for state in STATE_KEYS] for row in rows])
    return truth, estimates


def write_state_excitation(output_csv: Path, destination: Path | None = None) -> Path:
    """Write one machine-readable excitation receipt beside the reference scorecard. ☕🔍"""

    truth, estimates = read_state_arrays(output_csv)
    rows = summarize_state_excitation(truth, estimates)
    destination = destination or output_csv.with_name("state-excitation.csv")
    destination.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(rows[0])
    with destination.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Audit how much the six synthetic truth states actually move. ☕🔍🌱"
    )
    parser.add_argument("output_csv", type=Path, help="synthetic output.csv to inspect")
    parser.add_argument("--out", type=Path, default=None, help="optional audit CSV destination")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    destination = write_state_excitation(args.output_csv, args.out)
    print(f"🔍 state excitation receipt : {destination}")
    print("🌱 Low truth variation is evidence about the experiment, not permission to tune the model.")


if __name__ == "__main__":
    main()
