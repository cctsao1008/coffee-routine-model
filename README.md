# Coffee Routine Model ☕🐾✨

A tiny coffee routine with suspiciously serious math.

> **Humans are not state machines.**  
> This model works with observable clues, keeps uncertainty visible, and describes the routine rather than claiming access to anyone's hidden mind.

This README is the **first guided walk** through the project:

```text
story → observation → modeling problem → abstraction → uncertainty → code → self-checks
```

For the full step-by-step model-design tutorial, start at [`docs/tutorial/README.md`](docs/tutorial/README.md).  
If you only want the formal contract, jump to [`docs/architecture.md`](docs/architecture.md).  
If you want the shorter gentle explanation, see [`docs/how-the-coffee-works.md`](docs/how-the-coffee-works.md).

## 1. Start with one tiny routine 📖☕

Meet **Cheng** and **Linda** — synthetic story personas used only to make the model easier to read.
They are illustrative characters here, not a published private transcript or a ground-truth psychology dataset.

A small week might look like this:

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
busy morning, slower reply 🌧️

Thursday
leave / pause 🏖️

Friday
resume 🌱

Next Monday
ordinary coffee again ☕
```

The story feels simple. The modeling problem begins when we ask what we can actually know from it.

## 2. What can we actually observe? 👀

The model starts from behavior-level events:

```text
Cheng asks +1?     → invite
Linda says 要      → opt_in
coffee arrives     → routine_maintenance
Linda reacts 👍    → reaction
pass               → pass_event
state update       → proactive_update
resume             → resume_signal
```

Those are observations and actions. They are **not** direct measurements of intention, emotion, or private meaning.

```text
Observed event != internal truth
Story != evidence
```

The companion [`coffee-routine-protocol`](https://github.com/cctsao1008/coffee-routine-protocol) provides the tiny interaction vocabulary. `coffee_brain/protocol_adapter.py` translates that vocabulary into generic model fields.

Even a familiar token can be contextual:

```text
after +1?  → 👍 may be an opt-in
after ☕   → 👍 may be a reaction
alone      → 👍 may stay ambiguous
```

Missing facts stay missing. Ambiguous clues do not get forced into a story.

## 3. Is counting coffee enough? 🧩

Not really.

A simple counter can tell us whether coffee happened, but it cannot represent several recurring questions:

```text
If coffee usually follows a clear opt-in, is the routine becoming predictable?

If both sides contribute in different ways, is 50/50 symmetry really the right idea?

If someone says pass, should that count as failure?

If a busy day or leave interrupts the pattern, did the routine actually break?

If familiar callbacks and little conventions accumulate, should one quiet day erase them?
```

These questions are what gradually create the model. The model is not the starting point; it is the abstraction that comes after the problems appear.

## 4. So... what is CSRDM? ☕🧠

**CSRDM** stands for **Coupled Shared Routine Dynamics Model**.

It is a stochastic model for a repeated voluntary routine maintained through interaction between two sides.
The object being modeled is the **shared routine and how it changes over time** — not either person's hidden mind.

```text
Coupled        → actions from both sides can affect how the routine evolves
Shared Routine → the routine itself is the modeling object
Dynamics       → the routine can change over time
Model          → an uncertain mathematical abstraction
```

So CSRDM asks three modest questions:

```text
What can we observe?
What hidden routine state could explain those observations?
How uncertain should the model remain?
```

The story names stop at the edge:

```text
Cheng / Linda story
        ↓
Persona / Protocol Adapter
        ↓
Generic actions + observations
        ↓
CSRDM Core
```

**Story at the edge. Generic math in the center.** ☕🧠

The runnable persona example lives in [`examples/cheng_linda_story.py`](examples/cheng_linda_story.py).

## 5. Six modeling questions become six soft states 🌱

Instead of declaring six variables first, start with the problems that require them.

### `P` — Predictability

If invitations, replies, delivery, and resumption usually follow familiar patterns, the routine becomes easier to anticipate.

### `M` — Mutuality

Two sides do not need to contribute in identical ways. One may initiate more often while the other maintains the loop through opt-in, acknowledgment, updates, or closure.

```text
Mutuality != 50/50 symmetry
```

### `V` — Voluntariness

A voluntary model must allow `pass` to remain a valid choice.

```text
Continuity != obligation
Pass != failure
```

### `C` — Shared Context

Callbacks, recurring conventions, familiar shorthand, and repeated coordination can accumulate over time.

### `E` — Everyday State Sharing

Observable everyday states such as busy / tired / okay can enter the interaction without becoming mind-reading labels.

### `F` — Friction

Some routines become easier to coordinate; others become more costly, awkward, or difficult to maintain.

Only now do the six names come together:

```text
x(t) = [P, M, V, C, E, F]
```

These are **soft latent properties of the routine model**, not six meters attached to a person.

## 6. Actions and observations are different 🎮👀

Another modeling problem appears quickly:

> An observable action can help move the routine forward, while an observation gives evidence about the state we cannot see directly.

CSRDM therefore keeps known actions and observation clues separate.

```text
known actions a[t]
      ↓
