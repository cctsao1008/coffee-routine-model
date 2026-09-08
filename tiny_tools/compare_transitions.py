from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.actions import RoutineActions
from coffee_brain.transitions import (
    TransitionContext,
    context_transition_probabilities,
    fixed_transition_probabilities,
)


DEFAULT_SEED = 20260908
MODE_NAMES = ("Normal", "Busy", "Leave", "Special", "Recovery")


def _tiny_weather(day: int, rng: np.random.Generator):
    """Return one synthetic state + explicit context phase for transition benchmarking. 🌦️☕"""

    phase = day % 100
    state = np.array([0.80, 0.72, 0.90, 0.76, 0.42, 0.10], dtype=float)
    state += rng.normal(0.0, [0.025, 0.025, 0.015, 0.015, 0.025, 0.015])
    actions = RoutineActions()
    context = TransitionContext()
    label = "ordinary"

    if 40 <= phase < 55:
        label = "disturbance"
        state += [-0.18, -0.10, 0.00, 0.00, -0.04, 0.30]
        context = TransitionContext(disturbance=0.75)
    elif 55 <= phase < 65:
        label = "coordinated-exception"
        actions = RoutineActions(a_boundary_preserving=1.0, b_exception_sync=1.0)
        context = TransitionContext(disturbance=0.35)
    elif 65 <= phase < 80:
        label = "recovery"
        actions = RoutineActions(a_notify=1.0, b_closure=1.0)
        context = TransitionContext(recovery_hint=0.85)
    elif 80 <= phase < 90:
        label = "special"
        context = TransitionContext(special_event=1.0)

    return np.clip(state, 0.02, 0.98), actions, context, label


def _multiclass_brier(probability: np.ndarray, target: int) -> float:
    one_hot = np.zeros(5, dtype=float)
    one_hot[target] = 1.0
    return float(np.sum((probability - one_hot) ** 2))


def run_benchmark(days: int, seed: int):
    if days < 120:
        raise ValueError("🌦️🐾 Give the tiny weather track at least 120 days to show its seasons.")

    rng = np.random.default_rng(seed)
    modes = np.zeros(days, dtype=int)
    rows = []

    context_nll = []
    fixed_nll = []
    context_brier = []
    fixed_brier = []
    context_correct = []
    fixed_correct = []

    for t in range(1, days):
        state, actions, context, label = _tiny_weather(t - 1, rng)
        previous = int(modes[t - 1])
        p_context = context_transition_probabilities(previous, state, actions, context)
        p_fixed = fixed_transition_probabilities(previous)

        modes[t] = int(rng.choice(5, p=p_context))
        target = int(modes[t])

        c_nll = -float(np.log(max(p_context[target], 1e-12)))
        f_nll = -float(np.log(max(p_fixed[target], 1e-12)))
        c_brier = _multiclass_brier(p_context, target)
        f_brier = _multiclass_brier(p_fixed, target)
        c_ok = int(np.argmax(p_context) == target)
        f_ok = int(np.argmax(p_fixed) == target)

        context_nll.append(c_nll)
        fixed_nll.append(f_nll)
        context_brier.append(c_brier)
        fixed_brier.append(f_brier)
        context_correct.append(c_ok)
        fixed_correct.append(f_ok)

        rows.append(
            {
                "day": t + 1,
                "weather": label,
                "previous_mode": MODE_NAMES[previous],
                "true_next_mode": MODE_NAMES[target],
                "context_nll": c_nll,
                "fixed_nll": f_nll,
                "context_brier": c_brier,
                "fixed_brier": f_brier,
                "context_top1_correct": c_ok,
                "fixed_top1_correct": f_ok,
            }
        )

    summary = {
        "days": days,
        "transitions": days - 1,
        "seed": seed,
        "context_mean_nll": float(np.mean(context_nll)),
        "fixed_mean_nll": float(np.mean(fixed_nll)),
        "nll_improvement": float(np.mean(fixed_nll) - np.mean(context_nll)),
        "context_mean_brier": float(np.mean(context_brier)),
        "fixed_mean_brier": float(np.mean(fixed_brier)),
        "brier_improvement": float(np.mean(fixed_brier) - np.mean(context_brier)),
        "context_top1_accuracy": float(np.mean(context_correct)),
        "fixed_top1_accuracy": float(np.mean(fixed_correct)),
    }
    return rows, summary


def _paint(path: Path, rows: list[dict]) -> None:
    day = np.array([row["day"] for row in rows], dtype=int)
    context = np.cumsum([row["context_nll"] for row in rows])
    fixed = np.cumsum([row["fixed_nll"] for row in rows])

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(day, context, label="context-aware cumulative NLL")
    ax.plot(day, fixed, label="fixed-matrix cumulative NLL")
    ax.set_xlabel("synthetic day")
    ax.set_ylabel("cumulative negative log likelihood")
    ax.set_title("Tiny mode-dice weather race 🌦️🎲☕")
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Let fixed mode dice race context-aware dice on the same synthetic weather track. 🌦️🎲"
    )
    parser.add_argument("--days", type=int, default=400)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out", type=Path, default=Path("examples/transition-weather"))
    return parser.parse_args()


def main():
    args = parse_args()
    rows, summary = run_benchmark(args.days, args.seed)
    args.out.mkdir(parents=True, exist_ok=True)

    with (args.out / "transitions.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    with (args.out / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        for key, value in summary.items():
            writer.writerow([key, value])

    _paint(args.out / "transition-race.png", rows)

    print(f"🌦️ synthetic transition days : {args.days}")
    print(f"🎲 context-aware mean NLL    : {summary['context_mean_nll']:.4f}")
    print(f"🧺 fixed-matrix mean NLL     : {summary['fixed_mean_nll']:.4f}")
    print(f"✨ NLL improvement           : {summary['nll_improvement']:.4f}")
    print(f"🐣 context-aware top-1      : {summary['context_top1_accuracy']:.2%}")
    print(f"☕ fixed-matrix top-1       : {summary['fixed_top1_accuracy']:.2%}")
    print(f"🗺️ tiny weather basket      : {args.out}")


if __name__ == "__main__":
    main()
