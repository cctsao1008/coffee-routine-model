from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Iterable, Sequence

import numpy as np

from .calibration import CalibrationResult, calibrate_dataset
from .observation_model import (
    BINARY_CHANNEL_NAMES,
    DEFAULT_OBSERVATION_MODEL,
    ObservationModelConfig,
    predict_delay_log_mean,
    predict_warmth_mean,
)


@dataclass(frozen=True)
class ParameterEstimate:
    """One learned knob with a small approximate uncertainty ribbon. 🎚️🐣"""

    name: str
    before: float
    after: float
    standard_error: float
    ci95_low: float
    ci95_high: float
    lower_bound: float
    upper_bound: float


@dataclass(frozen=True)
class LearningExperiment:
    """A train/validation learning report that keeps every spoonful inspectable. 🥄☕"""

    split_index: int
    learned_config: ObservationModelConfig
    parameters: tuple[ParameterEstimate, ...]
    train_before: CalibrationResult
    train_after: CalibrationResult
    validation_before: CalibrationResult
    validation_after: CalibrationResult


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-np.clip(x, -40.0, 40.0)))


def _channel_training_pairs(
    states: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[dict],
    channel: str,
    config: ObservationModelConfig,
) -> tuple[np.ndarray, np.ndarray]:
    recipe = getattr(config, channel)
    offset = recipe.logits(states, modes) - float(recipe.intercept)
    y = np.array([obs.get(channel) for obs in observations], dtype=object)
    mask = np.array([value is not None for value in y], dtype=bool)

    if channel in {"opt_in", "pass_event"}:
        invites = np.array([obs.get("invite") for obs in observations], dtype=object)
        mask &= np.array([value is not None and int(value) == 1 for value in invites], dtype=bool)

    return np.asarray(offset[mask], dtype=float), np.asarray(y[mask], dtype=float)


def _bounded_newton_intercept(
    offset: np.ndarray,
    y: np.ndarray,
    initial: float,
    *,
    lower: float = -6.0,
    upper: float = 6.0,
    iterations: int = 30,
) -> tuple[float, float]:
    """Fit one logistic intercept while every structural slope stays frozen. 🐣🎚️"""

    if len(y) == 0:
        return float(initial), float("nan")

    value = float(np.clip(initial, lower, upper))
    for _ in range(iterations):
        p = _sigmoid(offset + value)
        gradient = float(np.sum(p - y))
        hessian = float(np.sum(p * (1.0 - p))) + 1e-9
        candidate = float(np.clip(value - gradient / hessian, lower, upper))
        if abs(candidate - value) < 1e-9:
            value = candidate
            break
        value = candidate

    p = _sigmoid(offset + value)
    information = float(np.sum(p * (1.0 - p)))
    standard_error = float(1.0 / np.sqrt(max(information, 1e-12)))
    return value, standard_error


def _bounded_sigma(
    residual: np.ndarray,
    *,
    lower: float,
    upper: float,
) -> tuple[float, float]:
    """Use residual RMS as the Gaussian/log-normal sigma MLE, then keep it sane. 📏🐾"""

    residual = np.asarray(residual, dtype=float)
    residual = residual[np.isfinite(residual)]
    if len(residual) == 0:
        return float("nan"), float("nan")
    sigma = float(np.clip(np.sqrt(np.mean(residual**2)), lower, upper))
    standard_error = float(sigma / np.sqrt(max(2 * len(residual), 1)))
    return sigma, standard_error


