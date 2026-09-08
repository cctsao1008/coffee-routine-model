from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np


FEATURE_NAMES = (
    "invite",
    "opt_in",
    "text_reply",
    "reaction",
    "state_share",
    "proactive_update",
    "routine_maintenance",
    "pass_event",
    "resume_signal",
    "tone_warmth",
    "log_response_delay",
)


@dataclass(frozen=True)
class BoundaryEvidence:
    """Evidence attached to one candidate boundary between two tiny regimes. ✂️🐣"""

    boundary_index: int
    boundary_day: int
    score: float
    posterior_probability: float
    conditional_probability: float


@dataclass(frozen=True)
class ChangePointResult:
    """One inspectable offline single-change-point report. ☕✂️"""

    detected: bool
    sample_count: int
    feature_count: int
    min_segment: int
    change_probability: float
    no_change_probability: float
    best_boundary_index: int
    best_boundary_day: int
    best_posterior_probability: float
    best_conditional_probability: float
    conditional_ci90_start_day: int
    conditional_ci90_end_day: int
    evidence: tuple[BoundaryEvidence, ...]


def observations_to_matrix(observations: Sequence[dict]) -> np.ndarray:
    """Turn observable coffee clues into a numeric change-point basket. 🧺👀

    Missing clues remain missing until the detector standardizes the full timeline.
    Reply delay is transformed into log-minutes so one very sleepy reply does not
    dominate the whole little garden. XD
    """

    rows: list[list[float]] = []
    for obs in observations:
        delay = obs.get("response_delay_min")
        rows.append(
            [
                _maybe_float(obs.get("invite")),
                _maybe_float(obs.get("opt_in")),
                _maybe_float(obs.get("text_reply")),
                _maybe_float(obs.get("reaction")),
                _maybe_float(obs.get("state_share")),
                _maybe_float(obs.get("proactive_update")),
                _maybe_float(obs.get("routine_maintenance")),
                _maybe_float(obs.get("pass_event")),
                _maybe_float(obs.get("resume_signal")),
                _maybe_float(obs.get("tone_warmth")),
                float("nan") if delay is None else math.log(max(0.2, float(delay))),
            ]
        )
    return np.asarray(rows, dtype=float)


def _maybe_float(value) -> float:
    return float("nan") if value is None else float(value)


def _prepare_features(matrix: np.ndarray) -> np.ndarray:
    tiny = np.asarray(matrix, dtype=float).copy()
    if tiny.ndim != 2 or tiny.shape[0] < 2 or tiny.shape[1] < 1:
        raise ValueError("🐾 Change-point features need shape (days, clues).")

    means = np.nanmean(tiny, axis=0)
    if np.any(~np.isfinite(means)):
        raise ValueError("🙈 At least one tiny clue column is missing for the whole timeline.")

    missing = np.where(~np.isfinite(tiny))
    tiny[missing] = means[missing[1]]

    raw_scale = np.std(tiny, axis=0)
    active = raw_scale > 1e-9
    if not np.any(active):
        raise ValueError("🐣 Every clue stayed perfectly constant; there is nothing to cut.")

    tiny = tiny[:, active]
    scale = np.std(tiny, axis=0)
    return (tiny - np.mean(tiny, axis=0)) / np.maximum(scale, 1e-6)


def _segment_sse(prefix: np.ndarray, prefix_sq: np.ndarray, start: int, stop: int) -> float:
    count = stop - start
    total = prefix[stop] - prefix[start]
    total_sq = prefix_sq[stop] - prefix_sq[start]
    return float(np.sum(total_sq - total * total / count))


