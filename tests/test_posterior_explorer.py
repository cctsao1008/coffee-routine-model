from __future__ import annotations

import csv
from pathlib import Path

import pytest

from tiny_tools.explore_posterior import load_explorer_rows


STATE_KEYS = ("P", "M", "V", "C", "E", "F")


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _output_row(sample_id: int) -> dict[str, object]:
    row: dict[str, object] = {
        "sample_id": sample_id,
        "scenario": "tiny-test",
        "estimated_mode": "Normal",
        "true_mode": "Normal",
        "ESS": 321.0,
    }
    for index, state in enumerate(STATE_KEYS):
        center = 0.20 + index * 0.10
        row[f"est_{state}"] = center
        row[f"ci95_low_{state}"] = center - 0.05
        row[f"ci95_high_{state}"] = center + 0.05
    return row


def test_loader_joins_observable_events_without_inventing_meaning(tmp_path: Path):
    output_path = tmp_path / "output.csv"
    event_path = tmp_path / "input.csv"

    output_rows = [_output_row(1), _output_row(2)]
    _write_csv(output_path, list(output_rows[0]), output_rows)
    _write_csv(
        event_path,
        ["sample_id", "opt_in", "state_share", "pass_event", "resume_signal"],
        [
            {"sample_id": 1, "opt_in": 1, "state_share": 1, "pass_event": 0, "resume_signal": 0},
            {"sample_id": 2, "opt_in": 0, "state_share": 0, "pass_event": 1, "resume_signal": 1},
        ],
    )

    rows = load_explorer_rows(output_path, event_path)

    assert rows[0]["events"] == ["opt_in", "state_share"]
    assert rows[1]["events"] == ["pass_event", "resume_signal"]
    assert rows[0]["states"]["P"] == {
        "estimate": pytest.approx(0.20),
        "low": pytest.approx(0.15),
        "high": pytest.approx(0.25),
    }


def test_loader_rejects_an_incomplete_posterior_contract(tmp_path: Path):
    output_path = tmp_path / "output.csv"
    row = _output_row(1)
    row.pop("ci95_high_F")
    _write_csv(output_path, list(row), [row])

    with pytest.raises(ValueError, match="ci95_high_F"):
        load_explorer_rows(output_path)
