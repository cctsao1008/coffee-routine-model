import numpy as np
import pytest

from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.protocol_adapter import CoffeeEvent, coffee_to_observation


def test_plus_one_to_coffee_to_thumb_becomes_a_clean_tiny_basket():
    obs = coffee_to_observation(["+1?", "+", "☕", "👍"])
    assert obs["invite"] == 1
    assert obs["opt_in"] == 1
    assert obs["routine_maintenance"] == 1
    assert obs["reaction"] == 1
    assert obs["pass_event"] is None
    assert obs["unknown_events"] == []


def test_pass_stays_a_real_choice_instead_of_a_failure():
    obs = coffee_to_observation(["+1?", "pass"])
    assert obs["invite"] == 1
    assert obs["opt_in"] == 0
    assert obs["pass_event"] == 1
    assert obs["text_reply"] == 1


def test_silence_after_invite_is_not_secretly_yes_or_no():
    obs = coffee_to_observation(["+1?"])
    assert obs["invite"] == 1
    assert obs["opt_in"] is None
    assert obs["pass_event"] is None


def test_lonely_thumb_is_allowed_to_be_ambiguous():
    obs = coffee_to_observation(["👍"])
    assert obs["opt_in"] is None
    assert obs["reaction"] is None
    assert obs["unknown_events"] == ["👍"]


def test_thumb_after_invite_can_mean_yes_but_after_coffee_can_mean_reaction():
    yes = coffee_to_observation(["+1?", "👍"])
    ack = coffee_to_observation(["☕", "👍"])
    assert yes["opt_in"] == 1
    assert yes["reaction"] is None
    assert ack["opt_in"] is None
    assert ack["reaction"] == 1


def test_pause_resume_payment_and_updates_can_live_in_the_basket_without_mind_reading():
    obs = coffee_to_observation([
        CoffeeEvent("pause", "leave"),
        CoffeeEvent("proactive_update", "leave notice"),
        CoffeeEvent("payment", "水費"),
        CoffeeEvent("resume", "back tomorrow"),
    ])
    assert obs["pause_event"] == 1
    assert obs["proactive_update"] == 1
    assert obs["payment_event"] == 1
    assert obs["resume_signal"] == 1


def test_unknown_tiny_tokens_are_kept_instead_of_forced_into_a_story():
    assert coffee_to_observation(["mystery-bean-telepathy XD"])["unknown_events"] == ["mystery-bean-telepathy XD"]


def test_optional_warmth_and_delay_are_checked_before_entering_the_basket():
    obs = coffee_to_observation(["+1?", "+"], tone_warmth=0.6, response_delay_min=7.5)
    assert obs["tone_warmth"] == 0.6
    assert obs["response_delay_min"] == 7.5
    with pytest.raises(ValueError):
        coffee_to_observation([], tone_warmth=1.5)
    with pytest.raises(ValueError):
        coffee_to_observation([], response_delay_min=-1.0)


def test_adapter_basket_can_go_directly_to_the_tiny_particle_friends():
    pf = CoffeeParticleFilter(particle_count=300, seed=2026)
    posterior = pf.update(coffee_to_observation(["+1?", "+", "☕", "👍"]))
    assert np.all(np.isfinite(posterior.mean))
    assert np.isclose(posterior.mode_probabilities.sum(), 1.0)
