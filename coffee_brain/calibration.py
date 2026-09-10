from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np

from .observation_model import (
    BINARY_CHANNEL_NAMES,
    DEFAULT_OBSERVATION_MODEL,
    ObservationModelConfig,
    predict_binary_channels,
    predict_delay_log_mean,
    predict_warmth_mean,
)


@dataclass(frozen=True)
class BinaryCalibrationSummary:
    """One tiny calibration report card for a Bernoulli clue. 🎛️🐣"""

    channel: str
    n: int
    brier_score: float
    log_loss: float
    mean_predicted: float
    observed_rate: float
    calibration_gap: float
    expected_calibration_error: float


@dataclass(frozen=True)
class ReliabilityBin:
    """One little predicted-probability bucket. 🧺☕"""

    channel: str
    bin_index: int
    lower: float
    upper: float
    n: int
    mean_predicted: float
    observed_rate: float
    gap: float


@dataclass(frozen=True)
class ContinuousCalibrationSummary:
    """Residual diagnostics for one continuous observation channel. 📏☕"""

    channel: str
    n: int
    rmse: float
    mean_residual: float
    residual_std: float
    expected_sigma: float
    normalized_mean: float
    normalized_std: float


@dataclass(frozen=True)
class CalibrationResult:
    binary: tuple[BinaryCalibrationSummary, ...]
    reliability: tuple[ReliabilityBin, ...]
    continuous: tuple[ContinuousCalibrationSummary, ...]

    @property
    def mean_brier(self) -> float:
        values = [row.brier_score for row in self.binary]
        return float(np.mean(values)) if values else float("nan")

    @property
    def mean_ece(self) -> float:
        values = [row.expected_calibration_error for row in self.binary]
        return float(np.mean(values)) if values else float("nan")


def _finite_binary_pairs(predicted: np.ndarray, observed: Sequence[object]) -> tuple[np.ndarray, np.ndarray]:
    p = np.asarray(predicted, dtype=float).reshape(-1)
    raw = np.asarray(observed, dtype=object).reshape(-1)
    if len(p) != len(raw):
        raise ValueError("🐾 Predicted and observed clue baskets must be the same length.")

    mask = np.array([value is not None for value in raw], dtype=bool) & np.isfinite(p)
    y = np.array([float(value) for value in raw[mask]], dtype=float)
    p = p[mask]
    if np.any((y < 0.0) | (y > 1.0)):
        raise ValueError("🐾 Binary clues must stay between 0 and 1.")
    return p, y


def _optional_float_array(values: Sequence[object]) -> np.ndarray:
    """Turn missing continuous clues into NaN so residual diagnostics can ignore them. 🌱📏"""

    return np.array(
        [np.nan if value is None else float(value) for value in values],
        dtype=float,
    )


def calibrate_binary_channel(
    channel: str,
    predicted: np.ndarray,
    observed: Sequence[object],
    *,
    bins: int = 10,
) -> tuple[BinaryCalibrationSummary, tuple[ReliabilityBin, ...]]:
    """Measure whether tiny predicted probabilities keep their promises. ☕🎛️

    Four complementary views are kept instead of collapsing calibration into one score:

        Brier   = mean((p - y)^2)
        LogLoss = -mean(y log p + (1-y) log(1-p))
        Gap     = mean(y) - mean(p)
        ECE     = sum_b (n_b / n) * |observed_rate_b - mean_predicted_b|

    Brier/log-loss score individual probabilistic predictions; gap/ECE ask whether
    stated probabilities line up with empirical frequencies in the synthetic bench.
    """

    if bins < 2:
        raise ValueError("🐣 Reliability needs at least two tiny bins.")

    p, y = _finite_binary_pairs(predicted, observed)
    if len(p) == 0:
        empty = BinaryCalibrationSummary(channel, 0, *(float("nan"),) * 6)
        return empty, ()

    # Probability clipping is only for log-loss numerical safety. Brier and reported
    # mean probabilities use the original model predictions.
    clipped = np.clip(p, 1e-9, 1.0 - 1e-9)
    brier = float(np.mean((p - y) ** 2))
    log_loss = float(-np.mean(y * np.log(clipped) + (1.0 - y) * np.log(1.0 - clipped)))
    mean_pred = float(np.mean(p))
    observed_rate = float(np.mean(y))

    # Reliability diagram bins partition predicted probability into equal-width
    # intervals. ECE below weights each absolute bin gap by the number of samples in it.
    edges = np.linspace(0.0, 1.0, bins + 1)
    bin_ids = np.minimum((p * bins).astype(int), bins - 1)
    reliability: list[ReliabilityBin] = []
    weighted_gap = 0.0

    for index in range(bins):
        mask = bin_ids == index
        if not np.any(mask):
            continue
        bp = float(np.mean(p[mask]))
        by = float(np.mean(y[mask]))
        gap = by - bp
        count = int(np.sum(mask))
        weighted_gap += count * abs(gap)
        reliability.append(
            ReliabilityBin(
                channel=channel,
                bin_index=index,
                lower=float(edges[index]),
                upper=float(edges[index + 1]),
                n=count,
                mean_predicted=bp,
                observed_rate=by,
                gap=float(gap),
            )
        )

    summary = BinaryCalibrationSummary(
        channel=channel,
        n=len(p),
        brier_score=brier,
        log_loss=log_loss,
        mean_predicted=mean_pred,
        observed_rate=observed_rate,
        calibration_gap=observed_rate - mean_pred,
        expected_calibration_error=float(weighted_gap / len(p)),
    )
    return summary, tuple(reliability)


