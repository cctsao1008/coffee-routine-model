# Design Principles Distilled from Routine History 📚🌱☕

Coffee Routine Model did not begin with six states and a Particle Filter.

It began with repeated modeling problems noticed around a small routine. The private history is **not** published here. What survives publicly is a set of generic design lessons that can be taught without exposing the source record.

> **Design inspiration != public evidence.**

This document records the distilled principles and, just as importantly, separates them from the later modeling choices built on top of them.

## Distillation contract 🧺

The transformation is intentionally lossy:

```text
private observable history
        ↓
recurring pattern class
        ↓ remove names / timestamps / company context / verbatim records
generic design problem
        ↓
public principle
        ↓
synthetic teaching example
        ↓
modeling choice
```

What does **not** cross the boundary:

- private message text or screenshots;
- private timestamps;
- company or workplace-identifying facts;
- private exports, files, or reconstructable event sequences;
- claims that the public personas are a verbatim record;
- hidden-state labels presented as facts about real people.

The private history motivated questions. It does not validate the equations.

## Three kinds of provenance 🧭

The principles below use three different provenance labels.

```text
History-supported pattern class
→ a recurring observable pattern was present in the private design history
→ the public repo keeps only the abstract pattern

Modeling interpretation
→ an engineering abstraction created to represent or test that pattern
→ useful design, not source truth

Epistemic guardrail
→ a later rule that prevents the model from claiming more than the evidence supports
```

These categories should not be collapsed into one word like “evidence.”

---

## 1. Observable event before interpretation 👀

**History-supported pattern class:** repeated routines contain things we can observe — invitation, opt-in, pass, delivery, acknowledgement, pause, update, resume.

**Public principle:**

```text
Event != meaning
Observation != latent state
```

Synthetic example:

```text
A: +1?
B: +
coffee delivered
acknowledgement observed
```

The adapter may record observable fields from that sequence. It may not jump directly to a claim about an internal motive.

**Modeling interpretation:** keep protocol events outside the latent state and let the observation model update uncertainty instead.

**Tutorial:** [`tutorial/01-a-tiny-routine.md`](tutorial/01-a-tiny-routine.md), [`tutorial/02-event-not-meaning.md`](tutorial/02-event-not-meaning.md)

---

## 2. Stable routine does not create entitlement 🌿

**History-supported pattern class:** continuity repeatedly coexisted with explicit participation choices, including clean `pass` branches.

**Public principle:**

```text
Continuity != obligation
Stable routine != default entitlement
```

A routine can be familiar and highly probable while still requiring room for each next choice.

**Modeling interpretation:** Voluntariness `V` remains a structural state instead of disappearing once the routine becomes stable.

**Epistemic guardrail:**

```text
high historical probability != future commitment
```

**Tutorial:** [`tutorial/03-pass-is-not-failure.md`](tutorial/03-pass-is-not-failure.md), [`tutorial/04-six-soft-states.md`](tutorial/04-six-soft-states.md)

---

## 3. `pass` is a valid branch, not a failure code ☕↩️

**History-supported pattern class:** a declined instance could be followed by ordinary continuation without special repair.

Synthetic teaching sequence:

```text
day A: +1? → +
day B: +1? → pass
day C: +1? → +
```

**Public principle:**

```text
Pass != failure
Choice != rupture
```

**Modeling interpretation:** an explicit voluntary pass can preserve the Voluntariness boundary without automatically penalizing Mutuality or declaring a broken routine.

The exact action coefficients remain model assumptions, not facts extracted from the source history.

**Tutorial:** [`tutorial/03-pass-is-not-failure.md`](tutorial/03-pass-is-not-failure.md)

---

## 4. Mutuality does not require 50/50 symmetry ⚖️

**History-supported pattern class:** the two sides could contribute in different recurring ways while both still participated in maintaining the routine.

Generic examples of different contributions:

```text
Side A
→ invite / deliver / notify / remember a callback

Side B
→ opt in / pass / acknowledge / synchronize an exception / close the loop
```

**Public principle:**

```text
Mutuality != identical actions
Mutuality != 50/50 accounting
```

