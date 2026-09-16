# References 📚☕🐣

**Tiny model, visible assumptions, honest math.**

This page explains where the main inference ideas in `coffee-routine-model` come from, and where CSRDM adds its **own modeling choices**.

It is a bookshelf, not a second specification.

```text
Math docs       → define the mathematical model
Architecture    → defines the software contract
Code + tests    → prove the current implemented behavior
References      → show where the inference ideas came from
```

## Why keep a bookshelf? 🌱

CSRDM has two layers that are easy to accidentally mix together:

```text
general inference machinery
→ Bayesian filtering
→ Particle Filter / Sequential Monte Carlo
→ importance weighting
→ ESS / resampling
→ smoothing

project-specific modeling choices
→ P / M / V / C / E / F
→ routine modes
→ Shared Context memory
→ observation relationships
→ action effects
```

The first layer has a long statistics / robotics literature behind it.
The second layer is where this project makes explicit modeling choices for a shared routine.

```text
Literature-backed inference
!=
literature-proved routine ontology
```

A good reference can support an algorithm without magically proving every variable wrapped around it.

## The five-source reading ladder 🪜📚

If Particle Filters are new, there is no need to begin with the densest paper.

```text
I want the friendly picture
→ Particle Filter Made Simple
→ Sridharan's Particle Filter slides

I want the compact math
→ Greg Mori's notes

I want the full SMC / smoothing framework
→ Doucet & Johansen

I want a specialized real-time extension
→ Kwok, Fox & Meila
```

Same family of ideas. Different depth. Different job.

---

## 1. A Tutorial on Particle Filtering and Smoothing: Fifteen Years Later 📐🐣

**Arnaud Doucet · Adam M. Johansen — Version 1.1, December 2008**

This is the **main theory shelf** for the current reference set.

### Useful for

- hidden Markov / state-space model framing;
- Monte Carlo and importance sampling;
- Sequential Importance Sampling (SIS);
- Sequential Monte Carlo (SMC);
- resampling;
- effective sample size (ESS);
- adaptive resampling;
- particle filtering;
- particle smoothing.

The tutorial also shows that SMC is broader than one particular Particle Filter recipe. That is useful because CSRDM should not confuse **one implementation** with **the entire method family**.

### Used here to understand

- the general inference skeleton behind `coffee_brain/particles.py`;
- why particle weights approximate a posterior distribution;
- why ESS is useful as a degeneracy signal;
- why resampling is a numerical maintenance step rather than new evidence;
- the filtering-vs-smoothing distinction used by `coffee_brain/smoothing.py` and `docs/math/full-math.md`.

### Does not justify by itself

- why CSRDM has exactly six continuous states;
- what `P / M / V / C / E / F` should mean;
- the five routine-mode names;
- any CSRDM observation or action coefficient;
- any claim about a real person's internal state.

```text
Strong inference reference
!=
human-behavior ground truth
```

---

## 2. The Particle Filter 🧮☕

**Greg Mori — Particle Filter Notes**

This is the **compact math shelf**.

It gets quickly to the central idea: when the filtering distribution cannot be kept in a neat linear-Gaussian form, represent it with weighted samples instead.

### Useful for

- recursive Bayesian filtering;
- particle representations of a posterior;
- importance sampling;
- proposal distributions;
- likelihood weighting;
- the advantage of particles for complicated or multimodal posteriors;
- the high-dimensional cost of Particle Filters.

### Used here to understand

- why a particle is one candidate hidden state, not one detected fact;
- why the observation likelihood changes particle weight;
- why proposal quality matters even when the public CSRDM API hides that machinery.

### Does not justify by itself

- CSRDM state semantics;
- coffee-event meanings;
- action semantics;
- routine-mode semantics;
- person-level interpretation.

```text
Particle hypothesis
!=
private human truth
```

---

## 3. Particle Filter Made Simple: A Step-by-Step Beginner-friendly Guide 🌱🐣

**Sahil Rajesh Dhayalkar — arXiv:2511.01281v1, 3 November 2025**

This is the **friendly teaching shelf**.

