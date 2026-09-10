# Coffee Routine Model ☕🐾✨

<p align="center">
  <img src="docs/assets/coffee-routine-model-readme-banner.svg" alt="coffee-routine-model — CSRDM mascot banner" width="100%">
</p>

A tiny coffee routine with suspiciously serious math.

> **Humans are not state machines.**

This project starts with observable routine events and gradually turns them into a stochastic model — while keeping uncertainty, assumptions, and unknowns visible.

```text
story
→ observation
→ modeling question
→ hidden state
→ inference
→ diagnostics
```

There is only **one Coupled Shared Routine Dynamics Model (CSRDM)**. You choose how deep you want to read.

## Choose a path 🪜☕

```text
I just want the idea
→ README → Glossary → Starter Math

I want to use it
→ README → Public API → examples/

I want to inspect the model
→ Architecture → Full Math → diagnostics
```

Quick doors:

- [`Glossary`](docs/glossary.md) — project vocabulary;
- [`Common Confusions`](docs/common-confusions.md) — recurring category mistakes;
- [`Tutorial`](docs/tutorial/README.md) — guided design story;
- [`Starter Math`](docs/math/starter-math.md) — readable mathematical entry point;
- [`Public API`](docs/public-api.md) — safe calling rules;
- [`Architecture`](docs/architecture.md) — software/config contract;
- [`Documentation map`](docs/README.md) — everything else.

> **Same model. Same example. Different depth.**

## 1. Start with one tiny routine 📖☕

Meet **Cheng** and **Linda** — synthetic teaching personas used only to make the examples easier to follow.

```text
Monday
Cheng: +1?
Linda: 要
coffee arrives ☕
Linda: 👍

Tuesday
Cheng: +1?
Linda: pass

Wednesday
busy morning 🌧️

Thursday
leave / pause 🏖️

Friday
resume 🌱
```

The public story is illustrative, not a private transcript and not a ground-truth psychology dataset.

```text
Story != evidence
```

## 2. What can we actually observe? 👀

The model starts from behavior-level events:

```text
+1?      → invite
要        → opt_in
pass     → pass_event
☕        → routine_maintenance
👍        → reaction, depending on context
busy     → observable update when explicitly provided
resume   → resume_signal
```

Those events do **not** directly reveal intention or hidden meaning.

```text
Observed event != internal truth
Action != intention
Missing clue != zero
```

The companion [`coffee-routine-protocol`](https://github.com/cctsao1008/coffee-routine-protocol) provides the tiny interaction vocabulary. The protocol adapter turns that vocabulary into generic model fields before the math begins.

## 3. Why is counting coffee not enough? 🧩

A simple counter cannot distinguish:

```text
voluntary pass
busy interruption
leave
ordinary return
shared context that accumulated over time
coordination that becomes easier or harder
```

That creates the modeling questions:

```text
Can the routine become predictable?
Can both sides contribute differently?
Can pass stay a valid choice?
Can context accumulate?
Can ordinary state updates matter?
Can friction change over time?
```

## 4. CSRDM appears ☕🧠

**CSRDM** means **Coupled Shared Routine Dynamics Model**.

```text
Coupled        → both sides can affect the routine
Shared Routine → the routine itself is the modeling object
Dynamics       → it can change over time
Model          → it remains an uncertain abstraction
```

The six soft hidden states are:

```text
P = Predictability
M = Mutuality
V = Voluntariness
C = Shared Context
E = Everyday State Sharing
F = Friction
```

Together:

```text
x_t = [P, M, V, C, E, F]
```

Read `x_t` as the hidden routine-state vector at time `t`.
These are model variables, not six meters attached to a person.

Useful boundaries:

```text
Mutuality != 50/50 symmetry
Continuity != obligation
Pass != failure
Probability != fact
High historical probability != future commitment
```

## 5. Run the tiny brain ☕➡️🐣

The stable public API stays small:

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])

