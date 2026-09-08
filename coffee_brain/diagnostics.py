from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

import numpy as np

from .model import MODE_NAMES, RoutineMode
from .particles import CoffeeParticleFilter


STATE_KEYS = ("P", "M", "V", "C", "E", "F")

CLUE_FAMILIES: dict[str, tuple[str, ...]] = {
    "opt_in_or_pass": ("opt_in", "pass_event"),
    "text_reply": ("text_reply",),
    "reaction": ("reaction",),
    "state_share": ("state_share",),
    "proactive_update": ("proactive_update",),
    "routine_maintenance": ("routine_maintenance",),
    "resume_signal": ("resume_signal",),
    "tone_warmth": ("tone_warmth",),
    "response_delay": ("response_delay_min",),
}


def _safe_pearson(a: np.ndarray, b: np.ndarray) -> float:
    """Return a calm little correlation, or NaN when the data cannot speak. 🐣"""

    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    if a.size < 2 or b.size < 2 or np.std(a) == 0.0 or np.std(b) == 0.0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def ablate_observations(
    observations: Sequence[Mapping[str, object]],
    keys: Iterable[str],
) -> list[dict[str, object]]:
    """Hide selected clue channels without rewriting the observed little story. 🙈☕"""

    hidden = tuple(keys)
    tiny_baskets: list[dict[str, object]] = []
    for observation in observations:
        basket = dict(observation)
        for key in hidden:
            basket[key] = None
        tiny_baskets.append(basket)
    return tiny_baskets


@dataclass(frozen=True)
class ExperimentMetrics:
    label: str
    removed_family: str
    estimates: np.ndarray
    rmse: np.ndarray
    mae: np.ndarray
    correlation: np.ndarray
    ci95_mean_width: np.ndarray
    ci95_coverage: np.ndarray
    mode_accuracy: float


@dataclass(frozen=True)
class ObservabilityReport:
    """Practical synthetic observability evidence, not a magical proof. 🔍🐾"""

    baseline: ExperimentMetrics
    ablations: dict[str, ExperimentMetrics]
    state_identifiability: tuple[dict[str, object], ...]

    def scorecard_rows(self) -> list[dict[str, object]]:
        """Flatten every experiment into a CSV-friendly little scorecard. 🧺"""

        rows: list[dict[str, object]] = []
        experiments = [self.baseline, *self.ablations.values()]
        for experiment in experiments:
            for index, state in enumerate(STATE_KEYS):
                rows.append(
                    {
                        "experiment": experiment.label,
                        "removed_family": experiment.removed_family,
                        "state": state,
                        "RMSE": float(experiment.rmse[index]),
                        "MAE": float(experiment.mae[index]),
                        "Pearson_r": float(experiment.correlation[index]),
                        "CI95_mean_width": float(experiment.ci95_mean_width[index]),
                        "CI95_coverage": float(experiment.ci95_coverage[index]),
                        "mode_accuracy": float(experiment.mode_accuracy),
                    }
                )
        return rows

    def clue_visibility_rows(self) -> list[dict[str, object]]:
        """Show how much each hidden clue family makes every state wobble. 🌱🔍"""

        rows: list[dict[str, object]] = []
        base = self.baseline
        for family, experiment in self.ablations.items():
            for index, state in enumerate(STATE_KEYS):
                rows.append(
                    {
                        "removed_family": family,
                        "state": state,
                        "RMSE_penalty": float(experiment.rmse[index] - base.rmse[index]),
                        "correlation_loss": float(base.correlation[index] - experiment.correlation[index]),
                        "CI95_width_increase": float(
                            experiment.ci95_mean_width[index] - base.ci95_mean_width[index]
                        ),
                    }
                )
        return rows


