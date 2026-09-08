from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .actions import RoutineActions
from .config import CSRDMConfig
from .particles import CoffeeParticleFilter, Posterior
from .protocol_adapter import CoffeeEvent, CoffeeStep, coffee_to_step
from .smoothing import SmoothedPosterior, smooth_history
from .transitions import TransitionContext


@dataclass(frozen=True)
class CSRDMResult:
    """One public online result: facts, controls, and posterior kept in separate cups. ☕🧺"""

    step_index: int
    posterior: Posterior
    actions: RoutineActions
    observation: dict


class CSRDM:
    """Stable public facade for the tiny coffee brain. 🏛️☕🐣

    External callers should not need to know which internal drawer owns memory,
    transitions, observations, filtering, or smoothing. That plumbing stays behind
    this little door so the architecture can evolve without moving every coffee mug.
    """

    def __init__(self, config: CSRDMConfig | None = None):
        self.config = config or CSRDMConfig()
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
        """Advance one generic controlled state-space step. 🎮👀🐣"""

        action_basket = actions if isinstance(actions, RoutineActions) else RoutineActions.from_mapping(actions)
        obs = dict(observation)
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
            raise RuntimeError("🔭 Tiny smoothing is disabled in CSRDMConfig.")
        return smooth_history(
            self._filter.history,
            lag=self.config.smoothing.lag,
            full_history=self.config.smoothing.full_history,
        )
