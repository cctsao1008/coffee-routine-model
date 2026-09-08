from __future__ import annotations

import numpy as np
import pytest

from coffee_brain.actions import RoutineActions, action_effect
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.protocol_adapter import CoffeeEvent, coffee_to_actions, coffee_to_step
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
        "response_delay_min": 18.0,
    }


def test_tiny_action_values_stay_inside_their_little_cup():
    with pytest.raises(ValueError, match="must stay between 0 and 1"):
        RoutineActions(a_boundary_preserving=1.2)


def test_a_voluntary_pass_protects_v_without_secretly_punishing_m():
    effect = action_effect(RoutineActions(b_pass_choice=1.0))

    assert effect[2] > 0.0
    assert effect[1] >= 0.0


def test_coordinated_little_actions_can_have_coupled_effects():
    separate = action_effect(RoutineActions(a_deliver=1.0)) + action_effect(
        RoutineActions(b_acknowledge=1.0)
    )
    together = action_effect(RoutineActions(a_deliver=1.0, b_acknowledge=1.0))

    assert together[0] > separate[0]
    assert together[1] > separate[1]
    assert together[5] < separate[5]


def test_protocol_step_keeps_action_basket_and_observation_basket_separate():
    step = coffee_to_step(
        [
            "+1?",
            "+",
            "☕",
            "👍",
            CoffeeEvent("notify"),
            CoffeeEvent("callback"),
            CoffeeEvent("boundary_preserving"),
        ]
    )

    assert step.actions.a_invite == 1.0
    assert step.actions.a_deliver == 1.0
    assert step.actions.a_notify == 1.0
    assert step.actions.a_callback == 1.0
    assert step.actions.a_boundary_preserving == 1.0
    assert step.actions.b_opt_in == 1.0
    assert step.actions.b_acknowledge == 1.0
    assert step.observation["routine_maintenance"] == 1
    assert step.observation["reaction"] == 1


def test_exception_and_closure_events_find_their_generic_action_drawers():
    actions = coffee_to_actions(
        [
            CoffeeEvent("exception_sync"),
            CoffeeEvent("closure"),
        ]
    )

    assert actions.b_exception_sync == 1.0
    assert actions.b_closure == 1.0


def test_same_synthetic_world_can_diverge_only_because_actions_differ():
    days = 24
    scenario = get_scenario("cozy-normal-year")
    neutral = [RoutineActions() for _ in range(days)]
    coordinated = [
        RoutineActions(
            a_deliver=1.0,
            a_notify=1.0,
            a_boundary_preserving=1.0,
            b_opt_in=1.0,
            b_acknowledge=1.0,
        )
        for _ in range(days)
    ]

    neutral_states, neutral_modes = generate_truth(
        days,
        np.random.default_rng(4242),
        scenario,
        actions=neutral,
    )
    coordinated_states, coordinated_modes = generate_truth(
        days,
        np.random.default_rng(4242),
        scenario,
        actions=coordinated,
    )

    assert np.array_equal(neutral_modes, coordinated_modes)
    assert not np.allclose(neutral_states, coordinated_states)
    assert coordinated_states[-1, 2] > neutral_states[-1, 2]
    assert coordinated_states[-1, 5] < neutral_states[-1, 5]


def test_same_filter_and_same_clues_can_diverge_when_known_actions_differ():
    quiet = CoffeeParticleFilter(particle_count=500, seed=2026)
    active = CoffeeParticleFilter(particle_count=500, seed=2026)
    obs = cozy_observation()

    quiet.update(obs)
    active.update(obs)

    quiet_posterior = quiet.update(obs, actions=RoutineActions())
    active_posterior = active.update(
        obs,
        actions=RoutineActions(
            a_deliver=1.0,
            a_notify=1.0,
            a_boundary_preserving=1.0,
            b_opt_in=1.0,
            b_acknowledge=1.0,
        ),
    )

    assert not np.allclose(quiet_posterior.mean, active_posterior.mean)
    assert active_posterior.mean[2] > quiet_posterior.mean[2]
    assert active_posterior.mean[5] < quiet_posterior.mean[5]


def test_sparse_mapping_can_become_a_tiny_action_basket():
    effect = action_effect({"a_callback": 1.0, "b_acknowledge": 0.5})
    assert effect.shape == (6,)

    with pytest.raises(ValueError, match="Unknown tiny action"):
        action_effect({"telepathy": 1.0})
