from __future__ import annotations

import pytest

from coffee_brain import (
    CSRDM,
    CSRDMConfig,
    DEFAULT_CONTEXT_TRANSITIONS,
    InferenceConfig,
    LearningConfig,
    SmoothingConfig,
)


def tiny_brain(seed: int = 9001) -> CSRDM:
    return CSRDM(
        CSRDMConfig(
            inference=InferenceConfig(particle_count=100, seed=seed),
        )
    )


def test_public_result_attaches_names_to_the_six_state_numbers():
    result = tiny_brain().step(["+1?", "要", "☕", "👍"])

    assert tuple(result.mean_by_state) == (
        "predictability",
        "mutuality",
        "voluntariness",
        "shared_context",
        "state_sharing",
        "friction",
    )
    assert set(result.ci95_by_state) == set(result.mean_by_state)
    assert tuple(result.mode_probabilities_by_name) == (
        "Normal",
        "Busy",
        "Leave",
        "Special",
        "Recovery",
    )
    assert sum(result.mode_probabilities_by_name.values()) == pytest.approx(1.0)


def test_missing_public_clues_can_be_omitted_or_explicit_none():
    brain = tiny_brain(9002)
    first = brain.update({})
    second = brain.update({"reaction": None, "response_delay_min": None})

    assert first.observation == {}
    assert second.observation["reaction"] is None
    assert second.observation["response_delay_min"] is None


def test_unknown_public_observation_key_fails_instead_of_becoming_hidden_missing_data():
    with pytest.raises(ValueError, match="Unknown observation field"):
        tiny_brain(9003).update({"reacion": 1})


def test_fractional_binary_clue_is_rejected_instead_of_int_truncation():
    with pytest.raises(ValueError, match="must be 0, 1, or None"):
        tiny_brain(9004).update({"reaction": 0.7})


def test_public_continuous_clues_get_actionable_range_checks():
    brain = tiny_brain(9005)

    with pytest.raises(ValueError, match="tone_warmth.*between 0 and 1"):
        brain.update({"tone_warmth": 1.2})
    with pytest.raises(ValueError, match="response_delay_min.*cannot be negative"):
        brain.update({"response_delay_min": -3.0})


def test_measured_reply_delay_implies_reply_presence_without_duplicate_input():
    result = tiny_brain(9006).update({"response_delay_min": 4.2})

    assert result.observation["text_reply"] == 1
    assert result.observation["response_delay_min"] == pytest.approx(4.2)


def test_reply_delay_cannot_coexist_with_an_explicit_no_reply():
    with pytest.raises(ValueError, match="cannot be combined with text_reply=0"):
        tiny_brain(9007).update(
            {
                "text_reply": 0,
                "response_delay_min": 4.2,
            }
        )


def test_protocol_contradictions_are_rejected_at_the_public_door():
    brain = tiny_brain(9008)

    with pytest.raises(ValueError, match="opt_in=1 and pass_event=1"):
        brain.update({"opt_in": 1, "pass_event": 1})
    with pytest.raises(ValueError, match="pass_event=1.*routine_maintenance=1"):
        brain.update({"pass_event": 1, "routine_maintenance": 1})
    with pytest.raises(ValueError, match="routine_maintenance=1.*opt_in=0"):
        brain.update({"opt_in": 0, "routine_maintenance": 1})
    with pytest.raises(ValueError, match="invite=0 closes the response opportunity"):
        brain.update({"invite": 0, "opt_in": 1})


def test_result_makes_the_first_step_transition_boundary_visible():
    brain = tiny_brain(9009)

    first = brain.update({"reaction": 1}, actions={"b_acknowledge": 1.0})
    second = brain.update({"reaction": 1}, actions={"b_acknowledge": 1.0})

    assert first.actions.b_acknowledge == 1.0
    assert first.transition_applied is False
    assert second.transition_applied is True


def test_transition_context_cannot_be_silently_ignored_by_fixed_only_default():
    with pytest.raises(ValueError, match="context-aware transitions are disabled"):
        tiny_brain(9010).update({}, transition_context={"disturbance": 0.8})


def test_context_aware_transition_default_is_reachable_from_public_imports():
    brain = CSRDM(
        CSRDMConfig(
            transition=DEFAULT_CONTEXT_TRANSITIONS,
            inference=InferenceConfig(particle_count=100, seed=9011),
        )
    )

    first = brain.update({}, transition_context={"disturbance": 0.8})
    second = brain.update({}, transition_context={"recovery_hint": 0.7})

    assert first.transition_applied is False
    assert second.transition_applied is True


def test_online_csrmd_does_not_silently_turn_on_parameter_learning():
    with pytest.raises(ValueError, match="does not perform online learning"):
        CSRDM(
            CSRDMConfig(
                learning=LearningConfig(enabled=True),
                inference=InferenceConfig(particle_count=100, seed=9012),
            )
        )


def test_smoothing_error_points_to_the_configuration_that_enables_history():
    brain = tiny_brain(9013)
    brain.update({})

    with pytest.raises(RuntimeError, match="SmoothingConfig\(enabled=True"):
        brain.smooth()


def test_smoothing_still_works_when_enabled_before_the_timeline():
    brain = CSRDM(
        CSRDMConfig(
            inference=InferenceConfig(particle_count=100, seed=9014),
            smoothing=SmoothingConfig(enabled=True, lag=1),
        )
    )
    brain.update({})
    brain.update({"reaction": 1})

    hindsight = brain.smooth()
    assert len(hindsight) == 2
