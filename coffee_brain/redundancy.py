from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

from .diagnostics import STATE_KEYS
from .model import relationship_index
from .observation_model import (
    BINARY_CHANNEL_NAMES,
    DEFAULT_OBSERVATION_MODEL,
    predict_binary_channels,
    predict_delay_log_mean,
    predict_warmth_mean,
)
from .particles import CoffeeParticleFilter


@dataclass(frozen=True)
class RedundancyReport:
    """A synthetic chair test for the six soft states. 🪑🐣"""

    posterior_correlation: np.ndarray
    reconstruction_rows: tuple[dict[str, object], ...]
    variant_rows: tuple[dict[str, object], ...]


def _run_full_filter(
    observations: Sequence[Mapping[str, object]],
    *,
    particle_count: int,
    seed: int,
) -> np.ndarray:
    pf = CoffeeParticleFilter(particle_count=particle_count, seed=seed)
    estimates = [pf.update(dict(obs)).mean for obs in observations]
    return np.asarray(estimates, dtype=float)


def _ridge_fit(x: np.ndarray, y: np.ndarray, alpha: float = 1e-3) -> np.ndarray:
    design = np.column_stack([np.ones(len(x)), x])
    penalty = np.eye(design.shape[1]) * alpha
    penalty[0, 0] = 0.0
    return np.linalg.solve(design.T @ design + penalty, design.T @ y)


def _ridge_predict(x: np.ndarray, beta: np.ndarray) -> np.ndarray:
    return np.column_stack([np.ones(len(x)), x]) @ beta


def _binary_nll(
    states: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
) -> float:
    probabilities = predict_binary_channels(states, modes, DEFAULT_OBSERVATION_MODEL)
    losses: list[float] = []
    invite = np.array([int(obs.get("invite", 0) or 0) for obs in observations], dtype=int)

    for name in BINARY_CHANNEL_NAMES:
        y = np.array([int(obs[name]) for obs in observations], dtype=int)
        p = np.clip(probabilities[name], 1e-6, 1.0 - 1e-6)
        mask = np.ones(len(y), dtype=bool)
        if name in {"opt_in", "pass_event"}:
            mask = invite == 1
        if np.any(mask):
            losses.extend((-y[mask] * np.log(p[mask]) - (1 - y[mask]) * np.log(1 - p[mask])).tolist())
    return float(np.mean(losses))


def _continuous_errors(
    states: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
) -> tuple[float, float]:
    warmth = np.array([float(obs["tone_warmth"]) for obs in observations], dtype=float)
    delay = np.log(np.maximum(0.2, np.array([float(obs["response_delay_min"]) for obs in observations])))
    warmth_hat = predict_warmth_mean(states, modes, DEFAULT_OBSERVATION_MODEL)
    delay_hat = predict_delay_log_mean(states, modes, DEFAULT_OBSERVATION_MODEL)
    warmth_rmse = float(np.sqrt(np.mean((warmth_hat - warmth) ** 2)))
    delay_log_rmse = float(np.sqrt(np.mean((delay_hat - delay) ** 2)))
    return warmth_rmse, delay_log_rmse


