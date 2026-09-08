from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Protocol, Sequence

import numpy as np

from .calibration import calibrate_dataset
from .learning import run_learning_experiment
from .memory import DEFAULT_SHARED_CONTEXT_MEMORY, SharedContextMemoryConfig
from .model import MODE_NAMES, RoutineMode, relationship_index
from .observation_model import DEFAULT_OBSERVATION_MODEL, ObservationModelConfig
from .particles import CoffeeParticleFilter
from .smoothing import smooth_history


STATE_KEYS = ("P", "M", "V", "C", "E", "F")


@dataclass(frozen=True)
class ArenaDataset:
    """One shared synthetic picnic basket that every competitor must use. 🧺☕"""

    truth: np.ndarray
    modes: np.ndarray
    observations: tuple[dict, ...]
    train_fraction: float = 0.60

    @property
    def split_index(self) -> int:
        split = int(round(len(self.truth) * self.train_fraction))
        return min(max(split, 20), len(self.truth) - 20)


@dataclass(frozen=True)
class ArenaRun:
    """Common output contract for every tiny model family. 🗺️🐣"""

    name: str
    latent_dimensions: int
    estimates: np.ndarray
    ci95_low: np.ndarray | None
    ci95_high: np.ndarray | None
    mode_names: tuple[str, ...] | None
    runtime_seconds: float
    memory_bytes: int
    hybrid: bool
    smoothing: bool
    learned_parameters: int
    synthetic_truth_used_for_training: bool
    notes: str


class ArenaRunner(Protocol):
    """Every competitor gets the same dataset and returns the same little contract. ☕🏁"""

    name: str

    def run(self, dataset: ArenaDataset, *, particle_count: int, seed: int) -> ArenaRun:
        ...


def _history_bytes(pf: CoffeeParticleFilter) -> int:
    total = int(pf.particles.nbytes + pf.modes.nbytes + pf.weights.nbytes)
    for step in pf.history:
        total += int(step.particles.nbytes + step.modes.nbytes + step.weights.nbytes)
        if step.parents is not None:
            total += int(step.parents.nbytes)
    return total


@dataclass(frozen=True)
class ParticleArenaRunner:
    name: str
    observation_config: ObservationModelConfig = DEFAULT_OBSERVATION_MODEL
    memory_config: SharedContextMemoryConfig = DEFAULT_SHARED_CONTEXT_MEMORY
    smoothing_lag: int = 0
    learned_parameters: int = 0
    synthetic_truth_used_for_training: bool = False
    notes: str = "six-state hybrid Particle Filter"

    def run(self, dataset: ArenaDataset, *, particle_count: int, seed: int) -> ArenaRun:
        record_history = self.smoothing_lag > 0
        pf = CoffeeParticleFilter(
            particle_count=particle_count,
            seed=seed,
            record_history=record_history,
            memory_config=self.memory_config,
            observation_config=self.observation_config,
        )
        filtered = []
        start = perf_counter()
        for observation in dataset.observations:
            filtered.append(pf.update(dict(observation)))

        if record_history:
            smooth = smooth_history(pf.history, lag=self.smoothing_lag)
            estimates = np.asarray([row.mean for row in smooth], dtype=float)
            low = np.asarray([row.ci95_low for row in smooth], dtype=float)
            high = np.asarray([row.ci95_high for row in smooth], dtype=float)
            mode_names = tuple(row.mode for row in smooth)
        else:
            estimates = np.asarray([row.mean for row in filtered], dtype=float)
            low = np.asarray([row.ci95_low for row in filtered], dtype=float)
            high = np.asarray([row.ci95_high for row in filtered], dtype=float)
            mode_names = tuple(row.mode for row in filtered)

        runtime = perf_counter() - start
        return ArenaRun(
            name=self.name,
            latent_dimensions=6,
            estimates=estimates,
            ci95_low=low,
            ci95_high=high,
            mode_names=mode_names,
            runtime_seconds=float(runtime),
            memory_bytes=_history_bytes(pf),
            hybrid=True,
            smoothing=record_history,
            learned_parameters=self.learned_parameters,
            synthetic_truth_used_for_training=self.synthetic_truth_used_for_training,
            notes=self.notes,
        )


