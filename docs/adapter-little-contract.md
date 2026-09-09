# Tiny Adapter Contract ☕🤝🐾

`coffee_brain/protocol_adapter.py` protects a small but important boundary.

It promises four things:

1. **Observable in, observable out.** 👀
2. **Missing clues stay missing.** 🌱
3. **Ambiguous clues stay ambiguous.** 🙈
4. **Story vocabulary becomes generic semantics before core inference.** 🧠

```text
protocol / persona event
        ↓
parse once
        ↓
┌────────────────┬────────────────┐
│ known actions  │ observed clues │
│      a_t       │      z_t       │
└────────┬───────┴────────┬───────┘
         │                │
         └────── CSRDM ───┘
                  ↓
       uncertain posterior
```

The adapter never skips directly from a coffee token to a claim about a person's internal state.

```text
Protocol event != latent state
Action != intention
Missing clue != zero
Ambiguous clue != forced story
```

For the detailed translation rules, see [`tiny-protocol-bridge.md`](tiny-protocol-bridge.md). For the teaching path, see [`tutorial/02-event-not-meaning.md`](tutorial/02-event-not-meaning.md).

Cute bridge. Serious boundary. ☕✨
