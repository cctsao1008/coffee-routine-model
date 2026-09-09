# Full Math 📐☕🧠

**Same model, all the gears.**

This page presents the complete mathematical view of CSRDM architecture `0.3`.

If the notation feels like too much at once, start with [`starter-math.md`](starter-math.md). The Starter page is a projection of this model, not a different model.

```text
Starter Math → understand the mathematical shape
Full Math    → inspect the complete equations
Architecture → inspect the software contract
```

## 1. The hidden routine state 🧺

The continuous latent state is:

```math
x_t=
\begin{bmatrix}
P_t & M_t & V_t & C_t & E_t & F_t
\end{bmatrix}^{T}
```

with:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

The model also carries one discrete routine mode:

```math
m_t\in\{Normal,Busy,Leave,Special,Recovery\}
```

So the hidden condition at time `t` is not only one six-number vector. It is a continuous state plus a discrete operating mode.

## 2. Known inputs and observable clues 🎮👀

CSRDM separates known actions from observation clues:

```text
a_t → observable actions that can affect the transition
z_t → observable clues used to update uncertainty
d_t → explicit known context / disturbance when available
```

This boundary matters:

```text
Action != intention
Observation != latent state
```

The controlled state-space contract is:

```math
x_{t+1}\sim p(x_{t+1}\mid x_t,m_t,a_t,d_t)
```

```math
m_{t+1}\sim p(m_{t+1}\mid m_t,x_t,a_t,d_t)
```

```math
z_t\sim p(z_t\mid x_t,m_t)
```

These three relationships are the mathematical skeleton.

## 3. Read the transition one piece at a time 🌦️

The first equation says:

> The next soft state depends probabilistically on the current soft state, current mode, known actions, and any explicit context the model is given.

The second says:

> The next operating mode is also uncertain. A Busy day can stay Busy, return to Normal, move toward Recovery, and so on according to transition probabilities.

The third says:

> Hidden state and mode influence which observable clues are more or less likely to appear.

CSRDM therefore combines continuous dynamics with discrete mode switching: a small stochastic hybrid model.

## 4. The mode transition table 🎲

The default estimator carries one five-mode transition matrix:

```math
T_{ij}=P(m_{t+1}=j\mid m_t=i)
```

The fixed matrix is the default structural baseline.

Optional context-aware transition logic may nudge those probabilities using declared state/action/context information, but it does not deterministically select the next mode.

```text
Mode != regime
Probability != fact
```

Synthetic scenarios may use different generating behavior. The estimator does not import the simulator's answer key.

```text
Synthetic World != Estimator Assumptions
```

## 5. Five states use ordinary transition dynamics; C owns memory 🧠🌱

`P / M / V / E / F` participate in the ordinary soft-state transition path.
Known actions can create small structural prototype effects, mode can change drift, and process noise preserves uncertainty.

`C = Shared Context` is deliberately different.

Its dedicated memory law is:

```math
C_{t+1}=C_t+\eta I_t(1-C_t)-\lambda C_t+w_t^C
```

where:

```text
η       → accumulation rate
I_t     → bounded Shared Context input from observable coordination actions
1-C_t   → saturation room
λ       → slow decay rate
w_t^C   → dedicated memory-process noise
```

The implementation intentionally keeps `C` out of ordinary target pull, generic mode drift, and generic process noise so two mechanisms do not compete to update the same state.

The input `I_t` is itself a structural prototype mapping from observable coordination actions, not a learned human constant.

## 6. Observation likelihoods: clues are not all the same shape 👀

The gentle equation:

```math
z_t=h(x_t)+v_t
```

is useful for intuition, but the implementation uses clue-specific likelihoods.

Conceptually:

```text
binary clues
→ Bernoulli-style probabilities

continuous clues
→ continuous likelihoods

missing clues
→ no invented zero measurement
```

The observation model contains hand-set structural prototype relationships between clues and latent states.
Those relationships are assumptions of the current model unless independently supported.

```text
Assumption != evidence
Undefined relationship != zero relationship
Missing clue != zero
```

The provenance audit for these relationships belongs to the model-documentation layer, not inside the equation itself.

