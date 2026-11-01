import re
import sys
import tomllib
from pathlib import Path
from typing import Any

NAME_AND_EXTRAS = re.compile(r"\s*([A-Za-z0-9._-]+)\s*(\[[^\]]*\])?\s*")
EXACT_PIN = re.compile(r"\s*([A-Za-z0-9._-]+)\s*==\s*[^\s,;]+\s*")


def _normalized(*, name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def _pinned_names(*, root_pyproject: dict[str, Any]) -> set[str]:
    constraints = root_pyproject.get("tool", {}).get("uv", {}).get("constraint-dependencies", [])
    matches = (EXACT_PIN.fullmatch(constraint) for constraint in constraints)
    return {_normalized(name=match.group(1)) for match in matches if match}


def _requirements(*, pyproject: dict[str, Any]) -> list[str]:
    project = pyproject.get("project", {})
    uv = pyproject.get("tool", {}).get("uv", {})
    declared = [
        *project.get("dependencies", []),
        *uv.get("dev-dependencies", []),
    ]
    for extra in project.get("optional-dependencies", {}).values():
        declared.extend(extra)
    for group in pyproject.get("dependency-groups", {}).values():
        declared.extend(entry for entry in group if isinstance(entry, str))
    return declared


def _problem(*, requirement: str, pyproject: dict[str, Any], pinned: set[str]) -> str | None:
    match = NAME_AND_EXTRAS.match(requirement)
    if match is None:
        return "is not a valid requirement"
    name = match.group(1)
    sources = pyproject.get("tool", {}).get("uv", {}).get("sources", {})
    if name in sources:
        source = sources[name]
        if isinstance(source, dict) and source.get("workspace") is True:
            return None
        return "must not declare its own source"
    if requirement[match.end() :].split(";", maxsplit=1)[0].strip():
        return "must not declare a version"
    if _normalized(name=name) not in pinned:
        return "is not pinned in the root pyproject.toml"
    return None


def find_violations(*, root: Path) -> list[str]:
    root_pyproject = tomllib.loads((root / "pyproject.toml").read_text())
    pinned = _pinned_names(root_pyproject=root_pyproject)
    violations = []
    members = root_pyproject["tool"]["uv"]["workspace"]["members"]
    paths = {path for member in members for path in root.glob(f"{member}/pyproject.toml")}
    for path in sorted(paths):
        pyproject = tomllib.loads(path.read_text())
        for requirement in _requirements(pyproject=pyproject):
            problem = _problem(requirement=requirement, pyproject=pyproject, pinned=pinned)
            if problem is not None:
                violations.append(f"{path.relative_to(root)}: {requirement} {problem}")
    return violations


def main() -> None:
    found = find_violations(root=Path.cwd())
    for violation in found:
        print(violation)
    if found:
        print("Pin versions in [tool.uv] constraint-dependencies and list only names in members")
        sys.exit(1)