previous hidden state → current hidden state
                              ↑
                       observed clues z[t]
```

For example, an invitation or delivery can be represented as an action, while a reaction or response delay can be used as an observation clue.

```text
Action != intention
Observation != latent state
Missing clue != zero
```

The implementation details live in [`docs/action-aware-dynamics.md`](docs/action-aware-dynamics.md) and [`docs/tiny-protocol-bridge.md`](docs/tiny-protocol-bridge.md).

## 7. One kind of day is not enough 🌦️

A single continuous state vector still misses an obvious fact: ordinary days, busy days, leave, special days, and recovery do not all behave the same way.

So CSRDM also carries a discrete routine mode:

```text
☕ Normal
🌧️ Busy
🏖️ Leave
🎂 Special
🌱 Recovery
```

A small sequence might be:

```text
Normal → Busy → Leave → Leave → Recovery → Normal
```

The important distinction is:

```text
Disturbance != rupture
Mode != regime
```

A temporary Leave mode does not automatically mean the generating process has permanently changed.

Mode transitions remain stochastic:

```math
p(m_{t+1}\mid m_t,x_t,a_t,d_t)
```

Context can nudge the probabilities. It does not deterministically choose the answer.

Recovery is treated separately rather than being smuggled into a generic failure score. See [`docs/recovery-garden.md`](docs/recovery-garden.md).

## 8. Some things should remember slowly 🧠🌱

Now `C = Shared Context` creates its own design problem.

If `C` moved like an ordinary daily variable, one quiet day could erase too much accumulated history. So `C` uses a dedicated slow memory law:

```math
C_{t+1}=C_t+\eta I_t(1-C_t)-\lambda C_t+w_t^C
```

where `I_t` is bounded shared-context input from observable coordination.

The intuition is simple:

```text
one callback              → one event
many remembered patterns  → accumulated context
one quiet day             → not instant forgetting
long disconnection        → slow decay can matter
```

```text
Memory != mood
No event today != no shared history
```

The deeper version lives in [`docs/memory-garden.md`](docs/memory-garden.md).

## 9. But we still cannot see the hidden state 🐣🐣🐣

At this point the model has six latent states and five possible modes.

Tiny problem: **none of them is directly observable.**

Suppose one quiet day arrives. Several explanations may still fit:

```text
🐣 #1  probably ordinary noise
🐣 #2  maybe today is Busy
🐣 #3  maybe friction is a bit higher
🐣 #4  maybe nothing structural changed at all
```

Instead of forcing one explanation too early, the Particle Filter keeps many candidate hidden states alive and reweights them when new evidence arrives.

Filtering asks:

```math
p(x_t,m_t\mid z_{1:t})
```

Later evidence can also help reinterpret **uncertainty** about an earlier hidden state through smoothing:

```math
p(x_t,m_t\mid z_{1:T})
```

But the observed event itself never changes.

```text
Later evidence may update uncertainty.
Later evidence does not rewrite observed facts.
```

See [`docs/smoothing-garden.md`](docs/smoothing-garden.md) for the fixed-lag smoother.

## 10. Now the full engineering shape makes sense 🏛️☕

Architecture **`0.3`** uses the following symbols:

```text
x_t = latent continuous routine state [P M V C E F]
m_t = latent routine mode
a_t = known observable action basket
d_t = explicit known disturbance / context when available
z_t = observable clue basket
```

The controlled stochastic model is conceptually:

```math
x_{t+1}\sim p(x_{t+1}\mid x_t,m_t,a_t,d_t)
```

```math
z_t\sim p(z_t\mid x_t,m_t)
```

And the stable public API stays small:

```python
from coffee_brain import CSRDM, CSRDMConfig

brain = CSRDM(CSRDMConfig())
result = brain.step(["+1?", "要", "☕", "👍"])