Its strongest contribution to this project is not a new CSRDM algorithm. It is the clear progression from intuition to implementation:

```text
prediction
→ weighting
→ normalization
→ resampling
```

### Useful for

- why Particle Filters are useful beyond linear / Gaussian assumptions;
- the “cloud of weighted guesses” intuition;
- one-dimensional and two-dimensional worked examples;
- ESS intuition;
- adaptive resampling;
- simple Python implementation patterns.

### Used here to understand

- how to explain the inference loop without making the reader climb a wall of notation first;
- how a posterior particle cloud can move, spread, concentrate, and resample;
- why `ESS` is easier to understand as “how many particles are still doing useful work?” than as a mysterious formula.

### Does not define

- the canonical CSRDM math;
- the architecture contract;
- CSRDM coefficients;
- CSRDM's latent-state ontology.

```text
Friendly explanation
!=
second architecture authority
```

---

## 4. Particle Filters — Non-parametric Bayes Filter Implementation 🤖☕

**Mohan Sridharan — University of Edinburgh**

This is the **picture-and-robot shelf**.

The slides make Particle Filters easy to see: a cloud of samples moves under the motion model, observations make some samples more plausible, and resampling concentrates effort where posterior mass lives.

### Useful for

- non-parametric Bayes filtering intuition;
- importance sampling;
- motion / observation update pictures;
- systematic resampling;
- mobile-robot localization examples;
- practical limitations such as sampling variance and particle deprivation.

### Used here to understand

- what resampling is doing visually;
- why systematic resampling is a practical low-variance choice;
- why “many weighted possibilities” is often a better mental model than “one magic state estimate.”

### Does not imply

- that CSRDM is a robotics-localization problem;
- that a shared routine is literally a robot pose;
- that localization semantics transfer into human semantics.

The connection is mathematical, not literal.

```text
Same inference tool
!=
same problem domain
```

---

## 5. Real-time Particle Filters ⏱️🐣

**Cody Kwok · Dieter Fox · Marina Meila**

This is the **advanced real-time shelf**.

The paper starts from a specific engineering problem:

> What happens when observations arrive faster than a Particle Filter can perform full updates?

A common shortcut is to skip sensor readings. The paper instead distributes samples across observations in an estimation window and represents the result as a **mixture of sample sets**. It then adjusts mixture weights so the approximation stays close to the fuller posterior it would like to compute.

### Useful for

- computation-limited Particle Filters;
- observation-rate vs filter-update-rate mismatch;
- mixtures of sample-set beliefs;
- allocating computation toward more informative observations;
- thinking about real-time inference as a resource-allocation problem.

### Relevance to CSRDM

It is a useful reference **if** CSRDM ever develops a measured problem where observation flow exceeds available inference time.

That is not the current architecture.

```text
Interesting advanced direction
!=
feature request
```

### Current implementation status

**Reference only — not implemented.**

The current `CoffeeParticleFilter` follows a bootstrap-style Particle Filter loop, not the RTPF mixture-of-sample-sets architecture.

No reader should infer RTPF support merely because this paper appears on the shelf.

---

## What CSRDM currently implements 🛠️☕

At the inference layer, the current code follows a small bootstrap-style Particle Filter skeleton:

```text
predict hidden state / mode
        ↓
score observed clues
        ↓
importance reweight
        ↓
normalize
        ↓
summarize posterior
        ↓
check ESS
        ↓
systematic resampling when needed
```

The implementation also supports particle-history recording for genealogical smoothing.

Main implementation doors:

- [`../coffee_brain/particles.py`](../coffee_brain/particles.py) — filtering, weights, ESS, posterior summaries, systematic resampling;
- [`../coffee_brain/smoothing.py`](../coffee_brain/smoothing.py) — particle-history / genealogical smoothing;
- [`math/full-math.md`](math/full-math.md) — canonical mathematical view;
- [`architecture.md`](architecture.md) — architecture and public/internal boundaries.

The references explain the **method family**. The repository still decides its own exact implementation contract.

---

