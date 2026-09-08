from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

import numpy as np

from .actions import RoutineActions
from .scenarios import BASE_TRANSITION


TARGET_MODE_NAMES = ("Normal", "Busy", "Leave", "Special", "Recovery")
CONTEXT_FEATURE_NAMES = (
    "friction",
    "unpredictability",
    "low_mutuality",
    "coordinated_exception",
    "recovery_evidence",
    "special_signal",
    "disturbance",
)


@dataclass(frozen=True)
class TransitionContext:
    """Known context that may gently reshape the next-mode dice. 🌦️🎲"""

    disturbance: float = 0.0
    regime_logits: tuple[float, float, float, float, float] = (0.0, 0.0, 0.0, 0.0, 0.0)

    def __post_init__(self) -> None:
        if not 0.0 <= float(self.disturbance) <= 1.0:
            raise ValueError("🐾 Disturbance context must stay between 0 and 1.")
        if len(self.regime_logits) != 5:
            raise ValueError("🐾 Regime context needs five tiny target-mode logits.")

    @classmethod
    def from_mapping(cls, values: Mapping[str, object] | None) -> "TransitionContext":
        if values is None:
            return cls()
        allowed = {"disturbance", "regime_logits"}
        unknown = sorted(set(values) - allowed)
        if unknown:
            raise ValueError(f"🙈 Unknown tiny transition context: {', '.join(unknown)}")
        regime = values.get("regime_logits", cls().regime_logits)
        return cls(
            disturbance=float(values.get("disturbance", 0.0)),
            regime_logits=tuple(float(value) for value in regime),
        )


@dataclass(frozen=True)
class ContextTransitionConfig:
    """Inspectable context coefficients layered on top of the fixed transition table. ☕🎛️"""

    base_transition: np.ndarray
    feature_effects: np.ndarray
    max_logit_shift: float = 1.6
    provenance: str = "hand-set structural transition baseline; not learned from real humans"

    def __post_init__(self) -> None:
        base = np.asarray(self.base_transition, dtype=float)
        effects = np.asarray(self.feature_effects, dtype=float)
        if base.shape != (5, 5):
            raise ValueError("🐾 Base transition matrix must be 5x5.")
        if effects.shape != (len(CONTEXT_FEATURE_NAMES), 5):
            raise ValueError("🐾 Context transition effects have the wrong tiny shape.")
        if np.any(base <= 0.0) or not np.allclose(base.sum(axis=1), 1.0):
            raise ValueError("🐾 Base transition rows must be positive and sum to 1.")
        if self.max_logit_shift <= 0.0:
            raise ValueError("🐾 max_logit_shift must be positive.")


DEFAULT_CONTEXT_TRANSITIONS = ContextTransitionConfig(
    base_transition=np.array(BASE_TRANSITION, dtype=float, copy=True),
    feature_effects=np.array(
        [
            [-0.35, 0.80, 0.25, 0.00, 0.20],  # friction
            [-0.20, 0.55, 0.10, 0.00, 0.25],  # unpredictability
            [-0.20, 0.40, 0.10, 0.00, 0.15],  # low mutuality
            [-0.30, 0.05, 1.45, 0.00, 0.40],  # coordinated exception / leave
            [0.25, -0.20, -0.45, 0.00, 1.35],  # recovery evidence
            [0.05, 0.00, 0.00, 1.55, 0.05],  # special signal
            [-0.45, 0.75, 0.55, 0.00, 0.35],  # external disturbance
        ],
        dtype=float,
    ),
)


def _action_basket(actions: RoutineActions | Mapping[str, float] | None) -> RoutineActions:
    return actions if isinstance(actions, RoutineActions) else RoutineActions.from_mapping(actions)


def _context_basket(
    context: TransitionContext | Mapping[str, object] | None,
) -> TransitionContext:
    return context if isinstance(context, TransitionContext) else TransitionContext.from_mapping(context)


