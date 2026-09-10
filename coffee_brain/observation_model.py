from __future__ import annotations

from dataclasses import asdict, dataclass, replace

import numpy as np


# Canonical coefficient order used by every observation recipe below.
# x = [P, M, V, C, E, F] = predictability, mutuality, voluntariness,
# shared context, everyday state sharing, and friction. Keeping this order visible
# matters because the tuples below are mathematical model parameters, not labels.
STATE_ORDER = ("P", "M", "V", "C", "E", "F")
BINARY_CHANNEL_NAMES = (
    "opt_in",
    "text_reply",
    "reaction",
    "state_share",
    "proactive_update",
    "routine_maintenance",
    "pass_event",
    "resume_signal",
)


def _sigmoid(x: np.ndarray) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-x))


def _as_state_matrix(states: np.ndarray) -> np.ndarray:
    tiny_states = np.asarray(states, dtype=float)
    if tiny_states.ndim == 1:
        tiny_states = tiny_states[None, :]
    if tiny_states.ndim != 2 or tiny_states.shape[1] != 6:
        raise ValueError("🐾 Tiny observation states must have shape (n, 6).")
    return tiny_states


def _as_modes(modes: np.ndarray | int, n: int) -> np.ndarray:
    tiny_modes = np.asarray(modes, dtype=int)
    if tiny_modes.ndim == 0:
        tiny_modes = np.full(n, int(tiny_modes), dtype=int)
    tiny_modes = tiny_modes.reshape(-1)
    if len(tiny_modes) != n:
        raise ValueError("🐾 Tiny mode basket must have one mode per state.")
    if np.any((tiny_modes < 0) | (tiny_modes > 4)):
        raise ValueError("🐾 Tiny modes must live between 0 and 4.")
    return tiny_modes


@dataclass(frozen=True)
class BinaryChannelConfig:
    """One inspectable Bernoulli clue recipe. 🎛️🐣

    For state vector ``x`` and discrete routine mode ``z``:

        logit P(y=1 | x, z) = intercept + beta^T x + mode_offset[z]

    ``beta`` follows STATE_ORDER. Positive coefficients raise the model probability
    of observing the clue; negative coefficients lower it. These coefficients encode
    a structural prototype, not a discovered law of human behavior.
    """

    intercept: float
    state_coefficients: tuple[float, float, float, float, float, float]
    mode_offsets: tuple[float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0)

    def __post_init__(self) -> None:
        if len(self.state_coefficients) != 6:
            raise ValueError("🐾 A binary clue needs six state coefficients.")
        if len(self.mode_offsets) != 5:
            raise ValueError("🐾 A binary clue needs five mode offsets.")

    def logits(self, states: np.ndarray, modes: np.ndarray | int) -> np.ndarray:
        tiny_states = _as_state_matrix(states)
        tiny_modes = _as_modes(modes, len(tiny_states))
        beta = np.asarray(self.state_coefficients, dtype=float)
        offsets = np.asarray(self.mode_offsets, dtype=float)
        return float(self.intercept) + tiny_states @ beta + offsets[tiny_modes]

    def probabilities(self, states: np.ndarray, modes: np.ndarray | int) -> np.ndarray:
        # Logistic link maps an unconstrained score back into a Bernoulli probability.
        return _sigmoid(self.logits(states, modes))


@dataclass(frozen=True)
class WarmthChannelConfig:
    """A small Gaussian recipe for observable tone warmth. 🌤️☕

    The conditional mean uses the same linear predictor shape as the binary channels:

        E[warmth | x, z] = intercept + beta^T x + mode_offset[z]

    ``sigma`` is the shared observation-noise scale around that mean.
    """

    intercept: float
    state_coefficients: tuple[float, float, float, float, float, float]
    mode_offsets: tuple[float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0)
    sigma: float = 0.07

    def __post_init__(self) -> None:
        if len(self.state_coefficients) != 6 or len(self.mode_offsets) != 5:
            raise ValueError("🐾 Warmth needs six state coefficients and five mode offsets.")
        if self.sigma <= 0.0:
            raise ValueError("🐾 Warmth sigma must be positive.")

    def mean(self, states: np.ndarray, modes: np.ndarray | int) -> np.ndarray:
        tiny_states = _as_state_matrix(states)
        tiny_modes = _as_modes(modes, len(tiny_states))
        beta = np.asarray(self.state_coefficients, dtype=float)
        offsets = np.asarray(self.mode_offsets, dtype=float)
        return float(self.intercept) + tiny_states @ beta + offsets[tiny_modes]


