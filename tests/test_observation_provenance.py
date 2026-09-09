from coffee_brain.observation_model import BINARY_CHANNEL_NAMES, DEFAULT_OBSERVATION_MODEL, STATE_ORDER
from tiny_tools.inspect_observation_provenance import MODE_ORDER, build_inventory


def test_provenance_inventory_covers_every_default_observation_knob():
    rows = build_inventory()
    channels = {row["channel"] for row in rows}
    assert channels == set(BINARY_CHANNEL_NAMES) | {"tone_warmth", "response_delay"}

    for name in BINARY_CHANNEL_NAMES:
        channel_rows = [row for row in rows if row["channel"] == name]
        assert len([row for row in channel_rows if row["parameter_kind"] == "state_coefficient"]) == len(STATE_ORDER)
        assert len([row for row in channel_rows if row["parameter_kind"] == "mode_offset"]) == len(MODE_ORDER)

    warmth_rows = [row for row in rows if row["channel"] == "tone_warmth"]
    assert len([row for row in warmth_rows if row["parameter_kind"] == "state_coefficient"]) == len(STATE_ORDER)
    assert len([row for row in warmth_rows if row["parameter_kind"] == "mode_offset"]) == len(MODE_ORDER)

    delay_rows = [row for row in rows if row["channel"] == "response_delay"]
    assert {row["target"] for row in delay_rows if row["parameter_kind"] == "state_gap"} == {"P", "M"}
    assert len([row for row in delay_rows if row["parameter_kind"] == "mode_add_minutes"]) == len(MODE_ORDER)


def test_nonzero_edges_are_assumptions_and_zero_edges_do_not_claim_independence():
    for row in build_inventory():
        if row["model_edge"] == "present":
            assert row["epistemic_status"] == "Assumed"
        if row["model_edge"] == "no-direct-edge":
            assert row["epistemic_status"] == "Undefined beyond the current direct specification"


def test_inventory_reads_the_runtime_config_instead_of_copying_numbers():
    rows = build_inventory()
    opt_in_p = next(
        row
        for row in rows
        if row["channel"] == "opt_in"
        and row["parameter_kind"] == "state_coefficient"
        and row["target"] == "P"
    )
    assert opt_in_p["value"] == DEFAULT_OBSERVATION_MODEL.opt_in.state_coefficients[0]

    delay_busy = next(
        row
        for row in rows
        if row["channel"] == "response_delay"
        and row["parameter_kind"] == "mode_add_minutes"
        and row["target"] == "Busy"
    )
    assert delay_busy["value"] == DEFAULT_OBSERVATION_MODEL.response_delay.mode_add_minutes[1]


def test_provenance_doc_keeps_the_main_epistemic_boundaries_visible():
    text = open("docs/observation-provenance.md", encoding="utf-8").read()
    for channel in (*BINARY_CHANNEL_NAMES, "tone_warmth", "response_delay"):
        assert f"`{channel}`" in text
    for rule in (
        "Assumed coefficient != discovered law",
        "Zero coefficient != proven independence",
        "Undefined relationship != zero relationship",
        "Calibration != ontology discovery",
        "numeric precision != epistemic certainty",
    ):
        assert rule in text
    assert "provenance stays outside runtime config" in text
