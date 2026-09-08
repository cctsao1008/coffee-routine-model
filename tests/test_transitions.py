import numpy as np
import pytest

from coffee_brain.actions import RoutineActions
from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.scenarios import BASE_TRANSITION
from coffee_brain.transitions import (
    DEFAULT_CONTEXT_TRANSITIONS,
    TransitionContext,
    context_transition_probabilities,
    fixed_transition_probabilities,
)


COZY_STATE = np.array([0.80, 0.72, 0.90, 0.76, 0.42, 0.10])


def test_fixed_baseline_is_still_exactly_the_old_little_matrix():
    probability = fixed_transition_probabilities(np.arange(5))
    assert np.allclose(probability, BASE_TRANSITION)


def test_context_probabilities_always_keep_probability_gravity():
    states = np.tile(COZY_STATE, (5, 1))
    probability = context_transition_probabilities(np.arange(5), states)

    assert probability.shape == (5, 5)
    assert np.all(probability > 0.0)
    assert np.allclose(probability.sum(axis=1), 1.0)


def test_same_previous_mode_can_roll_different_dice_under_different_contexts():
    baseline = context_transition_probabilities(0, COZY_STATE)
    exception = context_transition_probabilities(
        0,
        COZY_STATE,
        RoutineActions(a_boundary_preserving=1.0, b_exception_sync=1.0),
        TransitionContext(disturbance=0.6),
    )
    recovery = context_transition_probabilities(
        0,
        COZY_STATE,
        RoutineActions(a_notify=1.0, b_exception_sync=1.0, b_closure=1.0),
    )

    assert exception[2] > baseline[2]  # Leave becomes more plausible.
    assert recovery[4] > baseline[4]  # Recovery becomes more plausible.
    assert not np.allclose(exception, recovery)


def test_explicit_special_event_can_make_special_more_plausible_without_forcing_it():
    ordinary = context_transition_probabilities(0, COZY_STATE)
    special = context_transition_probabilities(
        0,
        COZY_STATE,
        context=TransitionContext(special_event=1.0),
    )

    assert special[3] > ordinary[3]
    assert special[3] < 1.0


def test_regime_logits_are_explicit_external_context_not_a_secret_story():
    ordinary = context_transition_probabilities(0, COZY_STATE)
    shifted = context_transition_probabilities(
        0,
        COZY_STATE,
        context=TransitionContext(regime_logits=(-0.4, 0.5, 0.0, 0.0, 0.2)),
    )

    assert shifted[1] > ordinary[1]


def test_one_context_nudge_is_clipped_before_the_tiny_dice_fly_away():
    wild = TransitionContext(
        disturbance=1.0,
        regime_logits=(-99.0, 99.0, -99.0, -99.0, -99.0),
    )
    probability = context_transition_probabilities(0, COZY_STATE, context=wild)

    assert np.all(probability > 0.0)
    assert probability[1] < 1.0
    assert np.isclose(probability.sum(), 1.0)


def test_particle_filter_keeps_fixed_mode_baseline_unless_context_model_is_invited():
    fixed = CoffeeParticleFilter(particle_count=400, seed=55)
    aware = CoffeeParticleFilter(
        particle_count=400,
        seed=55,
        transition_config=DEFAULT_CONTEXT_TRANSITIONS,
    )
    obs = {
        "invite": 1,
        "opt_in": 1,
        "routine_maintenance": 1,
        "tone_warmth": 0.55,
        "response_delay_min": 20.0,
    }

    fixed.update(obs)
    aware.update(obs)
    fixed.update(obs, actions=RoutineActions(a_boundary_preserving=1.0, b_exception_sync=1.0))
    aware.update(
        obs,
        actions=RoutineActions(a_boundary_preserving=1.0, b_exception_sync=1.0),
        transition_context=TransitionContext(disturbance=0.8),
    )

    fixed_leave_fraction = np.mean(fixed.modes == 2)
    aware_leave_fraction = np.mean(aware.modes == 2)
    assert aware_leave_fraction > fixed_leave_fraction


def test_bad_transition_context_gets_a_cute_nope():
    with pytest.raises(ValueError, match="Transition context 'disturbance'"):
        TransitionContext(disturbance=1.5)
