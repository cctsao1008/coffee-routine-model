from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.arena import run_model_arena
from coffee_brain.scenarios import get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _paint_bars(path: Path, labels: list[str], values: list[float], title: str, ylabel: str) -> None:
    fig, ax = plt.subplots(figsize=(9.5, 4.8))
    positions = np.arange(len(labels))
    ax.bar(positions, values)
    ax.set_xticks(positions, labels=labels, rotation=24, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Let several tiny model families share one basket without declaring a universal champion. 🗺️☕🐣"
    )
    parser.add_argument("--days", type=int, default=240)
    parser.add_argument("--particles", type=int, default=400)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--train-fraction", type=float, default=0.60)
    parser.add_argument("--smoothing-lag", type=int, default=12)
    parser.add_argument(
        "--scenario",
        choices=scenario_names(),
        default="special-day-sparkle",
    )
    parser.add_argument("--out", type=Path, default=Path("examples/model-arena"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 80:
        raise SystemExit("🗺️🐣 --days must be at least 80. Tiny models need enough track to race fairly.")
    if args.particles < 100:
        raise SystemExit("🐣 --particles must be at least 100. The arena flock is too tiny otherwise.")

    scenario = get_scenario(args.scenario)
    rng = np.random.default_rng(args.seed)
    truth, modes = generate_truth(args.days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(args.days)]

    summaries, state_rows, runs = run_model_arena(
        truth,
        modes,
        observations,
        particle_count=args.particles,
        seed=args.seed,
        train_fraction=args.train_fraction,
        smoothing_lag=args.smoothing_lag,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    _write_rows(args.out / "comparison.csv", summaries)
    _write_rows(args.out / "state-rmse.csv", state_rows)

    labels = [row["model"] for row in summaries]
    _paint_bars(
        args.out / "arena-state-rmse.png",
        labels,
        [float(row["mean_state_RMSE"]) for row in summaries],
        "Tiny model arena: held-out mean state RMSE",
        "RMSE",
    )
    _paint_bars(
        args.out / "arena-runtime.png",
        labels,
        [float(row["runtime_seconds"]) for row in summaries],
        "Tiny model arena: runtime cost",
        "seconds",
    )

    with (args.out / "arena-notes.md").open("w", encoding="utf-8") as handle:
        handle.write("# Tiny Arena Notes 🗺️☕🐣\n\n")
        handle.write(f"Synthetic weather: `{scenario.slug}`  \n")
        handle.write(f"Days: `{args.days}`  \n")
        handle.write(f"Particles per PF competitor: `{args.particles}`  \n")
        handle.write(f"Train fraction: `{args.train_fraction:.2f}`  \n\n")
        handle.write("```text\nWinner != truth.\nOne metric != model quality.\n```\n\n")
        for run in runs:
            handle.write(f"- **{run.name}** — {run.notes}\n")
        handle.write("\nObservation NLL/Brier are scored with the synthetic true mode held fixed so they isolate state-representation quality. That is a diagnostic convenience, not a deployable real-world privilege.\n")
        handle.write("\nChange-point metrics are marked not-applicable because this arena uses one stationary synthetic weather basket.\n")

    print(f"{scenario.emoji} arena weather            : {scenario.title}")
    print(f"🗺️ tiny competitors         : {len(summaries)}")
    print("☕ held-out trade-offs:")
    for row in summaries:
        print(
            f"  🐣 {row['model']:<32} "
            f"stateRMSE={float(row['mean_state_RMSE']):.4f}  "
            f"NLL={float(row['obs_NLL_given_true_mode']):.4f}  "
            f"runtime={float(row['runtime_seconds']):.3f}s"
        )
    print(f"🧺 arena basket             : {args.out}")
    print("🧠 No crown awarded. Tiny models keep their trade-offs visible.")


if __name__ == "__main__":
    main()