## 7. Filtering: estimate a distribution, not a verdict 🐣

After observations arrive through time `t`, filtering asks for the posterior distribution over hidden state and mode:

```math
p(x_t,m_t\mid z_{1:t})
```

Known actions and explicit contexts are conditioned-on inputs to the transition process; the compact posterior notation suppresses them for readability.

CSRDM approximates this posterior with a Particle Filter.

Each particle carries one candidate:

```text
x_t
+
m_t
```

The filter cycle is:

```text
predict
→ score against observations
→ normalize weights
→ resample when needed
→ keep the new particle cloud
```

In more formal terms, particles approximate the filtering distribution rather than producing one exact hidden truth.

```text
Posterior certainty != model correctness
```

## 8. Importance weighting, in plain formal language ⚖️

Suppose particle `i` has predicted hidden state and mode `(x_t^(i),m_t^(i))`.
Its weight is updated in proportion to the observation likelihood:

```math
\tilde w_t^{(i)}\propto
w_{t-1}^{(i)}\,
p(z_t\mid x_t^{(i)},m_t^{(i)})
```

Then normalize:

```math
w_t^{(i)}=
\frac{\tilde w_t^{(i)}}{\sum_j \tilde w_t^{(j)}}
```

Particles that fit the observed clues better receive more posterior mass.

This still means **more plausible under the current model**, not “proved correct.”

## 9. Effective sample size and resampling 🐣🧺

Over time, a few particles can collect most of the weight while many contribute almost nothing.

A common diagnostic is effective sample size:

```math
ESS=\frac{1}{\sum_i (w_t^{(i)})^2}
```

When the particle cloud becomes too weight-degenerate, resampling creates a fresh equally weighted cloud by drawing more often from high-weight candidates.

Resampling does not create new evidence. It is a computational step for maintaining a useful approximation.

## 10. Smoothing: later clues can help earlier uncertainty 🔭

Filtering uses evidence available up to time `t`:

```math
p(x_t,m_t\mid z_{1:t})
```

Smoothing asks what we believe about time `t` after later observations are also available:

```math
p(x_t,m_t\mid z_{1:T})
```

The implementation uses particle ancestry and fixed-lag genealogical smoothing.

```text
Later evidence may update uncertainty.
Later evidence does not rewrite observed facts.
```

## 11. The complete flow on one page 🗺️

```text
Observable events
      ↓
Protocol Adapter
      ↓
known actions a_t        observation clues z_t
      │                         │
      ▼                         │
state / mode transition         │
(x_t,m_t) → (x_t+1,m_t+1)       │
      │                         │
      └────────────┬────────────┘
                   ▼
             Particle Filter
                   ↓
       p(x_t,m_t | z_1:t)
                   ↓
          optional smoothing
                   ↓
       p(x_t,m_t | z_1:T)
```

`C` uses its dedicated memory path inside the state transition.

## 12. Epistemic status still applies to every equation 🧭

A formal equation can look authoritative even when some relationships inside it are prototype assumptions.

Keep the statuses separate:

```text
Observed
→ events / measurements supplied to the model

Probable
→ posterior statements produced by inference

Assumed
→ structural transition / likelihood / coefficient choices

Undefined
→ relationships intentionally not specified

Not-yet-decided
→ future actions that have not occurred yet
```

```text
Probability != fact
Assumption != evidence
High historical probability != future commitment
```

## 13. What this page does not do 🙈

This is the mathematical model page, not the full implementation reference.

For code/config/public-boundary details, see [`../architecture.md`](../architecture.md).

For focused mechanisms and diagnostics, see:

- [`../action-aware-dynamics.md`](../action-aware-dynamics.md)
- [`../memory-garden.md`](../memory-garden.md)
- [`../smoothing-garden.md`](../smoothing-garden.md)
- [`../observability-garden.md`](../observability-garden.md)
- [`../calibration-bench.md`](../calibration-bench.md)

For the gentler route back up the ladder, return to [`starter-math.md`](starter-math.md).

Same model. All the gears. Still only a model. ☕📐🐣
