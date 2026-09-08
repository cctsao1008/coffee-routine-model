import numpy as np

from particles import CoffeeParticleFilter


def cozy_observation(**overrides):
    obs = {
        "cheng_invite": 1,
        "linda_opt_in": 1,
        "text_reply": 1,
        "reaction": 1,
        "state_share": 0,
        "proactive_update": 0,
        "routine_maintenance": 1,
        "pass_event": 0,
        "resume_signal": 0,
        "tone_warmth": 0.55,
        "response_delay_min": 18.0,
    }
    obs.update(overrides)
    return obs


def test_posterior_probability_cup_is_filled_to_one():
    pf = CoffeeParticleFilter(particle_count=400, seed=1234)

    posterior = pf.update(cozy_observation())

    assert np.isclose(posterior.mode_probabilities.sum(), 1.0)
    assert np.all(posterior.mode_probabilities >= 0.0)


def test_tiny_intervals_keep_their_left_and_right_socks_on():
    pf = CoffeeParticleFilter(particle_count=400, seed=1234)

    posterior = pf.update(cozy_observation())

    assert np.all(posterior.ci95_low <= posterior.ci95_high)
    assert np.all(posterior.ci95_low >= 0.01)
    assert np.all(posterior.ci95_high <= 0.99)


def test_ess_stays_finite_positive_and_inside_the_flock():
    particle_count = 500
    pf = CoffeeParticleFilter(particle_count=particle_count, seed=4321)

    posterior = pf.update(cozy_observation())

    assert np.isfinite(posterior.ess)
    assert 0.0 < posterior.ess <= particle_count


def test_resampling_never_loses_any_tiny_particle_friends():
    particle_count = 350
    pf = CoffeeParticleFilter(particle_count=particle_count, seed=99)

    for i in range(12):
        obs = cozy_observation(
            linda_opt_in=i % 2,
            pass_event=(i + 1) % 2,
            reaction=i % 2,
            response_delay_min=5.0 + i * 20.0,
        )
        pf.update(obs)

        assert pf.particles.shape == (particle_count, 6)
        assert pf.modes.shape == (particle_count,)
        assert pf.weights.shape == (particle_count,)
        assert np.isclose(pf.weights.sum(), 1.0)


def test_same_seed_gives_the_same_tiny_guess_parade():
    first = CoffeeParticleFilter(particle_count=300, seed=2026)
    second = CoffeeParticleFilter(particle_count=300, seed=2026)
    observations = [
        cozy_observation(),
        cozy_observation(text_reply=0, reaction=0, response_delay_min=75.0),
        cozy_observation(pass_event=1, linda_opt_in=0, routine_maintenance=0),
        cozy_observation(resume_signal=1, response_delay_min=12.0),
    ]

    for obs in observations:
        a = first.update(obs)
        b = second.update(obs)

        assert np.allclose(a.mean, b.mean)
        assert np.allclose(a.ci95_low, b.ci95_low)
        assert np.allclose(a.ci95_high, b.ci95_high)
        assert np.allclose(a.mode_probabilities, b.mode_probabilities)
        assert np.isclose(a.ess, b.ess)


def test_everyday_pass_and_resume_clues_do_not_make_the_nest_explode():
    pf = CoffeeParticleFilter(particle_count=300, seed=7)
    observations = [
        cozy_observation(pass_event=1, linda_opt_in=0, routine_maintenance=0),
        cozy_observation(cheng_invite=0, linda_opt_in=0, text_reply=0, reaction=0),
        cozy_observation(resume_signal=1, routine_maintenance=1, response_delay_min=10.0),
    ]

    for obs in observations:
        posterior = pf.update(obs)
        assert np.all(np.isfinite(posterior.mean))
        assert np.all((posterior.mean >= 0.01) & (posterior.mean <= 0.99))
