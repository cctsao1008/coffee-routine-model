import numpy as np

from tiny_tools.scan_v_dynamics import (
    CANDIDATES,
    SHAPES,
    build_v_shape,
    scan_v_dynamics,
)


def test_v_shape_family_really_changes_the_synthetic_path():
    paths = {}
    for shape in SHAPES:
        truth, modes = build_v_shape(60, shape, low_v=0.58, high_v=0.94)
        paths[shape] = truth[:, 2]
        assert np.ptp(truth[:, 2]) >= 0.35
        assert np.all(modes == 0)
    assert not np.allclose(paths["ramp"], paths["step"])
    assert not np.allclose(paths["ramp"], paths["triangle"])


def test_v_prior_grid_keeps_current_default_and_bounded_comparators():
    default = next(candidate for candidate in CANDIDATES if candidate.name == "default")
    assert default.mean_reversion == 0.035
    assert default.process_sigma == 0.011
    assert any(candidate.mean_reversion < default.mean_reversion for candidate in CANDIDATES)
    assert any(candidate.process_sigma > default.process_sigma for candidate in CANDIDATES)


def test_small_v_dynamics_scan_is_deterministic_without_committed_baseline():
    first, first_runs, first_baseline = scan_v_dynamics(
        days=60,
        particles=220,
        seeds=(1234,),
        shapes=("ramp", "step"),
        baseline_dir=None,
    )
    second, second_runs, second_baseline = scan_v_dynamics(
        days=60,
        particles=220,
        seeds=(1234,),
        shapes=("ramp", "step"),
        baseline_dir=None,
    )
    assert first_baseline == second_baseline == []
    assert len(first) == len(CANDIDATES)
    assert len(first_runs) == 2 * len(CANDIDATES)
    assert first == second
    assert first_runs == second_runs
    for row in first:
        assert np.isfinite(float(row["stress_RMSE_mean"]))
        assert np.isfinite(float(row["stress_amplitude_ratio_mean"]))
