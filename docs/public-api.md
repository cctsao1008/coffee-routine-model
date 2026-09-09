# Public API — One Small Door ☕🚪🐣

This page is for callers who want to **use CSRDM without learning the repository's internal drawer layout first**.

The public rule is simple:

```text
story / protocol events
        ↓
CSRDM.step(...)
        ↓
CSRDMResult
        ↓
posterior + uncertainty
```

When you need more control, use `CSRDM.update(...)` with explicit generic observations and actions.

> **Small public surface is a feature. Silent mistakes are not.**

## 1. First cup ☕

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])

print(result.mean_by_state)
print(result.posterior.mode)
```

`result.posterior.mean` is still available when you want the raw six-element array.
For normal reading, the named view avoids six mystery numbers:

```text
predictability
mutuality
voluntariness
shared_context
state_sharing
friction
```

The result also exposes:

```text
result.ci95_by_state
result.mode_probabilities_by_name
result.observation
result.actions
result.step_index
result.transition_applied
```

These are posterior summaries, not measured human traits.

```text
Posterior != observed truth
```

## 2. Missing clues stay missing 🌱

Generic observations may omit a clue or set it to `None`:

```python
result = brain.update(
    {
        "reaction": 1,
        "tone_warmth": None,
        "response_delay_min": None,
    }
)
```

Both mean:

> this clue was not observed for this step.

They do **not** mean zero.

```text
Missing clue != zero
```

A completely empty observation basket is also valid when the model needs to advance without new observation evidence:

```python
result = brain.update({})
```

## 3. Public observation baskets are strict on purpose 👀🧺

The public facade rejects observation typos instead of quietly turning them into missing evidence.

For example:

```python
brain.update({"reacion": 1})
```

raises an error because `reacion` is not a known public field.

Binary clues accept only:

```text
0
1
None
```

Continuous clues have explicit ranges:

```text
tone_warmth       → 0 .. 1
response_delay_min→ finite and >= 0
```

This matters because a value such as `reaction=0.7` should not be silently truncated into a binary observation.

## 4. A measured delay already implies a reply ⏰💬

This is enough:

```python
result = brain.update({"response_delay_min": 4.2})
```

The public facade records:

```text
text_reply = 1
response_delay_min = 4.2
```

because a measured reply delay is already evidence that a reply occurred.

This combination is rejected:

```python
brain.update(
    {
        "text_reply": 0,
        "response_delay_min": 4.2,
    }
)
```

```text
No reply
!=
reply with a measured delay
```

## 5. Protocol contradictions get a visible no 🌿

The public API rejects combinations that cannot describe one protocol step, including:

```text
opt_in=1 + pass_event=1
pass_event=1 + routine_maintenance=1
opt_in=0 + routine_maintenance=1
invite=0 + an explicit opt-in/pass observation
```

This is input validation, not mind reading.

```text
Protocol grammar
!=
psychological interpretation
```

## 6. Known actions and timing 🎮☕

`CSRDM.update(...)` accepts generic action mappings:

```python
result = brain.update(
    {"reaction": 1},
    actions={
        "a_deliver": 1.0,
        "b_acknowledge": 1.0,
    },
)
```

The timing contract is:

```text
call t actions
→ drive the previous hidden state
→ into the current hidden state
→ then current observations score that state
```

The first call is special because there is no preceding hidden transition yet.

```python
first = brain.step(["+1?", "要"])
print(first.transition_applied)   # False

second = brain.step(["☕", "👍"])
print(second.transition_applied)  # True
```

The first call still records the parsed actions in `result.actions`; it simply has no previous transition on which to apply them.

```text
Action recorded
!=
transition existed
```

## 7. Context-aware mode transitions are explicit opt-in weather 🌦️🎲

The default estimator uses the fixed transition baseline.
Passing `transition_context` while context-aware transitions are disabled raises an actionable error instead of being silently ignored.

Enable the public default context model explicitly:

```python
from coffee_brain import (
    CSRDM,
    CSRDMConfig,
    DEFAULT_CONTEXT_TRANSITIONS,
)

brain = CSRDM(
    CSRDMConfig(
        transition=DEFAULT_CONTEXT_TRANSITIONS,
    )
)

brain.step(
    ["+1?", "要"],
    transition_context={"disturbance": 0.8},
)
```

Context remains known input, not an inferred private story.

```text
Context input != intention
```

## 8. Smoothing needs history before hindsight 🔭🐣

Enable smoothing before collecting the timeline:

```python
from coffee_brain import CSRDM, CSRDMConfig, SmoothingConfig

brain = CSRDM(
    CSRDMConfig(
        smoothing=SmoothingConfig(enabled=True, lag=3),
    )
)

for events in (
    ["+1?", "要"],
    ["☕", "👍"],
    ["+1?", "pass"],
):
    brain.step(events)

hindsight = brain.smooth()
```

Calling `smooth()` on a model that did not enable smoothing gives an error that points back to `SmoothingConfig(enabled=True, ...)`.

Later clues may change earlier posterior uncertainty.
They do not rewrite observed events.

```text
Smoothing != rewriting history
```

## 9. Learning is a bench, not hidden online adaptation 🎚️🥄

`LearningConfig` exists in the architecture recipe tree, but `CSRDM` itself does **not** silently learn while it runs.

Trying to construct the online estimator with:

```python
LearningConfig(enabled=True)
```

is rejected with guidance toward the bounded learning bench:

```bash
python -m tiny_tools.learn_parameters
```

This keeps the contract explicit:

```text
Online inference
!=
parameter learning
```

## 10. Reproducible recipe cards 🛂☕

For reproducible settings:

```python
from coffee_brain import (
    CSRDMConfig,
    ExperimentSpec,
    InferenceConfig,
    config_snapshot,
)

config = CSRDMConfig(
    inference=InferenceConfig(
        particle_count=6000,
        seed=20260908,
    )
)

print(config_snapshot(config))

spec = ExperimentSpec(
    name="tiny-check",
    scenario="cozy-normal-year",
    days=365,
    config=config,
)

print(spec.fingerprint)
```

```text
Same recipe
→ same fingerprint
```

Display labels do not define model identity.

## 11. Where to go next 🗺️

```text
Want protocol semantics → tiny-protocol-bridge.md
Want the math          → math/starter-math.md / math/full-math.md
Want architecture      → architecture.md
Want estimator details → tutorial/08-why-particles.md
Want diagnostics       → docs/README.md
```

The public API should make the ordinary path boring in the good way:

```text
known input
→ visible validation
→ explicit result
→ uncertainty preserved
```

Tiny door. No secret trapdoors. ☕🚪🐣