print(result.mean_by_state)
print(result.posterior.mode)
```

Raw arrays remain available under `result.posterior`; named views keep the ordinary path readable.
For missing-data rules, action timing, smoothing, context-aware transitions, and input validation, see [`docs/public-api.md`](docs/public-api.md).

Install the package from the repository root:

```bash
python -m pip install .
```

Current package: `0.3.1`  
CSRDM architecture: `0.3`

Release details live in [`docs/release-notes-0.3.1.md`](docs/release-notes-0.3.1.md).

Run a synthetic world:

```bash
python -m tiny_tools.simulate --scenario slow-recovery --days 365
```

The committed observation-only reference lives in [`examples/365-cute-days/`](examples/365-cute-days/).
The separate known-action reference can be generated with:

```bash
python -m tiny_tools.controlled_reference
```

Its result summary lives in [`docs/controlled-reference-result.md`](docs/controlled-reference-result.md).

```text
Synthetic reference != real-human validation
Synthetic World != Estimator Assumptions
```

## 6. What happens behind the small API? 🧠

At a high level:

```text
observable events
      ↓
protocol adapter
      ↓
actions + observation clues
      ↓
CSRDM hidden-state dynamics
      ↓
Particle Filter
      ↓
posterior uncertainty
      ↓
optional smoothing + diagnostics
```

For equations and implementation boundaries:

- [`Starter Math`](docs/math/starter-math.md) — variables and main relationships;
- [`Full Math`](docs/math/full-math.md) — complete stochastic hybrid model;
- [`Architecture`](docs/architecture.md) — software/config/public contract.

## 7. What did the diagnostics actually find? 🔬

The repository does not only report successful runs. Some of the most useful diagnostics start from a mismatch and ask what caused it.

| Diagnostic | Baseline symptom | Diagnostic comparator | What the test supports |
|---|---|---|---|
| **Voluntariness (`V`) compression** | V-only default prior recovered only `0.201` of the truth amplitude; 95% coverage was `47.2%` | A deliberately relaxed diagnostic prior recovered `0.900` of the amplitude; coverage rose to `95.6%` | In this synthetic stress test, the default V dynamics prior is the strongest identified limiter; cross-state aliasing is secondary |
| **Shared Context (`C`) bias** | Default 95% coverage was `57.8%` | Matching only the diagnostic starting center raised coverage to `92.6%` | About `0.8976` of default MSE was explained by the squared mean offset; initialization + slow memory explain most, but not all, of the bias |

The full receipts are in:

- [`V Posterior Compression Result`](docs/v-compression-result.md);
- [`Shared Context Bias Decomposition`](docs/shared-context-bias-result.md).

These results are deliberately narrower than a production recommendation.

```text
Diagnostic improvement != production recommendation
Better fit != better ontology
Synthetic result != real-human validation
```

Other focused labs cover observability, calibration, sensitivity, change points, recovery, smoothing, model comparison, and state sufficiency. Start from the [`documentation map`](docs/README.md) if you want the full trail.

## 8. Boundaries and house rules ⚖️☕

The repo-wide claim vocabulary is:

```text
Observed
Probable
Assumed
Undefined
Not-yet-decided
```

See [`docs/epistemic-status.md`](docs/epistemic-status.md).
For compact definitions, use the [`Glossary`](docs/glossary.md).
For recurring category mistakes, use [`Common Confusions`](docs/common-confusions.md).

The public story contract lives in [`docs/objective-story-contract.md`](docs/objective-story-contract.md).
The distilled design principles live in [`docs/design-principles.md`](docs/design-principles.md).
The tiny constitution lives in [`CUTE_RULES.md`](CUTE_RULES.md).

```text
Cute != sloppy
Plain language != missing rigor
Model != human
```

And yes: `XD` is still seasoning, not punctuation. ☕

## 9. Test nest and license 🐣✅📜

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

CI exercises the public model, adapters, diagnostics, memory, smoothing, calibration, change points, controlled reference, synthetic runs, and an installed-package smoke test from outside the source tree.

Coffee, code, and tiny particles are shared under the **MIT License**.
See [`LICENSE`](LICENSE) for the full legal text.

One tiny routine. Many levels of depth. Same mathematical skeleton. ☕🌱📐🐣
