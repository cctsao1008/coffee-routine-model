from __future__ import annotations

from pathlib import Path
import tomllib

from coffee_brain import ARCHITECTURE_VERSION


ROOT = Path(__file__).resolve().parents[1]


def _pyproject() -> dict:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)


def _plain_requirements(path: Path) -> list[str]:
    lines: list[str] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-r "):
            continue
        lines.append(line)
    return lines


def test_release_version_wraps_the_architecture_version_without_relabeling_it():
    project = _pyproject()["project"]

    assert project["version"].rsplit(".", 1)[0] == ARCHITECTURE_VERSION
    assert ARCHITECTURE_VERSION == "0.3"


def test_runtime_requirement_mirror_matches_package_metadata():
    project = _pyproject()["project"]
    mirrored = _plain_requirements(ROOT / "requirements.txt")

    assert sorted(project["dependencies"]) == sorted(mirrored)


def test_package_metadata_keeps_the_supported_python_boundary_explicit():
    project = _pyproject()["project"]

    assert project["requires-python"] == ">=3.12"


def test_both_public_runtime_drawers_are_packaged():
    package_find = _pyproject()["tool"]["setuptools"]["packages"]["find"]

    assert "coffee_brain*" in package_find["include"]
    assert "tiny_tools*" in package_find["include"]
