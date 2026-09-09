from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TUTORIAL = ROOT / "docs" / "tutorial"
MATH = ROOT / "docs" / "math"

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

EXPECTED_MATH_DOORS = (
    "README.md",
    "starter-math.md",
    "full-math.md",
)


def test_tutorial_spine_keeps_all_ten_little_steps():
    missing = [name for name in EXPECTED_TUTORIAL_CHAPTERS if not (TUTORIAL / name).is_file()]
    assert missing == []


def test_math_path_keeps_starter_and_full_views_together():
    missing = [name for name in EXPECTED_MATH_DOORS if not (MATH / name).is_file()]
    assert missing == []

    starter = (MATH / "starter-math.md").read_text(encoding="utf-8")
    full = (MATH / "full-math.md").read_text(encoding="utf-8")

    for state in ("Predictability", "Mutuality", "Voluntariness", "Shared Context", "Everyday State Sharing", "Friction"):
        assert state in starter
        assert state in full

    assert "Starter Math\n= fewer symbols, same meaning" in starter
    assert "architecture `0.3`" in full
    assert "x_{t+1}\\sim p(x_{t+1}\\mid x_t,m_t,a_t,d_t)" in full
    assert "C_{t+1}=C_t+\\eta I_t(1-C_t)-\\lambda C_t+w_t^C" in starter
    assert "C_{t+1}=C_t+\\eta I_t(1-C_t)-\\lambda C_t+w_t^C" in full


def test_readme_keeps_depth_doors_visible_without_becoming_the_math_textbook():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for door in (
        "docs/tutorial/README.md",
        "docs/math/starter-math.md",
        "docs/math/full-math.md",
        "docs/public-api.md",
        "docs/architecture.md",
        "docs/objective-story-contract.md",
    ):
        assert door in readme

    assert "Same model. Same example. Different depth." in readme
    # The front door should point to the formal math rather than reproducing it. ☕🚪
    assert "x_{t+1}\\sim p(x_{t+1}\\mid x_t,m_t,a_t,d_t)" not in readme
    assert "p(x_t,m_t\\mid z_{1:T})" not in readme


def test_redundant_doc_residue_stays_out_of_the_current_map():
    stale_paths = (
        ROOT / "docs" / "adapter-little-contract.md",
        ROOT / "docs" / "source-notes.md",
        ROOT / "examples" / "controlled-cute-days" / "README.md",
    )
    assert [str(path.relative_to(ROOT)) for path in stale_paths if path.exists()] == []

    docs_map = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    examples_map = (ROOT / "examples" / "README.md").read_text(encoding="utf-8")
    root_readme = (ROOT / "README.md").read_text(encoding="utf-8")

    assert "adapter-little-contract.md" not in docs_map
    assert "source-notes.md" not in docs_map
    assert "../examples/controlled-cute-days/" not in docs_map
    assert "tiny_tools/controlled_reference.py" in docs_map
    assert "tiny_tools.controlled_reference" in examples_map
    assert "../docs/controlled-reference-result.md" in examples_map

    # The root front door must not link to a generated-and-gitignored basket as if it were committed. ☕🧹
    assert "examples/controlled-cute-days/" not in root_readme
    assert "python -m tiny_tools.controlled_reference" in root_readme
    assert "docs/controlled-reference-result.md" in root_readme


def test_public_api_guide_keeps_the_real_friction_boundaries_visible():
    guide = (ROOT / "docs" / "public-api.md").read_text(encoding="utf-8")
    for rule in (
        "Missing clue != zero",
        "transition_applied",
        "DEFAULT_CONTEXT_TRANSITIONS",
        "response_delay_min",
        "LearningConfig(enabled=True)",
        "SmoothingConfig(enabled=True",
    ):
        assert rule in guide

    docs_map = (ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    core_map = (ROOT / "coffee_brain" / "README.md").read_text(encoding="utf-8")
    architecture = (ROOT / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "public-api.md" in docs_map
    assert "docs/public-api.md" in core_map
    assert "public-api.md" in architecture


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
    # GitHub rendered legacy \[ ... \] blocks as plain text once.
    # Keep equation-bearing docs on fenced `math` blocks instead. ☕🛡️
    paths = (
        ROOT / "README.md",
        ROOT / "docs" / "architecture.md",
        ROOT / "docs" / "epistemic-status.md",
        ROOT / "docs" / "memory-garden.md",
        ROOT / "docs" / "recovery-garden.md",
        ROOT / "docs" / "smoothing-garden.md",
        MATH / "starter-math.md",
        MATH / "full-math.md",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "\n\\[\n" not in text, path
        assert "\n\\]\n" not in text, path


def test_cute_rules_keep_plain_words_and_xd_in_their_proper_places():
    rules = (ROOT / "CUTE_RULES.md").read_text(encoding="utf-8")
    assert "Plain words get the first sip" in rules
    assert "Simple != false" in rules
    assert "Plain language != missing rigor" in rules
    assert "`XD` is seasoning, not punctuation" in rules
