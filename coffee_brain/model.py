from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

import numpy as np


# One source of truth for the estimator's default five-mode transition table.
# Synthetic scenarios may copy and perturb it, but the core does not read scenario
# definitions back in. Synthetic World != Estimator Assumptions. 🎲☕
DEFAULT_MODE_TRANSITION = np.array(
    [
        [0.78, 0.12, 0.03, 0.04, 0.03],
        [0.35, 0.45, 0.08, 0.02, 0.10],
        [0.10, 0.03, 0.65, 0.01, 0.21],
        [0.55, 0.10, 0.02, 0.25, 0.08],
        [0.65, 0.08, 0.02, 0.03, 0.22],
    ],
    dtype=float,
)
DEFAULT_MODE_TRANSITION.setflags(write=False)


class RoutineMode(IntEnum):
    NORMAL = 0
    BUSY = 1
    LEAVE = 2
    SPECIAL = 3
    RECOVERY = 4


MODE_NAMES = {
    RoutineMode.NORMAL: "Normal",
    RoutineMode.BUSY: "Busy",
    RoutineMode.LEAVE: "Leave",
    RoutineMode.SPECIAL: "Special",
    RoutineMode.RECOVERY: "Recovery",
}

MODE_LABELS = tuple(MODE_NAMES[mode] for mode in RoutineMode)


@dataclass(frozen=True)
class RoutineState:
    """Six soft states used by the coffee routine model. ☕"""

    predictability: float
    mutuality: float
    voluntariness: float
    shared_context: float
    state_sharing: float
    friction: float

    def as_array(self) -> np.ndarray:
        return np.array(
            [
                self.predictability,
                self.mutuality,
                self.voluntariness,
                self.shared_context,
                self.state_sharing,
                self.friction,
            ],
            dtype=float,
        )


STATE_NAMES = (
    "predictability",
    "mutuality",
    "voluntariness",
    "shared_context",
    "state_sharing",
    "friction",
)


def relationship_index(x: np.ndarray) -> np.ndarray:
    """A tiny synthetic summary metric used only for demo evaluation.

    This is not a validated psychological scale.
    """

    x = np.asarray(x, dtype=float)
    p, m, v, c, e, f = np.moveaxis(x, -1, 0)
    return 0.18 * p + 0.25 * m + 0.20 * v + 0.16 * c + 0.11 * e + 0.10 * (1.0 - f)


def clip_state(x: np.ndarray) -> np.ndarray:
    """Keep soft states away from exact 0/1 extremes, which are not literal truths. 🌿"""

    return np.clip(np.asarray(x, dtype=float), 0.01, 0.99)
