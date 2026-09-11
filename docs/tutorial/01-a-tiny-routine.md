# 01 — We Only Had a Tiny Routine ☕👀

Start with something deliberately ordinary.

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
busy morning

Thursday
leave / pause

Friday
resume
```

Nothing here needs to be dramatic.

One person asks. Another says yes, says pass, gets busy, or comes back later. A tiny routine can become familiar precisely because most of its moments are ordinary.

That ordinariness is worth preserving. If we explain every small action as hidden meaning, the model stops describing a routine and starts inventing a story about the people inside it.

These are synthetic teaching beats. At this stage, do not explain them psychologically. Just list what happened.

That is the first modeling discipline:

> **Begin with observables before inventing hidden meaning.**

And the first human-facing discipline is just as important:

> **Ordinary does not mean meaningless. It means we do not have to manufacture meaning.**

## What can the model actually see?

A small event vocabulary is enough to begin:

```text
+1?      → invite
要        → opt_in
pass     → pass_event
☕        → routine_maintenance
👍        → reaction, depending on context
busy     → observable state/update clue when explicitly provided
resume   → resume_signal
```

The important word is **observable**.

The model does not receive:

```text
intention
private emotion
unspoken meaning
future commitment
```

unless some later design explicitly represents a measurable proxy — and even then, the proxy is still not the hidden truth itself.

```text
Observed event != internal truth
```

## Why this matters before any math

If we skip this boundary, the model can become circular:

```text
we assume what a behavior means
        ↓
encode that meaning as data
        ↓
run inference
        ↓
announce that the inference discovered the meaning
```

That would not be inference. It would be our assumption coming back wearing a tiny hat.

So the project keeps behavior-level events separate from latent state.

That separation does not make the story less human. It does the opposite: it leaves room for people to remain more complicated than the variables used to describe one small routine.

## The first code boundary

The companion protocol speaks small human-readable tokens. The adapter translates them into generic fields:

```python
from coffee_brain.protocol_adapter import coffee_to_step

step = coffee_to_step(["+1?", "要", "☕", "👍"])

print(step.actions)
print(step.observation)
```

The exact token is less important than the boundary:

```text
story vocabulary
      ↓
generic event semantics
      ↓
model
```

The synthetic persona example in [`../../examples/cheng_linda_story.py`](../../examples/cheng_linda_story.py) shows the same idea with readable names at the edge.

## A first correction worth remembering

A tempting first model would be:

```text
coffee happened = good
coffee did not happen = bad
```

That is easy to count, but it already throws away too much information.

A voluntary `pass`, a busy day, leave, a delayed reply, and a broken routine would all collapse into the same bucket: **no coffee**.

They are not the same observable situation.

That distinction is small, but it carries much of the project's philosophy: choice should stay choice, interruption should stay interruption, and uncertainty should stay uncertainty.

So the next question is unavoidable:

> **When does a collection of small events become a protocol with context, rather than a pile of isolated tokens?**

Continue to [`02-event-not-meaning.md`](02-event-not-meaning.md).
