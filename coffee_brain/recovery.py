from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np

from .actions import RoutineActions
from .model import RoutineMode


STATE_KEYS = ("P", "M", "V", "C", "E", "F")

REPAIR_ACTION_WEIGHTS = {
    "a_notify": 0.25,
    "a_callback": 0.50,
    "a_boundary_preserving": 0.25,
    "b_exception_sync": 0.40,
    "b_closure": 0.25,
}

REPAIR_OBSERVATION_WEIGHTS = {
    "proactive_update": 0.25,
    "resume_signal": 0.40,
}


@dataclass(frozen=True)
class NominalRoutineSet:
    """A soft little box around ordinary routine behavior, not one magic point. 🌿☕"""

    center: np.ndarray
    tolerance: np.ndarray

    def __post_init__(self) -> None:
        center = np.asarray(self.center, dtype=float)
        tolerance = np.asarray(self.tolerance, dtype=float)
        if center.shape != (6,) or tolerance.shape != (6,):
            raise ValueError("🐾 Nominal routine set needs six centers and six tiny tolerances.")
        if np.any(tolerance <= 0.0):
            raise ValueError("🌱 Every nominal tolerance must be greater than zero.")
        object.__setattr__(self, "center", center)
        object.__setattr__(self, "tolerance", tolerance)

    @classmethod
    def from_target(
        cls,
        target: Sequence[float],
        tolerance: Sequence[float] = (0.12, 0.12, 0.10, 0.14, 0.20, 0.12),
    ) -> "NominalRoutineSet":
        return cls(np.asarray(target, dtype=float), np.asarray(tolerance, dtype=float))

    @property
    def lower(self) -> np.ndarray:
        return np.clip(self.center - self.tolerance, 0.0, 1.0)

    @property
    def upper(self) -> np.ndarray:
        return np.clip(self.center + self.tolerance, 0.0, 1.0)

    def distance(self, state: Sequence[float]) -> float:
        """Normalized distance outside the nominal box; zero means comfortably inside. 🌱"""

        x = np.asarray(state, dtype=float)
        if x.shape != (6,):
            raise ValueError("🐾 Recovery distance expects one six-state coffee vector.")
        below = np.maximum(self.lower - x, 0.0)
        above = np.maximum(x - self.upper, 0.0)
        excess = (below + above) / self.tolerance
        return float(np.linalg.norm(excess) / np.sqrt(6.0))

    def contains(self, state: Sequence[float], epsilon: float = 0.0) -> bool:
        return self.distance(state) <= float(epsilon)


@dataclass(frozen=True)
class RecoveryEvent:
    disturbance_id: int
    start_index: int
    disturbance_end_index: int
    disturbance_duration: int
    recovered_index: int | None
    recovery_time: int | None
    repair_cost: float
    natural_resume: bool
    resilience: float

    @property
    def recovered(self) -> bool:
        return self.recovered_index is not None


@dataclass(frozen=True)
class RecoverySummary:
    total_disturbances: int
    recovered_disturbances: int
    recovery_ratio: float
    median_recovery_time: float | None
    mean_repair_cost: float
    natural_resume_ratio: float
    mean_resilience: float

    def as_row(self) -> dict[str, object]:
        return {
            "total_disturbances": self.total_disturbances,
            "recovered_disturbances": self.recovered_disturbances,
            "recovery_ratio": self.recovery_ratio,
            "median_recovery_time": self.median_recovery_time,
            "mean_repair_cost": self.mean_repair_cost,
            "natural_resume_ratio": self.natural_resume_ratio,
            "mean_resilience": self.mean_resilience,
        }


def _action_cost(action: RoutineActions | Mapping[str, float] | None) -> float:
    basket = action if isinstance(action, RoutineActions) else RoutineActions.from_mapping(action)
    return float(
        sum(REPAIR_ACTION_WEIGHTS[name] * float(getattr(basket, name)) for name in REPAIR_ACTION_WEIGHTS)
    )


def _observation_cost(observation: Mapping[str, object] | None) -> float:
    if observation is None:
        return 0.0
    total = 0.0
    for key, weight in REPAIR_OBSERVATION_WEIGHTS.items():
        value = observation.get(key)
        if value is not None:
            total += weight * float(value)
    return float(total)


def _repair_cost(
    start: int,
    stop: int,
    *,
    actions: Sequence[RoutineActions | Mapping[str, float]] | None,
    observations: Sequence[Mapping[str, object]] | None,
) -> float:
    """Count explicit repair effort after a disturbance, without billing ordinary coffee. 🩹☕"""

    if stop <= start:
        return 0.0
    if actions is not None:
        return float(sum(_action_cost(actions[index]) for index in range(start, stop)))
    if observations is not None:
        return float(sum(_observation_cost(observations[index]) for index in range(start, stop)))
    return 0.0