def detect_feature_change_point(
    matrix: np.ndarray,
    *,
    min_segment: int = 30,
    change_prior: float = 0.35,
    penalty_scale: float = 1.0,
    detection_threshold: float = 0.80,
) -> ChangePointResult:
    """Detect one persistent mean-regime change with an inspectable penalized split. ✂️☕

    The score is a BIC-like approximation to the log evidence gained by allowing
    different feature means before and after a candidate boundary. Candidate weights
    are combined with an explicit prior over ``no change`` vs ``one change``.

    This is intentionally conservative: one strange day should usually lose against
    the model-complexity penalty, while a persistent shift may earn a boundary.
    """

    if min_segment < 2:
        raise ValueError("🐾 min_segment must leave at least two tiny days on each side.")
    if not 0.0 < change_prior < 1.0:
        raise ValueError("🐾 change_prior must live strictly between 0 and 1.")
    if penalty_scale < 0.0:
        raise ValueError("🐾 penalty_scale cannot be negative.")
    if not 0.0 < detection_threshold < 1.0:
        raise ValueError("🐾 detection_threshold must live strictly between 0 and 1.")

    z = _prepare_features(matrix)
    n, d = z.shape
    if n < 2 * min_segment:
        raise ValueError(
            f"🐾 {n} tiny days cannot fit two segments of {min_segment}. Give the scissors more room."
        )

    prefix = np.vstack([np.zeros(d), np.cumsum(z, axis=0)])
    prefix_sq = np.vstack([np.zeros(d), np.cumsum(z * z, axis=0)])
    base_sse = _segment_sse(prefix, prefix_sq, 0, n)

    boundaries = np.arange(min_segment, n - min_segment + 1, dtype=int)
    penalty = float(penalty_scale * d * math.log(n))
    scores = np.empty(len(boundaries), dtype=float)

    for i, boundary in enumerate(boundaries):
        split_sse = _segment_sse(prefix, prefix_sq, 0, boundary) + _segment_sse(
            prefix, prefix_sq, boundary, n
        )
        improvement = base_sse - split_sse
        scores[i] = 0.5 * (improvement - penalty)

    # Prior mass for "one change" is shared across all candidate boundaries. This
    # naturally discourages boundary fishing across a very long timeline. 🎣✂️
    log_no_change = math.log(1.0 - change_prior)
    log_boundary_prior = math.log(change_prior) - math.log(len(boundaries))
    log_weights = np.concatenate([[log_no_change], log_boundary_prior + scores])
    log_weights -= np.max(log_weights)
    posterior = np.exp(log_weights)
    posterior /= np.sum(posterior)

    no_change_probability = float(posterior[0])
    boundary_probabilities = posterior[1:]
    change_probability = float(1.0 - no_change_probability)

    if change_probability > 0.0:
        conditional = boundary_probabilities / change_probability
    else:  # pragma: no cover - floating-point guard for an impossible exact zero
        conditional = np.ones_like(boundary_probabilities) / len(boundary_probabilities)

    best_i = int(np.argmax(conditional))
    best_boundary = int(boundaries[best_i])

    cdf = np.cumsum(conditional)
    low_i = int(np.searchsorted(cdf, 0.05, side="left"))
    high_i = int(np.searchsorted(cdf, 0.95, side="left"))
    low_i = min(low_i, len(boundaries) - 1)
    high_i = min(high_i, len(boundaries) - 1)

    evidence = tuple(
        BoundaryEvidence(
            boundary_index=int(boundary),
            boundary_day=int(boundary + 1),
            score=float(score),
            posterior_probability=float(probability),
            conditional_probability=float(given_change),
        )
        for boundary, score, probability, given_change in zip(
            boundaries, scores, boundary_probabilities, conditional
        )
    )

    return ChangePointResult(
        detected=change_probability >= detection_threshold,
        sample_count=n,
        feature_count=d,
        min_segment=min_segment,
        change_probability=change_probability,
        no_change_probability=no_change_probability,
        best_boundary_index=best_boundary,
        best_boundary_day=best_boundary + 1,
        best_posterior_probability=float(boundary_probabilities[best_i]),
        best_conditional_probability=float(conditional[best_i]),
        conditional_ci90_start_day=int(boundaries[low_i] + 1),
        conditional_ci90_end_day=int(boundaries[high_i] + 1),
        evidence=evidence,
    )


def detect_observation_change_point(
    observations: Sequence[dict],
    **kwargs,
) -> ChangePointResult:
    """Convenience wrapper for ordinary observable coffee baskets. ☕🧺✂️"""

    return detect_feature_change_point(observations_to_matrix(observations), **kwargs)
