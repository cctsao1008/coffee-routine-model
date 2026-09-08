from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from coffee_brain.diagnostics import evaluate_observability
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 365
DEFAULT_PARTICLES = 2000


def _write_rows(path: Path, rows: list[dict[str, object]]) -> None:
    if not rows:
        raise ValueError("🙈 No tiny diagnostic rows showed up for this basket.")
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ask which clues can actually see the six tiny coffee states. 🐣🔍☕"
    )
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="synthetic days (default: 365)")
    parser.add_argument(
        "--particles",
        type=int,
        default=DEFAULT_PARTICLES,
        help="particle friends per ablation run (default: 2000)",
    )
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="random seed")
    parser.add_argument(
        "--scenario",
        choices=scenario_names(),
        default=DEFAULT_SCENARIO,
        help=f"tiny coffee weather (default: {DEFAULT_SCENARIO})",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("examples/observability-garden"),
        help="little diagnostic basket",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 12:
        raise SystemExit("🔍🐣 --days must be at least 12 so the tiny correlations have something to chew on.")
    if args.particles < 100:
        raise SystemExit("🐣 --particles must be at least 100. The observability flock feels too lonely.")

    scenario = get_scenario(args.scenario)
    out = args.out
    if scenario.slug != DEFAULT_SCENARIO and out == Path("examples/observability-garden"):
        out = out / scenario.slug

    rng = np.random.default_rng(args.seed)
    truth, true_modes = generate_truth(args.days, rng, scenario)
    observations = [
        observe(truth[t], true_modes[t], rng, scenario)
        for t in range(args.days)
    ]

    report = evaluate_observability(
        truth,
        true_modes,
        observations,
        particle_count=args.particles,
        seed=args.seed,
    )

    out.mkdir(parents=True, exist_ok=True)
    _write_rows(out / "scorecard.csv", report.scorecard_rows())
    _write_rows(out / "clue-visibility.csv", report.clue_visibility_rows())
    _write_rows(out / "state-identifiability.csv", list(report.state_identifiability))

    weakest_index = int(np.nanargmin(report.baseline.correlation))
    weakest_state = ("P", "M", "V", "C", "E", "F")[weakest_index]
    weakest_r = report.baseline.correlation[weakest_index]
    smallest_margin = min(
        report.state_identifiability,
        key=lambda row: row["identification_margin"],
    )

    print(f"{scenario.emoji} weather                  : {scenario.title}")
    print(f"🔍 observability days       : {args.days}")
    print(f"🐣 particles per experiment : {args.particles}")
    print(f"🙈 weakest baseline state   : {weakest_state} (r={weakest_r:.3f})")
    print(
        "🧩 smallest identity margin : "
        f"{smallest_margin['estimated_state']} vs "
        f"{smallest_margin['strongest_other_truth_state']} "
        f"({smallest_margin['identification_margin']:.3f})"
    )
    print(f"🧺 tiny diagnostic basket   : {out}")
    print("☕✨ Estimable is not automatically identifiable. Tiny brain has been warned.")


if __name__ == "__main__":
    main()