def transition_features(
    states: np.ndarray,
    actions: RoutineActions | Mapping[str, float] | None = None,
    context: TransitionContext | Mapping[str, object] | None = None,
) -> np.ndarray:
    """Build small, inspectable transition features without reading minds. 🌦️🐣"""

    tiny_states = np.asarray(states, dtype=float)
    if tiny_states.ndim == 1:
        tiny_states = tiny_states[None, :]
    if tiny_states.ndim != 2 or tiny_states.shape[1] != 6:
        raise ValueError("🐾 Transition states must have shape (n, 6).")

    basket = _action_basket(actions)
    weather = _context_basket(context)
    p, m, _, _, _, f = tiny_states.T

    coordinated_exception = max(
        basket.a_boundary_preserving,
        basket.b_exception_sync,
        basket.b_pass_choice,
    )
    recovery_evidence = max(
        basket.a_notify * basket.b_exception_sync,
        basket.b_closure,
        basket.a_deliver * basket.b_acknowledge,
    )
    special_signal = basket.a_callback

    return np.column_stack(
        [
            np.clip(f, 0.0, 1.0),
            np.clip(1.0 - p, 0.0, 1.0),
            np.clip(1.0 - m, 0.0, 1.0),
            np.full(len(tiny_states), coordinated_exception),
            np.full(len(tiny_states), recovery_evidence),
            np.full(len(tiny_states), special_signal),
            np.full(len(tiny_states), weather.disturbance),
        ]
    )


def fixed_transition_probabilities(
    previous_modes: np.ndarray | int,
    *,
    base_transition: np.ndarray = BASE_TRANSITION,
) -> np.ndarray:
    """The old fixed matrix, preserved as a reproducible little baseline. 🎲🧺"""

    previous = np.asarray(previous_modes, dtype=int)
    scalar = previous.ndim == 0
    previous = previous.reshape(-1)
    if np.any((previous < 0) | (previous > 4)):
        raise ValueError("🐾 Previous modes must live between 0 and 4.")
    result = np.asarray(base_transition, dtype=float)[previous]
    return result[0] if scalar else result


def context_transition_probabilities(
    previous_modes: np.ndarray | int,
    states: np.ndarray,
    actions: RoutineActions | Mapping[str, float] | None = None,
    context: TransitionContext | Mapping[str, object] | None = None,
    *,
    config: ContextTransitionConfig = DEFAULT_CONTEXT_TRANSITIONS,
) -> np.ndarray:
    """Return context-aware next-mode probabilities while keeping the dice stochastic. 🌦️🎲

    Context only nudges log probabilities. It never deterministically chooses a mode,
    and every total logit nudge is clipped so one tiny clue cannot fling the dice
    across the room. XD
    """

    previous = np.asarray(previous_modes, dtype=int)
    scalar = previous.ndim == 0
    previous = previous.reshape(-1)
    tiny_states = np.asarray(states, dtype=float)
    if tiny_states.ndim == 1:
        tiny_states = tiny_states[None, :]
    if len(previous) == 1 and len(tiny_states) > 1:
        previous = np.full(len(tiny_states), int(previous[0]), dtype=int)
    if len(previous) != len(tiny_states):
        raise ValueError("🐾 Need one previous mode per tiny state.")
    if np.any((previous < 0) | (previous > 4)):
        raise ValueError("🐾 Previous modes must live between 0 and 4.")

    features = transition_features(tiny_states, actions, context)
    delta = features @ np.asarray(config.feature_effects, dtype=float)
    weather = _context_basket(context)
    delta += np.asarray(weather.regime_logits, dtype=float)[None, :]
    delta = np.clip(delta, -config.max_logit_shift, config.max_logit_shift)

    base = np.asarray(config.base_transition, dtype=float)[previous]
    logits = np.log(np.clip(base, 1e-12, 1.0)) + delta
    logits -= np.max(logits, axis=1, keepdims=True)
    probability = np.exp(logits)
    probability /= probability.sum(axis=1, keepdims=True)
    return probability[0] if scalar and len(tiny_states) == 1 else probability


def sample_next_modes(
    rng: np.random.Generator,
    previous_modes: np.ndarray,
    states: np.ndarray,
    actions: RoutineActions | Mapping[str, float] | None = None,
    context: TransitionContext | Mapping[str, object] | None = None,
    *,
    config: ContextTransitionConfig = DEFAULT_CONTEXT_TRANSITIONS,
) -> np.ndarray:
    """Roll one context-aware tiny die per particle. 🎲🐣"""

    probabilities = context_transition_probabilities(
        previous_modes,
        states,
        actions,
        context,
        config=config,
    )
    if probabilities.ndim == 1:
        probabilities = probabilities[None, :]
    u = rng.random(len(probabilities))
    cdf = np.cumsum(probabilities, axis=1)
    return np.sum(u[:, None] > cdf, axis=1).astype(int)