def fit_observation_parameters(
    states: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[dict],
    *,
    baseline_config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL,
    binary_channels: Iterable[str] = BINARY_CHANNEL_NAMES,
    learn_warmth_sigma: bool = True,
    learn_delay_sigma: bool = True,
    provenance: str = "learned from synthetic hidden-state training data; not real-human truth",
) -> tuple[ObservationModelConfig, tuple[ParameterEstimate, ...]]:
    """Learn a deliberately tiny parameter subset without opening the whole buffet. 🎚️🥄

    Only selected Bernoulli intercepts and optional continuous sigmas are learned.
    State slopes, mode offsets, transitions, process noise, memory constants, and all
    structural semantics stay frozen.
    """

    states = np.asarray(states, dtype=float)
    modes = np.asarray(modes, dtype=int)
    if len(states) != len(modes) or len(states) != len(observations):
        raise ValueError("🐾 Learning states, modes, and clue baskets must have matching lengths.")
    if len(states) < 20:
        raise ValueError("🎚️🐣 Give the learning spoon at least 20 synthetic days.")

    selected = tuple(binary_channels)
    unknown = [name for name in selected if name not in BINARY_CHANNEL_NAMES]
    if unknown:
        raise ValueError(f"🙈 Unknown learnable binary channel: {', '.join(unknown)}")

    learned = baseline_config
    estimates: list[ParameterEstimate] = []

    for name in selected:
        recipe = getattr(baseline_config, name)
        offset, y = _channel_training_pairs(states, modes, observations, name, baseline_config)
        after, se = _bounded_newton_intercept(offset, y, float(recipe.intercept))
        learned = learned.with_binary_channel(name, intercept=after)
        estimates.append(
            ParameterEstimate(
                name=f"{name}.intercept",
                before=float(recipe.intercept),
                after=after,
                standard_error=se,
                ci95_low=float(max(-6.0, after - 1.96 * se)) if np.isfinite(se) else float("nan"),
                ci95_high=float(min(6.0, after + 1.96 * se)) if np.isfinite(se) else float("nan"),
                lower_bound=-6.0,
                upper_bound=6.0,
            )
        )

    if learn_warmth_sigma:
        observed = np.array([float(obs["tone_warmth"]) for obs in observations], dtype=float)
        expected = predict_warmth_mean(states, modes, baseline_config)
        sigma, se = _bounded_sigma(observed - expected, lower=0.02, upper=0.50)
        before = float(baseline_config.tone_warmth.sigma)
        learned = replace(learned, tone_warmth=replace(learned.tone_warmth, sigma=sigma))
        estimates.append(
            ParameterEstimate(
                name="tone_warmth.sigma",
                before=before,
                after=sigma,
                standard_error=se,
                ci95_low=float(max(0.02, sigma - 1.96 * se)),
                ci95_high=float(min(0.50, sigma + 1.96 * se)),
                lower_bound=0.02,
                upper_bound=0.50,
            )
        )

    if learn_delay_sigma:
        observed = np.log(
            np.maximum(0.2, np.array([float(obs["response_delay_min"]) for obs in observations], dtype=float))
        )
        expected = predict_delay_log_mean(states, modes, baseline_config)
        sigma, se = _bounded_sigma(observed - expected, lower=0.10, upper=1.50)
        before = float(baseline_config.response_delay.sigma_log)
        learned = replace(learned, response_delay=replace(learned.response_delay, sigma_log=sigma))
        estimates.append(
            ParameterEstimate(
                name="response_delay.sigma_log",
                before=before,
                after=sigma,
                standard_error=se,
                ci95_low=float(max(0.10, sigma - 1.96 * se)),
                ci95_high=float(min(1.50, sigma + 1.96 * se)),
                lower_bound=0.10,
                upper_bound=1.50,
            )
        )

    learned = replace(learned, provenance=provenance)
    return learned, tuple(estimates)


def run_learning_experiment(
    states: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[dict],
    *,
    train_fraction: float = 0.60,
    bins: int = 8,
    baseline_config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL,
    binary_channels: Iterable[str] = BINARY_CHANNEL_NAMES,
) -> LearningExperiment:
    """Train on the first synthetic segment and judge the learned knobs on held-out days. 🐣📚"""

    states = np.asarray(states, dtype=float)
    modes = np.asarray(modes, dtype=int)
    if not 0.40 <= train_fraction <= 0.80:
        raise ValueError("🐾 train_fraction should stay between 0.40 and 0.80.")
    if len(states) < 40:
        raise ValueError("🎚️🐣 Learning experiments need at least 40 synthetic days.")

    split = int(round(len(states) * train_fraction))
    split = min(max(split, 20), len(states) - 20)
    train_obs = list(observations[:split])
    val_obs = list(observations[split:])

    learned, parameters = fit_observation_parameters(
        states[:split],
        modes[:split],
        train_obs,
        baseline_config=baseline_config,
        binary_channels=binary_channels,
        provenance=(
            f"synthetic bounded-Newton intercept learning + residual-sigma fitting; "
            f"train_days={split}; hidden truth used only in synthetic bench"
        ),
    )

    return LearningExperiment(
        split_index=split,
        learned_config=learned,
        parameters=parameters,
        train_before=calibrate_dataset(states[:split], modes[:split], train_obs, config=baseline_config, bins=bins),
        train_after=calibrate_dataset(states[:split], modes[:split], train_obs, config=learned, bins=bins),
        validation_before=calibrate_dataset(states[split:], modes[split:], val_obs, config=baseline_config, bins=bins),
        validation_after=calibrate_dataset(states[split:], modes[split:], val_obs, config=learned, bins=bins),
    )


def calibration_metrics(result: CalibrationResult) -> dict[str, float]:
    """Flatten the most useful calibration checks without inventing one winner score. 🧺📏"""

    binary_log_loss = float(np.mean([row.log_loss for row in result.binary]))
    warmth = next(row for row in result.continuous if row.channel == "tone_warmth")
    delay = next(row for row in result.continuous if row.channel == "log_response_delay")
    return {
        "mean_binary_brier": result.mean_brier,
        "mean_binary_log_loss": binary_log_loss,
        "mean_binary_ECE": result.mean_ece,
        "warmth_RMSE": warmth.rmse,
        "warmth_normalized_std": warmth.normalized_std,
        "delay_log_RMSE": delay.rmse,
        "delay_normalized_std": delay.normalized_std,
    }
