from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .model import MODE_NAMES, RoutineMode
from .particles import ParticleHistoryStep


@dataclass(frozen=True)
class SmoothedPosterior:
    """One tiny hindsight posterior. Later clues may help, observed facts do not change. 🔭🐣"""

    mean: np.ndarray
    ci95_low: np.ndarray
    ci95_high: np.ndarray
    mode_probabilities: np.ndarray
    endpoint: int

    @property
    def mode(self) -> str:
        return MODE_NAMES[RoutineMode(int(np.argmax(self.mode_probabilities)))]


def _normalized_weights(weights: np.ndarray) -> np.ndarray:
    w = np.asarray(weights, dtype=float)
    total = float(np.sum(w))
    if not np.isfinite(total) or total <= 0.0:
        raise ValueError("🐣 Tiny smoother received a weight cloud with no usable gravity.")
    return w / total


def _weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    order = np.argsort(values)
    ordered_values = np.asarray(values, dtype=float)[order]
    ordered_weights = _normalized_weights(np.asarray(weights, dtype=float)[order])
    cdf = np.cumsum(ordered_weights)
    index = min(int(np.searchsorted(cdf, q, side="left")), len(ordered_values) - 1)
    return float(ordered_values[index])


def _trace_ancestors(
    history: Sequence[ParticleHistoryStep],
    start: int,
    endpoint: int,
) -> np.ndarray:
    """Trace endpoint particles backward to one earlier filtered support. 🐾🔭"""

    particle_count = len(history[endpoint].weights)
    indices = np.arange(particle_count, dtype=np.int32)
    for step_index in range(endpoint, start, -1):
        parents = history[step_index].parents
        if parents is None:
            raise ValueError("🙈 Tiny smoother found a missing ancestry bridge.")
        indices = parents[indices]
    return indices


def smooth_history(
    history: Sequence[ParticleHistoryStep],
    *,
    lag: int = 30,
    full_history: bool = False,
) -> list[SmoothedPosterior]:
    """Run a genealogical fixed-lag particle smoother over recorded PF history. 🔭☕

    For each day ``t``, descendants are followed up to ``t + lag`` and their later
    filtered weights are projected backward through the recorded ancestry. This is a
    practical SMC smoother, not a magic time machine; very long horizons can suffer
    particle path degeneracy, which is why fixed-lag smoothing is the default. 🐣
    """

    if lag < 0:
        raise ValueError("🔭 Tiny smoothing lag cannot be negative.")
    if not history:
        return []

    particle_count = len(history[0].weights)
    if particle_count == 0:
        raise ValueError("🐣 Tiny smoother needs at least one particle friend.")
    for step in history:
        if len(step.weights) != particle_count or len(step.particles) != particle_count:
            raise ValueError("🧺 Every recorded particle cloud must keep the same tiny flock size.")

    total_steps = len(history)
    result: list[SmoothedPosterior] = []

    for start in range(total_steps):
        endpoint = total_steps - 1 if full_history else min(total_steps - 1, start + lag)
        descendant_weights = _normalized_weights(history[endpoint].weights)
        ancestors = _trace_ancestors(history, start, endpoint)

        states = np.asarray(history[start].particles[ancestors], dtype=float)
        modes = np.asarray(history[start].modes[ancestors], dtype=int)
        mean = np.sum(descendant_weights[:, None] * states, axis=0)

        low = np.zeros(states.shape[1], dtype=float)
        high = np.zeros(states.shape[1], dtype=float)
        for state_index in range(states.shape[1]):
            low[state_index] = _weighted_quantile(states[:, state_index], descendant_weights, 0.025)
            high[state_index] = _weighted_quantile(states[:, state_index], descendant_weights, 0.975)

        mode_probabilities = np.array(
            [np.sum(descendant_weights[modes == mode]) for mode in range(5)],
            dtype=float,
        )

        result.append(
            SmoothedPosterior(
                mean=mean,
                ci95_low=low,
                ci95_high=high,
                mode_probabilities=mode_probabilities,
                endpoint=endpoint,
            )
        )

    return result
