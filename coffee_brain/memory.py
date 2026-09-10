from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .actions import RoutineActions


@dataclass(frozen=True)
class SharedContextMemoryConfig:
    """Slow little gravity for accumulated shared context. 🧠🌱"""

    accumulation_rate: float = 0.035
    decay_rate: float = 0.0015
    process_noise: float = 0.004
    minimum: float = 0.01
    maximum: float = 0.99

    def __post_init__(self) -> None:
        if not 0.0 <= self.accumulation_rate <= 1.0:
            raise ValueError("🌱 Memory accumulation rate must stay between 0 and 1.")
        if not 0.0 <= self.decay_rate <= 1.0:
            raise ValueError("🍂 Memory decay rate must stay between 0 and 1.")
        if self.process_noise < 0.0:
            raise ValueError("🐣 Memory process noise cannot be negative.")
        if not 0.0 <= self.minimum < self.maximum <= 1.0:
            raise ValueError("🧺 Memory bounds must fit inside the tiny unit cup.")


DEFAULT_SHARED_CONTEXT_MEMORY = SharedContextMemoryConfig()


def _basket(actions: RoutineActions | Mapping[str, float] | None) -> RoutineActions:
    return actions if isinstance(actions, RoutineActions) else RoutineActions.from_mapping(actions)


def shared_context_input(actions: RoutineActions | Mapping[str, float] | None) -> float:
    """Turn observable coordination actions into bounded memory-building input. 🧠☕

    The scalar input I[t] is a weighted mixture of explicit coordination actions plus
    two pairwise completion terms. Products such as invite*opt_in only contribute when
    both sides of that observable exchange are present.

    The weights are structural prototype assumptions, not learned human constants.
    A quiet day simply contributes zero input; it does not erase existing history.
    """

    a = _basket(actions)
    little_input = (
        0.45 * a.a_callback
        + 0.10 * a.a_notify
        + 0.10 * a.b_exception_sync
        + 0.10 * a.b_closure
        + 0.15 * a.a_invite * a.b_opt_in
        + 0.20 * a.a_deliver * a.b_acknowledge
    )
    return float(np.clip(little_input, 0.0, 1.0))


def shared_context_step(
    current: np.ndarray | float,
    memory_input: float,
    *,
    config: SharedContextMemoryConfig = DEFAULT_SHARED_CONTEXT_MEMORY,
    noise: np.ndarray | float = 0.0,
) -> np.ndarray:
    """Advance the Shared Context reservoir with accumulation, decay, and saturation. 🌱

    The update is:

        C[t+1] = C[t] + eta * I[t] * (1 - C[t]) - lambda * C[t] + epsilon[t]

    where ``eta`` is accumulation_rate, ``lambda`` is decay_rate, and ``I[t]`` is the
    bounded coordination input. The ``(1-C)`` factor creates saturation: equal positive
    input adds less when C is already high. The decay term is proportional to existing
    memory, so no-input days produce slow fading rather than an immediate reset.

    Ignoring noise and clipping, a constant input I has fixed point:

        C* = eta * I / (eta * I + lambda)

    which makes the long-run balance between accumulation and decay explicit.
    """

    c = np.asarray(current, dtype=float)
    strength = float(np.clip(memory_input, 0.0, 1.0))
    next_c = (
        c
        + config.accumulation_rate * strength * (1.0 - c)
        - config.decay_rate * c
        + np.asarray(noise, dtype=float)
    )
    return np.clip(next_c, config.minimum, config.maximum)