@dataclass(frozen=True)
class LearnedObservationArenaRunner:
    name: str = "CSRDM-6 learned observation"

    def run(self, dataset: ArenaDataset, *, particle_count: int, seed: int) -> ArenaRun:
        experiment = run_learning_experiment(
            dataset.truth,
            dataset.modes,
            dataset.observations,
            train_fraction=dataset.train_fraction,
        )
        runner = ParticleArenaRunner(
            name=self.name,
            observation_config=experiment.learned_config,
            learned_parameters=len(experiment.parameters),
            synthetic_truth_used_for_training=True,
            notes="six-state PF with 10 synthetic-trained observation calibration knobs",
        )
        return runner.run(dataset, particle_count=particle_count, seed=seed)


@dataclass(frozen=True)
class ReducedCProjectionArenaRunner:
    """A five-seat projection diagnostic derived from the full PF, not a retrained PF. 🪑🐣"""

    name: str = "CSRDM-5 reconstruct C"

    def run(self, dataset: ArenaDataset, *, particle_count: int, seed: int) -> ArenaRun:
        baseline = ParticleArenaRunner(name="hidden full-6 source").run(
            dataset,
            particle_count=particle_count,
            seed=seed,
        )
        split = dataset.split_index
        keep = [0, 1, 2, 4, 5]
        design = np.column_stack([np.ones(split), baseline.estimates[:split, keep]])
        target = dataset.truth[:split, 3]
        penalty = np.eye(design.shape[1]) * 1e-3
        penalty[0, 0] = 0.0
        beta = np.linalg.solve(design.T @ design + penalty, design.T @ target)

        estimates = baseline.estimates.copy()
        val_design = np.column_stack(
            [np.ones(len(dataset.truth) - split), baseline.estimates[split:, keep]]
        )
        estimates[split:, 3] = np.clip(val_design @ beta, 0.02, 0.98)

        low = baseline.ci95_low.copy() if baseline.ci95_low is not None else None
        high = baseline.ci95_high.copy() if baseline.ci95_high is not None else None
        if low is not None and high is not None:
            low[split:, 3] = np.nan
            high[split:, 3] = np.nan

        return ArenaRun(
            name=self.name,
            latent_dimensions=5,
            estimates=estimates,
            ci95_low=low,
            ci95_high=high,
            mode_names=baseline.mode_names,
            runtime_seconds=baseline.runtime_seconds,
            memory_bytes=baseline.memory_bytes,
            hybrid=True,
            smoothing=False,
            learned_parameters=6,
            synthetic_truth_used_for_training=True,
            notes="projection/reconstruction diagnostic; C reconstructed from other five states using synthetic train truth",
        )


@dataclass(frozen=True)
class StaticPriorArenaRunner:
    name: str = "static prior non-hybrid"

    def run(self, dataset: ArenaDataset, *, particle_count: int, seed: int) -> ArenaRun:
        del particle_count, seed
        start = perf_counter()
        center = np.array([0.68, 0.58, 0.80, 0.58, 0.28, 0.22], dtype=float)
        estimates = np.tile(center, (len(dataset.truth), 1))
        runtime = perf_counter() - start
        return ArenaRun(
            name=self.name,
            latent_dimensions=6,
            estimates=estimates,
            ci95_low=None,
            ci95_high=None,
            mode_names=None,
            runtime_seconds=float(runtime),
            memory_bytes=int(estimates.nbytes),
            hybrid=False,
            smoothing=False,
            learned_parameters=0,
            synthetic_truth_used_for_training=False,
            notes="constant prior; no observations, no mode model, no smoothing",
        )


def _mean_binary_log_loss(calibration) -> float:
    return float(np.mean([row.log_loss for row in calibration.binary]))