**Modeling interpretation:** Mutuality `M` describes coupled participation, not a requirement that every observable action be mirrored.

This principle does **not** prove that any particular asymmetric exchange is fair or healthy. Those are separate questions.

**Tutorial:** [`tutorial/04-six-soft-states.md`](tutorial/04-six-soft-states.md), [`tutorial/05-actions-vs-observations.md`](tutorial/05-actions-vs-observations.md)

---

## 5. Disturbance is not automatically rupture 🌦️🌱

**History-supported pattern class:** busy periods, leave, missed execution, or other interruptions could occur and later be followed by an ordinary return.

**Public principle:**

```text
Disturbance != rupture
Interruption != structural failure
```

**Modeling interpretation:** temporary conditions deserve modes and recovery diagnostics rather than one dramatic permanent-state jump.

This is why the architecture separates:

```text
local mode
persistent regime change
recovery toward a nominal routine set
```

A return can also be ordinary. It does not need a special hidden story merely because an interruption happened first.

**Tutorial:** [`tutorial/07-weather-and-recovery.md`](tutorial/07-weather-and-recovery.md)

---

## 6. Repeated coordination can accumulate context 🧠🌱

**History-supported pattern class:** recurring shorthand, callbacks, exception handling, familiar handoff conventions, and lightweight accounting conventions can become easier to use over time.

**Public principle:**

```text
Repeated coordination can leave memory.
One quiet day does not erase accumulated context.
```

**Modeling interpretation:** Shared Context `C` is represented as a slow reservoir rather than a daily mood:

```text
C[t+1] = C[t] + eta * I[t] * (1 - C[t]) - lambda * C[t] + noise
```

The existence of recurring coordination motivated the memory question. The specific equation, `eta`, `lambda`, action weights, and process noise are model assumptions.

**Tutorial:** [`tutorial/06-shared-context-memory.md`](tutorial/06-shared-context-memory.md)

---

## 7. Implementation details can change while semantics stay stable 🔌☕

**History-supported pattern class:** concrete details around a routine could vary while the basic coordination grammar remained recognizable.

Synthetic analogy:

```text
implementation detail
→ café / bean / pickup detail changes

protocol semantics
→ ask / opt in or pass / deliver / acknowledge
```

**Public principle:**

```text
Implementation detail != system semantics
```

**Modeling interpretation:** the adapter owns domain vocabulary; the core receives generic actions and observations. This is the same separation-of-concerns idea used in ordinary software architecture.

**Tutorial:** [`tutorial/02-event-not-meaning.md`](tutorial/02-event-not-meaning.md), [`tutorial/05-actions-vs-observations.md`](tutorial/05-actions-vs-observations.md)

---

## 8. Missing or quiet evidence is not automatically zero 🌙

**History-supported pattern class:** not every day contains every clue, and quiet periods need not carry an explicit negative event.

**Public principle:**

```text
Missing clue != zero
Absence of an observation != observed negative event
```

A missing reaction is different from an observed negative reaction. A quiet day is different from an explicit `pass`. An unknown relation is different from a measured zero relation.

**Modeling interpretation:** observation fields may be `None`, and the likelihood skips clues that were not observed instead of inventing a value.

**Epistemic guardrail:**

```text
Undefined relationship != zero relationship
```

**Tutorial:** [`tutorial/01-a-tiny-routine.md`](tutorial/01-a-tiny-routine.md), [`tutorial/08-why-particles.md`](tutorial/08-why-particles.md)

---

## 9. One anomaly is not a new regime 🔎🌦️

**History-supported pattern class:** isolated unusual days and ordinary variation occurred inside a longer-running routine.

**Public principle:**

```text
Single anomaly = log it
Repeated generating shift = investigate a pattern
```

**Modeling interpretation:** local modes, change-point detection, smoothing, and recovery answer different questions. One slow reply or one unusual event should not automatically become a persistent structural story.

**Epistemic guardrail:**

```text
Mode != regime
Anomaly != change point
Change point != story conclusion
```

