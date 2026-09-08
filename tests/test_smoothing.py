import numpy as np

from coffee_brain.particles import CoffeeParticleFilter
from coffee_brain.smoothing import smooth_history


OBS = {
    "invite": 1,
    "opt_in": 1,
    "text_reply": 1,
    "reaction": 1,
    "state_share": 0,
    "proactive_update": 0,
    "routine_maintenance": 1,
    "pass_event": 0,
    "resume_signal": 0,
    "tone_warmth": 0.55,
    "response_delay_min": 12.0,
}


def _run(seed=7):
    pf = CoffeeParticleFilter(particle_count=180, seed=seed, record_history=True)
    filtered = []
    for day in range(12):
        obs = dict(OBS)
        if day == 5:
            obs.update(opt_in=0, pass_event=1, routine_maintenance=0, reaction=0)
        if day == 6:
            obs.update(resume_signal=1)
        filtered.append(pf.update(obs).mean)
    return pf, np.asarray(filtered)


def test_history_is_opt_in():
    pf = CoffeeParticleFilter(particle_count=120, seed=1)
    pf.update(OBS)
    assert pf.history == []


def test_recorded_history_keeps_valid_ancestry():
    pf, _ = _run()
    assert len(pf.history) == 12
    assert pf.history[0].parents is None
    for step in pf.history[1:]:
        assert step.parents is not None
        assert step.parents.shape == (180,)
        assert np.all(step.parents >= 0)
        assert np.all(step.parents < 180)


def test_zero_lag_matches_filtered_posterior_means():
    pf, filtered = _run()
    smoothed = smooth_history(pf.history, lag=0)
    hindsight = np.asarray([item.mean for item in smoothed])
    assert np.allclose(hindsight, filtered, atol=2e-6)


def test_fixed_lag_is_deterministic_and_keeps_bounds():
    pf_a, _ = _run(seed=11)
    pf_b, _ = _run(seed=11)
    a = smooth_history(pf_a.history, lag=4)
    b = smooth_history(pf_b.history, lag=4)
    means_a = np.asarray([item.mean for item in a])
    means_b = np.asarray([item.mean for item in b])
    assert np.allclose(means_a, means_b)
    assert np.all((means_a >= 0.01) & (means_a <= 0.99))
    assert all(item.endpoint >= index for index, item in enumerate(a))
    assert all(item.endpoint <= min(len(a) - 1, index + 4) for index, item in enumerate(a))


def test_full_history_uses_last_day_as_hindsight_endpoint():
    pf, _ = _run(seed=19)
    smoothed = smooth_history(pf.history, lag=1, full_history=True)
    assert all(item.endpoint == len(pf.history) - 1 for item in smoothed)
