import numpy as np
import pytest

from coffee_brain.learning import calibration_metrics, fit_observation_parameters, run_learning_experiment
from coffee_brain.observation_model import DEFAULT_OBSERVATION_MODEL, ObservationModelConfig
from coffee_brain.scenarios import get_scenario
from tiny_tools.simulate import generate_truth, observe


def _world(days=220, seed=20260908, scenario_name="special-day-sparkle"):
    scenario = get_scenario(scenario_name)
    rng = np.random.default_rng(seed)
    truth, modes = generate_truth(days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(days)]
    return truth, modes, observations


def test_learning_returns_normal_config_and_bounded_knobs():
    truth, modes, observations = _world()
    learned, estimates = fit_observation_parameters(truth, modes, observations)

    assert isinstance(learned, ObservationModelConfig)
    assert len(estimates) == 10
    assert all(row.lower_bound <= row.after <= row.upper_bound for row in estimates)
    assert learned.provenance != DEFAULT_OBSERVATION_MODEL.provenance


def test_train_validation_learning_keeps_held_out_metrics_inspectable():
    truth, modes, observations = _world(days=360)
    experiment = run_learning_experiment(truth, modes, observations, train_fraction=0.6)
    before = calibration_metrics(experiment.validation_before)
    after = calibration_metrics(experiment.validation_after)

    assert experiment.split_index == 216
    assert np.isfinite(before["mean_binary_log_loss"])
    assert np.isfinite(after["mean_binary_log_loss"])
    assert np.isfinite(after["delay_normalized_std"])
    # This synthetic world intentionally shifts several observation intercepts.
    assert after["mean_binary_log_loss"] <= before["mean_binary_log_loss"] + 0.03


def test_too_short_learning_basket_gets_a_cute_nope():
    truth, modes, observations = _world(days=18)
    with pytest.raises(ValueError, match="at least 20 synthetic days"):
        fit_observation_parameters(truth, modes, observations)
