from __future__ import annotations

from dataclasses import dataclass

import numpy as np


BASE_TRANSITION = np.array(
    [
        [0.78, 0.12, 0.03, 0.04, 0.03],
        [0.35, 0.45, 0.08, 0.02, 0.10],
        [0.10, 0.03, 0.65, 0.01, 0.21],
        [0.55, 0.10, 0.02, 0.25, 0.08],
        [0.65, 0.08, 0.02, 0.03, 0.22],
    ],
    dtype=float,
)

BASE_TARGET = np.array([0.80, 0.72, 0.90, 0.76, 0.42, 0.10], dtype=float)

BASE_MODE_EFFECTS = np.array(
    [
        [0.000, 0.000, 0.000, 0.000, 0.000, 0.000],  # Normal ☕
        [-0.005, -0.008, 0.000, -0.002, -0.002, 0.008],  # Busy 🌧️
        [-0.008, -0.010, 0.000, -0.005, -0.005, 0.005],  # Leave 💤
        [0.010, 0.012, 0.005, 0.015, 0.020, -0.004],  # Special 🎂
        [0.006, 0.006, 0.003, 0.008, 0.005, -0.005],  # Recovery 🌱
    ],
    dtype=float,
)

BASE_PROCESS_NOISE = np.array([0.012, 0.014, 0.009, 0.012, 0.018, 0.009], dtype=float)


@dataclass(frozen=True)
class CoffeeScenario:
    """One tiny synthetic coffee world with its own weather. 🌦️☕"""

    slug: str
    emoji: str
    title: str
    description: str
    transition: np.ndarray
    target: np.ndarray
    mode_effects: np.ndarray
    process_noise: np.ndarray
    mean_reversion: float = 0.035
    invite_probability: float = 0.92
    logit_noise_sigma: float = 0.0
    warmth_bias: float = 0.0
    warmth_sigma: float = 0.07
    delay_multiplier: float = 1.0
    delay_sigma: float = 0.45
    opt_in_bias: float = 0.0
    text_reply_bias: float = 0.0
    reaction_bias: float = 0.0
    state_share_bias: float = 0.0
    proactive_update_bias: float = 0.0
    maintenance_bias: float = 0.0
    pass_bias: float = 0.0
    resume_bias: float = 0.0

    def validate(self) -> None:
        """Make sure this tiny universe does not have broken probability gravity. 🪐🐾"""

        if self.transition.shape != (5, 5):
            raise ValueError(f"🐾 {self.slug}: transition matrix must be 5x5")
        if not np.allclose(self.transition.sum(axis=1), 1.0):
            raise ValueError(f"🐾 {self.slug}: every transition row must sum to 1")
        if self.target.shape != (6,):
            raise ValueError(f"🐾 {self.slug}: target must contain six soft states")
        if self.mode_effects.shape != (5, 6):
            raise ValueError(f"🐾 {self.slug}: mode effects must be 5x6")
        if self.process_noise.shape != (6,):
            raise ValueError(f"🐾 {self.slug}: process noise must contain six values")
        if not 0.0 <= self.invite_probability <= 1.0:
            raise ValueError(f"🐾 {self.slug}: invite probability must live between 0 and 1")


def _scenario(
    *,
    slug: str,
    emoji: str,
    title: str,
    description: str,
    transition: np.ndarray = BASE_TRANSITION,
    target: np.ndarray = BASE_TARGET,
    mode_effects: np.ndarray = BASE_MODE_EFFECTS,
    process_noise: np.ndarray = BASE_PROCESS_NOISE,
    **kwargs,
) -> CoffeeScenario:
    tiny_world = CoffeeScenario(
        slug=slug,
        emoji=emoji,
        title=title,
        description=description,
        transition=np.array(transition, dtype=float, copy=True),
        target=np.array(target, dtype=float, copy=True),
        mode_effects=np.array(mode_effects, dtype=float, copy=True),
        process_noise=np.array(process_noise, dtype=float, copy=True),
        **kwargs,
    )
    tiny_world.validate()
    return tiny_world


