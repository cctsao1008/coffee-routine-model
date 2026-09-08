from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
import json
from pathlib import Path
from typing import Any, Mapping

from .config import ARCHITECTURE_VERSION, CSRDMConfig, config_snapshot


@dataclass(frozen=True)
class ExperimentSpec:
    """One deterministic recipe card for a model experiment. 🛂☕🐣"""

    name: str
    scenario: str
    days: int
    seed: int = 20260908
    particle_count: int = 6000
    dataset_identity: str = "synthetic-generated"
    config: CSRDMConfig = CSRDMConfig()
    architecture_version: str = ARCHITECTURE_VERSION
    tags: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("🛂 Tiny experiment name cannot be empty.")
        if not self.scenario.strip():
            raise ValueError("🌦️ Tiny experiment scenario cannot be empty.")
        if self.days <= 0:
            raise ValueError("🗓️ Tiny experiment needs at least one day.")
        if self.particle_count < 1:
            raise ValueError("🐣 particle_count must be positive.")
        if not self.dataset_identity.strip():
            raise ValueError("🧺 dataset_identity cannot be an empty basket.")
        if self.architecture_version != self.config.architecture_version:
            raise ValueError("🏛️ Experiment and config architecture versions must match.")

    def recipe_dict(self) -> dict[str, Any]:
        """Return only identity-bearing recipe fields; display labels stay outside. 🧾"""

        return {
            "scenario": self.scenario,
            "days": self.days,
            "seed": self.seed,
            "particle_count": self.particle_count,
            "dataset_identity": self.dataset_identity,
            "architecture_version": self.architecture_version,
            "config": config_snapshot(self.config),
        }

    @property
    def fingerprint(self) -> str:
        """Stable short identity for the exact recipe, without clocks or filenames. 🐾"""

        payload = json.dumps(
            self.recipe_dict(),
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")
        return sha256(payload).hexdigest()[:16]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "fingerprint": self.fingerprint,
            **self.recipe_dict(),
            "tags": list(self.tags),
        }


@dataclass(frozen=True)
class ExperimentResult:
    """Portable experiment receipt: recipe, metrics, diagnostics, and artifact names. 🧺📋"""

    spec: ExperimentSpec
    metrics: Mapping[str, Any] = field(default_factory=dict)
    diagnostics: Mapping[str, Any] = field(default_factory=dict)
    artifacts: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment": self.spec.to_dict(),
            "metrics": _json_ready(dict(self.metrics)),
            "diagnostics": _json_ready(dict(self.diagnostics)),
            "artifacts": list(self.artifacts),
            "notes": list(self.notes),
        }

    def write_json(self, path: str | Path) -> Path:
        """Put one complete tiny receipt on disk without changing its identity. 🧺✨"""

        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            json.dumps(self.to_dict(), indent=2, sort_keys=True, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        return destination


def _json_ready(value: Any) -> Any:
    """Keep result payloads portable without importing experiment-specific modules. 🐣"""

    if hasattr(value, "tolist"):
        return value.tolist()
    if hasattr(value, "item") and callable(value.item):
        try:
            return value.item()
        except (ValueError, TypeError):
            pass
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [_json_ready(item) for item in value]
    return value
