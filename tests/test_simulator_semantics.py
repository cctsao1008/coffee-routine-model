from __future__ import annotations

import numpy as np

from coffee_brain.scenarios import get_scenario, scenario_names
from tiny_tools.simulate import DEFAULT_SEED, generate_truth, observe


def test_synthetic_observations_respect_protocol_grammar_across_weather():
    """The synthetic exam may be noisy, but it should not contradict its own protocol. ☕🧭"""

    for scenario_index, scenario_name in enumerate(scenario_names()):
        scenario = get_scenario(scenario_name)
        rng = np.random.default_rng(DEFAULT_SEED + scenario_index)
        truth, modes = generate_truth(180, rng, scenario)
        observations = [observe(truth[t], modes[t], rng, scenario) for t in range(len(truth))]

        for obs in observations:
            invite = int(obs["invite"])
            opt_in = int(obs["opt_in"])
            text_reply = int(obs["text_reply"])
            maintenance = int(obs["routine_maintenance"])
            pass_event = int(obs["pass_event"])

            assert not (opt_in and pass_event)
            assert invite or not (opt_in or pass_event)
            assert text_reply or not (opt_in or pass_event)
            assert opt_in or not maintenance
