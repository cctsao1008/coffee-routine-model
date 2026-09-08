import numpy as np

from coffee_brain.model import RoutineState, clip_state, relationship_index


def test_tiny_state_can_pack_itself_into_an_array():
    state = RoutineState(0.8, 0.7, 0.9, 0.6, 0.4, 0.1)
    packed = state.as_array()
    assert packed.shape == (6,)
    assert np.allclose(packed, [0.8, 0.7, 0.9, 0.6, 0.4, 0.1])


def test_soft_states_stay_inside_the_little_fence():
    wiggly = np.array([-2.0, 0.2, 0.8, 1.7, 4.2, -0.5])
    clipped = clip_state(wiggly)
    assert np.all(clipped >= 0.01)
    assert np.all(clipped <= 0.99)


def test_relationship_index_matches_its_tiny_recipe():
    state = np.array([0.80, 0.70, 0.90, 0.60, 0.40, 0.10])
    expected = 0.18*0.80 + 0.25*0.70 + 0.20*0.90 + 0.16*0.60 + 0.11*0.40 + 0.10*(1.0-0.10)
    assert np.isclose(relationship_index(state), expected)


def test_relationship_index_can_follow_a_whole_tiny_parade():
    states = np.array([
        [0.70, 0.60, 0.90, 0.50, 0.30, 0.20],
        [0.80, 0.70, 0.90, 0.60, 0.40, 0.10],
        [0.75, 0.65, 0.85, 0.55, 0.35, 0.15],
    ])
    scores = relationship_index(states)
    assert scores.shape == (3,)
    assert np.all(np.isfinite(scores))
