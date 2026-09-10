from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping, Sequence

import numpy as np

from .diagnostics import CLUE_FAMILIES, STATE_KEYS, ablate_observations
from .memory import DEFAULT_SHARED_CONTEXT_MEMORY
from .model import MODE_NAMES, RoutineMode
from .observation_model import DEFAULT_OBSERVATION_MODEL
from .particles import CoffeeParticleFilter


@dataclass(frozen=True)
class SensitivityMetrics:
    label: str
    category: str
    rmse: np.ndarray
    correlation: np.ndarray
    ci95_width: np.ndarray
    ci95_coverage: np.ndarray
    mode_accuracy: float


@dataclass(frozen=True)
class SensitivityReport:
    """One reproducible map of which assumptions make which tiny states wobble. 🧪🗺️"""

    baseline: SensitivityMetrics
    variants: tuple[SensitivityMetrics, ...]

    def rows(self) -> list[dict[str, object]]:
        rows: list[dict[str, object]] = []
        base = self.baseline
        for variant in self.variants:
            for i, state in enumerate(STATE_KEYS):
                denom = max(float(base.rmse[i]), 1e-9)
                rows.append(
                    {
                        "variant": variant.label,
                        "category": variant.category,
                        "state": state,
                        "RMSE": float(variant.rmse[i]),
                        "RMSE_delta": float(variant.rmse[i] - base.rmse[i]),
                        "RMSE_relative_change": float((variant.rmse[i] - base.rmse[i]) / denom),
                        "Pearson_r": float(variant.correlation[i]),
                        "correlation_delta": float(variant.correlation[i] - base.correlation[i]),
                        "CI95_mean_width": float(variant.ci95_width[i]),
                        "CI95_width_delta": float(variant.ci95_width[i] - base.ci95_width[i]),
                        "CI95_coverage": float(variant.ci95_coverage[i]),
                        "coverage_delta": float(variant.ci95_coverage[i] - base.ci95_coverage[i]),
                        "mode_accuracy": float(variant.mode_accuracy),
                        "mode_accuracy_delta": float(variant.mode_accuracy - base.mode_accuracy),
                    }
                )
        return rows

    def matrix(self) -> tuple[tuple[str, ...], np.ndarray]:
        """Return signed relative-RMSE sensitivity: rows=variants, cols=states. 🐣📏

        Entry (v,j) is:

            (RMSE_variant[v,j] - RMSE_baseline[j]) / RMSE_baseline[j]

        Positive values mean the perturbation worsened point-estimate error for that
        state; negative values mean lower RMSE under that variant. It is a local
        robustness diagnostic, not an importance or causal-effect score.
        """

        labels = tuple(variant.label for variant in self.variants)
        base = np.maximum(self.baseline.rmse, 1e-9)
        matrix = np.vstack([(variant.rmse - self.baseline.rmse) / base for variant in self.variants])
        return labels, matrix


