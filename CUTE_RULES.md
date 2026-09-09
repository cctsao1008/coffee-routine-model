# The Cute Rules ☕🐾✨

This repository has one extremely serious rule:

> **Everything must be cute.**

Yes. Everything. XD

But there is a second rule hiding inside the first one:

> **Cute != sloppy.**

The coffee can wear tiny paws.  
The math still has to work. 🧠✨

---

## 1. The whole repo lives in the same tiny coffee universe ☕🌱

Cute is not just a README decoration.

It applies to the whole project:

- `README.md` ☕
- docs 📖
- commit messages 🐾
- code comments and docstrings 🧠✨
- CLI output 🐣
- error messages 🙈
- tests ✅
- plots 🎨
- examples 🧺
- issues 🌸
- pull requests 🐾
- release notes 🎁
- changelogs 📖
- workflow names 🤖☕

If humans can see it, it should feel like it belongs here.

---

## 2. Cute outside. Cute inside. Math still works. 🧠☕

The tone may be silly.

The implementation may not be silly.

```text
Cute wording      = yes ✨
Cute variable bug = no  🙈
```

Keep these things precise:

- equations
- state definitions
- probability calculations
- reproducibility
- tests
- uncertainty
- file formats
- numerical results

A tiny particle is still a particle. 🐣

---

## 3. Hard math should still tell a little story 📖☕🐣

This model contains stochastic dynamics, latent states, hybrid modes, memory,
Particle Filtering, smoothing, calibration, and a suspicious number of matrices.

That is not permission to make the reader suffer. XD

Prefer this reading order:

```text
Story → Intuition → Model → Math
```

A story may explain **why a concept exists** before an equation explains **how it works**.

Good:

```text
A voluntary pass happens.
The routine returns normally.
Now explain why Pass != Failure and how Recovery is modeled.
```

Less helpful:

```text
Here is a 6x6-ish pile of symbols. Good luck. 🙈
```

Story is an interface for understanding, not evidence for the model.

```text
Story != evidence
Persona != core ontology
```

---

## 4. Persona at the edge, generic math in the center 🎭🧠

Synthetic story personas are welcome in examples because names make difficult models easier to follow.

For example, `Cheng` and `Linda` may appear as clearly synthetic story characters in `examples/` and README explanations.

They must translate into generic model semantics before entering the core:

```text
Cheng / Linda story
        ↓
Persona / Protocol Adapter
        ↓
invite / opt_in / reaction / ...
        ↓
CSRDM Core
```

Do **not** hard-code persona names into Particle Filter likelihoods, latent states,
transition logic, config keys, or architecture-defining mathematics.

And do not publish private source material just because the story layer has names.

```text
Synthetic persona label != private transcript
Public story            != private data
```

---

## 5. Humans are not state machines 🌿

This project models **observable routine dynamics**.

It does not claim direct access to anybody's internal truth.

Keep these little guardrails nearby:

```text
Observed behavior != internal truth
Action != intention
Continuity != obligation
Pass != failure
Disturbance != rupture
Model != human
```

Uncertainty is allowed.

Surprises are allowed too. XD

---

## 6. Comments should protect meaning, not narrate syntax 🧠🛡️

Useful comments explain a design reason, invariant, or surprising choice:

```python
# C remembers accumulated shared context, so it deliberately skips
# ordinary daily-state drift used by the other five states. 🧠🌱
```

Not useful:

```python
# calculate probability
probability = ...
```

Comments are especially valuable around:

- temporal alignment
- state-space invariants
- intentionally omitted terms
- synthetic-world vs estimator assumptions
- numerical guards
- boundaries between story and core semantics

---

## 7. Commit messages must also drink coffee ☕🐾

Please do not suddenly become a corporate robot in the Git history.

Good little commits:

```text
☕ brew a whole year of 365 cute days
🐣 teach tiny particles how to guess better
🌱 let the routine find its way back
🧺 tidy up the little coffee basket
📖 give the scary math a tiny story to walk in with
```

Less cozy:

```text
Update simulator
Refactor code
Fix bug
Implement feature
```

The message should still say what changed. Cute does not mean mysterious. 🐾

---

## 8. Errors may be adorable, but they must still help 🙈🛠️

Bad:

```text
Oopsie! Something happened! ✨
```

Better:

```text
🐾 Oops... --days must be at least 1. The tiny calendar cannot have zero days.
```

A useful error should tell us what went wrong and, when practical, how to fix it.
Then it may wear a tiny hat. 🎩

---

## 9. Tests live in a tiny nest 🐣✅

Tests should be precise and reproducible.

Ideal ending:

```text
☕✨ All tiny tests are happy.
```

But only print that when the tests are actually happy. XD

---

## 10. Plots should be cute, not confusing 🎨☕

A plot belongs here when it is readable, honest about uncertainty, visually friendly,
and technically useful.

```text
Cute plot != confusing plot
```

The data gets the front seat. The sparkles sit politely in the back. ✨

---

## 11. Synthetic coffee stays synthetic 🧪☕

Synthetic examples are welcome.

Real private conversations, company data, exports, screenshots, timestamps, or sensitive source material are **not** part of this public repo.

```text
Synthetic reference != real human truth
Public demo         != private data
```

Keep the little coffee basket clean. 🧺

---

## 12. The final tiny rule 🌸

When choosing between:

```text
boring + correct
cute   + correct
```

choose:

```text
cute + correct ☕🐾✨
```

When choosing between:

```text
cute + wrong
boring + correct
```

choose correctness first, then come back and make it cute. XD

---

☕ Cute outside.  
🐣 Cute inside.  
🧠 Math still works.  
📖 Hard math still tells a little story.  
🌱 Humans may still surprise the model.
