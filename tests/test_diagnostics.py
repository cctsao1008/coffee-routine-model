from __future__ import annotations

import numpy as np
import pytest

from coffee_brain.diagnostics import (
    CLUE_FAMILIES,
    ablate_observations,
    evaluate_observability,
)
from coffee_brain.scenarios import get_scenario
from tiny_tools.simulate import generate_truth, observe


def _tiny_fixture(days: int = 28):
    scenario = get_scenario("cozy-normal-year")
    rng = np.random.default_rng(20260908)
    truth, modes = generate_truth(days, rng, scenario)
    observations = [observe(truth[t], modes[t], rng, scenario) for t in range(days)]
    return truth, modes, observations


def test_ablation_hides_clues_without_rewriting_the_original_little_story():
    observations = [{"reaction": 1, "state_share": 0}]

    hidden = ablate_observations(observations, ("reaction",))

    assert hidden[0]["reaction"] is None
    assert hidden[0]["state_share"] == 0
    assert observations[0]["reaction"] == 1


def test_observability_garden_grows_a_baseline_and_selected_tiny_ablations():
    truth, modes, observations = _tiny_fixture()

    report = evaluate_observability(
        truth,
        modes,
        observations,
        particle_count=180,
        seed=1234,
        families=("reaction", "response_delay"),
    )

    assert report.baseline.label == "all-clues"
    assert set(report.ablations) == {"reaction", "response_delay"}
    assert report.baseline.rmse.shape == (6,)
    assert report.baseline.correlation.shape == (6,)
    assert len(report.scorecard_rows()) == 18
    assert len(report.clue_visibility_rows()) == 12
    assert len(report.state_identifiability) == 6


def test_same_seed_gives_the_same_tiny_observability_scorecard():
    truth, modes, observations = _tiny_fixture()

    first = evaluate_observability(
        truth,
        modes,
        observations,
        particle_count=160,
        seed=777,
        families=("state_share",),
    )
    second = evaluate_observability(
        truth,
        modes,
        observations,
        particle_count=160,
        seed=777,
        families=("state_share",),
    )

    assert np.allclose(first.baseline.rmse, second.baseline.rmse)
    assert np.allclose(first.ablations["state_share"].mae, second.ablations["state_share"].mae)
    assert first.state_identifiability == second.state_identifiability


def test_unknown_clue_family_gets_a_cute_but_useful_nope():
    truth, modes, observations = _tiny_fixture(16)

    with pytest.raises(ValueError, match="Unknown clue family"):
        evaluate_observability(
            truth,
            modes,
            observations,
            particle_count=120,
            families=("telepathy-beans",),
        )


def test_the_garden_knows_all_expected_clue_families():
    assert {
        "opt_in_or_pass",
        "text_reply",
        "reaction",
        "state_share",
        "proactive_update",
        "routine_maintenance",
        "resume_signal",
        "tone_warmth",
        "response_delay",
    } == set(CLUE_FAMILIES)
