# Action-Aware Tiny Coffee Dynamics ☕🎮🧠

## Why this exists

The first simple estimator mostly looked like:

```text
hidden state
    ↓
observed clues
    ↓
Particle Filter
```

That is useful, but it leaves out one important modeling role:

> **Observable actions can help move the next hidden state, while observations provide evidence about the state we cannot see directly.**

So the controlled model keeps those roles separate.

```text
actions
   ↓
hidden state ──→ next hidden state
                     ↑
                observations
```

This is the deeper version of tutorial chapter [`tutorial/05-actions-vs-observations.md`](tutorial/05-actions-vs-observations.md).

## Tiny controlled equations ✨

```math
x_{t+1}\sim p(x_{t+1}\mid x_t,m_t,a_t,d_t)
```

```math
z_t\sim p(z_t\mid x_t,m_t)
```

Read the symbols as:

```text
x_t → hidden routine-state vector at time t
m_t → hidden routine mode
a_t → known observable action input
d_t → explicit known context / disturbance
z_t → observation clue basket
```

The current implementation uses small structural prototype action effects inside the state transition.

They are **not learned human coefficients**.
They are inspectable model assumptions.

## The two little action baskets 🧺

Role A:

```text
a_invite
a_deliver
a_notify
a_callback
a_boundary_preserving
```

Role B:

```text
b_opt_in
b_pass_choice
b_acknowledge
b_exception_sync
b_closure
```

These are generic action roles.

Synthetic persona names may appear in README/tutorial/examples for readability, but they are translated into generic semantics before entering the core.

```text
Persona at the edge
Generic actions in the center
```

## Pass is not a failure 🌿

One deliberate modeling choice is:

```text
b_pass_choice → may preserve Voluntariness
```

A voluntary pass does not secretly subtract Mutuality just because nothing was delivered that day.

That keeps these rules alive inside the transition model:

```text
Continuity != obligation
Pass != failure
```

## Coupled little moments ☕🤝

Some actions can matter differently when they occur together.

For example:

```text
deliver + acknowledge
boundary-preserving + pass
notify + exception sync
```

The current prototype includes small interaction terms for those combinations.

The point is not that the coefficients are universal.
The point is that the model can represent **coupled action effects explicitly** instead of hiding them inside observation likelihoods.

## Protocol bridge 🎮➡️👀

`coffee_brain.protocol_adapter` exposes one combined step:

```python
from coffee_brain.protocol_adapter import coffee_to_step

step = coffee_to_step(["+1?", "+", "☕", "👍"])

step.actions
step.observation
```

The action basket and observation basket are separate objects.

Missing clues remain missing, and contextual ambiguity is handled by the adapter rather than by person-specific compatibility keys inside the Particle Filter.

## Particle Filter timing 🐣

`CoffeeParticleFilter.update(obs, actions=...)` treats the supplied action basket as the known controls associated with the transition from the **previous** step toward the current observation.

```text
previous posterior
      +
known actions
      ↓
predicted current state
      +
current observations
      ↓
current posterior
```

On the very first update there is no previous transition yet, so there is no earlier state for that action basket to move forward from.

This temporal alignment is an architecture invariant. A mathematically valid off-by-one implementation would still represent the wrong model semantics.

## Important tiny boundaries 🧠✨

```text
Action != intention
Observation != latent state
Structural coefficient != learned fact
Persona != core ontology
```

The model may know that an observable action happened.
It is still not allowed to invent why somebody did it.
