from __future__ import annotations

import numpy as np
import pytest

from tiny_tools.audit_reference import summarize_state_excitation


def test_state_excitation_receipt_measures_truth_motion_without_replacing_metrics():
    truth = np.array(
        [
            [0.10, 0.20, 0.30, 0.40, 0.50, 0.60],
            [0.20, 0.20, 0.30, 0.50, 0.70, 0.55],
            [0.30, 0.20, 0.30, 0.60, 0.90, 0.50],
        ]
    )
    estimates = truth + np.array([0.01, -0.02, 0.03, 0.04, -0.05, 0.06])

    rows = summarize_state_excitation(truth, estimates)
    assert [row["state"] for row in rows] == ["P", "M", "V", "C", "E", "F"]

    by_state = {row["state"]: row for row in rows}
    assert by_state["P"]["truth_span"] == pytest.approx(0.20)
    assert by_state["M"]["truth_std"] == pytest.approx(0.0)
    assert by_state["V"]["truth_span"] == pytest.approx(0.0)
    assert by_state["C"]["initial_estimate_minus_truth"] == pytest.approx(0.04)
    assert by_state["E"]["mean_estimate_minus_truth"] == pytest.approx(-0.05)

    # Keep this receipt about excitation / offset. The estimator scorecard remains
    # the one home for RMSE, correlation, and interval coverage. ☕📏
    assert "RMSE" not in rows[0]
    assert "Pearson_r" not in rows[0]
    assert "CI95_coverage" not in rows[0]


def test_state_excitation_rejects_wrong_or_nonfinite_baskets():
    with pytest.raises(ValueError, match="shape"):
        summarize_state_excitation(np.zeros((3, 5)), np.zeros((3, 5)))

    truth = np.zeros((3, 6))
    estimates = np.zeros((3, 6))
    truth[1, 2] = np.nan
    with pytest.raises(ValueError, match="finite"):
        summarize_state_excitation(truth, estimates)
