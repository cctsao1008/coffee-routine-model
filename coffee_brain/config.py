from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from typing import Any

import numpy as np

from .memory import DEFAULT_SHARED_CONTEXT_MEMORY, SharedContextMemoryConfig
from .observation_model import DEFAULT_OBSERVATION_MODEL, ObservationModelConfig
from .transitions import ContextTransitionConfig


ARCHITECTURE_VERSION = "0.3"


@dataclass(frozen=True)
class DynamicsConfig:
    """Structural motion knobs that belong to dynamics, not observations. 🎮🌱"""

    process_noise_scale: float = 1.0
    fixed_transition: tuple[tuple[float, ...], ...] | None = None

    def __post_init__(self) -> None:
        if self.process_noise_scale <= 0.0:
            raise ValueError("🐾 process_noise_scale must be positive.")
        if self.fixed_transition is not None:
            matrix = np.asarray(self.fixed_transition, dtype=float)
            if matrix.shape != (5, 5):
                raise ValueError("🎲 Tiny fixed transition must be a 5x5 table.")
            if np.any(matrix <= 0.0) or not np.allclose(matrix.sum(axis=1), 1.0):
                raise ValueError("🎲 Every fixed-transition row must be positive and sum to 1.")

    def transition_array(self) -> np.ndarray | None:
        if self.fixed_transition is None:
            return None
        return np.asarray(self.fixed_transition, dtype=float)


@dataclass(frozen=True)
class InferenceConfig:
    """How many tiny guesses the online estimator keeps around. 🐣🐣🐣"""

    particle_count: int = 6000
    seed: int = 20260908
    record_history: bool = False

    def __post_init__(self) -> None:
        if self.particle_count < 100:
            raise ValueError("🐣 The public CSRDM API needs at least 100 tiny particle friends.")


@dataclass(frozen=True)
class SmoothingConfig:
    """Optional hindsight hat. Filtering stays the default. 🔭🎩"""

    enabled: bool = False
    lag: int = 30
    full_history: bool = False

    def __post_init__(self) -> None:
        if self.lag < 0:
            raise ValueError("🔭 Tiny smoothing lag cannot be negative.")


@dataclass(frozen=True)
class LearningConfig:
    """Architecture-level learning policy; the optimizer still owns its local details. 🎚️🥄"""

    enabled: bool = False
    train_fraction: float = 0.60
    bounded_parameters_only: bool = True

    def __post_init__(self) -> None:
        if not 0.4 <= self.train_fraction <= 0.8:
            raise ValueError("🎚️ train_fraction should stay between 0.4 and 0.8.")


@dataclass(frozen=True)
class CSRDMConfig:
    """One complete configuration tree for the public tiny-brain boundary. 🧺🧠✨"""

    dynamics: DynamicsConfig = DynamicsConfig()
    memory: SharedContextMemoryConfig = DEFAULT_SHARED_CONTEXT_MEMORY
    observation: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL
    transition: ContextTransitionConfig | None = None
    inference: InferenceConfig = InferenceConfig()
    smoothing: SmoothingConfig = SmoothingConfig()
    learning: LearningConfig = LearningConfig()
    architecture_version: str = ARCHITECTURE_VERSION

    def __post_init__(self) -> None:
        if not self.architecture_version:
            raise ValueError("🏛️ Architecture version cannot be an empty little cup.")


def _snapshot(value: Any) -> Any:
    """Turn immutable configs and numpy bits into boring, portable JSON-shaped data. 🧺"""

    if is_dataclass(value):
        return {key: _snapshot(item) for key, item in asdict(value).items()}
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, dict):
        return {str(key): _snapshot(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_snapshot(item) for item in value]
    return value


def config_snapshot(config: CSRDMConfig) -> dict[str, Any]:
    """Freeze the full model-definition basket into a serializable snapshot. 📸☕"""

    return _snapshot(config)
