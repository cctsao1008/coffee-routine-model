from __future__ import annotations

import numpy as np

from tiny_tools.decompose_shared_context import (
    CPriorCandidate,
    _centered_rmse,
    _shift_initial_c,
    quiet_bias_curve,
    quiet_memory_rows,
)
from coffee_brain.particles import CoffeeParticleFilter


def test_quiet_bias_curve_decays_with_memory_law():
    curve = quiet_bias_curve(-0.12, 365)
    assert curve[0] == -0.12
    assert abs(curve[-1]) < abs(curve[0])
    expected = -0.12 * (1.0 - 0.0015) ** 364
    assert np.isclose(curve[-1], expected, atol=1e-12)


def test_quiet_memory_receipt_uses_unclipped_offset_retention():
    rows = {int(row["days"]): row for row in quiet_memory_rows(365)}
    assert np.isclose(float(rows[30]["offset_retention_ratio"]), (1.0 - 0.0015) ** 29)
    assert np.isclose(float(rows[365]["offset_retention_ratio"]), (1.0 - 0.0015) ** 364)
    assert 0.57 < float(rows[365]["offset_retention_ratio"]) < 0.59


def test_centered_rmse_separates_offset_from_shape_error():
    error = np.array([-0.10, -0.08, -0.12, -0.10], dtype=float)
    bias = float(np.mean(error))
    rmse = float(np.sqrt(np.mean(error * error)))
    shape = _centered_rmse(error)
    assert np.isclose(rmse * rmse, bias * bias + shape * shape)
    assert shape < rmse


def test_diagnostic_prior_shift_moves_only_shared_context_center():
    pf = CoffeeParticleFilter(particle_count=400, seed=20260908)
    before = pf.particles.copy()
    actual = _shift_initial_c(pf, 0.70)
    assert actual > float(np.mean(before[:, 3]))
    assert np.allclose(pf.particles[:, [0, 1, 2, 4, 5]], before[:, [0, 1, 2, 4, 5]])


def test_prior_candidate_is_explicitly_diagnostic_when_shifted():
    candidate = CPriorCandidate("matched-truth-start", 0.70, "diagnostic-matched-prior")
    assert candidate.requested_center == 0.70
    assert candidate.role.startswith("diagnostic-")
