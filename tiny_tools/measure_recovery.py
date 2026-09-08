from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.recovery import (
    NominalRoutineSet,
    detect_recovery_events,
    event_rows,
    summarize_recovery,
)
from coffee_brain.scenarios import DEFAULT_SCENARIO, get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908
DEFAULT_DAYS = 365


def _write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _paint_recovery_story(
    path: Path,
    states: np.ndarray,
    modes: np.ndarray,
    nominal_set: NominalRoutineSet,
    events,
) -> None:
    distances = np.array([nominal_set.distance(state) for state in states], dtype=float)

    if events:
        event = events[0]
        left = max(0, event.start_index - 4)
        right_anchor = event.recovered_index if event.recovered_index is not None else event.disturbance_end_index + 8
        right = min(len(states), right_anchor + 5)
    else:
        left = 0
        right = len(states)

    days = np.arange(left, right)
    fig, ax = plt.subplots(figsize=(11, 4.8))
    ax.plot(days, distances[left:right], label="distance outside the cozy nominal set")
    ax.axhline(0.0, linestyle="--", label="inside the nominal set")

    if events:
        event = events[0]
        ax.axvline(event.start_index, linestyle=":", label="disturbance starts")
        ax.axvline(event.disturbance_end_index, linestyle=":", label="disturbance ends")
        if event.recovered_index is not None:
            ax.axvline(event.recovered_index, linestyle=":", label="tiny recovery arrives 🌱")
        ax.set_title("One tiny wobble finding its way back home 🌧️➡️🌱")
    else:
        ax.set_title("No tiny disturbance wandered through this little window ☕🌤️")

    ax.set_xlabel("Synthetic day")
    ax.set_ylabel("Normalized distance")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(description="Measure how tiny routine wobbles find their way home. 🌱🩹☕")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="synthetic days (default: 365)")
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
        default=Path("examples/recovery-garden"),
        help="little recovery basket",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 8:
        raise SystemExit("🌱🐾 --days must be at least 8 so a tiny wobble has room to come home.")

    scenario = get_scenario(args.scenario)
    out = args.out
    if scenario.slug != DEFAULT_SCENARIO and out == Path("examples/recovery-garden"):
        out = out / scenario.slug

    rng = np.random.default_rng(args.seed)
    states, modes = generate_truth(args.days, rng, scenario)
    observations = [observe(states[t], modes[t], rng, scenario) for t in range(args.days)]
    nominal_set = NominalRoutineSet.from_target(scenario.target)
    events = detect_recovery_events(
        states,
        modes,
        nominal_set,
        observations=observations,
    )
    summary = summarize_recovery(events)

    out.mkdir(parents=True, exist_ok=True)
    _write_csv(
        out / "events.csv",
        event_rows(events),
        [
            "disturbance_id",
            "start_index",
            "disturbance_end_index",
            "disturbance_duration",
            "recovered_index",
            "recovery_time",
            "repair_cost",
            "natural_resume",
            "resilience",
        ],
    )
    _write_csv(out / "summary.csv", [summary.as_row()], list(summary.as_row().keys()))
    _paint_recovery_story(out / "recovery-story.png", states, modes, nominal_set, events)

    print(f"{scenario.emoji} weather              : {scenario.title}")
    print(f"🌧️ disturbances         : {summary.total_disturbances}")
    print(f"🌱 recovered             : {summary.recovered_disturbances}")
    print(f"🧭 recovery ratio        : {summary.recovery_ratio:.2%}")
    print(f"🩹 mean repair cost      : {summary.mean_repair_cost:.3f}")
    print(f"☕ mean resilience       : {summary.mean_resilience:.3f}")
    print(f"🧺 tiny recovery basket : {out}")


if __name__ == "__main__":
    main()
