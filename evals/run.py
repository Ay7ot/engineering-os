#!/usr/bin/env python3
"""Run the EngineeringOS agent eval.

Phase 0 of the subagent review: measure a task-completion baseline before
changing routing. The harness is not part of CI. It costs real model tokens.

    python3 evals/run.py --self-check          # checks fail on the untouched fixture
    python3 evals/run.py --config both --runs 1
    python3 evals/run.py --report

Each config gets its own engine copy, OpenCode config dir, HOME and data dir, so
the only difference between baseline and current is the agents/ sources.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sqlite3
import statistics
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
# Keep the work tree outside ROOT. OpenCode walks up to the enclosing git repo,
# so a sandbox under the engine makes the engine the project.
WORK = Path(os.environ.get("EOS_EVAL_WORK", "/tmp/opencode/eos-evals"))
RESULTS = WORK / "results.jsonl"
DB = Path.home() / ".local" / "share" / "opencode" / "opencode.db"
SCHEMA_VERSION = 1


def now_ms() -> int:
    return int(time.time() * 1000)


def log(msg: str) -> None:
    print(msg, flush=True)


# --- engines and homes ---------------------------------------------------------

def _copy_current(dest: Path) -> None:
    def ignore(directory, names):
        skip = {".git", "data", "evals", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache"}
        return [n for n in names if n in skip]
    shutil.copytree(ROOT, dest, ignore=ignore)


def _copy_baseline(dest: Path) -> None:
    archive = subprocess.run(["git", "archive", "HEAD"], cwd=ROOT, check=True,
                             stdout=subprocess.PIPE)
    dest.mkdir(parents=True)
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive.stdout, check=True)
    # The engine copy is the agent's install, not an eval task. Keep fixtures out.
    shutil.rmtree(dest / "evals", ignore_errors=True)


def prepare_engine(name: str) -> Path:
    dest = WORK / "engines" / name
    if dest.exists():
        shutil.rmtree(dest)
    if name == "baseline":
        _copy_baseline(dest)
    elif name == "current":
        _copy_current(dest)
    else:
        raise SystemExit(f"unknown config {name!r}")
    data = dest / "data"
    data.mkdir(exist_ok=True)
    user = ROOT / "data" / "USER.md"
    (data / "USER.md").write_text(
        user.read_text(encoding="utf-8") if user.is_file() else (ROOT / "USER.example.md").read_text(encoding="utf-8"),
        encoding="utf-8")
    return dest


def prepare_home(name: str, engine: Path) -> tuple[Path, Path]:
    home = WORK / "homes" / name
    if home.exists():
        shutil.rmtree(home)
    (home / ".local" / "share").mkdir(parents=True)
    linked = home / ".local" / "share" / "opencode"
    if DB.parent.exists():
        linked.symlink_to(DB.parent, target_is_directory=True)
    else:
        linked.mkdir()
    (home / "EngineeringOS").symlink_to(engine, target_is_directory=True)
    config_home = home / ".config"
    env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(config_home),
               XDG_DATA_HOME=str(home / ".local" / "share"),
               ENGINEERING_OS_DATA=str(engine / "data"))
    proc = subprocess.run([str(engine / "scripts" / "eng"), "sync", "opencode"],
                          cwd=engine, env=env, capture_output=True, text=True, timeout=300)
    if proc.returncode != 0:
        log(proc.stdout)
        log(proc.stderr)
        raise SystemExit(f"eng sync failed for {name}")
    _rewrite_engine_paths(config_home / "opencode", engine)
    real_service = Path.home() / ".config" / "opencode" / "service.json"
    if real_service.is_file():
        shutil.copy(real_service, config_home / "opencode" / "service.json")
    return home, config_home


def flatten_models(agents_dir: Path, model: str | None) -> None:
    """Put every installed agent on one model, for a fair routing comparison.

    Provider 503s make OpenCode fall back to a free model and retry for minutes,
    which corrupts a run. Flattening also removes the model-tier difference, so
    the only variable is routing and prompt content.
    """
    if not model:
        return
    for path in agents_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        if not re.search(r"(?m)^model:", text):
            continue
        path.write_text(re.sub(r"(?m)^model:.*$", f'model: "{model}"', text), encoding="utf-8")


def _rewrite_engine_paths(config_dir: Path, engine: Path) -> None:
    """Point the installed prompts at this config's engine copy.

    The source prompts use `~/EngineeringOS`. A model expands `~` from what it
    knows, not from our env, so an absolute path is the only reliable isolation.
    """
    target = str(engine.resolve())
    old = ("~/EngineeringOS", "/home/ayomide/EngineeringOS")
    for path in config_dir.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".json", ".jsonc"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if not any(o in text for o in old):
            continue
        for o in old:
            text = text.replace(o, target)
        path.write_text(text, encoding="utf-8")


# --- one run -------------------------------------------------------------------

def _text(value) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", "replace")
    return value or ""


def _run(cmd, cwd, env, timeout):
    try:
        proc = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True, timeout=timeout)
        return proc.returncode, _text(proc.stdout), _text(proc.stderr), False
    except subprocess.TimeoutExpired as exc:
        return 124, _text(exc.stdout), _text(exc.stderr) + "\n[timeout]", True


def _git(repo: Path, env: dict) -> None:
    _run(["git", "init", "-q"], repo, env, 30)
    _run(["git", "add", "-A"], repo, env, 30)
    _run(["git", "commit", "-q", "-m", "eval baseline"], repo, env, 30)


def session_metrics(repo: Path, start_ms: int, db: Path) -> dict:
    empty = {"session_id": None, "duration_s": None, "cost": None, "tokens_input": None,
             "tokens_output": None, "tokens_reasoning": None, "subagents": None}
    if not db.is_file():
        return empty
    con = None
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        con.row_factory = sqlite3.Row
        row = con.execute(
            "select id from session_v2 where directory=? and parent_id is null and time_created>=? "
            "order by time_created desc limit 1",
            (str(repo.resolve()), start_ms - 5000)).fetchone()
        if not row:
            return empty
        rows = con.execute(
            "with recursive tree(id) as ("
            "  select id from session_v2 where id=?"
            "  union all"
            "  select s.id from session_v2 s join tree t on s.parent_id=t.id"
            ") select s.* from session_v2 s join tree t on s.id=t.id",
            (row["id"],)).fetchall()
    except sqlite3.Error:
        return empty
    finally:
        if con is not None:
            try:
                con.close()
            except Exception:
                pass
    created = min(r["time_created"] for r in rows)
    updated = max(r["time_updated"] for r in rows)
    return {
        "session_id": row["id"],
        "duration_s": round((updated - created) / 1000.0, 1),
        "cost": round(sum(r["cost"] or 0 for r in rows), 6),
        "tokens_input": sum(r["tokens_input"] or 0 for r in rows),
        "tokens_output": sum(r["tokens_output"] or 0 for r in rows),
        "tokens_reasoning": sum(r["tokens_reasoning"] or 0 for r in rows),
        "subagents": max(len(rows) - 1, 0),
    }


def run_one(config: str, task, index: int, engine: Path, home: Path,
            config_home: Path, model: str | None, flatten_model: str | None,
            timeout_override: int, dry: bool) -> dict:
    from tasks import prepare

    run_dir = WORK / "runs" / config / task.id / str(index)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    repo = run_dir / "repo"
    baseline = prepare(repo, task)
    env = dict(os.environ, HOME=str(home), XDG_CONFIG_HOME=str(config_home),
               XDG_DATA_HOME=str(home / ".local" / "share"), PWD=str(repo),
               ENGINEERING_OS_DATA=str(engine / "data"),
               PYTHONPATH=str(repo), NO_COLOR="1",
               GIT_AUTHOR_NAME="EngineeringOS Eval", GIT_AUTHOR_EMAIL="eval@example.invalid",
               GIT_COMMITTER_NAME="EngineeringOS Eval", GIT_COMMITTER_EMAIL="eval@example.invalid")
    _git(repo, env)
    prompt = ("You are in an isolated evaluation sandbox. Your working directory is the project under "
              "evaluation; work only inside it. Do not read or edit the EngineeringOS engine repository. "
              "Complete the task without asking questions; make reasonable assumptions. Do not access "
              "the network.\n\n" + task.prompt)
    # A static title skips OpenCode's title-generation call, which uses a small
    # default model and fails the whole run when that endpoint is unavailable.
    cmd = ["opencode", "run", "--standalone", "--agent", "lead", "--format", "json", "--auto",
           "--title", f"eval {config} {task.id} {index}"]
    if model:
        cmd += ["--model", model]
    cmd.append(prompt)
    if dry:
        log(f"  DRY {config}/{task.id}/{index}: {task.prompt[:60]}...")
        return {}
    start = now_ms()
    code, out, err, timed_out = _run(cmd, repo, env, timeout_override or task.timeout)
    wall = round((time.time() * 1000 - start) / 1000.0, 1)
    (run_dir / "agent.log").write_text(out + "\n--- stderr ---\n" + err, encoding="utf-8")
    try:
        passed, detail = task.check(repo, baseline)
    except Exception as exc:  # a broken check must not abort the suite
        passed, detail = False, f"check raised: {exc!r}"
    if timed_out:
        passed, detail = False, "run timed out\n" + detail
    metrics = session_metrics(repo, start, home / ".local" / "share" / "opencode" / "opencode.db")
    result = {"schema": SCHEMA_VERSION, "ts": datetime.now(timezone.utc).isoformat(),
              "config": config, "task": task.id, "run": index,
              "model": flatten_model or model, "timeout_s": timeout_override or task.timeout,
              "passed": passed, "detail": detail[-4000:], "wall_s": wall, "exit": code,
              "timed_out": timed_out,
              **metrics}
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    with RESULTS.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(result) + "\n")
    status = "PASS" if passed else "FAIL"
    cost = f"${metrics['cost']:.4f}" if metrics["cost"] is not None else "$?"
    subs = metrics["subagents"] if metrics["subagents"] is not None else "?"
    log(f"  {status} {config}/{task.id}/{index}  {wall}s  {cost}  subagents={subs}")
    if not passed:
        log("        " + detail.replace("\n", "\n        ")[:800])
    return result


# --- self-check ----------------------------------------------------------------

def self_check() -> int:
    from tasks import TASKS, prepare
    log("self-check: every check must FAIL on the untouched fixture")
    bad = []
    for task in TASKS:
        repo = WORK / "selfcheck" / task.id
        baseline = prepare(repo, task)
        try:
            passed, detail = task.check(repo, baseline)
        except Exception as exc:
            passed, detail = False, f"raised {exc!r}"
        log(f"  {'BAD' if passed else 'ok '} {task.id}: {detail.splitlines()[0][:100]}")
        if passed:
            bad.append(task.id)
    if bad:
        log(f"self-check FAILED: checks pass without work: {bad}")
        return 1
    log("self-check passed")
    return 0


# --- report --------------------------------------------------------------------

def report(path: Path = RESULTS) -> int:
    if not path.is_file():
        log(f"no results at {path}")
        return 1
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if not rows:
        log("no results")
        return 1
    configs = sorted({r["config"] for r in rows})
    tasks = sorted({r["task"] for r in rows})
    log(f"{'task':22}" + "".join(f"{c:>26}" for c in configs))
    for task in tasks:
        cells = []
        for config in configs:
            rs = [r for r in rows if r["task"] == task and r["config"] == config]
            if not rs:
                cells.append("-")
                continue
            passed = sum(1 for r in rs if r["passed"])
            wall = statistics.median([r["wall_s"] for r in rs])
            costs = [r["cost"] for r in rs if r["cost"] is not None]
            cost = f"${statistics.median(costs):.3f}" if costs else "$?"
            subs = [r["subagents"] for r in rs if r["subagents"] is not None]
            sub = f" sa={statistics.median(subs):.0f}" if subs else ""
            cells.append(f"{passed}/{len(rs)} {wall:.0f}s {cost}{sub}")
        log(f"{task:22}" + "".join(f"{c:>26}" for c in cells))
    log("")
    for config in configs:
        rs = [r for r in rows if r["config"] == config]
        if not rs:
            continue
        log(f"{config}: {sum(1 for r in rs if r['passed'])}/{len(rs)} pass, "
            f"${sum(r['cost'] or 0 for r in rs):.4f}, "
            f"{sum(r['wall_s'] for r in rs):.0f}s, "
            f"{sum(r['subagents'] or 0 for r in rs)} subagents, "
            f"{sum(r['tokens_input'] or 0 for r in rs):,} in / "
            f"{sum(r['tokens_output'] or 0 for r in rs):,} out")
    log("")
    for task in tasks:
        outcomes = {}
        for config in configs:
            rs = [r for r in rows if r["task"] == task and r["config"] == config]
            outcomes[config] = sum(1 for r in rs if r["passed"]) / len(rs) if rs else None
        if len(set(outcomes.values())) > 1:
            log(f"DIFF {task}: " + ", ".join(f"{c}={v:.0%}" for c, v in outcomes.items()))
    return 0


# --- main ----------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--config", choices=["both", "baseline", "current"], default="both")
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--tasks", default="", help="comma-separated task ids")
    ap.add_argument("--model", default=None, help="override the lead model, e.g. provider/model#variant")
    ap.add_argument("--flatten-model", default=None,
                    help="put every installed agent on this model (recommended for comparisons)")
    ap.add_argument("--timeout", type=int, default=0, help="override the per-task timeout in seconds")
    ap.add_argument("--self-check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--clean", action="store_true", help="delete evals/.work before running")
    args = ap.parse_args()

    if args.clean and WORK.exists():
        shutil.rmtree(WORK)
    if args.self_check:
        return self_check()
    if args.report:
        return report()
    if not args.model and not args.dry_run:
        log("warning: no --model; OpenCode may fall back to a free model. "
            "Pass --model and --flatten-model for a comparison.")

    sys.path.insert(0, str(HERE))
    from tasks import TASKS_BY_ID
    wanted = [t.strip() for t in args.tasks.split(",") if t.strip()]
    tasks = [TASKS_BY_ID[t] for t in wanted] if wanted else list(TASKS_BY_ID.values())
    configs = ["baseline", "current"] if args.config == "both" else [args.config]
    WORK.mkdir(parents=True, exist_ok=True)

    for config in configs:
        log(f"preparing {config} ...")
        engine = prepare_engine(config)
        home, config_home = prepare_home(config, engine)
        flatten_models(config_home / "opencode" / "agents", args.flatten_model)
        for task in tasks:
            for i in range(1, args.runs + 1):
                run_one(config, task, i, engine, home, config_home,
                        args.model, args.flatten_model, args.timeout, args.dry_run)
    if not args.dry_run:
        log("")
        report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
