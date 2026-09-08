from __future__ import annotations

import numpy as np

from coffee_brain.actions import RoutineActions
from coffee_brain.model import RoutineMode
from coffee_brain.recovery import (
    NominalRoutineSet,
    detect_recovery_events,
    summarize_recovery,
)


INSIDE = np.array([0.80, 0.70, 0.90, 0.75, 0.40, 0.10])
OUTSIDE = np.array([0.45, 0.40, 0.60, 0.40, 0.10, 0.50])
NOMINAL = NominalRoutineSet(INSIDE, np.array([0.10, 0.10, 0.08, 0.12, 0.18, 0.10]))


def test_nominal_set_is_a_cozy_region_not_one_magic_point():
    nearby = INSIDE + np.array([0.04, -0.03, 0.02, 0.05, -0.06, 0.03])

    assert NOMINAL.contains(INSIDE)
    assert NOMINAL.contains(nearby)
    assert NOMINAL.distance(nearby) == 0.0
    assert NOMINAL.distance(OUTSIDE) > 0.0


def test_one_day_recovery_gets_measured_without_calling_the_wobble_a_failure():
    states = np.array([INSIDE, OUTSIDE, OUTSIDE, INSIDE])
    modes = [RoutineMode.NORMAL, RoutineMode.BUSY, RoutineMode.RECOVERY, RoutineMode.NORMAL]

    events = detect_recovery_events(states, modes, NOMINAL)

    assert len(events) == 1
    event = events[0]
    assert event.disturbance_duration == 1
    assert event.recovered_index == 3
    assert event.recovery_time == 1
    assert event.repair_cost == 0.0
    assert event.natural_resume
    assert np.isclose(event.resilience, 0.5)


def test_slow_recovery_is_still_recovery_just_with_tiny_steps():
    states = np.array([INSIDE, OUTSIDE, OUTSIDE, OUTSIDE, OUTSIDE, INSIDE])
    modes = [
        RoutineMode.NORMAL,
        RoutineMode.BUSY,
        RoutineMode.RECOVERY,
        RoutineMode.RECOVERY,
        RoutineMode.RECOVERY,
        RoutineMode.NORMAL,
    ]

    event = detect_recovery_events(states, modes, NOMINAL)[0]

    assert event.recovery_time == 3
    assert event.recovered
    assert event.resilience < 0.5


def test_non_recovery_keeps_the_uncertainty_instead_of_inventing_a_happy_ending():
    states = np.array([INSIDE, OUTSIDE, OUTSIDE, OUTSIDE])
    modes = [RoutineMode.NORMAL, RoutineMode.LEAVE, RoutineMode.RECOVERY, RoutineMode.NORMAL]

    event = detect_recovery_events(states, modes, NOMINAL)[0]

    assert not event.recovered
    assert event.recovered_index is None
    assert event.recovery_time is None
    assert event.resilience == 0.0


def test_long_coordinated_leave_duration_is_separate_from_recovery_lag():
    states = np.array([INSIDE, OUTSIDE, OUTSIDE, OUTSIDE, INSIDE])
    modes = [
        RoutineMode.NORMAL,
        RoutineMode.LEAVE,
        RoutineMode.LEAVE,
        RoutineMode.LEAVE,
        RoutineMode.NORMAL,
    ]

    event = detect_recovery_events(states, modes, NOMINAL)[0]

    assert event.disturbance_duration == 3
    assert event.recovery_time == 0
    assert np.isclose(event.resilience, 1.0)


def test_explicit_repair_actions_are_counted_separately_from_natural_resume():
    states = np.array([INSIDE, OUTSIDE, OUTSIDE, INSIDE])
    modes = [RoutineMode.NORMAL, RoutineMode.BUSY, RoutineMode.RECOVERY, RoutineMode.NORMAL]
    actions = [
        RoutineActions(),
        RoutineActions(),
        RoutineActions(a_callback=1.0),
        RoutineActions(),
    ]

    event = detect_recovery_events(states, modes, NOMINAL, actions=actions)[0]

    assert event.repair_cost > 0.0
    assert not event.natural_resume
    assert event.resilience < 0.5


def test_recovery_summary_keeps_the_little_year_compact():
    one = detect_recovery_events(
        np.array([INSIDE, OUTSIDE, OUTSIDE, INSIDE]),
        [RoutineMode.NORMAL, RoutineMode.BUSY, RoutineMode.RECOVERY, RoutineMode.NORMAL],
        NOMINAL,
    )[0]
    two = detect_recovery_events(
        np.array([INSIDE, OUTSIDE, OUTSIDE, OUTSIDE]),
        [RoutineMode.NORMAL, RoutineMode.LEAVE, RoutineMode.RECOVERY, RoutineMode.NORMAL],
        NOMINAL,
    )[0]

    summary = summarize_recovery([one, two])

    assert summary.total_disturbances == 2
    assert summary.recovered_disturbances == 1
    assert np.isclose(summary.recovery_ratio, 0.5)
    assert summary.median_recovery_time == 1.0
