from __future__ import annotations

import numpy as np
import pytest

from coffee_brain.calibration import calibrate_dataset
from coffee_brain.observation_model import (
    BinaryChannelConfig,
    DEFAULT_OBSERVATION_MODEL,
    predict_binary_channels,
    predict_delay_log_mean,
    predict_warmth_mean,
)
from coffee_brain.scenarios import get_scenario
from tiny_tools.simulate import generate_truth, observe


def test_default_knobs_reproduce_the_old_opt_in_recipe():
    state = np.array([[0.72, 0.64, 0.88, 0.61, 0.35, 0.16]])
    mode = np.array([1])
    p = predict_binary_channels(state, mode)["opt_in"][0]

    logit = -1.2 + 1.7 * 0.64 + 1.2 * 0.88 + 0.8 * 0.72 - 1.8 * 0.16 - 0.7
    expected = 1.0 / (1.0 + np.exp(-logit))
    assert p == pytest.approx(expected)


def test_tiny_knobs_are_inspectable_and_easy_to_swap_without_mutation():
    state = np.array([[0.75, 0.70, 0.90, 0.70, 0.40, 0.10]])
    mode = np.array([0])
    original = predict_binary_channels(state, mode, DEFAULT_OBSERVATION_MODEL)["opt_in"][0]

    louder = DEFAULT_OBSERVATION_MODEL.with_binary_channel("opt_in", intercept=1.8)
    changed = predict_binary_channels(state, mode, louder)["opt_in"][0]

    assert changed > original
    assert DEFAULT_OBSERVATION_MODEL.opt_in.intercept == -1.2
    assert louder.provenance == DEFAULT_OBSERVATION_MODEL.provenance


def test_broken_little_channel_shapes_are_rejected():
    with pytest.raises(ValueError, match="six state coefficients"):
        BinaryChannelConfig(intercept=0.0, state_coefficients=(1.0, 2.0))  # type: ignore[arg-type]


def _baseline_dataset(days: int = 1200):
    scenario = get_scenario("cozy-normal-year")
    rng = np.random.default_rng(123456)
    truth, modes = generate_truth(days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(days)]
    return truth, modes, observations


def test_calibration_bench_makes_binary_reliability_and_continuous_residuals():
    truth, modes, observations = _baseline_dataset(800)
    result = calibrate_dataset(truth, modes, observations, bins=8)

    assert len(result.binary) == 8
    assert len(result.continuous) == 2
    assert np.isfinite(result.mean_brier)
    assert np.isfinite(result.mean_ece)

    for row in result.binary:
        assert row.n > 0
        assert 0.0 <= row.brier_score <= 1.0
        assert row.log_loss >= 0.0
        bin_total = sum(item.n for item in result.reliability if item.channel == row.channel)
        assert bin_total == row.n

    warmth = next(row for row in result.continuous if row.channel == "tone_warmth")
    delay = next(row for row in result.continuous if row.channel == "log_response_delay")
    assert warmth.n == 800
    assert 0 < delay.n < 800
    for row in (warmth, delay):
        assert np.isfinite(row.normalized_mean)
        assert np.isfinite(row.normalized_std)
        assert 0.25 < row.normalized_std < 1.75


def test_missing_delay_is_missing_evidence_not_a_fake_zero():
    truth, modes, observations = _baseline_dataset(120)
    for obs in observations:
        obs["response_delay_min"] = None

    result = calibrate_dataset(truth, modes, observations, bins=6)
    delay = next(row for row in result.continuous if row.channel == "log_response_delay")

    assert delay.n == 0
    assert np.isnan(delay.rmse)
    assert np.isnan(delay.normalized_std)


def test_a_bad_opt_in_knob_gets_a_worse_brier_score_on_the_same_world():
    truth, modes, observations = _baseline_dataset(1500)
    baseline = calibrate_dataset(truth, modes, observations, bins=10)
    bad_config = DEFAULT_OBSERVATION_MODEL.with_binary_channel("opt_in", intercept=2.5)
    bad = calibrate_dataset(truth, modes, observations, config=bad_config, bins=10)

    base_row = next(row for row in baseline.binary if row.channel == "opt_in")
    bad_row = next(row for row in bad.binary if row.channel == "opt_in")
    assert bad_row.brier_score > base_row.brier_score
    assert abs(bad_row.calibration_gap) > abs(base_row.calibration_gap)


def test_warmth_and_delay_prediction_knobs_are_explicit_too():
    states = np.array(
        [
            [0.80, 0.70, 0.90, 0.75, 0.40, 0.10],
            [0.50, 0.45, 0.80, 0.55, 0.30, 0.25],
        ]
    )
    modes = np.array([0, 2])

    warmth = predict_warmth_mean(states, modes)
    delay = predict_delay_log_mean(states, modes)

    assert warmth.shape == (2,)
    assert delay.shape == (2,)
    assert delay[1] > delay[0]
    assert DEFAULT_OBSERVATION_MODEL.tone_warmth.sigma == pytest.approx(0.07)
    assert DEFAULT_OBSERVATION_MODEL.response_delay.sigma_log == pytest.approx(0.45)
