from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.diagnostics import STATE_KEYS
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario, scenario_names
from coffee_brain.sensitivity import evaluate_sensitivity
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _paint_heatmap(path: Path, labels: tuple[str, ...], matrix: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(10.5, max(6.0, 0.36 * len(labels))))
    image = ax.imshow(matrix, aspect="auto")
    ax.set_xticks(np.arange(len(STATE_KEYS)), labels=STATE_KEYS)
    ax.set_yticks(np.arange(len(labels)), labels=labels)
    ax.set_xlabel("tiny latent state")
    ax.set_ylabel("one-at-a-time poke")
    ax.set_title("Tiny sensitivity map: signed relative RMSE change")
    cbar = fig.colorbar(image, ax=ax)
    cbar.set_label("(variant RMSE - baseline RMSE) / baseline RMSE")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Poke one clue or assumption at a time and see which tiny state wiggles. 🧪🗺️☕"
    )
    parser.add_argument("--days", type=int, default=120)
    parser.add_argument("--particles", type=int, default=800)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--scenario", choices=scenario_names(), default=DEFAULT_SCENARIO)
    parser.add_argument("--out", type=Path, default=Path("examples/sensitivity-map"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 20:
        raise SystemExit("🧪🐣 --days must be at least 20 so the tiny pokes have room to show up.")
    if args.particles < 100:
        raise SystemExit("🐣 --particles must be at least 100. Tiny sensitivity flocks dislike loneliness.")

    scenario = get_scenario(args.scenario)
    rng = np.random.default_rng(args.seed)
    truth, modes = generate_truth(args.days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(args.days)]

    report = evaluate_sensitivity(
        truth,
        modes,
        observations,
        particle_count=args.particles,
        seed=args.seed,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    rows = report.rows()
    _write_rows(args.out / "sensitivity.csv", rows)
    labels, matrix = report.matrix()
    _paint_heatmap(args.out / "sensitivity-map.png", labels, matrix)

    with (args.out / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["state", "most_sensitive_variant", "absolute_relative_RMSE_change"])
        for i, state in enumerate(STATE_KEYS):
            index = int(np.argmax(np.abs(matrix[:, i])))
            writer.writerow([state, labels[index], abs(float(matrix[index, i]))])

    print(f"{scenario.emoji} weather                 : {scenario.title}")
    print(f"🧪 tiny sensitivity pokes : {len(labels)}")
    print(f"🐣 particles per poke      : {args.particles}")
    for i, state in enumerate(STATE_KEYS):
        index = int(np.argmax(np.abs(matrix[:, i])))
        print(f"🗺️ {state} biggest wobble         : {labels[index]} ({matrix[index, i]:+.3f})")
    print(f"🧺 sensitivity basket      : {args.out}")
    print("☕ Sensitivity is not causality. Tiny brain keeps its paws off that shortcut. XD")


if __name__ == "__main__":
    main()
