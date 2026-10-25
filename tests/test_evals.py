#!/usr/bin/env python3
"""Guard the eval harness without calling a model.

`evals/run.py --self-check` applies every task setup and asserts its check FAILS
on the untouched fixture. A check that passes without work is a tautology, so
this is the cheapest way to keep the eval honest in CI.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT / "evals"))
from tasks import TASKS  # noqa: E402

ids = [t.id for t in TASKS]
assert len(TASKS) == 10, f"expected 10 tasks, got {len(TASKS)}"
assert len(set(ids)) == len(ids), f"duplicate task ids: {ids}"

proc = subprocess.run(
    [sys.executable, str(ROOT / "evals" / "run.py"), "--self-check"],
    cwd=ROOT, capture_output=True, text=True, timeout=120,
)
ok = proc.returncode == 0
print(("PASS" if ok else "FAIL") + ": agent eval checks fail on the untouched fixture")
if not ok:
    print(proc.stdout[-4000:])
    print(proc.stderr[-2000:])
sys.exit(0 if ok else 1)