**Tutorial:** [`tutorial/07-weather-and-recovery.md`](tutorial/07-weather-and-recovery.md), [`tutorial/09-challenge-the-model.md`](tutorial/09-challenge-the-model.md)

---

## 10. Ordinary continuity and future undecidedness can coexist 🛤️

**History-supported pattern class:** repeated continuation can become ordinary without eliminating the possibility of a later `pass`, pause, or change.

**Public principle:**

```text
Ordinary continuity can be real.
Future choice can still remain open.
```

This avoids two opposite mistakes:

```text
repeated continuity → permanent commitment   ✗
future uncertainty  → current continuity is meaningless   ✗
```

**Epistemic guardrail:** posterior probability describes uncertainty under the model; it does not sign a contract for tomorrow.

**Tutorial:** [`tutorial/03-pass-is-not-failure.md`](tutorial/03-pass-is-not-failure.md), [`tutorial/08-why-particles.md`](tutorial/08-why-particles.md)

---

## 11. Probability, assumption, and undefined relation are different things 🧭

This principle is primarily an **epistemic guardrail**, not a claim extracted from one private event sequence.

```text
Probability != fact
Assumption != evidence
Undefined relationship != zero relationship
Not-yet-decided != false
```

It became necessary because a stochastic model can otherwise make uncertainty look more authoritative than it is.

The repository therefore uses:

```text
Observed
Probable
Assumed
Undefined
Not-yet-decided
```

See [`epistemic-status.md`](epistemic-status.md).

**Tutorial:** [`tutorial/08-why-particles.md`](tutorial/08-why-particles.md), [`tutorial/09-challenge-the-model.md`](tutorial/09-challenge-the-model.md), [`tutorial/10-let-the-model-lose.md`](tutorial/10-let-the-model-lose.md)

---

## What the history did **not** directly give us 🧪

The following are engineering constructions. They may have been motivated by the design problems above, but they are not facts read directly from the source history:

```text
exact six-state ontology P/M/V/C/E/F
numerical transition coefficients
action-effect coefficients
observation likelihood coefficients
Shared Context eta / lambda / noise values
Particle Filter particle count
95% interval calibration
change-point algorithm
recovery metric
model-arena scoring rules
```

Likewise:

```text
private observable pattern
!= validated latent-state label

useful synthetic benchmark
!= empirical human validation
```

This separation is deliberate. It lets design history explain **why a question mattered** without pretending it supplied the mathematical answer.

## Principle → architecture map 🗺️

| Distilled principle | Main architecture consequence |
|---|---|
| Event before interpretation | protocol adapter + observation model |
| Stable routine != entitlement | explicit Voluntariness `V` |
| Pass != failure | voluntary pass action / observation semantics |
| Mutuality != symmetry | coupled but role-different action vocabulary |
| Disturbance != rupture | hybrid modes + recovery diagnostics |
| Coordination can accumulate context | dedicated Shared Context `C` reservoir |
| Implementation detail != semantics | persona/domain layer outside generic core |
| Missing clue != zero | nullable observations + skipped likelihood terms |
| One anomaly != regime | modes separated from change-point logic |
| Continuity + undecided future can coexist | stochastic posterior, no future commitment claim |
| Probability != fact | explicit epistemic-status contract |

None of those arrows means “the source proved the implementation.” They mean “this recurring design problem motivated this engineering response.”

## Public review checklist 🐣

Before a future design-history lesson enters the repository:

- [ ] Can the lesson be stated without a name, timestamp, company fact, screenshot, or private quote?
- [ ] Is the recurring observable pattern separated from the later model interpretation?
- [ ] Is the synthetic example self-contained?
- [ ] Does the principle teach a reusable modeling problem rather than a private story detail?
- [ ] Are probabilities, assumptions, undefined relations, and future choices kept distinct?
- [ ] Does the lesson avoid inventing a new latent state just because the story sounds interesting?
- [ ] Could a reader understand the architecture lesson without reconstructing the source history?

If yes, the lesson can come outside and have coffee. ☕🐾

```text
Design inspiration != public dataset
Narrative richness != interpretive overreach
Story != evidence
Model != human
```
