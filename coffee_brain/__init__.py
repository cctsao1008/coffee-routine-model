"""The tiny coffee brain lives here. ☕🧠🐾

Public callers should start with :class:`CSRDM` and :class:`CSRDMConfig`.
The smaller modules remain available for diagnostics and model development.
"""

from .api import CSRDM, CSRDMResult
from .config import (
    ARCHITECTURE_VERSION,
    CSRDMConfig,
    DynamicsConfig,
    InferenceConfig,
    LearningConfig,
    SmoothingConfig,
    config_snapshot,
)
from .experiment import ExperimentResult, ExperimentSpec
from .transitions import DEFAULT_CONTEXT_TRANSITIONS

__all__ = [
    "ARCHITECTURE_VERSION",
    "CSRDM",
    "CSRDMConfig",
    "CSRDMResult",
    "DEFAULT_CONTEXT_TRANSITIONS",
    "DynamicsConfig",
    "ExperimentResult",
    "ExperimentSpec",
    "InferenceConfig",
    "LearningConfig",
    "SmoothingConfig",
    "config_snapshot",
]