print(result.posterior.mean)
```

The full architecture contract lives in [`docs/architecture.md`](docs/architecture.md).

## 11. A model should be allowed to argue with itself 🔍🧪

Building a model is only half the story. The next question is whether the abstractions we invented are useful inside the synthetic test world.

That is why the repo contains small diagnostic labs:

| Modeling doubt | Lab |
|---|---|
| We invented six states — can the clues distinguish them? | [`observability-garden.md`](docs/observability-garden.md) |
| Our observation probabilities are hand-set — are they calibrated? | [`calibration-bench.md`](docs/calibration-bench.md) |
| Which assumptions matter most? | [`sensitivity-map.md`](docs/sensitivity-map.md) |
| Does one strange day imply a new generating regime? | [`change-point-garden.md`](docs/change-point-garden.md) |
| Does hindsight help without rewriting history? | [`smoothing-garden.md`](docs/smoothing-garden.md) |
| Can accumulated context recover after interruption? | [`recovery-garden.md`](docs/recovery-garden.md) |
| Can a simpler model compete? | [`model-arena.md`](docs/model-arena.md) |
| Can a few bounded probability knobs learn without rewriting the ontology? | [`learning-spoon.md`](docs/learning-spoon.md) |

The repeated rule is:

```text
Better fit != better ontology
Estimable != identifiable
Synthetic success != real-human truth
Winner != truth
```

## 12. Try the little brain yourself ☕➡️🐣

Install and run a synthetic world:

```bash
python -m pip install -r requirements.txt
python -m tiny_tools.simulate --scenario slow-recovery --days 365
```

Available synthetic weather includes:

```text
🌤️ cozy-normal-year
🌧️ super-busy-month
🏖️ long-leave-and-return
💤 sleepy-reply-season
🎂 special-day-sparkle
🌪️ noisy-chaos-week
🌱 slow-recovery
```

The simulator deliberately does not always match the estimator assumptions:

```text
Synthetic World != Estimator Assumptions
```

That mismatch is useful because a model that only succeeds against itself has not learned much about its own weaknesses.

The synthetic world still obeys its observable protocol grammar: opt-in and pass cannot be the same reply, delivered-coffee maintenance requires opt-in, and an unobserved reply does not receive an invented finite delay.

```text
Protocol grammar != estimator factorization
```

## 13. The 365-day reference basket 🗓️☕

The committed synthetic reference lives at:

```text
examples/365-cute-days/
├── README.md
├── input.csv
├── output.csv
├── metrics.csv
├── recipe.json
├── source-revision.txt
├── environment.txt
└── tiny-year-summary.png + state/mode figures
```

The current scorecard is [`examples/365-cute-days/metrics.csv`](examples/365-cute-days/metrics.csv).
Exact metric values are intentionally **not copied into this README**: recipe-defining code can regenerate the reference basket, so `metrics.csv` stays the single scorecard source of truth.

`recipe.json`, `source-revision.txt`, and `environment.txt` record enough context to investigate reproducibility instead of pretending a seed alone freezes every future dependency version.

```text
Reference metric != universal performance
Synthetic reference != real-human validation
Seed != complete environment
```

Paint the year again:

```bash
python -m tiny_tools.visualize examples/365-cute-days/output.csv
```

![One tiny coffee routine across one synthetic year](examples/365-cute-days/tiny-year-summary.png)

Want a short scratch run instead?

```bash
python -m tiny_tools.simulate --days 100 --out .tiny-100-day-scratch
```

## 14. Pick the next door 📚✨

The README is the guided first journey. After that, choose the kind of question you have:

```text
📖 Model-design learner
   docs/tutorial/README.md
   ↓
   ten progressive chapters

☕ Curious human
   docs/how-the-coffee-works.md

🛠️ Software engineer
   public CSRDM API
   ↓
   docs/tiny-protocol-bridge.md
   ↓
   docs/architecture.md

🧠 Math / control reader
   docs/architecture.md
   ↓
   action-aware dynamics / memory / smoothing
   ↓
   diagnostics and model arena

🧪 Experiment reader
   observability / calibration / sensitivity
   ↓
   change points / recovery / learning / arena
```

The full documentation map lives in [`docs/README.md`](docs/README.md).

Same model. Different doors.

## 15. Test nest 🐣✅

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

CI also exercises the model, adapters, diagnostics, smoothing, memory, calibration, change points, transitions, and a small chaos simulation.

```text
Cute CI != weak CI
```

## House rules ☕🌸

The full tiny constitution lives in [`CUTE_RULES.md`](CUTE_RULES.md).  
The objective story contract lives in [`docs/objective-story-contract.md`](docs/objective-story-contract.md).  
The history book lives in [`COFFEELOG.md`](COFFEELOG.md).

Two useful rules:

> **Cute != sloppy.**

> **Hard math should still tell a little story. ☕📖🐣**

And the guardrails:

```text
Story != evidence
Persona != core ontology
Observed behavior != internal truth
Action != intention
Continuity != obligation
Pass != failure
Disturbance != rupture
Sensitivity != causality
Model != human
```

Cute outside. Cute inside. Math still works. ☕🐣🧠
