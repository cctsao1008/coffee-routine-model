import json

import numpy as np
import pytest

from coffee_brain import (
    ARCHITECTURE_VERSION,
    CSRDM,
    CSRDMConfig,
    DynamicsConfig,
    ExperimentResult,
    ExperimentSpec,
    InferenceConfig,
    SmoothingConfig,
    config_snapshot,
)


def test_public_facade_can_take_protocol_events_without_opening_internal_drawers():
    brain = CSRDM(CSRDMConfig(inference=InferenceConfig(particle_count=120, seed=11)))
    result = brain.step(["+1?", "+", "☕", "👍"], tone_warmth=0.7, response_delay_min=4.0)

    assert result.step_index == 0
    assert result.posterior.mean.shape == (6,)
    assert result.observation["invite"] == 1
    assert result.observation["opt_in"] == 1
    assert result.observation["routine_maintenance"] == 1
    assert result.observation["reaction"] == 1
    assert result.actions.a_invite == 1.0
    assert result.actions.b_opt_in == 1.0
    assert brain.step_count == 1


def test_smoothing_is_enabled_through_config_and_keeps_same_timeline_length():
    brain = CSRDM(
        CSRDMConfig(
            inference=InferenceConfig(particle_count=120, seed=12),
            smoothing=SmoothingConfig(enabled=True, lag=2),
        )
    )
    for events in (["+1?", "+"], ["☕", "👍"], ["+1?", "pass"], ["+1?", "+"]):
        brain.step(events)

    hindsight = brain.smooth()
    assert len(hindsight) == 4
    assert all(row.mean.shape == (6,) for row in hindsight)


def test_smoothing_disabled_gets_a_cute_nope():
    brain = CSRDM(CSRDMConfig(inference=InferenceConfig(particle_count=100, seed=13)))
    brain.step(["+1?", "+"])
    with pytest.raises(RuntimeError, match="smoothing is disabled"):
        brain.smooth()


def test_unified_config_snapshot_is_json_ready_and_versioned():
    config = CSRDMConfig(
        dynamics=DynamicsConfig(process_noise_scale=1.1),
        inference=InferenceConfig(particle_count=150, seed=22),
    )
    snapshot = config_snapshot(config)

    assert snapshot["architecture_version"] == ARCHITECTURE_VERSION
    assert snapshot["dynamics"]["process_noise_scale"] == 1.1
    assert snapshot["inference"]["particle_count"] == 150
    json.dumps(snapshot)


def test_broken_transition_table_is_rejected_before_it_reaches_the_filter():
    with pytest.raises(ValueError, match="5x5"):
        DynamicsConfig(fixed_transition=((1.0, 0.0), (0.0, 1.0)))


def test_experiment_fingerprint_is_recipe_stable_but_label_independent():
    config = CSRDMConfig(inference=InferenceConfig(particle_count=200, seed=7))
    left = ExperimentSpec(
        name="tiny-a",
        scenario="cozy-normal-year",
        days=120,
        config=config,
    )
    right = ExperimentSpec(
        name="renamed-for-display",
        scenario="cozy-normal-year",
        days=120,
        config=config,
    )
    changed = ExperimentSpec(
        name="tiny-a",
        scenario="cozy-normal-year",
        days=121,
        config=config,
    )

    assert left.seed == 7
    assert left.particle_count == 200
    assert left.fingerprint == right.fingerprint
    assert left.fingerprint != changed.fingerprint


def test_experiment_result_writes_one_complete_portable_receipt(tmp_path):
    spec = ExperimentSpec(
        name="tiny receipt",
        scenario="cozy-normal-year",
        days=24,
        config=CSRDMConfig(inference=InferenceConfig(particle_count=100)),
    )
    result = ExperimentResult(
        spec=spec,
        metrics={"rmse": np.float64(0.123)},
        diagnostics={"state": np.array([1, 2, 3])},
        artifacts=("tiny.png",),
        notes=("synthetic only",),
    )

    path = result.write_json(tmp_path / "receipt.json")
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["experiment"]["fingerprint"] == spec.fingerprint
    assert payload["experiment"]["particle_count"] == 100
    assert payload["metrics"]["rmse"] == pytest.approx(0.123)
    assert payload["diagnostics"]["state"] == [1, 2, 3]
    assert payload["artifacts"] == ["tiny.png"]
