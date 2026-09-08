# Action-Aware Tiny Coffee Dynamics ☕🎮🧠

The first version of the coffee brain mostly did this:

```text
hidden state
    ↓
observed clues
    ↓
Particle Filter
```

That is useful, but it leaves out one important thing:

> Observable actions can also move the next hidden state.

So the controlled version keeps three little layers apart:

```text
actions
   ↓
hidden state ──→ next hidden state
   ↓
observations
```

## Tiny controlled equation ✨

```text
x[t+1] ~ p(x[t+1] | x[t], m[t], a[t], d[t])
z[t]   ~ p(z[t]   | x[t], m[t])
```

The current implementation uses small structural prototype action effects inside the state transition.

They are **not learned human coefficients**.
They are inspectable assumptions that can later be calibrated or replaced.

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

These are generic roles.
No real names belong in the public model. ☕🐾

## Pass is not a failure 🌿

One deliberate modeling choice is:

```text
b_pass_choice -> may preserve Voluntariness
```

A voluntary pass does not secretly subtract Mutuality just because nothing was delivered that day.

That keeps this rule alive inside the transition model:

```text
Continuity != obligation
Pass != rupture
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
The point is that the model can represent **coupled action effects explicitly** instead of smuggling them into observation likelihoods.

## Protocol bridge 🎮➡️👀

`coffee_brain.protocol_adapter` now exposes:

```python
from coffee_brain.protocol_adapter import coffee_to_step

step = coffee_to_step(["+1?", "+", "☕", "👍"])

step.actions
step.observation
```

The action basket and observation basket are separate objects.

The older observation fields remain available for backward compatibility while the controlled model grows up one tiny step at a time. 🌱

## Particle Filter timing 🐣

`CoffeeParticleFilter.update(obs, actions=...)` treats the supplied action basket as the known controls that moved the system from the **previous** step toward the current observation.

So:

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

On the very first update there is no previous transition yet, so the action basket is ignored for that first step.

## Important tiny boundaries 🧠✨

```text
Action != intention.
Observation != internal truth.
Structural coefficient != learned fact.
```

The model is allowed to know that an observable action happened.
It is still not allowed to invent why somebody did it. XD
