import numpy as np
import pytest

from coffee_brain.arena import run_model_arena
from coffee_brain.scenarios import get_scenario
from tiny_tools.simulate import generate_truth, observe


def _world(days=100, seed=20260908):
    scenario = get_scenario("special-day-sparkle")
    rng = np.random.default_rng(seed)
    truth, modes = generate_truth(days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(days)]
    return truth, modes, observations


def test_model_arena_returns_multiple_comparable_tradeoffs():
    truth, modes, observations = _world()
    summaries, state_rows, runs = run_model_arena(
        truth,
        modes,
        observations,
        particle_count=100,
        seed=77,
        smoothing_lag=6,
    )

    names = {row["model"] for row in summaries}
    assert len(summaries) >= 6
    assert "CSRDM-6 hand-set PF" in names
    assert "CSRDM-6 learned observation" in names
    assert "CSRDM-5 reconstruct C" in names
    assert "static prior non-hybrid" in names
    assert len(state_rows) == 6 * len(summaries)
    assert len(runs) == len(summaries)
    assert all("runtime_seconds" in row for row in summaries)
    assert all("obs_NLL_given_true_mode" in row for row in summaries)


def test_arena_does_not_hide_noncomparable_mode_metric():
    truth, modes, observations = _world()
    summaries, _, _ = run_model_arena(truth, modes, observations, particle_count=100, seed=78)
    static = next(row for row in summaries if row["model"] == "static prior non-hybrid")
    assert np.isnan(float(static["mode_accuracy"]))
    assert static["change_point_metric"] == "n/a for one stationary arena basket"


def test_short_arena_track_gets_a_cute_nope():
    truth, modes, observations = _world(days=50)
    with pytest.raises(ValueError, match="at least 60 synthetic days"):
        run_model_arena(truth, modes, observations, particle_count=100)