@dataclass(frozen=True)
class DelayChannelConfig:
    """A log-normal reply-delay recipe kept in one tiny measuring cup. ⏰☕

    Mean delay is modeled in minutes before taking the logarithm used by the
    log-normal observation likelihood. Lower P/M create larger modeled delay gaps,
    while the discrete mode can add its own delay penalty.
    """

    base_minutes: float = 8.0
    predictability_gap_minutes: float = 45.0
    mutuality_gap_minutes: float = 30.0
    mode_add_minutes: tuple[float, float, float, float, float] = (0.0, 75.0, 110.0, 0.0, 0.0)
    sigma_log: float = 0.45
    minimum_mean_minutes: float = 1.0

    def __post_init__(self) -> None:
        if len(self.mode_add_minutes) != 5:
            raise ValueError("🐾 Reply delay needs five mode additions.")
        if self.sigma_log <= 0.0 or self.minimum_mean_minutes <= 0.0:
            raise ValueError("🐾 Reply-delay scale values must be positive.")

    def mean_minutes(self, states: np.ndarray, modes: np.ndarray | int) -> np.ndarray:
        tiny_states = _as_state_matrix(states)
        tiny_modes = _as_modes(modes, len(tiny_states))
        p = tiny_states[:, 0]
        m = tiny_states[:, 1]
        mode_add = np.asarray(self.mode_add_minutes, dtype=float)[tiny_modes]
        # mu_delay = base + a_P(1-P) + a_M(1-M) + mode_delay[z].
        # The gaps vanish as P/M approach 1 and grow as they approach 0.
        mean = (
            float(self.base_minutes)
            + float(self.predictability_gap_minutes) * (1.0 - p)
            + float(self.mutuality_gap_minutes) * (1.0 - m)
            + mode_add
        )
        return np.maximum(float(self.minimum_mean_minutes), mean)

    def log_mean(self, states: np.ndarray, modes: np.ndarray | int) -> np.ndarray:
        return np.log(self.mean_minutes(states, modes))


@dataclass(frozen=True)
class ObservationModelConfig:
    """Every hand-set observation knob, gathered into one visible little tray. 🎛️☕"""

    opt_in: BinaryChannelConfig
    text_reply: BinaryChannelConfig
    reaction: BinaryChannelConfig
    state_share: BinaryChannelConfig
    proactive_update: BinaryChannelConfig
    routine_maintenance: BinaryChannelConfig
    pass_event: BinaryChannelConfig
    resume_signal: BinaryChannelConfig
    tone_warmth: WarmthChannelConfig
    response_delay: DelayChannelConfig
    provenance: str = "hand-set structural baseline; not learned from real humans"

    def binary_channels(self) -> dict[str, BinaryChannelConfig]:
        return {name: getattr(self, name) for name in BINARY_CHANNEL_NAMES}

    def with_binary_channel(self, name: str, **changes: float) -> "ObservationModelConfig":
        """Return a new config with one clue recipe changed: a tiny optimizer hook. 🐣🔧"""

        if name not in BINARY_CHANNEL_NAMES:
            raise ValueError(f"🙈 Unknown tiny observation channel '{name}'.")
        updated = replace(getattr(self, name), **changes)
        return replace(self, **{name: updated})

    def to_dict(self) -> dict:
        return asdict(self)