def detect_recovery_events(
    states: np.ndarray,
    modes: Sequence[int],
    nominal_set: NominalRoutineSet,
    *,
    actions: Sequence[RoutineActions | Mapping[str, float]] | None = None,
    observations: Sequence[Mapping[str, object]] | None = None,
    epsilon: float = 0.0,
    repair_lambda: float = 1.0,
) -> list[RecoveryEvent]:
    """Find Busy/Leave disturbance windows and measure how gently they come home. 🌧️➡️🌱"""

    states = np.asarray(states, dtype=float)
    modes = np.asarray(modes, dtype=int)
    if states.ndim != 2 or states.shape[1] != 6:
        raise ValueError("🐾 Recovery meter expects a timeline shaped [days, 6].")
    if len(states) != len(modes):
        raise ValueError("🐾 Recovery states and modes must have the same tiny length.")
    if actions is not None and len(actions) != len(states):
        raise ValueError("🎮🐾 Recovery action schedule must match the state timeline.")
    if observations is not None and len(observations) != len(states):
        raise ValueError("👀🐾 Recovery observation baskets must match the state timeline.")

    disturbance = np.isin(modes, [int(RoutineMode.BUSY), int(RoutineMode.LEAVE)])
    events: list[RecoveryEvent] = []
    index = 0
    disturbance_id = 1

    while index < len(states):
        if not disturbance[index]:
            index += 1
            continue

        start = index
        while index < len(states) and disturbance[index]:
            index += 1
        disturbance_end = index
        disturbance_duration = disturbance_end - start

        recovered_index: int | None = None
        for candidate in range(disturbance_end, len(states)):
            if disturbance[candidate]:
                break
            if nominal_set.contains(states[candidate], epsilon=epsilon):
                recovered_index = candidate
                break

        if recovered_index is None:
            recovery_time = None
            cost_stop = len(states)
            resilience = 0.0
        else:
            recovery_time = recovered_index - disturbance_end
            cost_stop = recovered_index
            repair_cost = _repair_cost(
                disturbance_end,
                cost_stop,
                actions=actions,
                observations=observations,
            )
            resilience = 1.0 / (1.0 + recovery_time + repair_lambda * repair_cost)

        repair_cost = _repair_cost(
            disturbance_end,
            cost_stop,
            actions=actions,
            observations=observations,
        )
        natural_resume = recovered_index is not None and repair_cost <= 1e-12

        events.append(
            RecoveryEvent(
                disturbance_id=disturbance_id,
                start_index=start,
                disturbance_end_index=disturbance_end,
                disturbance_duration=disturbance_duration,
                recovered_index=recovered_index,
                recovery_time=recovery_time,
                repair_cost=repair_cost,
                natural_resume=natural_resume,
                resilience=float(resilience),
            )
        )
        disturbance_id += 1

    return events


def summarize_recovery(events: Sequence[RecoveryEvent]) -> RecoverySummary:
    """Turn many little wobbles into one compact resilience picnic card. 🧺🌱"""

    total = len(events)
    if total == 0:
        return RecoverySummary(0, 0, 0.0, None, 0.0, 0.0, 0.0)

    recovered = [event for event in events if event.recovered]
    recovery_times = [event.recovery_time for event in recovered if event.recovery_time is not None]
    repair_costs = [event.repair_cost for event in events]
    natural = [event for event in recovered if event.natural_resume]
    resilience = [event.resilience for event in events]

    return RecoverySummary(
        total_disturbances=total,
        recovered_disturbances=len(recovered),
        recovery_ratio=float(len(recovered) / total),
        median_recovery_time=(float(np.median(recovery_times)) if recovery_times else None),
        mean_repair_cost=float(np.mean(repair_costs)),
        natural_resume_ratio=(float(len(natural) / len(recovered)) if recovered else 0.0),
        mean_resilience=float(np.mean(resilience)),
    )


def event_rows(events: Sequence[RecoveryEvent]) -> list[dict[str, object]]:
    return [
        {
            "disturbance_id": event.disturbance_id,
            "start_index": event.start_index,
            "disturbance_end_index": event.disturbance_end_index,
            "disturbance_duration": event.disturbance_duration,
            "recovered_index": event.recovered_index,
            "recovery_time": event.recovery_time,
            "repair_cost": event.repair_cost,
            "natural_resume": int(event.natural_resume),
            "resilience": event.resilience,
        }
        for event in events
    ]