## Provenance map 🗺️☕✨

This table is the short answer to the most important question:

> **Which parts are established inference machinery, and which parts are CSRDM choices?**

| Component | Provenance status | Current CSRDM status |
|---|---|---|
| Bayesian filtering | **Literature-backed** | used as the inference foundation |
| Particle representation of the posterior | **Literature-backed** | implemented |
| Sequential Monte Carlo / bootstrap-style PF | **Literature-backed** | implemented |
| Importance / likelihood weighting | **Literature-backed** | implemented |
| Effective sample size (ESS) | **Literature-backed** | implemented |
| Systematic resampling | **Literature-backed** | implemented |
| Particle smoothing | **Literature-backed method family** | genealogical smoothing implemented |
| Continuous hidden state + discrete mode | **Standard state-space / switching-model pattern + CSRDM specialization** | implemented |
| `P / M / V / C / E / F` | **CSRDM modeling choice** | architecture `0.3` baseline |
| `Normal / Busy / Leave / Special / Recovery` | **CSRDM modeling choice** | architecture `0.3` baseline |
| Shared Context `C` memory law | **CSRDM-designed mechanism** | implemented |
| Observation relationships / coefficients | **CSRDM prototype assumptions unless separately supported** | implemented and audited separately |
| Action-effect relationships / coefficients | **CSRDM prototype assumptions** | implemented |
| Context-aware transition recipe | **CSRDM modeling mechanism** | optional implementation path |
| RTPF mixture-of-sample-sets inference | **Literature-backed advanced method** | **not implemented** |

For clue-to-state provenance specifically, use [`observation-provenance.md`](observation-provenance.md). That page asks a different question: **what kind of claim is each observation relationship?**

```text
Literature provenance  → where the inference machinery came from
Observation provenance → what kind of CSRDM clue relationship is being claimed
```

---

## One tiny example: what a paper can and cannot buy us 🫘📐

Suppose the filter sees an observation and gives some particles more weight.

Particle Filter literature supports the general operation:

```math
\tilde w_t^{(i)} \propto
w_{t-1}^{(i)}\,p(z_t\mid x_t^{(i)},m_t^{(i)})
```

But the literature does **not** automatically tell CSRDM what `z_t` should mean or which state a particular coffee event should influence.

Those are separate questions:

```text
How do we update probability?
→ inference literature helps

What does this observation mean inside CSRDM?
→ project modeling assumption / provenance question
```

Keeping those questions separate is the whole point of this page.

---

## Tiny honesty box 🧭🐣

A formal method can be well established while the model wrapped around it is still experimental.

That is normal.

The important part is to say which is which.

```text
Probability != fact
Posterior != human truth
Assumption != evidence
Good math != automatic ontology validation
Model the routine, not the person
```

A narrow claim that keeps its boundaries is more useful than a grand claim that hides them.

---

## Where to go next 🚪☕

If you want the gentle model story:

- [`how-the-coffee-works.md`](how-the-coffee-works.md)
- [`tutorial/README.md`](tutorial/README.md)

If you want the equations:

- [`math/starter-math.md`](math/starter-math.md)
- [`math/full-math.md`](math/full-math.md)

If you want implementation contracts:

- [`architecture.md`](architecture.md)
- [`public-api.md`](public-api.md)

If you want assumption / claim status:

- [`epistemic-status.md`](epistemic-status.md)
- [`observation-provenance.md`](observation-provenance.md)

If you want the actual executable evidence:

- [`../coffee_brain/`](../coffee_brain/)
- [`../tests/`](../tests/)

---

## Non-goals 🙈📚

This page does **not** try to:

- become a complete Particle Filter textbook;
- duplicate Full Math or Architecture;
- convert every citation in the source papers into a repository bibliography;
- claim that Particle Filter literature validates the CSRDM state ontology;
- turn a promising research method into an implemented feature by citation alone;
- hide CSRDM-specific assumptions behind academic-looking notation.

```text
Reference map
!=
second source of truth
```

Same tiny coffee brain. Now the bookshelf has labels. ☕📚🐣
