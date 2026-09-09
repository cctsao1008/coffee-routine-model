import numpy as np
import pytest

from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import DEFAULT_SCENARIO, SCENARIOS, get_scenario, scenario_names


EXPECTED_TINY_WEATHER = {
    "cozy-normal-year", "super-busy-month", "long-leave-and-return",
    "sleepy-reply-season", "special-day-sparkle", "noisy-chaos-week",
    "slow-recovery",
}


def test_all_expected_weather_is_waiting_in_the_tiny_garden():
    assert set(scenario_names()) == EXPECTED_TINY_WEATHER
    assert DEFAULT_SCENARIO in SCENARIOS


def test_every_tiny_world_has_valid_probability_gravity():
    for scenario in SCENARIOS.values():
        scenario.validate()
        assert scenario.transition.shape == (5, 5)
        assert np.allclose(scenario.transition.sum(axis=1), 1.0)
        assert scenario.target.shape == (6,)
        assert scenario.mode_effects.shape == (5, 6)
        assert scenario.process_noise.shape == (6,)
        assert np.allclose(scenario.mode_effects[:, 3], 0.0)
        assert scenario.process_noise[3] == pytest.approx(0.0)
        assert scenario.target[3] == pytest.approx(0.0)


def test_some_worlds_really_hide_the_estimators_answer_key():
    mismatched_worlds = [scenario for name, scenario in SCENARIOS.items()
                         if name != DEFAULT_SCENARIO and not np.allclose(scenario.transition, CoffeeParticleFilter.transition)]
    assert mismatched_worlds


def test_scenario_recipe_arrays_are_frozen_little_receipts():
    scenario = get_scenario("cozy-normal-year")
    with pytest.raises(ValueError):
        scenario.transition[0, 0] = 0.5
    with pytest.raises(ValueError):
        scenario.process_noise[0] = 99.0


def test_get_scenario_returns_the_requested_little_weather_card():
    scenario = get_scenario("slow-recovery")
    assert scenario.slug == "slow-recovery"
    assert scenario.emoji
    assert "Recovery" in scenario.title


def test_unknown_weather_gets_a_useful_cute_error():
    with pytest.raises(ValueError, match="Unknown coffee weather"):
        get_scenario("espresso-tornado-from-mars")