def _run_filter(
    truth: np.ndarray,
    true_modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
    *,
    particle_count: int,
    seed: int,
    label: str,
    removed_family: str,
) -> ExperimentMetrics:
    if len(truth) != len(true_modes) or len(truth) != len(observations):
        raise ValueError("🐾 Truth, modes, and clue baskets must have the same tiny length.")

    pf = CoffeeParticleFilter(particle_count=particle_count, seed=seed)
    estimates: list[np.ndarray] = []
    lows: list[np.ndarray] = []
    highs: list[np.ndarray] = []
    estimated_modes: list[str] = []

    for observation in observations:
        posterior = pf.update(dict(observation))
        estimates.append(posterior.mean)
        lows.append(posterior.ci95_low)
        highs.append(posterior.ci95_high)
        estimated_modes.append(posterior.mode)

    estimate_array = np.asarray(estimates, dtype=float)
    low_array = np.asarray(lows, dtype=float)
    high_array = np.asarray(highs, dtype=float)
    truth = np.asarray(truth, dtype=float)
    true_modes = np.asarray(true_modes, dtype=int)

    rmse = np.sqrt(np.mean((estimate_array - truth) ** 2, axis=0))
    mae = np.mean(np.abs(estimate_array - truth), axis=0)
    correlation = np.array(
        [_safe_pearson(estimate_array[:, i], truth[:, i]) for i in range(len(STATE_KEYS))],
        dtype=float,
    )
    ci95_mean_width = np.mean(high_array - low_array, axis=0)
    ci95_coverage = np.mean((truth >= low_array) & (truth <= high_array), axis=0)
    mode_accuracy = float(
        np.mean(
            [
                estimated_modes[t] == MODE_NAMES[RoutineMode(int(true_modes[t]))]
                for t in range(len(true_modes))
            ]
        )
    )

    return ExperimentMetrics(
        label=label,
        removed_family=removed_family,
        estimates=estimate_array,
        rmse=rmse,
        mae=mae,
        correlation=correlation,
        ci95_mean_width=ci95_mean_width,
        ci95_coverage=ci95_coverage,
        mode_accuracy=mode_accuracy,
    )


def _state_identifiability_rows(
    estimates: np.ndarray,
    truth: np.ndarray,
) -> tuple[dict[str, object], ...]:
    """Compare each estimated state with every synthetic truth state for cross-talk clues. 🐾"""

    matrix = np.empty((len(STATE_KEYS), len(STATE_KEYS)), dtype=float)
    for estimate_index in range(len(STATE_KEYS)):
        for truth_index in range(len(STATE_KEYS)):
            matrix[estimate_index, truth_index] = _safe_pearson(
                estimates[:, estimate_index], truth[:, truth_index]
            )

    rows: list[dict[str, object]] = []
    for estimate_index, estimate_state in enumerate(STATE_KEYS):
        self_r = matrix[estimate_index, estimate_index]
        other_indices = [index for index in range(len(STATE_KEYS)) if index != estimate_index]
        strongest_other_index = max(
            other_indices,
            key=lambda index: -np.inf if np.isnan(matrix[estimate_index, index]) else abs(matrix[estimate_index, index]),
        )
        strongest_other_r = matrix[estimate_index, strongest_other_index]
        margin = abs(self_r) - abs(strongest_other_r)
        rows.append(
            {
                "estimated_state": estimate_state,
                "self_truth_r": float(self_r),
                "strongest_other_truth_state": STATE_KEYS[strongest_other_index],
                "strongest_other_truth_r": float(strongest_other_r),
                "identification_margin": float(margin),
            }
        )
    return tuple(rows)


def evaluate_observability(
    truth: np.ndarray,
    true_modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
    *,
    particle_count: int = 2000,
    seed: int = 20260908,
    families: Iterable[str] | None = None,
) -> ObservabilityReport:
    """Run practical clue ablations against one known synthetic world. 🔍☕

    This is a synthetic diagnostic for practical identifiability. It is not a formal
    nonlinear observability proof and it definitely is not permission to mind-read. XD
    """

    if particle_count < 100:
        raise ValueError("🐣 Observability needs at least 100 tiny particle friends.")

    selected = tuple(CLUE_FAMILIES if families is None else families)
    unknown = [family for family in selected if family not in CLUE_FAMILIES]
    if unknown:
        raise ValueError(f"🙈 Unknown clue family: {', '.join(unknown)}")

    baseline = _run_filter(
        truth,
        true_modes,
        observations,
        particle_count=particle_count,
        seed=seed,
        label="all-clues",
        removed_family="none",
    )

    ablations: dict[str, ExperimentMetrics] = {}
    for family in selected:
        hidden = ablate_observations(observations, CLUE_FAMILIES[family])
        ablations[family] = _run_filter(
            truth,
            true_modes,
            hidden,
            particle_count=particle_count,
            seed=seed,
            label=f"without-{family}",
            removed_family=family,
        )

    state_identifiability = _state_identifiability_rows(baseline.estimates, np.asarray(truth, dtype=float))
    return ObservabilityReport(
        baseline=baseline,
        ablations=ablations,
        state_identifiability=state_identifiability,
    )