def score_arena_run(dataset: ArenaDataset, run: ArenaRun) -> tuple[dict[str, object], list[dict[str, object]]]:
    """Score compatible quantities and leave non-comparable ones explicitly blank. 🧭☕"""

    split = dataset.split_index
    truth = np.asarray(dataset.truth[split:], dtype=float)
    modes = np.asarray(dataset.modes[split:], dtype=int)
    observations = dataset.observations[split:]
    estimates = np.asarray(run.estimates[split:], dtype=float)

    state_rmse = np.sqrt(np.mean((estimates - truth) ** 2, axis=0))
    state_mae = np.mean(np.abs(estimates - truth), axis=0)
    state_rows = [
        {
            "model": run.name,
            "state": state,
            "RMSE": float(state_rmse[index]),
            "MAE": float(state_mae[index]),
        }
        for index, state in enumerate(STATE_KEYS)
    ]

    coverage = float("nan")
    if run.ci95_low is not None and run.ci95_high is not None:
        low = np.asarray(run.ci95_low[split:], dtype=float)
        high = np.asarray(run.ci95_high[split:], dtype=float)
        valid = np.isfinite(low) & np.isfinite(high)
        if np.any(valid):
            coverage = float(np.mean(((truth >= low) & (truth <= high))[valid]))

    mode_accuracy = float("nan")
    if run.mode_names is not None:
        predicted = run.mode_names[split:]
        actual = tuple(MODE_NAMES[RoutineMode(int(mode))] for mode in modes)
        mode_accuracy = float(np.mean([left == right for left, right in zip(predicted, actual)]))

    calibration = calibrate_dataset(estimates, modes, observations)
    true_r = relationship_index(truth)
    est_r = relationship_index(estimates)
    relationship_rmse = float(np.sqrt(np.mean((est_r - true_r) ** 2)))
    recovery_mask = modes == int(RoutineMode.RECOVERY)
    recovery_rmse = float("nan")
    if np.any(recovery_mask):
        recovery_rmse = float(
            np.sqrt(np.mean((est_r[recovery_mask] - true_r[recovery_mask]) ** 2))
        )

    summary = {
        "model": run.name,
        "latent_dimensions": run.latent_dimensions,
        "mean_state_RMSE": float(np.mean(state_rmse)),
        "mean_state_MAE": float(np.mean(state_mae)),
        "relationship_RMSE": relationship_rmse,
        "CI95_coverage": coverage,
        "mode_accuracy": mode_accuracy,
        "obs_NLL_given_true_mode": _mean_binary_log_loss(calibration),
        "obs_Brier_given_true_mode": calibration.mean_brier,
        "recovery_R_RMSE": recovery_rmse,
        "runtime_seconds": run.runtime_seconds,
        "memory_bytes": run.memory_bytes,
        "hybrid": run.hybrid,
        "smoothing": run.smoothing,
        "learned_parameters": run.learned_parameters,
        "synthetic_truth_used_for_training": run.synthetic_truth_used_for_training,
        "change_point_metric": "n/a for one stationary arena basket",
        "notes": run.notes,
    }
    return summary, state_rows


def run_model_arena(
    truth: np.ndarray,
    modes: np.ndarray,
    observations: Sequence[dict],
    *,
    particle_count: int = 500,
    seed: int = 20260908,
    train_fraction: float = 0.60,
    smoothing_lag: int = 12,
) -> tuple[list[dict[str, object]], list[dict[str, object]], tuple[ArenaRun, ...]]:
    """Let several tiny model families answer the exact same synthetic basket. 🗺️☕🐣"""

    truth = np.asarray(truth, dtype=float)
    modes = np.asarray(modes, dtype=int)
    if len(truth) < 60:
        raise ValueError("🗺️🐣 The arena needs at least 60 synthetic days.")
    if particle_count < 100:
        raise ValueError("🐣 The arena needs at least 100 particle friends per PF competitor.")
    if len(truth) != len(modes) or len(truth) != len(observations):
        raise ValueError("🐾 Every arena competitor must receive the exact same timeline length.")

    dataset = ArenaDataset(truth, modes, tuple(dict(obs) for obs in observations), train_fraction)
    no_memory = SharedContextMemoryConfig(
        accumulation_rate=0.0,
        decay_rate=0.0,
        process_noise=0.0,
    )
    runners: tuple[ArenaRunner, ...] = (
        ParticleArenaRunner(name="CSRDM-6 hand-set PF"),
        LearnedObservationArenaRunner(),
        ParticleArenaRunner(
            name=f"CSRDM-6 smoother lag-{smoothing_lag}",
            smoothing_lag=smoothing_lag,
            notes="six-state hybrid PF plus fixed-lag genealogical smoothing",
        ),
        ParticleArenaRunner(
            name="CSRDM-6 frozen context memory",
            memory_config=no_memory,
            notes="memory ablation: C reservoir is frozen instead of accumulating/decaying",
        ),
        ReducedCProjectionArenaRunner(),
        StaticPriorArenaRunner(),
    )

    summaries: list[dict[str, object]] = []
    state_rows: list[dict[str, object]] = []
    runs: list[ArenaRun] = []
    for index, runner in enumerate(runners):
        run = runner.run(dataset, particle_count=particle_count, seed=seed + 97 * index)
        summary, rows = score_arena_run(dataset, run)
        summaries.append(summary)
        state_rows.extend(rows)
        runs.append(run)

    return summaries, state_rows, tuple(runs)
