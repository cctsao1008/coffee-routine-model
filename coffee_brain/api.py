from __future__ import annotations

import math
from dataclasses import dataclass
from numbers import Real
from typing import Iterable, Mapping

from .actions import RoutineActions
from .config import CSRDMConfig
from .model import MODE_LABELS, STATE_NAMES
from .particles import CoffeeParticleFilter, Posterior
from .protocol_adapter import CoffeeEvent, CoffeeStep, coffee_to_step
from .smoothing import SmoothedPosterior, smooth_history
from .transitions import TransitionContext


_BINARY_OBSERVATION_FIELDS = (
    "invite",
    "opt_in",
    "text_reply",
    "reaction",
    "state_share",
    "proactive_update",
    "routine_maintenance",
    "pass_event",
    "resume_signal",
    "pause_event",
    "payment_event",
)
_CONTINUOUS_OBSERVATION_FIELDS = ("tone_warmth", "response_delay_min")
_METADATA_OBSERVATION_FIELDS = ("unknown_events",)
_ALLOWED_OBSERVATION_FIELDS = frozenset(
    _BINARY_OBSERVATION_FIELDS + _CONTINUOUS_OBSERVATION_FIELDS + _METADATA_OBSERVATION_FIELDS
)


def _binary_value(name: str, value: object) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, Real):
        tiny = float(value)
        if math.isfinite(tiny) and tiny in (0.0, 1.0):
            return int(tiny)
    raise ValueError(
        f"👀 Observation '{name}' must be 0, 1, or None; got {value!r}."
    )


def _finite_number(name: str, value: object) -> float:
    if not isinstance(value, Real):
        raise ValueError(f"📏 Observation '{name}' must be a finite number; got {value!r}.")
    tiny = float(value)
    if not math.isfinite(tiny):
        raise ValueError(f"📏 Observation '{name}' must be finite; got {value!r}.")
    return tiny


def _normalize_public_observation(observation: Mapping[str, object]) -> dict:
    """Validate one public observation basket before specialist internals see it. ☕🧺

    This boundary keeps three ideas separate:

    1. schema validity — known field names and valid numeric domains,
    2. directly implied evidence — e.g. a measured reply delay implies a reply existed,
    3. protocol consistency — mutually incompatible observations are rejected.

    The function normalizes observations; it does not infer hidden states or intent.
    """

    obs = dict(observation)

    # 1. Schema guard: unknown keys should fail loudly rather than silently becoming
    # accidental missing evidence inside the particle filter.
    unknown = [key for key in obs if key not in _ALLOWED_OBSERVATION_FIELDS]
    if unknown:
        pretty = ", ".join(repr(key) for key in unknown)
        known = ", ".join(sorted(_ALLOWED_OBSERVATION_FIELDS))
        raise ValueError(
            f"🙈 Unknown observation field(s): {pretty}. Known public fields are: {known}."
        )

    # 2. Primitive value normalization: binary clues become {0,1,None}; continuous
    # clues remain finite numbers with their public-domain constraints enforced.
    for name in _BINARY_OBSERVATION_FIELDS:
        if name in obs:
            obs[name] = _binary_value(name, obs[name])

    if "tone_warmth" in obs and obs["tone_warmth"] is not None:
        warmth = _finite_number("tone_warmth", obs["tone_warmth"])
        if not 0.0 <= warmth <= 1.0:
            raise ValueError("🌡️ Observation 'tone_warmth' must stay between 0 and 1.")
        obs["tone_warmth"] = warmth

    if "response_delay_min" in obs and obs["response_delay_min"] is not None:
        delay = _finite_number("response_delay_min", obs["response_delay_min"])
        if delay < 0.0:
            raise ValueError("⏰ Observation 'response_delay_min' cannot be negative.")
        obs["response_delay_min"] = delay

        # 3. Direct implication, not hidden inference: measuring a reply delay already
        # proves that a reply occurred on this protocol step.
        if obs.get("text_reply") == 0:
            raise ValueError(
                "⏰ response_delay_min records a reply, so it cannot be combined with text_reply=0."
            )
        if obs.get("text_reply") is None:
            obs["text_reply"] = 1

    opt_in = obs.get("opt_in")
    pass_event = obs.get("pass_event")
    text_reply = obs.get("text_reply")
    maintenance = obs.get("routine_maintenance")
    invite = obs.get("invite")

    # 4. Protocol consistency constraints. These are logical contradictions among
    # observable event labels, not psychological judgments about the participants.
    if opt_in == 1 and pass_event == 1:
        raise ValueError("🌿 opt_in=1 and pass_event=1 cannot describe the same protocol step.")
    if pass_event == 1 and maintenance == 1:
        raise ValueError("🌿 pass_event=1 cannot share a step with routine_maintenance=1.")
    if opt_in == 0 and maintenance == 1:
        raise ValueError("☕ routine_maintenance=1 conflicts with an explicitly observed opt_in=0.")
    if invite == 0 and (opt_in == 1 or pass_event == 1):
        raise ValueError(
            "☕ invite=0 closes the response opportunity; leave invite missing if the invite itself was not observed."
        )

    # Explicit opt-in/pass is itself a textual response in this event vocabulary.
    if opt_in == 1 or pass_event == 1:
        if text_reply == 0:
            raise ValueError("💬 An explicit opt-in or pass cannot be combined with text_reply=0.")
        if text_reply is None:
            obs["text_reply"] = 1

    return obs


