from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


STATE_KEYS = ("P", "M", "V", "C", "E", "F")
STATE_TITLES = {
    "P": "Predictability",
    "M": "Mutuality",
    "V": "Voluntariness",
    "C": "Shared Context",
    "E": "State Sharing",
    "F": "Friction",
}
MODE_ORDER = ("Normal", "Busy", "Leave", "Special", "Recovery")
MODE_TO_Y = {name: i for i, name in enumerate(MODE_ORDER)}


def _read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _float_column(rows: list[dict[str, str]], name: str) -> np.ndarray:
    return np.array([float(row[name]) for row in rows], dtype=float)


def _save_state_picture(rows: list[dict[str, str]], state: str, out_dir: Path) -> Path:
    days = _float_column(rows, "sample_id")
    truth = _float_column(rows, f"true_{state}")
    estimate = _float_column(rows, f"est_{state}")
    low = _float_column(rows, f"ci95_low_{state}")
    high = _float_column(rows, f"ci95_high_{state}")

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.fill_between(days, low, high, label="95% tiny uncertainty blanket")
    ax.plot(days, truth, label="synthetic truth")
    ax.plot(days, estimate, label="particle-friend estimate")
    ax.set_xlabel("Cute synthetic day")
    ax.set_ylabel(state)
    ax.set_ylim(0.0, 1.0)
    ax.set_title(f"{state} — {STATE_TITLES[state]} | one tiny coffee year")
    ax.legend()
    fig.tight_layout()

    path = out_dir / f"state-{state}.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _save_mode_picture(rows: list[dict[str, str]], out_dir: Path) -> Path:
    days = _float_column(rows, "sample_id")
    true_mode = np.array([MODE_TO_Y[row["true_mode"]] for row in rows], dtype=float)
    estimated_mode = np.array([MODE_TO_Y[row["estimated_mode"]] for row in rows], dtype=float)

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.plot(days, true_mode, label="synthetic mode")
    ax.plot(days, estimated_mode, label="estimated mode")
    ax.set_xlabel("Cute synthetic day")
    ax.set_ylabel("Tiny routine mode")
    ax.set_yticks(range(len(MODE_ORDER)), MODE_ORDER)
    ax.set_title("Tiny routine weather across 365 coffee days")
    ax.legend()
    fig.tight_layout()

    path = out_dir / "modes.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _save_ess_picture(rows: list[dict[str, str]], out_dir: Path) -> Path:
    days = _float_column(rows, "sample_id")
    ess = _float_column(rows, "ESS")

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.plot(days, ess)
    ax.set_xlabel("Cute synthetic day")
    ax.set_ylabel("Effective sample size")
    ax.set_title("How many tiny particle friends still have useful opinions?")
    fig.tight_layout()

    path = out_dir / "ess.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def _save_summary_picture(rows: list[dict[str, str]], out_dir: Path) -> Path:
    days = _float_column(rows, "sample_id")
    true_r = _float_column(rows, "true_R")
    est_r = _float_column(rows, "est_R")

    fig, ax = plt.subplots(figsize=(12, 4.8))
    ax.plot(days, true_r, label="synthetic routine index")
    ax.plot(days, est_r, label="particle-friend estimate")
    ax.set_xlabel("Cute synthetic day")
    ax.set_ylabel("Synthetic routine index")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("One tiny coffee routine, one whole synthetic year")
    ax.legend()
    fig.tight_layout()

    path = out_dir / "tiny-year-summary.png"
    fig.savefig(path, dpi=160)
    plt.close(fig)
    return path


def paint_coffee_year(output_csv: Path, out_dir: Path | None = None) -> list[Path]:
    """Turn one CSV coffee year into several honest little pictures. 🎨☕"""

    rows = _read_rows(output_csv)
    if not rows:
        raise ValueError("🙈 This coffee-year CSV is empty. Even tiny pictures need tiny data.")

    target = out_dir or output_csv.parent
    target.mkdir(parents=True, exist_ok=True)

    pictures = [_save_state_picture(rows, state, target) for state in STATE_KEYS]
    pictures.append(_save_mode_picture(rows, target))
    pictures.append(_save_ess_picture(rows, target))
    pictures.append(_save_summary_picture(rows, target))
    return pictures


def parse_args():
    parser = argparse.ArgumentParser(description="Paint one tiny coffee year. 🎨☕")
    parser.add_argument(
        "output_csv",
        nargs="?",
        type=Path,
        default=Path("examples/365-cute-days/output.csv"),
        help="simulator output.csv to paint",
    )
    parser.add_argument("--out", type=Path, default=None, help="little picture basket")
    return parser.parse_args()


def main():
    args = parse_args()
    if not args.output_csv.exists():
        raise SystemExit(f"🙈 Tiny painter cannot find: {args.output_csv}")

    pictures = paint_coffee_year(args.output_csv, args.out)
    print("🎨☕ The tiny coffee year is ready for its gallery wall:")
    for picture in pictures:
        print(f"  🖼️  {picture}")


if __name__ == "__main__":
    main()
