from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .actions import RoutineActions, action_effect
from .model import MODE_NAMES, RoutineMode, clip_state


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _bern_loglik(y: int, p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 1e-6, 1.0 - 1e-6)
    return y * np.log(p) + (1 - y) * np.log(1 - p)


def _little_clue(obs: dict, key: str, legacy_key: str | None = None):
    """Fetch one observable clue, while politely supporting old baskets. 🧺"""

    value = obs.get(key)
    if value is None and legacy_key is not None:
        value = obs.get(legacy_key)
    return value


@dataclass
class Posterior:
    mean: np.ndarray
    ci95_low: np.ndarray
    ci95_high: np.ndarray
    mode_probabilities: np.ndarray
    ess: float

    @property
    def mode(self) -> str:
        return MODE_NAMES[RoutineMode(int(np.argmax(self.mode_probabilities)))]


@dataclass(frozen=True)
class ParticleHistoryStep:
    """One compact filtered particle cloud plus its tiny family tree. 🔭🐣"""

    particles: np.ndarray
    modes: np.ndarray
    weights: np.ndarray
    parents: np.ndarray | None


class CoffeeParticleFilter:
    """A small Sequential Monte Carlo estimator with many tiny guesses. 🐣"""

    transition = np.array(
        [
            [0.78, 0.12, 0.03, 0.04, 0.03],
            [0.35, 0.45, 0.08, 0.02, 0.10],
            [0.10, 0.03, 0.65, 0.01, 0.21],
            [0.55, 0.10, 0.02, 0.25, 0.08],
            [0.65, 0.08, 0.02, 0.03, 0.22],
        ],
        dtype=float,
    )

    target = np.array([0.80, 0.72, 0.90, 0.76, 0.42, 0.10], dtype=float)

    def __init__(
        self,
        particle_count: int = 6000,
        seed: int = 20260908,
        *,
        record_history: bool = False,
    ):
        self.rng = np.random.default_rng(seed)
        self.n = particle_count
        self.particles = np.tile(
            np.array([0.68, 0.58, 0.80, 0.58, 0.28, 0.22]),
            (self.n, 1),
        )
        self.particles += self.rng.normal(
            0.0,
            [0.12, 0.12, 0.09, 0.12, 0.12, 0.08],
            size=(self.n, 6),
        )
        self.particles = clip_state(self.particles)
        self.modes = np.zeros(self.n, dtype=int)
        self.weights = np.ones(self.n, dtype=float) / self.n
        self.started = False

        self.record_history = bool(record_history)
        self.history: list[ParticleHistoryStep] = []
        self._next_parent_map: np.ndarray | None = None

    def _predict(
        self,
        actions: RoutineActions | Mapping[str, float] | None = None,
    ) -> None:
        """Move the tiny hidden world one step, optionally nudged by observable actions. 🎮🌱"""

        u = self.rng.random(self.n)
        new_modes = np.empty(self.n, dtype=int)

        for mode in range(5):
            idx = np.where(self.modes == mode)[0]
            if len(idx):
                new_modes[idx] = np.searchsorted(np.cumsum(self.transition[mode]), u[idx])

        self.modes = new_modes
        mean_reversion = 0.035 * (self.target - self.particles)
        mode_effect = np.zeros_like(self.particles)

        mode_effect[self.modes == RoutineMode.BUSY] = [-0.005, -0.008, 0.000, -0.002, -0.002, 0.008]
        mode_effect[self.modes == RoutineMode.LEAVE] = [-0.008, -0.010, 0.000, -0.005, -0.005, 0.005]
        mode_effect[self.modes == RoutineMode.SPECIAL] = [0.010, 0.012, 0.005, 0.015, 0.020, -0.004]
        mode_effect[self.modes == RoutineMode.RECOVERY] = [0.006, 0.006, 0.003, 0.008, 0.005, -0.005]

        controlled_effect = action_effect(actions)

        self.particles = clip_state(
            self.particles
            + mean_reversion
            + mode_effect
            + controlled_effect
            + self.rng.normal(
                0.0,
                [0.015, 0.017, 0.011, 0.015, 0.021, 0.011],
                size=(self.n, 6),
            )
        )

    def _remember_filtered_cloud(self, w: np.ndarray) -> None:
        """Save only what the smoother needs, and only when invited. 🧺🔭"""

        if not self.record_history:
            return

        parents = None
        if self.history:
            if self._next_parent_map is None:
                raise RuntimeError("🐣 Tiny ancestry map wandered off before smoothing.")
            parents = self._next_parent_map.astype(np.int32, copy=True)

        self.history.append(
            ParticleHistoryStep(
                particles=self.particles.astype(np.float32, copy=True),
                modes=self.modes.astype(np.int8, copy=True),
                weights=w.astype(np.float32, copy=True),
                parents=parents,
            )
        )

    def update(
        self,
        obs: dict,
        actions: RoutineActions | Mapping[str, float] | None = None,
    ) -> Posterior:
        """Update from present clues and optional actions from the preceding transition. 🌱

        ``actions`` are treated as known controls that moved the routine from the
        previous step toward the current observation. On the very first update there
        is no previous transition, so the action basket patiently waits outside. ☕🎮
        """

        if self.started:
            self._predict(actions)
        self.started = True

        invite = _little_clue(obs, "invite", "cheng_invite")
        opt_in = _little_clue(obs, "opt_in", "linda_opt_in")
        text_reply = _little_clue(obs, "text_reply")
        reaction = _little_clue(obs, "reaction")
        state_share = _little_clue(obs, "state_share")
        proactive_update = _little_clue(obs, "proactive_update")
        routine_maintenance = _little_clue(obs, "routine_maintenance")
        pass_event = _little_clue(obs, "pass_event")
        resume_signal = _little_clue(obs, "resume_signal")
        tone_warmth = _little_clue(obs, "tone_warmth")
        response_delay_min = _little_clue(obs, "response_delay_min")

        p, m, v, c, e, f = self.particles.T
        mo = self.modes

        mode_opt = np.select(
            [mo == 1, mo == 2, mo == 3, mo == 4],
            [-0.7, -2.5, 0.2, 0.15],
            default=0.0,
        )
        prob_opt = _sigmoid(-1.2 + 1.7*m + 1.2*v + 0.8*p - 1.8*f + mode_opt)
        prob_text = _sigmoid(-0.7 + 1.1*m + 0.6*c + 0.3*e - 0.8*f + 0.2*(mo == 3) - 0.2*(mo == 1))
        prob_reaction = _sigmoid(-0.6 + 0.9*m + 0.5*p + 0.4*v - 0.5*f)
        prob_share = _sigmoid(-2.2 + 2.0*e + 0.8*c + 0.3*m - 0.3*(mo == 1))
        prob_update = _sigmoid(-1.8 + 1.3*m + 0.8*c + 0.5*e - 0.6*f + 0.45*((mo == 1) | (mo == 2)))

        mode_maint = np.select([mo == 1, mo == 2, mo == 3, mo == 4], [-0.3, -1.4, 0.3, 0.6], default=0.0)
        prob_maint = _sigmoid(-1.1 + 1.5*p + 1.4*m + 0.9*v + 0.7*c - 1.4*f + mode_maint)

        mode_pass = np.select([mo == 1, mo == 2, mo == 3, mo == 4], [1.2, 2.7, -0.5, -1.0], default=-0.5)
        prob_pass = _sigmoid(-2.5 - 1.0*m + 1.0*f + mode_pass)

        mode_resume = np.select([mo == 1, mo == 2, mo == 3, mo == 4], [-0.5, -1.0, 0.0, 2.8], default=-0.8)
        prob_resume = _sigmoid(-3.0 + 1.0*p + 0.6*m + mode_resume)

        ll = np.zeros(self.n)

        response_opportunity = invite is None or int(invite) == 1
        if response_opportunity and opt_in is not None:
            ll += _bern_loglik(int(opt_in), prob_opt)
        if response_opportunity and pass_event is not None:
            ll += _bern_loglik(int(pass_event), prob_pass)

        if text_reply is not None:
            ll += _bern_loglik(int(text_reply), prob_text)
        if reaction is not None:
            ll += _bern_loglik(int(reaction), prob_reaction)
        if state_share is not None:
            ll += _bern_loglik(int(state_share), prob_share)
        if proactive_update is not None:
            ll += _bern_loglik(int(proactive_update), prob_update)
        if routine_maintenance is not None:
            ll += _bern_loglik(int(routine_maintenance), prob_maint)
        if resume_signal is not None:
            ll += _bern_loglik(int(resume_signal), prob_resume)

        if tone_warmth is not None:
            mu_warmth = 0.15 + 0.28*m + 0.18*v + 0.16*c + 0.12*e - 0.20*f
            sigma_warmth = 0.07
            ll += -0.5*((float(tone_warmth) - mu_warmth)/sigma_warmth)**2

        if response_delay_min is not None:
            mu_delay = np.log(np.maximum(1.0, 8 + 45*(1-p) + 30*(1-m) + 75*(mo == 1) + 110*(mo == 2)))
            log_delay = math.log(max(float(response_delay_min), 0.2))
            sigma_delay = 0.45
            ll += -0.5*((log_delay - mu_delay)/sigma_delay)**2

        ll -= np.max(ll)
        w = np.exp(ll) * self.weights
        w /= np.sum(w)

        ess = 1.0 / np.sum(w*w)
        mean = np.sum(w[:, None] * self.particles, axis=0)

        low = np.zeros(6)
        high = np.zeros(6)
        for j in range(6):
            order = np.argsort(self.particles[:, j])
            cdf = np.cumsum(w[order])
            low[j] = self.particles[order[np.searchsorted(cdf, 0.025)], j]
            high[j] = self.particles[order[np.searchsorted(cdf, 0.975)], j]

        mode_probs = np.array([np.sum(w[self.modes == mode]) for mode in range(5)])

        self._remember_filtered_cloud(w)

        if ess < 0.55 * self.n:
            positions = (self.rng.random() + np.arange(self.n)) / self.n
            cdf = np.cumsum(w)
            idx = np.searchsorted(cdf, positions)
            self.particles = self.particles[idx]
            self.modes = self.modes[idx]
            self.weights = np.ones(self.n) / self.n
            self._next_parent_map = idx.astype(np.int32, copy=False)
        else:
            self.weights = w
            self._next_parent_map = np.arange(self.n, dtype=np.int32)

        return Posterior(mean=mean, ci95_low=low, ci95_high=high, mode_probabilities=mode_probs, ess=ess)