SCENARIOS = {
    "cozy-normal-year": _scenario(
        slug="cozy-normal-year",
        emoji="🌤️☕",
        title="Cozy Normal Year",
        description="The familiar little baseline world. Mostly steady, occasionally interrupted.",
    ),
    "super-busy-month": _scenario(
        slug="super-busy-month",
        emoji="🌧️☕",
        title="Super Busy Month",
        description="Busy mode arrives more often and tends to hang around for a while.",
        transition=np.array(
            [
                [0.62, 0.27, 0.03, 0.04, 0.04],
                [0.22, 0.62, 0.06, 0.02, 0.08],
                [0.10, 0.05, 0.62, 0.01, 0.22],
                [0.50, 0.18, 0.02, 0.22, 0.08],
                [0.52, 0.20, 0.03, 0.03, 0.22],
            ]
        ),
        target=np.array([0.76, 0.69, 0.90, 0.74, 0.40, 0.14]),
        process_noise=np.array([0.014, 0.017, 0.009, 0.013, 0.019, 0.011]),
        text_reply_bias=-0.12,
        delay_multiplier=1.25,
    ),
    "long-leave-and-return": _scenario(
        slug="long-leave-and-return",
        emoji="🏖️🌱",
        title="Long Leave and Return",
        description="Leave mode can persist, then the little routine has to find its way back.",
        transition=np.array(
            [
                [0.76, 0.10, 0.07, 0.03, 0.04],
                [0.28, 0.38, 0.18, 0.02, 0.14],
                [0.04, 0.01, 0.82, 0.01, 0.12],
                [0.50, 0.08, 0.08, 0.25, 0.09],
                [0.55, 0.05, 0.03, 0.02, 0.35],
            ]
        ),
        resume_bias=0.20,
        maintenance_bias=-0.05,
    ),
    "sleepy-reply-season": _scenario(
        slug="sleepy-reply-season",
        emoji="💤☕",
        title="Sleepy Reply Season",
        description="The routine is still alive, but replies wander in more slowly and quietly.",
        delay_multiplier=1.80,
        delay_sigma=0.62,
        text_reply_bias=-0.20,
        reaction_bias=-0.10,
        invite_probability=0.90,
    ),
    "special-day-sparkle": _scenario(
        slug="special-day-sparkle",
        emoji="🎂✨",
        title="Special Day Sparkle",
        description="Special mode appears more often and adds a little extra sparkle to the observations.",
        transition=np.array(
            [
                [0.73, 0.10, 0.02, 0.10, 0.05],
                [0.33, 0.42, 0.06, 0.08, 0.11],
                [0.10, 0.03, 0.62, 0.05, 0.20],
                [0.45, 0.08, 0.02, 0.38, 0.07],
                [0.60, 0.06, 0.02, 0.08, 0.24],
            ]
        ),
        warmth_bias=0.05,
        reaction_bias=0.18,
        state_share_bias=0.16,
        proactive_update_bias=0.12,
    ),
    "noisy-chaos-week": _scenario(
        slug="noisy-chaos-week",
        emoji="🌪️🐣",
        title="Noisy Chaos Week",
        description="The world gets wiggly: states move more and observations become much noisier.",
        transition=np.array(
            [
                [0.58, 0.18, 0.06, 0.10, 0.08],
                [0.28, 0.38, 0.10, 0.08, 0.16],
                [0.12, 0.08, 0.52, 0.06, 0.22],
                [0.36, 0.14, 0.06, 0.30, 0.14],
                [0.44, 0.14, 0.06, 0.08, 0.28],
            ]
        ),
        process_noise=np.array([0.024, 0.027, 0.017, 0.024, 0.032, 0.018]),
        logit_noise_sigma=0.42,
        warmth_sigma=0.13,
        delay_sigma=0.80,
        invite_probability=0.88,
    ),
    "slow-recovery": _scenario(
        slug="slow-recovery",
        emoji="🌱🐌",
        title="Slow Recovery",
        description="Recovery is real, just not in a hurry. Tiny steps still count. XD",
        transition=np.array(
            [
                [0.75, 0.12, 0.04, 0.03, 0.06],
                [0.27, 0.42, 0.08, 0.02, 0.21],
                [0.08, 0.02, 0.64, 0.01, 0.25],
                [0.50, 0.10, 0.02, 0.25, 0.13],
                [0.27, 0.08, 0.03, 0.04, 0.58],
            ]
        ),
        mode_effects=np.array(
            [
                [0.000, 0.000, 0.000, 0.000, 0.000, 0.000],
                [-0.005, -0.008, 0.000, -0.002, -0.002, 0.008],
                [-0.008, -0.010, 0.000, -0.005, -0.005, 0.005],
                [0.010, 0.012, 0.005, 0.015, 0.020, -0.004],
                [0.0025, 0.0025, 0.0015, 0.0035, 0.0020, -0.0020],
            ]
        ),
        mean_reversion=0.022,
        resume_bias=-0.30,
    ),
}


DEFAULT_SCENARIO = "cozy-normal-year"


def scenario_names() -> tuple[str, ...]:
    """Return every little weather option in stable CLI order. ☕🌦️"""

    return tuple(SCENARIOS.keys())


def get_scenario(name: str) -> CoffeeScenario:
    """Pick one tiny coffee universe by name. 🧺✨"""

    try:
        return SCENARIOS[name]
    except KeyError as exc:
        choices = ", ".join(scenario_names())
        raise ValueError(f"🐾 Unknown coffee weather '{name}'. Try one of: {choices}") from exc
