# 05 — Actions and Observations Are Different 🎮👀

Suppose one synthetic step contains:

```text
invite
opt-in
delivery
reaction
```

A first implementation might throw all four into one observation basket.

That is convenient, but it mixes two jobs.

## Two roles for observable events

Some events are known controls that can help move the modeled routine from the previous state toward the next state.

Other clues are evidence used to update uncertainty about the state we cannot observe directly.

So CSRDM separates:

```text
a_t = known action basket at time t
z_t = observation clue basket at time t
```

Conceptually:

```text
previous hidden state
        +
known actions a_t
        ↓
predicted current hidden state
        +
observed clues z_t
        ↓
updated posterior
```

## Why this distinction matters

If an action is hidden inside the observation likelihood, the model can confuse:

```text
"this happened and may influence the next state"
```

with:

```text
"this happened and is evidence about the current state"
```

Those are different causal roles in the model architecture.

A delivery can be represented as a known action. A later acknowledgment or response delay can act as evidence.

The exact mapping is a modeling choice, but the boundary should remain visible.

## Actions are still not intentions

Knowing that an action occurred does not reveal why it occurred.

```text
Action != intention
```

The model may use:

```text
invite = observed
pass_choice = observed
notify = observed
acknowledge = observed
```

It may not silently upgrade those facts into:

```text
"the person wanted X"
"the person felt Y"
```

unless such a claim is separately supported by explicit evidence — and even then it remains outside the generic CSRDM ontology.

## Timing matters

`CoffeeParticleFilter.update(obs, actions=...)` treats the supplied action basket as the known controls associated with the transition from the **previous** posterior toward the current observation.

Using the same notation as the math docs:

```text
x_{t-1} -- a_t --> predicted x_t
                         ↓
                        z_t
                         ↓
                   posterior x_t
```

Here `x_t` is the hidden routine-state vector at time `t`.

On the first update there is no previous transition yet, so there is no earlier state for those actions to move forward from.

That small timing detail is worth documenting because an off-by-one interpretation can produce a mathematically valid but semantically wrong model.

See [`../action-aware-dynamics.md`](../action-aware-dynamics.md) for the implementation details.

## Another useful correction

Initial intuition:

```text
more observed activity = stronger hidden state
```

Correction:

```text
some activity is an input
some activity is evidence
missing activity may be missing data
context determines the role
```

A state-space model becomes clearer when those roles are explicit.

## The next question

The state vector now has a special component, `C = Shared Context`.

If every state simply drifts and mean-reverts in the same way, accumulated context can disappear too quickly.

So the next design question is:

> **Should every hidden state forget at the same speed?**

Continue to [`06-shared-context-memory.md`](06-shared-context-memory.md).
