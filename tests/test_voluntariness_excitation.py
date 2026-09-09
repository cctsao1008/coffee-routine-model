import numpy as np

from coffee_brain.observation_model import DEFAULT_OBSERVATION_MODEL
from tiny_tools.excite_voluntariness import (
    build_v_excitation_truth,
    run_v_excitation,
    v_channel_sensitivity_rows,
)


def test_v_excitation_truth_has_real_dynamic_range_without_moving_everything_else():
    states, modes, phases = build_v_excitation_truth(100, low_v=0.58, high_v=0.94)

    assert np.isclose(np.ptp(states[:, 2]), 0.36)
    assert np.std(states[:, 2]) > 0.10
    assert np.allclose(states[:, 0], 0.80)
    assert np.allclose(states[:, 1], 0.72)
    assert np.allclose(states[:, 4], 0.42)
    assert np.allclose(states[:, 5], 0.10)
    assert np.all(modes == 0)
    assert phases[0] == "high-hold"
    assert "low-hold" in phases
    assert phases[-1] == "high-return"

    # C follows its declared quiet-memory path instead of being silently clamped.
    assert np.all(np.diff(states[:, 3]) <= 1e-12)


def test_v_channel_sensitivity_is_derived_from_the_current_observation_config():
    rows = v_channel_sensitivity_rows(low_v=0.58, high_v=0.94)
    by_name = {row["channel"]: row for row in rows}

    for name, channel in DEFAULT_OBSERVATION_MODEL.binary_channels().items():
        assert np.isclose(by_name[name]["direct_V_coefficient"], channel.state_coefficients[2])

    assert np.isclose(
        by_name["tone_warmth"]["direct_V_coefficient"],
        DEFAULT_OBSERVATION_MODEL.tone_warmth.state_coefficients[2],
    )
    assert by_name["response_delay_log_mean"]["direct_V_coefficient"] == 0.0


def test_small_v_excitation_run_returns_finite_metrics_and_wider_truth_range():
    _, _, _, _, _, _, metrics = run_v_excitation(
        days=60,
        particles=180,
        seed=1234,
        low_v=0.58,
        high_v=0.94,
    )

    assert metrics["truth_std"] > 0.10
    assert np.isclose(metrics["truth_span"], 0.36)
    for key in ("estimate_std", "RMSE", "MAE", "Pearson_r", "CI95_coverage", "mean_estimate_minus_truth"):
        assert np.isfinite(metrics[key])
    assert 0.0 <= metrics["CI95_coverage"] <= 1.0
