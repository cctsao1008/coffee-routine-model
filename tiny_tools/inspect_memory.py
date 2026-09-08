from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.actions import RoutineActions
from coffee_brain.memory import shared_context_input, shared_context_step


def rich_context_action() -> RoutineActions:
    return RoutineActions(
        a_invite=1.0,
        a_deliver=1.0,
        a_notify=1.0,
        a_callback=1.0,
        b_opt_in=1.0,
        b_acknowledge=1.0,
        b_closure=1.0,
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Watch one tiny shared-memory reservoir grow and rest. 🧠🌱")
    parser.add_argument("--build-days", type=int, default=45)
    parser.add_argument("--quiet-days", type=int, default=30)
    parser.add_argument("--long-pause-days", type=int, default=120)
    parser.add_argument("--start", type=float, default=0.35)
    parser.add_argument("--out", type=Path, default=Path("examples/memory-cute-days"))
    return parser.parse_args()


def main():
    args = parse_args()
    if min(args.build_days, args.quiet_days, args.long_pause_days) < 0:
        raise SystemExit("🌱 Tiny memory phases cannot have negative days.")
    if not 0.0 < args.start < 1.0:
        raise SystemExit("🧠 Tiny starting memory must live between 0 and 1.")

    phases = (
        ("build", args.build_days, rich_context_action()),
        ("quiet", args.quiet_days, RoutineActions()),
        ("long-pause", args.long_pause_days, RoutineActions()),
    )

    rows = []
    c = float(args.start)
    day = 0
    for phase, count, actions in phases:
        memory_input = shared_context_input(actions)
        for _ in range(count):
            day += 1
            before = c
            c = float(shared_context_step(c, memory_input))
            rows.append(
                {
                    "day": day,
                    "phase": phase,
                    "memory_input": memory_input,
                    "C_before": before,
                    "C_after": c,
                }
            )

    args.out.mkdir(parents=True, exist_ok=True)
    with (args.out / "memory-story.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["day", "phase", "memory_input", "C_before", "C_after"])
        writer.writeheader()
        writer.writerows(rows)

    day_axis = np.asarray([row["day"] for row in rows])
    c_axis = np.asarray([row["C_after"] for row in rows])
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(day_axis, c_axis, label="Shared Context memory C")
    ax.set_xlabel("tiny day")
    ax.set_ylabel("C")
    ax.set_ylim(0.0, 1.0)
    ax.set_title("🧠🌱 Tiny memories build, rest, and fade slowly")
    ax.legend()
    fig.tight_layout()
    fig.savefig(args.out / "memory-story.png", dpi=150)
    plt.close(fig)

    build_end = rows[args.build_days - 1]["C_after"] if args.build_days else args.start
    quiet_end_index = args.build_days + args.quiet_days - 1
    quiet_end = rows[quiet_end_index]["C_after"] if args.quiet_days else build_end
    final = rows[-1]["C_after"] if rows else args.start

    with (args.out / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["metric", "value"])
        writer.writerow(["start_C", args.start])
        writer.writerow(["after_build_C", build_end])
        writer.writerow(["after_quiet_C", quiet_end])
        writer.writerow(["after_long_pause_C", final])
        writer.writerow(["quiet_retention_ratio", quiet_end / build_end if build_end else ""])
        writer.writerow(["long_pause_retention_ratio", final / build_end if build_end else ""])

    print(f"🧠 start memory              : {args.start:.3f}")
    print(f"🌱 after build               : {build_end:.3f}")
    print(f"☕ after ordinary quiet      : {quiet_end:.3f}")
    print(f"🍂 after long pause          : {final:.3f}")
    print(f"🧺 memory basket             : {args.out}")


if __name__ == "__main__":
    main()
