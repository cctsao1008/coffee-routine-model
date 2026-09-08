import numpy as np
import pytest

from coffee_brain.change_points import (
    detect_feature_change_point,
    observations_to_matrix,
)


def test_persistent_mean_shift_earns_a_tiny_boundary():
    rng = np.random.default_rng(1234)
    before = rng.normal(0.0, 1.0, size=(70, 5))
    after = rng.normal(1.0, 1.0, size=(70, 5))
    result = detect_feature_change_point(
        np.vstack([before, after]),
        min_segment=20,
        change_prior=0.35,
    )

    assert result.detected
    assert result.change_probability > 0.95
    assert abs(result.best_boundary_index - 70) <= 4
    assert result.conditional_ci90_start_day <= 71 <= result.conditional_ci90_end_day


def test_stable_year_prefers_no_new_world():
    rng = np.random.default_rng(2026)
    stable = rng.normal(0.0, 1.0, size=(140, 5))
    result = detect_feature_change_point(stable, min_segment=20, change_prior=0.35)

    assert not result.detected
    assert result.no_change_probability > 0.80


def test_one_loud_day_is_not_automatically_a_regime_change():
    rng = np.random.default_rng(77)
    timeline = rng.normal(0.0, 1.0, size=(140, 5))
    timeline[70] += 5.0
    result = detect_feature_change_point(timeline, min_segment=20, change_prior=0.35)

    assert not result.detected
    assert result.no_change_probability > 0.70


def test_observation_basket_logs_reply_delay_and_keeps_missing_clues_missing_for_now():
    matrix = observations_to_matrix(
        [
            {
                "invite": 1,
                "opt_in": 1,
                "text_reply": 1,
                "reaction": 0,
                "state_share": None,
                "proactive_update": 0,
                "routine_maintenance": 1,
                "pass_event": 0,
                "resume_signal": 0,
                "tone_warmth": 0.5,
                "response_delay_min": 10.0,
            }
        ]
    )

    assert matrix.shape == (1, 11)
    assert np.isnan(matrix[0, 4])
    assert matrix[0, -1] == pytest.approx(np.log(10.0))


def test_tiny_scissors_reject_impossible_probability_gravity():
    tiny = np.arange(120, dtype=float).reshape(60, 2)

    with pytest.raises(ValueError, match="change_prior"):
        detect_feature_change_point(tiny, min_segment=10, change_prior=1.0)

    with pytest.raises(ValueError, match="cannot fit two segments"):
        detect_feature_change_point(tiny[:15], min_segment=10)
