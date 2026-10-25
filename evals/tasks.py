"""Deterministic tasks for the EngineeringOS agent eval.

Each task is a small sandbox plus a check that does not ask a model to judge.
The runner copies the fixture, applies `setup`, snapshots the tree, runs the
agent, then calls `check(repo, baseline)`.

Add tasks here rather than in the runner. Keep checks deterministic: exit codes,
file contents, and importable behaviour. A check that passes on the untouched
fixture is a bug; `run.py --self-check` catches that.
"""

from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Optional

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "pyapp"

NOISE_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".eval"}


# --- helpers -------------------------------------------------------------------

def _files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in NOISE_DIRS for part in path.parts):
            continue
        if path.suffix == ".pyc":
            continue
        yield path.relative_to(root).as_posix(), path


def tree_hashes(root: Path) -> dict[str, str]:
    return {rel: hashlib.sha256(path.read_bytes()).hexdigest() for rel, path in _files(root)}


def changed_files(root: Path, baseline: dict[str, str]) -> set[str]:
    now = tree_hashes(root)
    return {rel for rel in set(baseline) | set(now) if baseline.get(rel) != now.get(rel)}


def read(root: Path, rel: str) -> str:
    path = root / rel
    return path.read_text(encoding="utf-8", errors="replace") if path.is_file() else ""


def run_tests(root: Path, timeout: int = 120) -> tuple[bool, str]:
    env = dict(os.environ, PYTHONPATH=str(root))
    try:
        proc = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
            cwd=root, env=env, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, "test run timed out"
    output = (proc.stdout + proc.stderr)[-4000:]
    return proc.returncode == 0, output


