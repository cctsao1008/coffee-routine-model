from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.change_points import ChangePointResult, detect_observation_change_point
from coffee_brain.scenarios import get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908


def _make_observations(
    *,
    days: int,
    change_day: int | None,
    before_name: str,
    after_name: str,
    seed: int,
):
    """Grow one continuous hidden timeline, then optionally switch observation weather. 🌦️✂️"""

    before = get_scenario(before_name)
    after = get_scenario(after_name)
    truth_rng = np.random.default_rng(seed)
    obs_rng = np.random.default_rng(seed + 1)
    truth, modes = generate_truth(days, truth_rng, before)

    boundary = None if change_day is None else change_day - 1
    observations = []
    for t in range(days):
        world = before if boundary is None or t < boundary else after
        observations.append(observe(truth[t], modes[t], obs_rng, world))
    return observations


def _write_scores(path: Path, label: str, result: ChangePointResult) -> None:
    mode = "w" if not path.exists() else "a"
    with path.open(mode, newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        if mode == "w":
            writer.writerow(
                [
                    "timeline",
                    "boundary_day",
                    "score",
                    "posterior_probability",
                    "conditional_probability_given_change",
                ]
            )
        for row in result.evidence:
            writer.writerow(
                [
                    label,
                    row.boundary_day,
                    row.score,
                    row.posterior_probability,
                    row.conditional_probability,
                ]
            )


def _write_summary(
    path: Path,
    *,
    changed: ChangePointResult,
    stable: ChangePointResult,
    true_change_day: int,
    before_name: str,
    after_name: str,
) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "timeline",
                "before_world",
                "after_world",
                "detected",
                "change_probability",
                "no_change_probability",
                "best_boundary_day",
                "true_change_day",
                "absolute_timing_error_days",
                "ci90_start_day",
                "ci90_end_day",
            ]
        )
        writer.writerow(
            [
                "known-shift",
                before_name,
                after_name,
                changed.detected,
                changed.change_probability,
                changed.no_change_probability,
                changed.best_boundary_day,
                true_change_day,
                abs(changed.best_boundary_day - true_change_day),
                changed.conditional_ci90_start_day,
                changed.conditional_ci90_end_day,
            ]
        )
        writer.writerow(
            [
                "stable-control",
                before_name,
                before_name,
                stable.detected,
                stable.change_probability,
                stable.no_change_probability,
                stable.best_boundary_day,
                "",
                "",
                stable.conditional_ci90_start_day,
                stable.conditional_ci90_end_day,
            ]
        )


def _paint_story(
    path: Path,
    result: ChangePointResult,
    true_change_day: int,
) -> None:
    days = np.array([row.boundary_day for row in result.evidence], dtype=int)
    probability = np.array([row.conditional_probability for row in result.evidence], dtype=float)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(days, probability, label="boundary probability | one change")
    ax.axvline(true_change_day, linestyle="--", label="true tiny boundary")
    ax.axvline(result.best_boundary_day, linestyle=":", label="best detected boundary")
    ax.set_xlabel("candidate boundary day")
    ax.set_ylabel("conditional probability")
    ax.set_title("Tiny change-point garden ✂️🐣☕")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ask whether one synthetic coffee world quietly became another. ✂️☕🐣"
    )
    parser.add_argument("--days", type=int, default=240)
    parser.add_argument("--change-day", type=int, default=121)
    parser.add_argument("--min-segment", type=int, default=30)
    parser.add_argument("--change-prior", type=float, default=0.20)
    parser.add_argument("--before", choices=scenario_names(), default="cozy-normal-year")
    parser.add_argument("--after", choices=scenario_names(), default="sleepy-reply-season")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=Path("examples/change-point-garden"))
    return parser.parse_args()


def main():
    args = parse_args()
    if args.days < 2 * args.min_segment:
        raise SystemExit("✂️🐾 The tiny timeline is too short for two proper regimes.")
    if not args.min_segment < args.change_day <= args.days - args.min_segment + 1:
        raise SystemExit("✂️🐣 --change-day must leave a full tiny segment on both sides.")

    changed_obs = _make_observations(
        days=args.days,
        change_day=args.change_day,
        before_name=args.before,
        after_name=args.after,
        seed=args.seed,
    )
    stable_obs = _make_observations(
        days=args.days,
        change_day=None,
        before_name=args.before,
        after_name=args.before,
        seed=args.seed + 100,
    )

    changed = detect_observation_change_point(
        changed_obs,
        min_segment=args.min_segment,
        change_prior=args.change_prior,
    )
    stable = detect_observation_change_point(
        stable_obs,
        min_segment=args.min_segment,
        change_prior=args.change_prior,
    )

    args.out.mkdir(parents=True, exist_ok=True)
    score_path = args.out / "boundary-score.csv"
    if score_path.exists():
        score_path.unlink()
    _write_scores(score_path, "known-shift", changed)
    _write_scores(score_path, "stable-control", stable)
    _write_summary(
        args.out / "summary.csv",
        changed=changed,
        stable=stable,
        true_change_day=args.change_day,
        before_name=args.before,
        after_name=args.after,
    )
    _paint_story(args.out / "change-point.png", changed, args.change_day)

    print(f"✂️ true tiny boundary         : day {args.change_day}")
    print(f"🐣 best detected boundary    : day {changed.best_boundary_day}")
    print(f"🧭 timing error              : {abs(changed.best_boundary_day - args.change_day)} day(s)")
    print(f"☕ change probability        : {changed.change_probability:.3f}")
    print(f"🌤️ stable-control change p  : {stable.change_probability:.3f}")
    print(f"🧺 little scissors basket    : {args.out}")


if __name__ == "__main__":
    main()
