import numpy as np
import pytest

from coffee_brain.scenarios import get_scenario
from coffee_brain.sensitivity import evaluate_sensitivity, transition_temperature
from tiny_tools.simulate import generate_truth, observe


def _tiny_world(days=24, seed=20260908):
    scenario = get_scenario("cozy-normal-year")
    rng = np.random.default_rng(seed)
    truth, modes = generate_truth(days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(days)]
    return truth, modes, observations


def test_sensitivity_map_has_one_row_per_poke_and_six_tiny_states():
    truth, modes, observations = _tiny_world()
    report = evaluate_sensitivity(truth, modes, observations, particle_count=100, seed=77)
    labels, matrix = report.matrix()

    assert len(labels) == len(report.variants)
    assert matrix.shape == (len(report.variants), 6)
    assert np.all(np.isfinite(matrix))
    assert any(label.startswith("hide-") for label in labels)
    assert "process-noise-1.25x" in labels
    assert "transition-temp-1.15" in labels


def test_sensitivity_rows_keep_coverage_and_mode_deltas_visible():
    truth, modes, observations = _tiny_world()
    report = evaluate_sensitivity(truth, modes, observations, particle_count=100, seed=88)
    rows = report.rows()

    assert rows
    assert {row["state"] for row in rows} == {"P", "M", "V", "C", "E", "F"}
    assert all("CI95_coverage" in row for row in rows)
    assert all("mode_accuracy_delta" in row for row in rows)


def test_transition_temperature_keeps_each_tiny_row_normalized():
    base = np.array(
        [
            [0.7, 0.1, 0.1, 0.05, 0.05],
            [0.2, 0.5, 0.1, 0.1, 0.1],
            [0.1, 0.1, 0.6, 0.1, 0.1],
            [0.2, 0.1, 0.1, 0.5, 0.1],
            [0.2, 0.1, 0.1, 0.1, 0.5],
        ]
    )
    warmed = transition_temperature(base, 1.2)
    assert np.all(warmed > 0.0)
    assert np.allclose(warmed.sum(axis=1), 1.0)


def test_bad_temperature_gets_a_cute_nope():
    with pytest.raises(ValueError, match="temperature"):
        transition_temperature(np.eye(5), 0.0)