def run_python(root: Path, code: str, timeout: int = 60) -> tuple[bool, str]:
    env = dict(os.environ, PYTHONPATH=str(root))
    try:
        proc = subprocess.run(
            [sys.executable, "-c", code], cwd=root, env=env,
            capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, "python snippet timed out"
    return proc.returncode == 0, (proc.stdout + proc.stderr)[-2000:]


def only_changed(root: Path, baseline: dict[str, str], allowed: set[str]) -> tuple[bool, str]:
    extra = changed_files(root, baseline) - allowed
    return not extra, f"unexpected changes: {sorted(extra)}" if extra else "scope clean"


def mentions(text: str, *needles: str) -> bool:
    low = text.lower()
    return all(n.lower() in low for n in needles)


def count_tasks(text: str) -> int:
    """Count task markers: T-1 style ids or checklist rows."""
    return len(set(re.findall(r"\bT-\d+\b", text))) or len(re.findall(r"^\s*-\s*\[[ x]\]", text, re.M))


# --- fixture mutations ---------------------------------------------------------

def _write(root: Path, rel: str, content: str) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def setup_typo(root: Path) -> None:
    text = read(root, "README.md")
    _write(root, "README.md", text.rstrip("\n") + "\n\nThe libary is used by the billing service.\n")


def setup_broken_average(root: Path) -> None:
    text = read(root, "calc/core.py")
    broken = text.replace(
        '    items = list(values)\n    if not items:\n        return None\n    return sum(items) / len(items)',
        '    items = list(values)\n    return sum(items) / len(items)',
    )
    assert broken != text, "fixture changed: average guard not found"
    _write(root, "calc/core.py", broken)


def setup_security(root: Path) -> None:
    _write(root, "app/__init__.py", "")
    _write(root, "app/handler.py", '''"""Tiny user lookup used by the eval."""

import sqlite3


def get_user(conn: sqlite3.Connection, user_id: str):
    cur = conn.cursor()
    cur.execute(f"SELECT id, email FROM users WHERE id = '{user_id}'")
    return cur.fetchone()
''')


def setup_review(root: Path) -> None:
    _write(root, "calc/window.py", '''"""Sliding-window helpers."""


def last_n(items, n):
    """Return the last n items."""
    return items[-n:-1]
''')
    _write(root, "tests/test_window.py", '''import unittest

from calc.window import last_n


class TestWindow(unittest.TestCase):
    def test_last_two(self):
        self.assertEqual(last_n([1, 2, 3], 2), [2, 3])


if __name__ == "__main__":
    unittest.main()
''')


def setup_research(root: Path) -> None:
    _write(root, "docs/vendor-sync.md", """# Vendor Sync API

The Sync API retries a failed request up to 4 times.

The first retry waits 250 ms. Each subsequent retry doubles the wait.

A request times out after 30 seconds.
""")


def setup_rename(root: Path) -> None:
    _write(root, "calc/core.py", read(root, "calc/core.py").rstrip("\n") + '''


def mean(values):
    """Alias for average, kept for the legacy API."""
    return average(values)
''')
    _write(root, "calc/__init__.py", '''from .core import add, average, divide, mean

__all__ = ["add", "average", "divide", "mean"]
''')
    _write(root, "tests/test_core.py", read(root, "tests/test_core.py").rstrip("\n") + '''


class TestMean(unittest.TestCase):
    def test_mean(self):
        from calc import mean
        self.assertEqual(mean([1, 2, 3]), 2)
''')


# --- checks --------------------------------------------------------------------

def check_typo(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    readme = read(root, "README.md")
    ok_tests, out = run_tests(root)
    core_same = tree_hashes(root).get("calc/core.py") == baseline.get("calc/core.py")
    fixed = "The library is used by the billing service." in readme and "libary" not in readme
    ok = fixed and ok_tests and core_same
    return ok, f"library fixed={fixed} core_unchanged={core_same} tests={ok_tests}\n{out}"


def check_clamp(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    ok_tests, out = run_tests(root)
    ok_expr, expr_out = run_python(root, (
        "from calc import clamp\n"
        "assert clamp(5, 0, 10) == 5\n"
        "assert clamp(-1, 0, 10) == 0\n"
        "assert clamp(11, 0, 10) == 10\n"
        "assert clamp(0, 0, 10) == 0\n"
        "assert clamp(10, 0, 10) == 10\n"
    ))
    return ok_tests and ok_expr, f"tests={ok_tests} clamp={ok_expr}\n{out}{expr_out}"


def check_bug(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    ok_tests, out = run_tests(root)
    ok_expr, expr_out = run_python(root, "from calc import average\nassert average([]) is None\n")
    tests_same = tree_hashes(root).get("tests/test_core.py") == baseline.get("tests/test_core.py")
    return ok_tests and ok_expr and tests_same, f"tests={ok_tests} empty_none={ok_expr} tests_untouched={tests_same}\n{out}{expr_out}"


def check_map(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    text = read(root, "MAP.md")
    scope_ok, scope = only_changed(root, baseline, {"MAP.md"})
    ok = bool(text) and mentions(text, "python3 -m unittest", "calc/core.py", "calc/__init__.py", "convention")
    return ok and scope_ok, f"map={ok} {scope}\n{text[:1200]}"


def check_architecture(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    text = read(root, "ADR.md")
    scope_ok, scope = only_changed(root, baseline, {"ADR.md"})
    alternatives = text.lower().count("alternative")
    ok = (bool(text) and mentions(text, "csv", "json", "recommend", "tradeoff", "failure")
          and alternatives >= 2)
    return ok and scope_ok, f"adr={ok} alternatives={alternatives} {scope}\n{text[:1200]}"


def check_plan(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    text = read(root, "PLAN.md")
    scope_ok, scope = only_changed(root, baseline, {"PLAN.md"})
    tasks = count_tasks(text)
    ok = bool(text) and tasks >= 3 and mentions(text, "acceptance", "depend", "csv", "json")
    return ok and scope_ok, f"plan={ok} tasks={tasks} {scope}\n{text[:1200]}"


def check_security(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    text = read(root, "SECURITY.md")
    scope_ok, scope = only_changed(root, baseline, {"SECURITY.md"})
    injection = "injection" in text.lower() or "sql" in text.lower()
    severity = any(s in text.lower() for s in ("critical", "high"))
    ok = bool(text) and mentions(text, "handler.py") and injection and severity
    return ok and scope_ok, f"security={ok} injection={injection} severity={severity} {scope}\n{text[:1200]}"


def check_review(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    text = read(root, "REVIEW.md")
    scope_ok, scope = only_changed(root, baseline, {"REVIEW.md"})
    finding = mentions(text, "window.py") and (
        "off-by-one" in text.lower() or "off by one" in text.lower() or "last_n" in text.lower())
    verdict = any(v in text.upper() for v in ("CHANGES REQUESTED", "BLOCKER", "MAJOR"))
    return bool(text) and finding and verdict and scope_ok, f"review={finding and verdict} {scope}\n{text[:1200]}"


def check_research(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    text = read(root, "RESEARCH.md")
    scope_ok, scope = only_changed(root, baseline, {"RESEARCH.md"})
    retries = any(s in text.lower() for s in ("4 retries", "four retries", "4 times", "four times"))
    ok = bool(text) and retries and mentions(text, "250", "30", "vendor-sync.md")
    return ok and scope_ok, f"research={ok} retries={retries} {scope}\n{text[:1200]}"


def check_rename(root: Path, baseline: dict[str, str]) -> tuple[bool, str]:
    ok_tests, out = run_tests(root)
    old = [rel for rel, _ in _files(root) if rel.endswith(".py") and "mean(" in read(root, rel)]
    new = any("average_values" in read(root, rel) for rel, _ in _files(root) if rel.endswith(".py"))
    return ok_tests and not old and new, f"tests={ok_tests} old_refs={old} new_name={new}\n{out}"


# --- task table ----------------------------------------------------------------

@dataclass(frozen=True)
class Task:
    id: str
    title: str
    complexity: str
    prompt: str
    check: Callable[[Path, dict[str, str]], tuple[bool, str]]
    setup: Optional[Callable[[Path], None]] = None
    timeout: int = 600


TASKS = [
    Task("typo", "Fix a spelling mistake", "simple",
         "Fix the spelling mistake in ./README.md. The line about the billing service contains it. "
         "Change nothing else.",
         check_typo, setup_typo),
    Task("feature-clamp", "Add clamp with boundary tests", "moderate",
         "Add a function `clamp(value, low, high)` to calc/core.py and export it from calc/__init__.py. "
         "It returns low when value < low, high when value > high, otherwise value. Add unittest coverage "
         "for the boundaries. Run the tests.",
         check_clamp),
    Task("bug-average", "Fix the failing average test", "important",
         "The test suite has a failing test. Fix the bug in calc/core.py so all tests pass. Do not change the tests.",
         check_bug, setup_broken_average),
    Task("repo-map", "Map the repository", "moderate",
         "Map this repository and write the map to MAP.md. Include the stack, entry points, test command, "
         "key files, and conventions. Do not modify any other file.",
         check_map),
    Task("architecture-export", "Propose an export architecture", "complex",
         "Propose an architecture for adding CSV and JSON export to this library without changing the public API. "
         "Write the proposal to ADR.md. Include at least two alternatives, tradeoffs, failure modes, and a "
         "recommendation. Do not write implementation code.",
         check_architecture),
    Task("plan-export", "Plan the export work", "complex",
         "Write an implementation plan for adding CSV and JSON export. Write PLAN.md with phases, at least three "
         "tasks, dependencies, and acceptance criteria per task. Do not implement anything.",
         check_plan),
    Task("security-sql", "Review a seeded SQL injection", "important",
         "Perform a security review of this repository. Write your findings to SECURITY.md with severity, "
         "location, impact, and remediation. Do not change code.",
         check_security, setup_security),
    Task("review-offbyone", "Review a seeded off-by-one", "important",
         "Review the current changes in this repository. Write your review to REVIEW.md with severity, location, "
         "and a verdict. Do not fix anything.",
         check_review, setup_review),
    Task("research-retry", "Answer from bundled docs", "moderate",
         "Using only the bundled docs in this repository, answer: how many retries does the Sync API perform, "
         "and what is the backoff schedule? Write the answer to RESEARCH.md and cite the source file.",
         check_research, setup_research),
    Task("refactor-rename", "Rename mean across the codebase", "complex",
         "Rename `mean` to `average_values` across the codebase, including tests and exports. Run the tests.",
         check_rename, setup_rename),
]

TASKS_BY_ID = {t.id: t for t in TASKS}


def prepare(root: Path, task: Task) -> dict[str, str]:
    """Copy the fixture, apply the task setup, and return the baseline hashes."""
    import shutil
    if root.exists():
        shutil.rmtree(root)
    shutil.copytree(FIXTURE, root)
    if task.setup:
        task.setup(root)
    return tree_hashes(root)