def _safe_r(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 2 or np.std(a) == 0.0 or np.std(b) == 0.0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def _run(
    truth: np.ndarray,
    true_modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
    *,
    particle_count: int,
    seed: int,
    label: str,
    category: str,
    filter_kwargs: dict[str, object] | None = None,
) -> SensitivityMetrics:
    pf = CoffeeParticleFilter(
        particle_count=particle_count,
        seed=seed,
        **(filter_kwargs or {}),
    )
    estimates: list[np.ndarray] = []
    lows: list[np.ndarray] = []
    highs: list[np.ndarray] = []
    modes: list[str] = []

    for obs in observations:
        posterior = pf.update(dict(obs))
        estimates.append(posterior.mean)
        lows.append(posterior.ci95_low)
        highs.append(posterior.ci95_high)
        modes.append(posterior.mode)

    est = np.asarray(estimates, dtype=float)
    low = np.asarray(lows, dtype=float)
    high = np.asarray(highs, dtype=float)
    truth = np.asarray(truth, dtype=float)
    true_modes = np.asarray(true_modes, dtype=int)

    # Use the same diagnostic family as observability tests so sensitivity variants
    # remain directly comparable with the baseline run.
    rmse = np.sqrt(np.mean((est - truth) ** 2, axis=0))
    correlation = np.array([_safe_r(est[:, i], truth[:, i]) for i in range(6)], dtype=float)
    width = np.mean(high - low, axis=0)
    coverage = np.mean((truth >= low) & (truth <= high), axis=0)
    mode_accuracy = float(
        np.mean(
            [
                modes[t] == MODE_NAMES[RoutineMode(int(true_modes[t]))]
                for t in range(len(true_modes))
            ]
        )
    )
    return SensitivityMetrics(label, category, rmse, correlation, width, coverage, mode_accuracy)


def transition_temperature(matrix: np.ndarray, temperature: float) -> np.ndarray:
    """Warm or cool a transition table without changing its support. 🌡️🎲

    Temperature rescales row log-probabilities before softmax:

        p'_j ∝ exp(log(p_j) / T) = p_j^(1/T)

    ``T < 1`` sharpens each row toward its larger probabilities; ``T > 1`` flattens
    the row toward a more diffuse transition distribution. No entry is introduced or
    removed because the original positive support is preserved.
    """

    if temperature <= 0.0:
        raise ValueError("🐾 Transition temperature must be positive.")
    base = np.asarray(matrix, dtype=float)
    logits = np.log(np.clip(base, 1e-12, 1.0)) / float(temperature)
    logits -= np.max(logits, axis=1, keepdims=True)
    warmed = np.exp(logits)
    return warmed / warmed.sum(axis=1, keepdims=True)


def evaluate_sensitivity(
    truth: np.ndarray,
    true_modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
    *,
    particle_count: int = 1200,
    seed: int = 20260908,
) -> SensitivityReport:
    """Poke clue channels and estimator assumptions one at a time. 🧪🐾

    Every variant changes one clue family or one small estimator assumption while
    reusing the same synthetic timeline and random seed. Differences from baseline
    therefore expose local robustness to that perturbation while reducing Monte Carlo
    noise between runs.

    This is local synthetic sensitivity, not causal attribution and definitely not a
    ranking of human importance. Every variant reuses the same synthetic timeline.
    """

    if particle_count < 100:
        raise ValueError("🐣 Sensitivity needs at least 100 tiny particle friends.")

    baseline = _run(
        truth,
        true_modes,
        observations,
        particle_count=particle_count,
        seed=seed,
        label="baseline",
        category="baseline",
    )

    variants: list[SensitivityMetrics] = []

    # Observation ablations ask how much each clue family contributes under the fixed
    # synthetic world; they do not alter the hidden trajectory itself.
    for family, keys in CLUE_FAMILIES.items():
        variants.append(
            _run(
                truth,
                true_modes,
                ablate_observations(observations, keys),
                particle_count=particle_count,
                seed=seed,
                label=f"hide-{family}",
                category="clue-ablation",
            )
        )

    # Observation-model variants perturb one hand-set likelihood assumption at a time.
    obs = DEFAULT_OBSERVATION_MODEL
    observation_variants = {
        "warmth-sigma-0.75x": replace(obs, tone_warmth=replace(obs.tone_warmth, sigma=obs.tone_warmth.sigma * 0.75)),
        "warmth-sigma-1.25x": replace(obs, tone_warmth=replace(obs.tone_warmth, sigma=obs.tone_warmth.sigma * 1.25)),
        "warmth-intercept-plus-0.05": replace(obs, tone_warmth=replace(obs.tone_warmth, intercept=obs.tone_warmth.intercept + 0.05)),
        "delay-sigma-0.75x": replace(obs, response_delay=replace(obs.response_delay, sigma_log=obs.response_delay.sigma_log * 0.75)),
        "delay-sigma-1.25x": replace(obs, response_delay=replace(obs.response_delay, sigma_log=obs.response_delay.sigma_log * 1.25)),
        "delay-base-1.25x": replace(obs, response_delay=replace(obs.response_delay, base_minutes=obs.response_delay.base_minutes * 1.25)),
    }
    for label, config in observation_variants.items():
        variants.append(
            _run(
                truth,
                true_modes,
                observations,
                particle_count=particle_count,
                seed=seed,
                label=label,
                category="observation-assumption",
                filter_kwargs={"observation_config": config},
            )
        )

    # Memory perturbations test how inference reacts to a faster/slower C decay law.
    memory = DEFAULT_SHARED_CONTEXT_MEMORY
    for label, factor in (("memory-decay-0.5x", 0.5), ("memory-decay-2x", 2.0)):
        config = replace(memory, decay_rate=memory.decay_rate * factor)
        variants.append(
            _run(
                truth,
                true_modes,
                observations,
                particle_count=particle_count,
                seed=seed,
                label=label,
                category="memory-assumption",
                filter_kwargs={"memory_config": config},
            )
        )

    # Process-noise perturbations test confidence in the continuous state dynamics.
    for label, scale in (("process-noise-0.75x", 0.75), ("process-noise-1.25x", 1.25)):
        variants.append(
            _run(
                truth,
                true_modes,
                observations,
                particle_count=particle_count,
                seed=seed,
                label=label,
                category="dynamics-assumption",
                filter_kwargs={"process_noise_scale": scale},
            )
        )

    # Transition-temperature variants change only how concentrated the fixed Markov
    # rows are, while preserving their ordering/support.
    for label, temperature in (("transition-temp-0.85", 0.85), ("transition-temp-1.15", 1.15)):
        variants.append(
            _run(
                truth,
                true_modes,
                observations,
                particle_count=particle_count,
                seed=seed,
                label=label,
                category="transition-assumption",
                filter_kwargs={"fixed_transition": transition_temperature(CoffeeParticleFilter.transition, temperature)},
            )
        )

    return SensitivityReport(baseline=baseline, variants=tuple(variants))
