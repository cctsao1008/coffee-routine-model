from __future__ import annotations

from dataclasses import dataclass, fields
from typing import Mapping

import numpy as np


ACTION_NAMES = (
    "a_invite",
    "a_deliver",
    "a_notify",
    "a_callback",
    "a_boundary_preserving",
    "b_opt_in",
    "b_pass_choice",
    "b_acknowledge",
    "b_exception_sync",
    "b_closure",
)

# Linear controlled-state contribution:
#
#     delta_action = a @ ACTION_EFFECTS
#
# where ``a`` follows ACTION_NAMES and the six output columns are P / M / V / C / E / F.
# Positive entries nudge a modeled state upward; negative entries nudge it downward.
# C stays zero here on purpose: Shared Context has its own slow memory law in memory.py.
# These are small structural prototype effects, not learned human coefficients. ☕🐾
ACTION_EFFECTS = np.array(
    [
        [0.0015, 0.0000, 0.0010, 0.0000, 0.0000, 0.0000],  # A invite
        [0.0060, 0.0040, 0.0000, 0.0000, 0.0000, -0.0030],  # A deliver
        [0.0040, 0.0010, 0.0010, 0.0000, 0.0000, -0.0040],  # A notify
        [0.0010, 0.0030, 0.0000, 0.0000, 0.0010, -0.0010],  # A callback
        [0.0000, 0.0010, 0.0060, 0.0000, 0.0000, -0.0050],  # A boundary preserving
        [0.0020, 0.0060, 0.0020, 0.0000, 0.0000, -0.0010],  # B opt in
        [0.0000, 0.0000, 0.0060, 0.0000, 0.0000, -0.0010],  # B voluntary pass
        [0.0010, 0.0050, 0.0000, 0.0000, 0.0000, -0.0020],  # B acknowledge
        [0.0030, 0.0030, 0.0040, 0.0000, 0.0000, -0.0060],  # B exception sync
        [0.0030, 0.0040, 0.0010, 0.0000, 0.0000, -0.0040],  # B closure
    ],
    dtype=float,
)


@dataclass(frozen=True)
class RoutineActions:
    """Observable routine actions that may gently move the next hidden state. ☕🎮

    Values are bounded intensities in [0, 1]. They are controls / observations supplied
    to the model, not inferred private motives. Prefixes ``a_`` and ``b_`` only identify
    the two sides of the shared routine protocol.
    """

    a_invite: float = 0.0
    a_deliver: float = 0.0
    a_notify: float = 0.0
    a_callback: float = 0.0
    a_boundary_preserving: float = 0.0
    b_opt_in: float = 0.0
    b_pass_choice: float = 0.0
    b_acknowledge: float = 0.0
    b_exception_sync: float = 0.0
    b_closure: float = 0.0

    def __post_init__(self) -> None:
        for little_field in fields(self):
            value = float(getattr(self, little_field.name))
            if not 0.0 <= value <= 1.0:
                raise ValueError(
                    f"🐾 Action '{little_field.name}' must stay between 0 and 1, got {value}."
                )

    def as_array(self) -> np.ndarray:
        return np.array([float(getattr(self, name)) for name in ACTION_NAMES], dtype=float)

    @classmethod
    def from_mapping(cls, values: Mapping[str, float] | None) -> "RoutineActions":
        """Build one little action basket from sparse generic fields. 🧺"""

        if values is None:
            return cls()
        unknown = sorted(set(values) - set(ACTION_NAMES))
        if unknown:
            raise ValueError(f"🙈 Unknown tiny action field(s): {', '.join(unknown)}")
        return cls(**{name: float(value) for name, value in values.items()})


def action_effect(actions: RoutineActions | Mapping[str, float] | None) -> np.ndarray:
    """Return the small controlled drift contributed by observable actions. 🎮🌱

    The base term is linear in the supplied action vector. A few explicit pairwise
    products then encode coordination effects that only exist when both actions occur.

    A pass is deliberately not encoded as a failure penalty. When it is an explicit
    voluntary choice, it can preserve V without silently reducing M. Shared Context
    is handled separately by ``coffee_brain.memory`` so daily drift cannot masquerade
    as accumulated memory. ☕🧠
    """

    basket = actions if isinstance(actions, RoutineActions) else RoutineActions.from_mapping(actions)
    vector = basket.as_array()
    effect = vector @ ACTION_EFFECTS

    # Pairwise interaction terms use simple products, so the extra effect vanishes if
    # either participating action is zero and grows smoothly as both intensities grow.
    effect = np.asarray(effect, dtype=float)

    # Invitation + voluntary opt-in reinforces modeled mutuality beyond the sum of
    # their separate linear contributions.
    effect[1] += 0.0030 * basket.a_invite * basket.b_opt_in

    # Delivery + acknowledgment reinforces predictability and mutuality while reducing
    # friction: a completed handoff matters differently from either action in isolation.
    effect[0] += 0.0020 * basket.a_deliver * basket.b_acknowledge
    effect[1] += 0.0020 * basket.a_deliver * basket.b_acknowledge
    effect[5] -= 0.0020 * basket.a_deliver * basket.b_acknowledge

    # Boundary-preserving behavior + voluntary pass is modeled as evidence that choice
    # remained available, so V rises and F falls instead of treating the pass as failure.
    effect[2] += 0.0030 * basket.a_boundary_preserving * basket.b_pass_choice
    effect[5] -= 0.0020 * basket.a_boundary_preserving * basket.b_pass_choice

    # Notification + exception synchronization represents explicit coordination around
    # a deviation from routine, increasing predictability and reducing modeled friction.
    effect[0] += 0.0020 * basket.a_notify * basket.b_exception_sync
    effect[5] -= 0.0020 * basket.a_notify * basket.b_exception_sync

    return effect