@dataclass(frozen=True)
class CSRDMResult:
    """One public online result: facts, controls, and posterior kept in separate cups. ☕🧺"""

    step_index: int
    posterior: Posterior
    actions: RoutineActions
    observation: dict

    @property
    def transition_applied(self) -> bool:
        """Whether this call had a previous hidden state to transition from. 🎮🌱"""

        return self.step_index > 0

    @property
    def mean_by_state(self) -> dict[str, float]:
        """Posterior means with readable state names instead of six mystery numbers. 🧠☕"""

        return {
            name: float(value)
            for name, value in zip(STATE_NAMES, self.posterior.mean, strict=True)
        }

    @property
    def ci95_by_state(self) -> dict[str, tuple[float, float]]:
        """Posterior 95% intervals keyed by the six state names. 📏🐣"""

        return {
            name: (float(low), float(high))
            for name, low, high in zip(
                STATE_NAMES,
                self.posterior.ci95_low,
                self.posterior.ci95_high,
                strict=True,
            )
        }

    @property
    def mode_probabilities_by_name(self) -> dict[str, float]:
        """Mode probabilities with their labels attached. 🌦️🎲"""

        return {
            name: float(value)
            for name, value in zip(
                MODE_LABELS,
                self.posterior.mode_probabilities,
                strict=True,
            )
        }


class CSRDM:
    """Stable public facade for the tiny coffee brain. 🏛️☕🐣

    External callers should not need to know which internal drawer owns memory,
    transitions, observations, filtering, or smoothing. That plumbing stays behind
    this little door so the architecture can evolve without moving every coffee mug.
    """

    def __init__(self, config: CSRDMConfig | None = None):
        self.config = config or CSRDMConfig()
        if self.config.learning.enabled:
            raise ValueError(
                "🎚️ CSRDM does not perform online learning. Keep LearningConfig(enabled=False) "
                "for the online estimator and use tiny_tools.learn_parameters for the bounded learning bench."
            )
        record_history = self.config.inference.record_history or self.config.smoothing.enabled
        self._filter = CoffeeParticleFilter(
            particle_count=self.config.inference.particle_count,
            seed=self.config.inference.seed,
            record_history=record_history,
            memory_config=self.config.memory,
            observation_config=self.config.observation,
            transition_config=self.config.transition,
            fixed_transition=self.config.dynamics.transition_array(),
            process_noise_scale=self.config.dynamics.process_noise_scale,
        )
        self._step_index = 0

    @property
    def particle_filter(self) -> CoffeeParticleFilter:
        """Inspectable escape hatch for diagnostics; not the preferred public path. 🔧🐣"""

        return self._filter

    @property
    def step_count(self) -> int:
        return self._step_index

    def update(
        self,
        observation: Mapping[str, object],
        *,
        actions: RoutineActions | Mapping[str, float] | None = None,
        transition_context: TransitionContext | Mapping[str, object] | None = None,
    ) -> CSRDMResult:
        """Advance one generic controlled state-space step. 🎮👀🐣

        Missing clues may be omitted or set to ``None``. Public observations are
        validated here so typos and impossible protocol combinations do not quietly
        turn into missing evidence.

        Temporal contract: controls supplied with call ``t`` drive the previous
        hidden state into the current hidden state. The first call establishes the
        initial filtered state, so ``result.transition_applied`` is ``False`` there.
        """

        if transition_context is not None and self.config.transition is None:
            raise ValueError(
                "🌦️ transition_context was supplied while context-aware transitions are disabled. "
                "Use CSRDMConfig(transition=DEFAULT_CONTEXT_TRANSITIONS) to opt in."
            )

        action_basket = actions if isinstance(actions, RoutineActions) else RoutineActions.from_mapping(actions)
        obs = _normalize_public_observation(observation)
        posterior = self._filter.update(
            obs,
            actions=action_basket,
            transition_context=transition_context,
        )
        result = CSRDMResult(
            step_index=self._step_index,
            posterior=posterior,
            actions=action_basket,
            observation=obs,
        )
        self._step_index += 1
        return result

    def step(
        self,
        events: Iterable[str | CoffeeEvent],
        *,
        tone_warmth: float | None = None,
        response_delay_min: float | None = None,
        transition_context: TransitionContext | Mapping[str, object] | None = None,
    ) -> CSRDMResult:
        """Accept protocol events, split actions from clues, then update the posterior. ☕➡️🧠"""

        tiny_step: CoffeeStep = coffee_to_step(
            events,
            tone_warmth=tone_warmth,
            response_delay_min=response_delay_min,
        )
        return self.update(
            tiny_step.observation,
            actions=tiny_step.actions,
            transition_context=transition_context,
        )

    def smooth(self) -> list[SmoothedPosterior]:
        """Apply the configured hindsight policy without changing observed history. 🔭🐣"""

        if not self.config.smoothing.enabled:
            raise RuntimeError(
                "🔭 Tiny smoothing is disabled. Build CSRDM with "
                "CSRDMConfig(smoothing=SmoothingConfig(enabled=True, ...)) before collecting the timeline."
            )
        return smooth_history(
            self._filter.history,
            lag=self.config.smoothing.lag,
            full_history=self.config.smoothing.full_history,
        )
