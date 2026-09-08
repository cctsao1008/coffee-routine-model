import numpy as np
import pytest

from coffee_brain.redundancy import evaluate_state_redundancy
from coffee_brain.scenarios import get_scenario
from tiny_tools.simulate import generate_truth, observe


def _tiny_world(days=28, seed=20260908):
    scenario = get_scenario("cozy-normal-year")
    rng = np.random.default_rng(seed)
    truth, modes = generate_truth(days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(days)]
    return truth, modes, observations


def test_redundancy_report_has_full_correlation_and_reconstruction_rows():
    truth, modes, observations = _tiny_world()
    report = evaluate_state_redundancy(truth, modes, observations, particle_count=100, seed=44)

    assert report.posterior_correlation.shape == (6, 6)
    assert np.allclose(np.diag(report.posterior_correlation), 1.0)
    assert {row["state"] for row in report.reconstruction_rows} == {"P", "M", "V", "C", "E", "F"}


def test_reduced_variant_scorecard_keeps_tradeoffs_visible():
    truth, modes, observations = _tiny_world()
    report = evaluate_state_redundancy(truth, modes, observations, particle_count=100, seed=45)
    names = {row["variant"] for row in report.variant_rows}

    assert "full-6" in names
    assert "merge-C-E" in names
    assert "reconstruct-C-from-other-5" in names
    assert "reconstruct-E-from-other-5" in names
    assert "reconstruct-F-from-other-5" in names
    assert all("binary_observation_NLL" in row for row in report.variant_rows)
    assert all("relationship_RMSE" in row for row in report.variant_rows)


def test_short_chair_audition_gets_a_cute_nope():
    truth, modes, observations = _tiny_world(days=18)
    with pytest.raises(ValueError, match="20 synthetic days"):
        evaluate_state_redundancy(truth, modes, observations, particle_count=100)
