import pytest
from ci.scripts.check_member_dependencies import find_violations


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (
            '[project]\ndependencies = ["httpx"]\n',
            "httpx is not pinned in the root pyproject.toml",
        ),
        (
            '[project]\ndependencies = ["sqlalchemy"]\n',
            "sqlalchemy is not pinned in the root pyproject.toml",
        ),
        (
            '[project]\ndependencies = ["fastapi==0.162.0"]\n',
            "fastapi==0.162.0 must not declare a version",
        ),
        (
            '[project]\ndependencies = ["fastapi>=0.1"]\n',
            "fastapi>=0.1 must not declare a version",
        ),
        (
            '[project]\ndependencies = ["psycopg[binary]==3.3.6"]\n',
            "psycopg[binary]==3.3.6 must not declare a version",
        ),
        (
            '[project]\ndependencies = ["fastapi @ https://example.com/fastapi.whl"]\n',
            "fastapi @ https://example.com/fastapi.whl must not declare a version",
        ),
        (
            '[project]\ndependencies = ["fastapi"]\n'
            '[tool.uv.sources]\nfastapi = { git = "https://example.com/fastapi" }\n',
            "fastapi must not declare its own source",
        ),
        (
            '[project.optional-dependencies]\nweb = ["httpx"]\n',
            "httpx is not pinned in the root pyproject.toml",
        ),
        (
            '[dependency-groups]\nweb = ["httpx"]\n',
            "httpx is not pinned in the root pyproject.toml",
        ),
        (
            '[tool.uv]\ndev-dependencies = ["httpx"]\n',
            "httpx is not pinned in the root pyproject.toml",
        ),
    ],
)
def test_given_a_member_breaking_the_rule_when_checking_then_it_is_reported(write_member, content, expected):
    root = write_member(content=content)

    violations = find_violations(root=root)

    assert violations == [f"pkg/member/pyproject.toml: {expected}"]


@pytest.mark.parametrize(
    "content",
    [
        "[project]\ndependencies = []\n",
        '[project]\ndependencies = ["fastapi"]\n',
        '[project]\ndependencies = ["psycopg[binary]"]\n',
        '[project]\ndependencies = ["typing-extensions"]\n',
        "[project]\ndependencies = [\"fastapi; sys_platform == 'linux'\"]\n",
        '[project]\ndependencies = ["core"]\n[tool.uv.sources]\ncore = { workspace = true }\n',
        '[dependency-groups]\nall = [{ include-group = "other" }]\n',
    ],
)
def test_given_a_member_following_the_rule_when_checking_then_nothing_is_reported(write_member, content):
    root = write_member(content=content)

    violations = find_violations(root=root)

    assert violations == []