# Default observation recipes are intentionally inspectable structural assumptions.
# They express how the synthetic estimator is wired, not psychological facts about a
# particular person. Mode offsets always follow NORMAL / BUSY / LEAVE / SPECIAL / RECOVERY.
DEFAULT_OBSERVATION_MODEL = ObservationModelConfig(
    # Opt-in: modeled mainly as a function of M/V, with friction suppressing it;
    # BUSY and especially LEAVE reduce the observation probability.
    opt_in=BinaryChannelConfig(
        intercept=-1.2,
        state_coefficients=(0.8, 1.7, 1.2, 0.0, 0.0, -1.8),
        mode_offsets=(0.0, -0.7, -2.5, 0.2, 0.15),
    ),
    # Text reply: modeled as more likely with M/C/E and less likely with friction.
    text_reply=BinaryChannelConfig(
        intercept=-0.7,
        state_coefficients=(0.0, 1.1, 0.0, 0.6, 0.3, -0.8),
        mode_offsets=(0.0, -0.2, 0.0, 0.2, 0.0),
    ),
    # Reaction: a lightweight acknowledgment clue influenced by P/M/V and friction.
    reaction=BinaryChannelConfig(
        intercept=-0.6,
        state_coefficients=(0.5, 0.9, 0.4, 0.0, 0.0, -0.5),
    ),
    # State sharing: E is the dominant structural driver, with C carrying secondary
    # context. This is an observable-sharing channel, not direct access to inner state.
    state_share=BinaryChannelConfig(
        intercept=-2.2,
        state_coefficients=(0.0, 0.3, 0.0, 0.8, 2.0, 0.0),
        mode_offsets=(0.0, -0.3, 0.0, 0.0, 0.0),
    ),
    # Proactive update: modeled around mutuality/context/state-sharing, while friction
    # lowers the chance of observing an unsolicited coordination update.
    proactive_update=BinaryChannelConfig(
        intercept=-1.8,
        state_coefficients=(0.0, 1.3, 0.0, 0.8, 0.5, -0.6),
        mode_offsets=(0.0, 0.45, 0.45, 0.0, 0.0),
    ),
    # Routine maintenance: a broad continuity clue; P/M/V/C support it and F opposes it.
    # LEAVE reduces maintenance while RECOVERY raises it relative to the baseline mode.
    routine_maintenance=BinaryChannelConfig(
        intercept=-1.1,
        state_coefficients=(1.5, 1.4, 0.9, 0.7, 0.0, -1.4),
        mode_offsets=(0.0, -0.3, -1.4, 0.3, 0.6),
    ),
    # Voluntary pass: not treated as failure. In this structural recipe it becomes more
    # observable under friction / BUSY / LEAVE and less observable with higher M.
    pass_event=BinaryChannelConfig(
        intercept=-2.5,
        state_coefficients=(0.0, -1.0, 0.0, 0.0, 0.0, 1.0),
        mode_offsets=(-0.5, 1.2, 2.7, -0.5, -1.0),
    ),
    # Resume signal: modeled as evidence associated mainly with P/M plus a strong
    # RECOVERY-mode offset; it is intentionally uncommon in ordinary modes.
    resume_signal=BinaryChannelConfig(
        intercept=-3.0,
        state_coefficients=(1.0, 0.6, 0.0, 0.0, 0.0, 0.0),
        mode_offsets=(-0.8, -0.5, -1.0, 0.0, 2.8),
    ),
    # Tone warmth is continuous rather than Bernoulli. Its conditional mean is a
    # bounded-world modeling convenience driven mostly by M/V/C/E and reduced by F.
    tone_warmth=WarmthChannelConfig(
        intercept=0.15,
        state_coefficients=(0.0, 0.28, 0.18, 0.16, 0.12, -0.20),
        sigma=0.07,
    ),
    response_delay=DelayChannelConfig(),
)


def predict_binary_channels(
    states: np.ndarray,
    modes: np.ndarray | int,
    config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL,
) -> dict[str, np.ndarray]:
    """Predict every binary clue probability without hiding any magic seasoning. ☕🎛️"""

    return {
        name: channel.probabilities(states, modes)
        for name, channel in config.binary_channels().items()
    }


def predict_warmth_mean(
    states: np.ndarray,
    modes: np.ndarray | int,
    config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL,
) -> np.ndarray:
    return config.tone_warmth.mean(states, modes)


def predict_delay_log_mean(
    states: np.ndarray,
    modes: np.ndarray | int,
    config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL,
) -> np.ndarray:
    return config.response_delay.log_mean(states, modes)
