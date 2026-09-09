from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from coffee_brain.calibration import calibrate_dataset
from coffee_brain.observation_model import DEFAULT_OBSERVATION_MODEL
from coffee_brain.scenarios import get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 365


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ask whether the tiny observation probabilities keep their promises. 🎛️☕🐣"
    )
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--bins", type=int, default=10)
    parser.add_argument(
        "--scenario",
        choices=("all", *scenario_names()),
        default="all",
        help="one tiny weather world, or all of them",
    )
    parser.add_argument("--out", type=Path, default=Path("examples/calibration-bench"))
    return parser.parse_args()


def _write_rows(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main():
    args = parse_args()
    if args.days < 20:
        raise SystemExit("🐣 Calibration wants at least 20 tiny days so the bins are not completely lonely.")
    if args.bins < 2:
        raise SystemExit("🧺 --bins must be at least 2.")

    names = scenario_names() if args.scenario == "all" else (args.scenario,)
    out = args.out
    out.mkdir(parents=True, exist_ok=True)

    channel_rows: list[dict] = []
    reliability_rows: list[dict] = []
    continuous_rows: list[dict] = []
    scenario_rows: list[dict] = []

    for index, name in enumerate(names):
        scenario = get_scenario(name)
        rng = np.random.default_rng(args.seed + index * 1009)
        truth, modes = generate_truth(args.days, rng, scenario)
        observations = [observe(truth[t], modes[t], rng, scenario) for t in range(args.days)]
        result = calibrate_dataset(
            truth,
            modes,
            observations,
            config=DEFAULT_OBSERVATION_MODEL,
            bins=args.bins,
        )

        for row in result.binary:
            channel_rows.append({"scenario": name, **asdict(row)})
        for row in result.reliability:
            reliability_rows.append({"scenario": name, **asdict(row)})
        for row in result.continuous:
            continuous_rows.append({"scenario": name, **asdict(row)})

        max_abs_norm_mean = max(abs(row.normalized_mean) for row in result.continuous)
        mean_norm_std_gap = float(
            np.mean([abs(row.normalized_std - 1.0) for row in result.continuous])
        )
        scenario_rows.append(
            {
                "scenario": name,
                "days": args.days,
                "mean_brier": result.mean_brier,
                "mean_ece": result.mean_ece,
                "max_abs_continuous_normalized_mean": max_abs_norm_mean,
                "mean_abs_continuous_normalized_std_gap": mean_norm_std_gap,
            }
        )

    _write_rows(out / "channel-summary.csv", channel_rows)
    _write_rows(out / "reliability.csv", reliability_rows)
    _write_rows(out / "continuous-summary.csv", continuous_rows)
    _write_rows(out / "scenario-summary.csv", scenario_rows)

    with (out / "baseline-config.json").open("w", encoding="utf-8") as handle:
        json.dump(DEFAULT_OBSERVATION_MODEL.to_dict(), handle, ensure_ascii=False, indent=2)
        handle.write("\n")

    print(f"🎛️ tiny weather worlds checked : {len(names)}")
    print(f"☕ synthetic days per world    : {args.days}")
    print(f"🧺 reliability bins           : {args.bins}")
    print(f"🐣 observation config         : {DEFAULT_OBSERVATION_MODEL.provenance}")
    print(f"✨ calibration basket         : {out}")
    print("🧠 Calibration checks probability promises; learning stays a separate experiment.")


if __name__ == "__main__":
    main()
