from collections.abc import Callable
from pathlib import Path

import pytest

ROOT_PYPROJECT = """
[tool.uv]
constraint-dependencies = [
    "fastapi==0.162.0",
    "psycopg==3.3.6",
    "typing_extensions==4.15.0",
    "sqlalchemy>=2",
]

[tool.uv.workspace]
members = ["pkg/*"]
"""


@pytest.fixture
def write_member(tmp_path: Path) -> Callable[..., Path]:
    def write(*, content: str) -> Path:
        (tmp_path / "pyproject.toml").write_text(ROOT_PYPROJECT)
        member = tmp_path / "pkg" / "member"
        member.mkdir(parents=True)
        (member / "pyproject.toml").write_text(content)
        return tmp_path

    return write
