import numpy as np

from coffee_brain.model import RoutineMode
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import DEFAULT_SCENARIO, SCENARIOS, get_scenario
from tiny_tools.simulate import default_output_path, generate_truth, observe


FIXED_STATE = np.array([0.78, 0.68, 0.88, 0.70, 0.36, 0.14])


def test_same_seed_grows_the_same_tiny_coffee_year():
    scenario = get_scenario(DEFAULT_SCENARIO)
    first_states, first_modes = generate_truth(40, np.random.default_rng(20260908), scenario)
    second_states, second_modes = generate_truth(40, np.random.default_rng(20260908), scenario)
    assert np.allclose(first_states, second_states)
    assert np.array_equal(first_modes, second_modes)


def test_same_seed_makes_the_same_little_observation():
    scenario = get_scenario("noisy-chaos-week")
    first = observe(FIXED_STATE, RoutineMode.BUSY, np.random.default_rng(123), scenario)
    second = observe(FIXED_STATE, RoutineMode.BUSY, np.random.default_rng(123), scenario)
    assert first == second


def test_every_mode_can_make_a_tiny_clue_without_falling_over():
    scenario = get_scenario(DEFAULT_SCENARIO)
    for mode in RoutineMode:
        obs = observe(FIXED_STATE, mode, np.random.default_rng(100 + int(mode)), scenario)
        assert set(obs) == {
            "invite", "opt_in", "text_reply", "reaction", "state_share",
            "proactive_update", "routine_maintenance", "pass_event", "resume_signal",
            "tone_warmth", "response_delay_min",
        }
        assert 0.0 <= obs["tone_warmth"] <= 1.0
        assert 0.2 <= obs["response_delay_min"] <= 360.0


def test_every_weather_can_survive_a_small_particle_picnic():
    for i, scenario in enumerate(SCENARIOS.values()):
        rng = np.random.default_rng(500 + i)
        truth, modes = generate_truth(10, rng, scenario)
        pf = CoffeeParticleFilter(particle_count=150, seed=900 + i)
        for day in range(10):
            posterior = pf.update(observe(truth[day], RoutineMode(int(modes[day])), rng, scenario))
            assert np.all(np.isfinite(posterior.mean))


def test_alternate_weather_gets_its_own_little_output_cubby():
    cozy = default_output_path(365, get_scenario(DEFAULT_SCENARIO))
    slow = default_output_path(365, get_scenario("slow-recovery"))
    assert str(cozy).replace("\\", "/") == "examples/365-cute-days"
    assert str(slow).replace("\\", "/") == "examples/365-cute-days/slow-recovery"
