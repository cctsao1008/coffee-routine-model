# Starter Math 🌱🧮☕

**CSRDM, one sip at a time.**

This page is the first mathematical view of the model.

It is not a second simplified model.
It is a **pedagogical projection** of the same CSRDM described in [`full-math.md`](full-math.md) and implemented by architecture `0.3`.

```text
Starter Math
= fewer symbols, same meaning
```

## 1. Start with one ordinary question ☕

Suppose we observe a small repeated routine:

```text
invite
→ opt-in / pass
→ delivery when applicable
→ acknowledgment
→ sometimes busy / leave / resume
```

We can see those events.

But we cannot directly see things such as:

```text
How predictable is the routine right now?
How much shared context has accumulated?
How much friction is present?
```

So the first mathematical idea is simple:

> **The thing we want to estimate is hidden.**

## 2. Put the six hidden properties in one basket 🧺

CSRDM uses six soft state variables:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

Put them together:

```math
x_t=
\begin{bmatrix}
P_t & M_t & V_t & C_t & E_t & F_t
\end{bmatrix}^{T}
```

Read `x_t` as:

> **our hidden routine-state basket at time `t`.**

These values belong to the model of the routine.
They are not direct measurements of either person.

```text
Observation != latent state
Model != human
```

## 3. Hidden state can change over time 🌦️

Yesterday's routine state influences today's state.
Known actions can also matter.
And some uncertainty always remains.

For the Starter view, write that as:

```math
x_{t+1}=f(x_t,a_t)+w_t
```

Plain-language reading:

```text
next hidden state
=
what the model expects from the current state and known actions
+
a little uncertainty
```

where:

```text
x_t → current hidden state
a_t → known observable actions
w_t → process uncertainty / disturbance
```

This equation deliberately hides some machinery.
The Full Math page restores discrete mode `m_t` and explicit context / disturbance `d_t`.

```text
Starter view != different model
```

## 4. We still cannot measure `x_t` directly 👀

What we actually receive is an observation basket:

```text
invite
opt_in
pass_event
reaction
state_share
response delay
resume signal
...
```

Call that basket:

```math
z_t
```

A gentle observation equation is:

```math
z_t=h(x_t)+v_t
```

Plain-language reading:

> The hidden state influences what clues are likely to appear, but observations are noisy and incomplete.

`v_t` stands for observation uncertainty in this gentle view.

The real implementation does not treat every clue as one Gaussian number. Some clues are binary, some continuous, some missing, and the Full Math page keeps that distinction visible.

```text
Missing clue != zero
Probability != fact
```

## 5. So the answer should be a probability, not a verdict 🐣

Because `x_t` is hidden, the model does not produce a magical exact truth.

Instead it asks:

```math
p(x_t\mid z_{1:t})
```

Read this as:

> **Given all observations from the beginning through time `t`, which hidden routine states are currently more plausible?**

That is the main idea behind filtering.

The Particle Filter is one practical way to approximate this probability distribution with many small candidate states.

```text
one hard guess
      ↓ replace with
many weighted possibilities 🐣🐣🐣
```

You do not need the algorithm yet to understand the mathematical idea.

## 6. Shared Context gets one special memory cup 🧠🌱

`C = Shared Context` should not forget like an ordinary daily variable.

Repeated coordination can build context slowly, while quiet time should decay it slowly rather than erase it instantly.

CSRDM uses:

```math
C_{t+1}
=
C_t
+\eta I_t(1-C_t)
-\lambda C_t
+w_t^C
```

Read it one piece at a time:

```text
C_t
→ what the routine already remembers

+ η I_t (1 - C_t)
→ new context can accumulate, but there is less room near the top

- λ C_t
→ old context can fade slowly

+ w_t^C
→ a little memory-process uncertainty
```

`I_t` is bounded input derived from observable coordination actions.

The important idea is:

```text
one quiet day
!=
all shared context disappeared
```

## 7. What did we leave out on purpose? 🧺

Starter Math compresses the full model so the main relationships stay visible.

It does **not** show in full detail:

```text
discrete routine mode m_t
explicit context / disturbance d_t
mode-conditioned transition probabilities
mixed Bernoulli / continuous observation likelihoods
action-coupling details
Particle Filter weighting / resampling
fixed-lag smoothing
observability / calibration diagnostics
```

Nothing was deleted from CSRDM itself.
Those pieces are simply behind the next door.

## 8. The five equations worth remembering ☕

If you remember only the mathematical spine, remember these:

```math
x_t=[P_t,M_t,V_t,C_t,E_t,F_t]^T
```

```math
x_{t+1}=f(x_t,a_t)+w_t
```

```math
z_t=h(x_t)+v_t
```

```math
p(x_t\mid z_{1:t})
```

```math
C_{t+1}=C_t+\eta I_t(1-C_t)-\lambda C_t+w_t^C
```

Together they say:

```text
there is a hidden routine state
→ it changes over time
→ we only see noisy clues
→ so we estimate probabilities
→ one state owns slow memory
```

That is the mathematical heart of CSRDM before the gears are exposed.

## 9. Ready for all the gears? 📐

Continue to [`full-math.md`](full-math.md).

If you would rather understand Particle Filtering intuitively first, take the little chicken path to [`../tutorial/08-why-particles.md`](../tutorial/08-why-particles.md). 🐣