def _continuous_summary(
    channel: str,
    observed: np.ndarray,
    expected: np.ndarray,
    sigma: float,
) -> ContinuousCalibrationSummary:
    """Summarize residual scale in native and model-noise units.

    residual = observed - expected
    normalized_residual = residual / sigma

    If the conditional mean and shared sigma are well matched in the synthetic bench,
    normalized residuals should be centered near zero with standard deviation near one.
    This is a diagnostic expectation, not a guarantee for real-human data.
    """

    obs = np.asarray(observed, dtype=float).reshape(-1)
    exp = np.asarray(expected, dtype=float).reshape(-1)
    if len(obs) != len(exp):
        raise ValueError("🐾 Continuous observation and expectation baskets must match.")

    mask = np.isfinite(obs) & np.isfinite(exp)
    residual = obs[mask] - exp[mask]
    if len(residual) == 0:
        return ContinuousCalibrationSummary(channel, 0, *(float("nan"),) * 6)

    normalized = residual / float(sigma)
    return ContinuousCalibrationSummary(
        channel=channel,
        n=len(residual),
        rmse=float(np.sqrt(np.mean(residual**2))),
        mean_residual=float(np.mean(residual)),
        residual_std=float(np.std(residual)),
        expected_sigma=float(sigma),
        normalized_mean=float(np.mean(normalized)),
        normalized_std=float(np.std(normalized)),
    )


def calibrate_dataset(
    states: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[dict],
    *,
    config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL,
    bins: int = 10,
) -> CalibrationResult:
    """Run a synthetic calibration bench without pretending hidden truth is observable in real life. 🐣🧠

    The hidden states/modes supplied here come from a synthetic world where ground truth
    is available by construction. This function therefore evaluates the observation
    recipes; it does not imply that latent CSRDM states are directly measurable in people.
    """

    tiny_states = np.asarray(states, dtype=float)
    tiny_modes = np.asarray(modes, dtype=int)
    if len(tiny_states) != len(tiny_modes) or len(tiny_states) != len(observations):
        raise ValueError("🐾 States, modes, and observations need matching tiny timelines.")

    probabilities = predict_binary_channels(tiny_states, tiny_modes, config)
    binary_rows: list[BinaryCalibrationSummary] = []
    reliability_rows: list[ReliabilityBin] = []

    invites = np.array([obs.get("invite") for obs in observations], dtype=object)

    for channel in BINARY_CHANNEL_NAMES:
        observed = np.array([obs.get(channel) for obs in observations], dtype=object)

        # opt-in and pass are only meaningful when an invitation opened that little door. 🚪☕
        # A row without an observed invitation is removed from that channel's calibration
        # rather than counted as a negative outcome.
        if channel in {"opt_in", "pass_event"}:
            observed = observed.copy()
            for i, invite in enumerate(invites):
                if invite is None or int(invite) != 1:
                    observed[i] = None

        summary, bins_rows = calibrate_binary_channel(
            channel,
            probabilities[channel],
            observed,
            bins=bins,
        )
        binary_rows.append(summary)
        reliability_rows.extend(bins_rows)

    # Warmth residuals live in the channel's native linear scale.
    warmth_obs = _optional_float_array([obs.get("tone_warmth") for obs in observations])
    warmth_expected = predict_warmth_mean(tiny_states, tiny_modes, config)
    warmth = _continuous_summary(
        "tone_warmth",
        warmth_obs,
        warmth_expected,
        config.tone_warmth.sigma,
    )

    # Delay is modeled as log-normal, so calibration compares log(delay) with the
    # predicted log mean and uses sigma_log as its expected residual scale.
    delay_minutes = _optional_float_array([obs.get("response_delay_min") for obs in observations])
    delay_obs = np.full_like(delay_minutes, np.nan, dtype=float)
    finite_delay = np.isfinite(delay_minutes)
    delay_obs[finite_delay] = np.log(np.maximum(0.2, delay_minutes[finite_delay]))
    delay_expected = predict_delay_log_mean(tiny_states, tiny_modes, config)
    delay = _continuous_summary(
        "log_response_delay",
        delay_obs,
        delay_expected,
        config.response_delay.sigma_log,
    )

    return CalibrationResult(
        binary=tuple(binary_rows),
        reliability=tuple(reliability_rows),
        continuous=(warmth, delay),
    )
