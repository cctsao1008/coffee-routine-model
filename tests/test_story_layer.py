from examples.cheng_linda_story import ChengLindaBeat, tiny_story, to_generic_step


def test_persona_costumes_come_off_before_the_generic_core():
    step = to_generic_step(
        ChengLindaBeat(
            cheng_invite=True,
            linda_choice="要",
            cheng_delivery=True,
            linda_reaction="👍",
            linda_state_share=True,
            linda_update=True,
            cheng_notify=True,
            linda_closure=True,
        )
    )

    assert step.observation["invite"] == 1
    assert step.observation["opt_in"] == 1
    assert step.observation["reaction"] == 1
    assert step.observation["state_share"] == 1
    assert step.observation["proactive_update"] == 1
    assert step.observation["routine_maintenance"] == 1
    assert step.actions.a_invite == 1.0
    assert step.actions.a_deliver == 1.0
    assert step.actions.a_notify == 1.0
    assert step.actions.b_opt_in == 1.0
    assert step.actions.b_acknowledge == 1.0
    assert step.actions.b_exception_sync == 1.0
    assert step.actions.b_closure == 1.0

    # Cheng/Linda are story labels at the edge, never latent/core field names. 🎭➡️🧠
    assert not any("cheng" in key or "linda" in key for key in step.observation)


def test_story_can_show_a_pass_without_turning_it_into_failure():
    step = to_generic_step(ChengLindaBeat(cheng_invite=True, linda_choice="pass"))
    assert step.observation["pass_event"] == 1
    assert step.observation["opt_in"] == 0
    assert step.actions.b_pass_choice == 1.0


def test_three_story_beats_make_an_ordinary_pass_and_return_arc():
    story = tiny_story()
    assert len(story) == 3
    assert story[0].observation["routine_maintenance"] == 1
    assert story[1].observation["pass_event"] == 1
    assert story[2].observation["resume_signal"] == 1
