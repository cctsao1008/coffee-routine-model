from __future__ import annotations

import argparse
import csv
import json
from dataclasses import asdict
from pathlib import Path

import numpy as np

from coffee_brain.learning import calibration_metrics, run_learning_experiment
from coffee_brain.observation_model import DEFAULT_OBSERVATION_MODEL
from coffee_brain.scenarios import get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Teach a few tiny observation knobs without feeding the whole model to an optimizer. 🎚️🐣☕"
    )
    parser.add_argument("--days", type=int, default=480)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--train-fraction", type=float, default=0.60)
    parser.add_argument("--bins", type=int, default=8)
    parser.add_argument(
        "--scenario",
        choices=scenario_names(),
        default="special-day-sparkle",
        help="synthetic weather used for the learning bench",
    )
    parser.add_argument("--out", type=Path, default=Path("examples/parameter-learning-spoon"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 80:
        raise SystemExit("🎚️🐣 --days must be at least 80 so train and validation both get enough crumbs.")

    scenario = get_scenario(args.scenario)
    rng = np.random.default_rng(args.seed)
    truth, modes = generate_truth(args.days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(args.days)]
    experiment = run_learning_experiment(
        truth,
        modes,
        observations,
        train_fraction=args.train_fraction,
        bins=args.bins,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    parameter_rows = [asdict(row) for row in experiment.parameters]
    _write_rows(args.out / "parameters.csv", parameter_rows)

    metric_rows: list[dict[str, object]] = []
    for split_name, stage, result in (
        ("train", "before", experiment.train_before),
        ("train", "after", experiment.train_after),
        ("validation", "before", experiment.validation_before),
        ("validation", "after", experiment.validation_after),
    ):
        for metric, value in calibration_metrics(result).items():
            metric_rows.append({"split": split_name, "stage": stage, "metric": metric, "value": value})
    _write_rows(args.out / "metrics.csv", metric_rows)

    with (args.out / "baseline-config.json").open("w", encoding="utf-8") as handle:
        json.dump(DEFAULT_OBSERVATION_MODEL.to_dict(), handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    with (args.out / "learned-config.json").open("w", encoding="utf-8") as handle:
        json.dump(experiment.learned_config.to_dict(), handle, indent=2, ensure_ascii=False)
        handle.write("\n")

    before = calibration_metrics(experiment.validation_before)
    after = calibration_metrics(experiment.validation_after)
    print(f"{scenario.emoji} learning weather         : {scenario.title}")
    print(f"🎚️ train / validation days  : {experiment.split_index} / {args.days - experiment.split_index}")
    print(f"🥄 learned tiny knobs        : {len(experiment.parameters)}")
    print(f"☕ validation log loss       : {before['mean_binary_log_loss']:.4f} -> {after['mean_binary_log_loss']:.4f}")
    print(f"🐣 validation Brier          : {before['mean_binary_brier']:.4f} -> {after['mean_binary_brier']:.4f}")
    print(f"📏 delay normalized std      : {before['delay_normalized_std']:.3f} -> {after['delay_normalized_std']:.3f}")
    print(f"🧺 learning basket           : {args.out}")
    print("🧠 Better fit is not better ontology. Synthetic learning remains synthetic.")


if __name__ == "__main__":
    main()
