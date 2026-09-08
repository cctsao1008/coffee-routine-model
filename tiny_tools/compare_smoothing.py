from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.model import MODE_NAMES, RoutineMode, relationship_index
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import get_scenario, scenario_names
from coffee_brain.smoothing import smooth_history
from tiny_tools.simulate import generate_truth, observe


STATE_KEYS = ("P", "M", "V", "C", "E", "F")


def parse_args():
    parser = argparse.ArgumentParser(description="Give yesterday a tiny hindsight hat. 🔭🐣☕")
    parser.add_argument("--days", type=int, default=120)
    parser.add_argument("--particles", type=int, default=800)
    parser.add_argument("--lag", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--scenario", choices=scenario_names(), default="slow-recovery")
    parser.add_argument("--full-history", action="store_true")
    parser.add_argument("--out", type=Path, default=Path("examples/smoothing-cute-days"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 3:
        raise SystemExit("🔭🐾 Hindsight needs at least three tiny days to look backward from.")
    if args.particles < 100:
        raise SystemExit("🐣 Please invite at least 100 particle friends to the hindsight picnic.")
    if args.lag < 0:
        raise SystemExit("🔭 Tiny smoothing lag cannot be negative.")

    scenario = get_scenario(args.scenario)
    rng = np.random.default_rng(args.seed)
    truth, true_modes = generate_truth(args.days, rng, scenario)
    observations = [observe(truth[t], true_modes[t], rng, scenario) for t in range(args.days)]

    pf = CoffeeParticleFilter(particle_count=args.particles, seed=args.seed, record_history=True)
    filtered = []
    filtered_modes = []
    for obs in observations:
        posterior = pf.update(obs)
        filtered.append(posterior.mean)
        filtered_modes.append(posterior.mode)

    filtered = np.asarray(filtered)
    smoothed_items = smooth_history(pf.history, lag=args.lag, full_history=args.full_history)
    smoothed = np.asarray([item.mean for item in smoothed_items])
    smoothed_modes = [item.mode for item in smoothed_items]

    filtered_rmse = np.sqrt(np.mean((filtered - truth) ** 2, axis=0))
    smoothed_rmse = np.sqrt(np.mean((smoothed - truth) ** 2, axis=0))
    true_mode_names = [MODE_NAMES[RoutineMode(int(mode))] for mode in true_modes]
    filtered_mode_accuracy = float(np.mean(np.asarray(filtered_modes) == np.asarray(true_mode_names)))
    smoothed_mode_accuracy = float(np.mean(np.asarray(smoothed_modes) == np.asarray(true_mode_names)))

    true_r = relationship_index(truth)
    filtered_r = relationship_index(filtered)
    smoothed_r = relationship_index(smoothed)
    filtered_r_rmse = float(np.sqrt(np.mean((filtered_r - true_r) ** 2)))
    smoothed_r_rmse = float(np.sqrt(np.mean((smoothed_r - true_r) ** 2)))

    args.out.mkdir(parents=True, exist_ok=True)

    with (args.out / "comparison.csv").open("w", newline="", encoding="utf-8") as handle:
        fieldnames = ["sample_id", "true_mode", "filtered_mode", "smoothed_mode", "hindsight_endpoint"]
        for key in STATE_KEYS:
            fieldnames += [f"true_{key}", f"filtered_{key}", f"smoothed_{key}"]
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for index, item in enumerate(smoothed_items):
            row = {
                "sample_id": index + 1,
                "true_mode": true_mode_names[index],
                "filtered_mode": filtered_modes[index],
                "smoothed_mode": smoothed_modes[index],
                "hindsight_endpoint": item.endpoint + 1,
            }
            for state_index, key in enumerate(STATE_KEYS):
                row[f"true_{key}"] = truth[index, state_index]
                row[f"filtered_{key}"] = filtered[index, state_index]
                row[f"smoothed_{key}"] = smoothed[index, state_index]
            writer.writerow(row)

    with (args.out / "metrics.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric_scope", "filtered", "smoothed", "delta_smoothed_minus_filtered"])
        for key, before, after in zip(STATE_KEYS, filtered_rmse, smoothed_rmse):
            writer.writerow([f"{key}_RMSE", before, after, after - before])
        writer.writerow(["relationship_index_RMSE", filtered_r_rmse, smoothed_r_rmse, smoothed_r_rmse - filtered_r_rmse])
        writer.writerow(["mode_accuracy", filtered_mode_accuracy, smoothed_mode_accuracy, smoothed_mode_accuracy - filtered_mode_accuracy])

    day_axis = np.arange(1, args.days + 1)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(day_axis, true_r, label="synthetic truth")
    ax.plot(day_axis, filtered_r, label="filtered: what the tiny brain knew then")
    ax.plot(day_axis, smoothed_r, label="smoothed: tiny hindsight")
    ax.set_xlabel("tiny day")
    ax.set_ylabel("synthetic relationship index R")
    ax.set_title("🔭 One coffee timeline wearing a tiny hindsight hat")
    ax.legend()
    fig.tight_layout()
    fig.savefig(args.out / "hindsight.png", dpi=150)
    plt.close(fig)

    horizon = "full history" if args.full_history else f"fixed lag = {args.lag}"
    print(f"🔭 hindsight horizon          : {horizon}")
    print(f"☕ filtered R RMSE           : {filtered_r_rmse:.4f}")
    print(f"🎩 smoothed R RMSE           : {smoothed_r_rmse:.4f}")
    print(f"🐣 filtered mode accuracy    : {filtered_mode_accuracy:.2%}")
    print(f"✨ smoothed mode accuracy    : {smoothed_mode_accuracy:.2%}")
    print(f"🧺 hindsight basket          : {args.out}")


if __name__ == "__main__":
    main()