def _score_variant(
    name: str,
    latent_dimensions: int,
    states: np.ndarray,
    truth: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    state_rmse = np.sqrt(np.mean((states - truth) ** 2, axis=0))
    r_rmse = float(np.sqrt(np.mean((relationship_index(states) - relationship_index(truth)) ** 2)))
    warmth_rmse, delay_log_rmse = _continuous_errors(states, modes, observations)
    return {
        "variant": name,
        "latent_dimensions": latent_dimensions,
        "mean_state_RMSE": float(np.mean(state_rmse)),
        "max_state_RMSE": float(np.max(state_rmse)),
        "relationship_RMSE": r_rmse,
        "binary_observation_NLL": _binary_nll(states, modes, observations),
        "warmth_RMSE": warmth_rmse,
        "delay_log_RMSE": delay_log_rmse,
    }


def evaluate_state_redundancy(
    truth: np.ndarray,
    true_modes: np.ndarray,
    observations: Sequence[Mapping[str, object]],
    *,
    particle_count: int = 1200,
    seed: int = 20260908,
    train_fraction: float = 0.60,
) -> RedundancyReport:
    """Compare direct six-state estimates with simple five-dimensional projections. 🪑🧭

    Reduced variants here are reconstruction/projection diagnostics, not fully retrained
    lower-dimensional particle filters. They answer whether one state can be removed or
    merged *without much measurable information loss* under the current synthetic model.
    """

    if particle_count < 100:
        raise ValueError("🐣 Redundancy tests need at least 100 tiny particle friends.")
    if not 0.4 <= train_fraction <= 0.8:
        raise ValueError("🐾 train_fraction should stay between 0.4 and 0.8.")

    truth = np.asarray(truth, dtype=float)
    modes = np.asarray(true_modes, dtype=int)
    if len(truth) < 20:
        raise ValueError("🪑🐣 Give the chair test at least 20 synthetic days.")
    if len(truth) != len(modes) or len(truth) != len(observations):
        raise ValueError("🐾 Truth, modes, and observations need the same tiny length.")

    estimates = _run_full_filter(observations, particle_count=particle_count, seed=seed)
    posterior_correlation = np.corrcoef(estimates, rowvar=False)

    split = int(round(len(truth) * train_fraction))
    split = min(max(split, 8), len(truth) - 8)
    train_est, val_est = estimates[:split], estimates[split:]
    train_truth, val_truth = truth[:split], truth[split:]
    val_modes = modes[split:]
    val_obs = observations[split:]

    reconstruction_rows: list[dict[str, object]] = []
    reconstructed: dict[str, np.ndarray] = {}
    for target_index, state in enumerate(STATE_KEYS):
        keep = [i for i in range(6) if i != target_index]
        beta = _ridge_fit(train_est[:, keep], train_truth[:, target_index])
        prediction = np.clip(_ridge_predict(val_est[:, keep], beta), 0.02, 0.98)
        direct_rmse = float(np.sqrt(np.mean((val_est[:, target_index] - val_truth[:, target_index]) ** 2)))
        reconstructed_rmse = float(np.sqrt(np.mean((prediction - val_truth[:, target_index]) ** 2)))
        baseline_mean_rmse = float(
            np.sqrt(np.mean((np.mean(train_truth[:, target_index]) - val_truth[:, target_index]) ** 2))
        )
        reconstruction_rows.append(
            {
                "state": state,
                "direct_RMSE": direct_rmse,
                "reconstructed_RMSE": reconstructed_rmse,
                "reconstruction_penalty": reconstructed_rmse - direct_rmse,
                "mean_only_RMSE": baseline_mean_rmse,
                "reconstruction_gain_vs_mean": baseline_mean_rmse - reconstructed_rmse,
            }
        )
        reconstructed[state] = prediction

    variants: list[dict[str, object]] = []
    variants.append(_score_variant("full-6", 6, val_est, val_truth, val_modes, val_obs))

    merge_ce = val_est.copy()
    shared = 0.5 * (merge_ce[:, 3] + merge_ce[:, 4])
    merge_ce[:, 3] = shared
    merge_ce[:, 4] = shared
    variants.append(_score_variant("merge-C-E", 5, merge_ce, val_truth, val_modes, val_obs))

    for state in ("C", "E", "F"):
        index = STATE_KEYS.index(state)
        reduced = val_est.copy()
        reduced[:, index] = reconstructed[state]
        variants.append(
            _score_variant(
                f"reconstruct-{state}-from-other-5",
                5,
                reduced,
                val_truth,
                val_modes,
                val_obs,
            )
        )

    return RedundancyReport(
        posterior_correlation=posterior_correlation,
        reconstruction_rows=tuple(reconstruction_rows),
        variant_rows=tuple(variants),
    )
