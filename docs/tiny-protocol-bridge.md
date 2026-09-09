# Tiny Protocol Bridge ☕➡️🧠➡️🐣

## Why this exists

The coffee world begins with very small observable tokens:

```text
+1?
+
要
對
👍
pass
☕
pause
resume
水費
```

Those events describe **what happened**. They do not reveal **why it happened**.

The bridge exists to translate protocol-shaped vocabulary into generic observable model fields without jumping directly to latent-state claims.

This is the deeper reference for tutorial chapters [`tutorial/01-a-tiny-routine.md`](tutorial/01-a-tiny-routine.md) and [`tutorial/02-event-not-meaning.md`](tutorial/02-event-not-meaning.md).

```text
Protocol event != latent state
```

## Four little promises ☕🤝

The adapter boundary can be remembered with four promises:

1. **Observable in, observable out.** 👀
2. **Missing clues stay missing.** 🌱
3. **Ambiguous clues stay ambiguous.** 🙈
4. **Story vocabulary becomes generic semantics before core inference.** 🧠

They are small rules, but they protect a large boundary:

```text
protocol / persona event
        ↓
parse once
        ↓
known actions + observed clues
        ↓
CSRDM inference
```

The bridge does not skip directly from a coffee token to a claim about a person's internal state.

## Tiny translation table 🧺

| Little event | Generic observable field |
|---|---|
| `+1?` | `invite = 1` |
| `+`, `要`, `對` | `opt_in = 1` |
| `pass` | `pass_event = 1`, and `opt_in = 0` when an invite is present |
| `☕` | `routine_maintenance = 1` |
| `resume` | `resume_signal = 1` |
| explicit state-sharing event | `state_share = 1` |
| explicit leave / exception update | `proactive_update = 1` |
| `水費` / payment | `payment_event = 1` |

`pause_event` and `payment_event` are preserved as observable metadata even though the current Particle Filter does not score them directly.

That is intentional:

```text
observable metadata may exist without being forced into the current latent model
```

## The little `👍` problem

The protocol accepts `👍` as a yes in the right context, but the same symbol can also be a reaction after coffee arrives.

```text
+1? → 👍      = may be opt-in
☕  → 👍      = may be reaction
👍 by itself   = ambiguous
```

A lonely thumb is not forced into a story.

```text
Ambiguous clue != forced story
```

## Silence gets its own chair 🌿

If the only observed token is:

```text
+1?
```

then the adapter returns the response fields as missing:

```text
invite = 1
opt_in = None
pass_event = None
```

No hidden yes. No hidden no. Just missing information.

```text
Missing clue != zero
```

## Actions and observations are separate 🎮👀

The combined adapter path parses one protocol moment and splits it into the two baskets used by CSRDM:

```python
from coffee_brain.protocol_adapter import coffee_to_step

step = coffee_to_step(["+1?", "要", "☕", "👍"])

print(step.actions)
print(step.observation)
```

This avoids reparsing the same story moment independently for dynamics and inference.

## Explicit events 🐣

When raw text is too ambiguous, callers can use an explicit `CoffeeEvent`:

```python
from coffee_brain.protocol_adapter import CoffeeEvent, coffee_to_observation

obs = coffee_to_observation([
    CoffeeEvent("proactive_update", "leave notice"),
    CoffeeEvent("pause", "leave"),
    CoffeeEvent("resume", "back tomorrow"),
])
```

The bridge stays deliberately modest:

```text
Observable facts in
Generic event semantics out
Probabilistic hidden-state inference later
```

Cute bridge. Serious boundary. ☕✨
