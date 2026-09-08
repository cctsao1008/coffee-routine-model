from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from coffee_brain.diagnostics import STATE_KEYS
from coffee_brain.redundancy import evaluate_state_redundancy
from coffee_brain.scenarios import get_scenario, scenario_names
from tiny_tools.simulate import generate_truth, observe


DEFAULT_SEED = 20260908


def _write_dict_rows(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def _paint_correlation(path: Path, matrix: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(6.6, 5.5))
    image = ax.imshow(matrix, vmin=-1.0, vmax=1.0)
    ax.set_xticks(np.arange(6), labels=STATE_KEYS)
    ax.set_yticks(np.arange(6), labels=STATE_KEYS)
    ax.set_xlabel("estimated tiny state")
    ax.set_ylabel("estimated tiny state")
    ax.set_title("Posterior estimate correlation: tiny chair test")
    fig.colorbar(image, ax=ax, label="Pearson r")
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Ask whether every tiny latent state really deserves its own chair. 🪑🐣☕"
    )
    parser.add_argument("--days", type=int, default=120)
    parser.add_argument("--particles", type=int, default=800)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument(
        "--scenario",
        choices=["all", *scenario_names()],
        default="all",
        help="one synthetic weather world or all of them",
    )
    parser.add_argument("--out", type=Path, default=Path("examples/state-chair-test"))
    return parser.parse_args()


def _mean_metric(rows: list[dict[str, object]], variant: str, key: str) -> float:
    values = [float(row[key]) for row in rows if row["variant"] == variant and np.isfinite(float(row[key]))]
    return float(np.mean(values)) if values else float("nan")


def main():
    args = parse_args()
    if args.days < 24:
        raise SystemExit("🪑🐣 --days must be at least 24 so train and validation both get a seat.")
    if args.particles < 100:
        raise SystemExit("🐣 --particles must be at least 100. Chair auditions need a proper tiny flock.")

    names = scenario_names() if args.scenario == "all" else (args.scenario,)
    reconstruction_rows: list[dict[str, object]] = []
    variant_rows: list[dict[str, object]] = []
    correlation_rows: list[dict[str, object]] = []
    first_matrix = None

    for offset, name in enumerate(names):
        scenario = get_scenario(name)
        rng = np.random.default_rng(args.seed + 1000 * offset)
        truth, modes = generate_truth(args.days, rng, scenario)
        observations = [observe(truth[t], modes[t], rng, scenario) for t in range(args.days)]
        report = evaluate_state_redundancy(
            truth,
            modes,
            observations,
            particle_count=args.particles,
            seed=args.seed + 1000 * offset,
        )
        if first_matrix is None:
            first_matrix = report.posterior_correlation

        for row in report.reconstruction_rows:
            reconstruction_rows.append({"scenario": name, **row})
        for row in report.variant_rows:
            variant_rows.append({"scenario": name, **row})
        for i, left in enumerate(STATE_KEYS):
            for j, right in enumerate(STATE_KEYS):
                correlation_rows.append(
                    {
                        "scenario": name,
                        "state_a": left,
                        "state_b": right,
                        "Pearson_r": float(report.posterior_correlation[i, j]),
                    }
                )

    args.out.mkdir(parents=True, exist_ok=True)
    _write_dict_rows(args.out / "reconstruction-scorecard.csv", reconstruction_rows)
    _write_dict_rows(args.out / "variant-scorecard.csv", variant_rows)
    _write_dict_rows(args.out / "posterior-correlation.csv", correlation_rows)
    _paint_correlation(args.out / "posterior-correlation.png", np.asarray(first_matrix))

    aggregate: dict[str, list[float]] = {}
    for row in reconstruction_rows:
        aggregate.setdefault(str(row["state"]), []).append(float(row["reconstruction_penalty"]))
    with (args.out / "chair-summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["state", "mean_reconstruction_penalty", "max_abs_posterior_correlation_with_other_state"])
        for state in STATE_KEYS:
            correlations = [
                abs(float(row["Pearson_r"]))
                for row in correlation_rows
                if row["state_a"] == state and row["state_b"] != state
            ]
            writer.writerow([state, float(np.mean(aggregate[state])), max(correlations)])

    print(f"🪑 synthetic worlds checked : {len(names)}")
    for state in STATE_KEYS:
        print(f"🐣 {state} mean chair penalty   : {np.mean(aggregate[state]):+.4f}")

    variants = tuple(dict.fromkeys(str(row["variant"]) for row in variant_rows))
    print("☕ five-seat race averages:")
    for variant in variants:
        print(
            f"  🏁 {variant:30s} "
            f"stateRMSE={_mean_metric(variant_rows, variant, 'mean_state_RMSE'):.4f}  "
            f"NLL={_mean_metric(variant_rows, variant, 'binary_observation_NLL'):.4f}  "
            f"Brier={_mean_metric(variant_rows, variant, 'binary_observation_Brier'):.4f}  "
            f"recoveryR={_mean_metric(variant_rows, variant, 'recovery_relationship_RMSE'):.4f}"
        )

    print(f"🧺 chair-test basket        : {args.out}")
    print("☕ A removable-looking state is a model clue, not a declaration about humans. XD")


if __name__ == "__main__":
    main()
