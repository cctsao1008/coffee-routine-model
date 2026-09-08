from __future__ import annotations

import numpy as np

from coffee_brain.actions import RoutineActions
from coffee_brain.memory import (
    SharedContextMemoryConfig,
    shared_context_input,
    shared_context_step,
)
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import get_scenario
from tiny_tools.simulate import generate_truth


def cozy_observation():
    return {
        "invite": 1,
        "opt_in": 1,
        "text_reply": 1,
        "reaction": 1,
        "state_share": 0,
        "proactive_update": 0,
        "routine_maintenance": 1,
        "pass_event": 0,
        "resume_signal": 0,
        "tone_warmth": 0.55,
        "response_delay_min": 14.0,
    }


def memory_rich_action():
    return RoutineActions(
        a_invite=1.0,
        a_deliver=1.0,
        a_notify=1.0,
        a_callback=1.0,
        b_opt_in=1.0,
        b_acknowledge=1.0,
        b_closure=1.0,
    )


def test_memory_input_is_bounded_and_callbacks_really_count():
    assert shared_context_input(RoutineActions()) == 0.0
    rich = shared_context_input(memory_rich_action())
    assert 0.0 < rich <= 1.0


def test_repeated_context_input_builds_then_saturates():
    c = 0.25
    memory_input = shared_context_input(memory_rich_action())
    values = []
    for _ in range(180):
        c = float(shared_context_step(c, memory_input))
        values.append(c)

    assert values[-1] > values[0]
    assert values[-1] < 1.0
    assert values[-1] - values[-2] < values[1] - values[0]


def test_quiet_days_decay_slowly_instead_of_erasing_history():
    c = 0.80
    after_ten = c
    for _ in range(10):
        after_ten = float(shared_context_step(after_ten, 0.0))

    after_long_pause = after_ten
    for _ in range(170):
        after_long_pause = float(shared_context_step(after_long_pause, 0.0))

    assert after_ten > 0.78
    assert after_long_pause < after_ten
    assert after_long_pause > 0.50


def test_custom_memory_gravity_validates_its_tiny_knobs():
    config = SharedContextMemoryConfig(accumulation_rate=0.05, decay_rate=0.001, process_noise=0.0)
    assert float(shared_context_step(0.50, 1.0, config=config)) > 0.50


def test_same_filter_and_clues_remember_callbacks_more_than_quiet_actions():
    quiet = CoffeeParticleFilter(particle_count=500, seed=314)
    rich = CoffeeParticleFilter(particle_count=500, seed=314)
    obs = cozy_observation()

    quiet.update(obs)
    rich.update(obs)
    for _ in range(10):
        quiet_posterior = quiet.update(obs, actions=RoutineActions())
        rich_posterior = rich.update(obs, actions=memory_rich_action())

    assert rich_posterior.mean[3] > quiet_posterior.mean[3]


def test_synthetic_shared_context_builds_with_repeated_context_actions():
    days = 60
    scenario = get_scenario("cozy-normal-year")
    quiet_actions = [RoutineActions() for _ in range(days)]
    rich_actions = [memory_rich_action() for _ in range(days)]

    quiet_states, quiet_modes = generate_truth(
        days,
        np.random.default_rng(8080),
        scenario,
        actions=quiet_actions,
    )
    rich_states, rich_modes = generate_truth(
        days,
        np.random.default_rng(8080),
        scenario,
        actions=rich_actions,
    )

    assert np.array_equal(quiet_modes, rich_modes)
    assert rich_states[-1, 3] > quiet_states[-1, 3]
    assert rich_states[-1, 3] > rich_states[0, 3]
