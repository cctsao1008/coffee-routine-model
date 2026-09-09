import numpy as np

from tiny_tools.diagnose_v_compression import (
    likelihood_slice,
    run_compression_diagnostic,
)


def test_v_likelihood_slice_separates_low_and_high_clue_baskets():
    rows, summary = likelihood_slice(
        low_v=0.58,
        high_v=0.94,
        seed=20260908,
        samples_per_level=120,
        grid_points=61,
    )
    assert len(rows) == 61
    assert summary["high_peak_V"] > summary["low_peak_V"]
    assert summary["low_basket_preference_low_over_high"] > 0.0
    assert summary["high_basket_preference_high_over_low"] > 0.0


def test_v_compression_diagnostic_keeps_model_unchanged_and_returns_four_views():
    result = run_compression_diagnostic(
        days=60,
        particles=240,
        seed=20260908,
        low_v=0.58,
        high_v=0.94,
    )
    assert set(result["variants"]) == {
        "full-hidden-mode",
        "full-normal-locked",
        "v-only-default-prior",
        "v-only-relaxed-prior",
    }
    truth = result["truth"][:, 2]
    assert np.std(truth) > 0.10
    for _, _, _, metrics in result["variants"].values():
        assert np.isfinite(metrics["RMSE"])
        assert np.isfinite(metrics["MAE"])
        assert np.isfinite(metrics["amplitude_ratio"])
        assert 0.0 <= metrics["CI95_coverage"] <= 1.0


def test_relaxed_v_prior_is_only_a_diagnostic_comparator():
    result = run_compression_diagnostic(days=60, particles=240, seed=1234)
    default = result["variants"]["v-only-default-prior"][3]
    relaxed = result["variants"]["v-only-relaxed-prior"][3]
    assert default["truth_std"] == relaxed["truth_std"]
    assert default["estimate_std"] != relaxed["estimate_std"]
