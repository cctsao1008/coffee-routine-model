"""A tiny synthetic Cheng-and-Linda story that lives outside the generic core. ☕📖

These names are story personas only. No private messages, timestamps, company facts,
or real-world source material belong here. The point is to make the model readable,
then translate the story into generic CSRDM actions and observations.
"""

from __future__ import annotations

from dataclasses import dataclass

from coffee_brain.protocol_adapter import CoffeeEvent, CoffeeStep, coffee_to_step


@dataclass(frozen=True)
class ChengLindaBeat:
    """One readable story beat before the generic adapter removes the costumes. 🎭☕"""

    cheng_invite: bool = False
    linda_choice: str | None = None
    cheng_delivery: bool = False
    linda_reaction: str | None = None
    linda_state_share: bool = False
    linda_update: bool = False
    cheng_notify: bool = False
    linda_closure: bool = False
    resume: bool = False


def to_generic_step(beat: ChengLindaBeat) -> CoffeeStep:
    """Turn persona-shaped story fields into one generic CSRDM step. ☕➡️🧠"""

    events: list[str | CoffeeEvent] = []
    if beat.cheng_invite:
        events.append("+1?")
    if beat.linda_choice is not None:
        events.append(beat.linda_choice)
    if beat.cheng_delivery:
        events.append("☕")
    if beat.linda_reaction is not None:
        # The story says this is a reaction explicitly, so no token ambiguity remains.
        events.append(CoffeeEvent("reaction", beat.linda_reaction))
    if beat.linda_state_share:
        events.append(CoffeeEvent("state_share", "story state share"))
    if beat.linda_update:
        events.append(CoffeeEvent("proactive_update", "story update"))
    if beat.cheng_notify:
        events.append(CoffeeEvent("notify", "story notify"))
    if beat.linda_closure:
        events.append(CoffeeEvent("closure", "story closure"))
    if beat.resume:
        events.append(CoffeeEvent("resume", "story resume"))
    return coffee_to_step(events)


def tiny_story() -> list[CoffeeStep]:
    """Three little beats: ordinary coffee, voluntary pass, ordinary return. 🌱"""

    return [
        to_generic_step(
            ChengLindaBeat(
                cheng_invite=True,
                linda_choice="要",
                cheng_delivery=True,
                linda_reaction="👍",
            )
        ),
        to_generic_step(ChengLindaBeat(cheng_invite=True, linda_choice="pass")),
        to_generic_step(
            ChengLindaBeat(
                cheng_invite=True,
                linda_choice="+",
                cheng_delivery=True,
                linda_reaction="👍",
                resume=True,
            )
        ),
    ]


if __name__ == "__main__":
    for day, step in enumerate(tiny_story(), start=1):
        print(f"☕ story day {day}")
        print("  actions     =", step.actions)
        print("  observation =", step.observation)
