from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = ROOT / "docs" / "tutorial"

EXPECTED_TUTORIAL_CHAPTERS = (
    "README.md",
    "01-a-tiny-routine.md",
    "02-event-not-meaning.md",
    "03-pass-is-not-failure.md",
    "04-six-soft-states.md",
    "05-actions-vs-observations.md",
    "06-shared-context-memory.md",
    "07-weather-and-recovery.md",
    "08-why-particles.md",
    "09-challenge-the-model.md",
    "10-let-the-model-lose.md",
)


def test_tutorial_spine_keeps_all_ten_little_steps():
    missing = [name for name in EXPECTED_TUTORIAL_CHAPTERS if not (TUTORIAL / name).is_file()]
    assert missing == []


def test_readme_keeps_the_learning_and_reference_doors_visible():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/tutorial/README.md" in readme
    assert "docs/architecture.md" in readme
    assert "docs/objective-story-contract.md" in readme


def test_objective_story_contract_keeps_the_main_boundaries_explicit():
    contract = (ROOT / "docs" / "objective-story-contract.md").read_text(encoding="utf-8")
    for rule in (
        "Story != evidence",
        "Persona != core ontology",
        "Observation != latent state",
        "Action != intention",
        "Model != human",
    ):
        assert rule in contract


def test_epistemic_status_contract_keeps_probability_and_future_choice_distinct():
    contract = (ROOT / "docs" / "epistemic-status.md").read_text(encoding="utf-8")
    for status in (
        "Observed",
        "Probable",
        "Assumed",
        "Undefined",
        "Not-yet-decided",
    ):
        assert status in contract
    for rule in (
        "Probability != fact",
        "Assumption != evidence",
        "Undefined relationship != zero relationship",
        "High historical probability != future commitment",
    ):
        assert rule in contract

    story_contract = (ROOT / "docs" / "objective-story-contract.md").read_text(encoding="utf-8")
    pass_tutorial = (TUTORIAL / "03-pass-is-not-failure.md").read_text(encoding="utf-8")
    particle_tutorial = (TUTORIAL / "08-why-particles.md").read_text(encoding="utf-8")
    assert "epistemic-status.md" in story_contract
    assert "epistemic-status.md" in pass_tutorial
    assert "epistemic-status.md" in particle_tutorial


def test_key_markdown_uses_github_friendly_display_math():
    # GitHub rendered legacy \[ ... \] blocks as plain text in the README once.
    # Keep the main equation-bearing docs on fenced `math` blocks instead. ☕🛡️
    paths = (
        ROOT / "README.md",
        ROOT / "docs" / "architecture.md",
        ROOT / "docs" / "epistemic-status.md",
        ROOT / "docs" / "memory-garden.md",
        ROOT / "docs" / "recovery-garden.md",
        ROOT / "docs" / "smoothing-garden.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "\n\\[\n" not in text, path
        assert "\n\\]\n" not in text, path


def test_cute_rules_keep_xd_as_seasoning_not_punctuation():
    rules = (ROOT / "CUTE_RULES.md").read_text(encoding="utf-8")
    assert "`XD` is seasoning, not punctuation" in rules
