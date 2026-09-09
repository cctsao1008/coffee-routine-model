from __future__ import annotations

import numpy as np

from coffee_brain.actions import RoutineActions
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import get_scenario
from tiny_tools.controlled_reference import (
    ACTION_GRAMMAR,
    ACTION_CYCLE,
    build_action_schedule,
    controlled_observation,
)
from tiny_tools.simulate import generate_truth


def test_action_schedule_repeats_generic_grammar_and_exercises_required_paths():
    labels, actions = build_action_schedule(24)
    assert len(labels) == len(actions) == 24
    assert labels[: len(ACTION_CYCLE)] == list(ACTION_CYCLE)
    assert any(a.a_invite for a in actions)
    assert any(a.a_deliver and a.b_acknowledge for a in actions)
    assert any(a.a_boundary_preserving and a.b_pass_choice for a in actions)
    assert any(a.b_exception_sync for a in actions)
    assert any(a.a_callback for a in actions)


def test_controlled_observation_keeps_protocol_channels_consistent():
    base = {
        "invite": 0,
        "opt_in": 0,
        "text_reply": 0,
        "reaction": 0,
        "state_share": 0,
        "proactive_update": 0,
        "routine_maintenance": 0,
        "pass_event": 0,
        "resume_signal": 0,
        "tone_warmth": 0.5,
        "response_delay_min": None,
    }
    ordinary = controlled_observation(base, ACTION_GRAMMAR["ordinary-opt-in"], "ordinary-opt-in")
    assert ordinary["invite"] == 1
    assert ordinary["opt_in"] == 1
    assert ordinary["pass_event"] == 0
    assert ordinary["routine_maintenance"] == 1
    assert ordinary["text_reply"] == 1
    assert ordinary["reaction"] == 1

    passed = controlled_observation(base, ACTION_GRAMMAR["voluntary-pass"], "voluntary-pass")
    assert passed["invite"] == 1
    assert passed["opt_in"] == 0
    assert passed["pass_event"] == 1
    assert passed["routine_maintenance"] == 0
    assert passed["text_reply"] == 1


def test_generate_truth_uses_day_t_action_for_transition_into_day_t_plus_1():
    scenario = get_scenario("cozy-normal-year")
    days = 3
    strong = [RoutineActions(a_callback=1.0), RoutineActions(), RoutineActions()]
    quiet = [RoutineActions(), RoutineActions(), RoutineActions()]

    truth_strong, _ = generate_truth(days, np.random.default_rng(20260908), scenario, actions=strong)
    truth_quiet, _ = generate_truth(days, np.random.default_rng(20260908), scenario, actions=quiet)

    assert np.isclose(truth_strong[0, 3], truth_quiet[0, 3])
    assert truth_strong[1, 3] > truth_quiet[1, 3]


def test_particle_filter_ignores_control_on_first_update_then_uses_it_on_next_transition():
    action = RoutineActions(a_callback=1.0)
    aware = CoffeeParticleFilter(particle_count=500, seed=20260908)
    blind = CoffeeParticleFilter(particle_count=500, seed=20260908)

    first_aware = aware.update({}, actions=action)
    first_blind = blind.update({})
    assert np.allclose(first_aware.mean, first_blind.mean)

    second_aware = aware.update({}, actions=action)
    second_blind = blind.update({})
    assert second_aware.mean[3] > second_blind.mean[3]
