#!/usr/bin/env python3
"""Tests for the editor-neutral source, the shared adapter layer and the
OpenCode adapter. Hermetic: temp HOME, fake `opencode` on PATH, no network.
Run: python3 tests/test_adapters.py
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from adapters.common import (SourceError, Writer, emit_yaml, load_source,  # noqa: E402
                             parse_frontmatter, strip_jsonc)
from adapters.opencode import adapter as oc  # noqa: E402

FIXTURES = ROOT / "tests" / "fixtures" / "opencode-v1"
passed = failed = 0


def check(desc, cond, detail=""):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS: {desc}")
    else:
        failed += 1
        print(f"  FAIL: {desc}{' (' + str(detail) + ')' if detail else ''}")


def raises(fn):
    try:
        fn()
    except SourceError as exc:
        return str(exc)
    return None


def ordered(x):
    """Deep structure including key order, for order-sensitive comparisons."""
    if isinstance(x, dict):
        return [(k, ordered(v)) for k, v in x.items()]
    return x


def run_sync(home, target, extra_env=None, engine=ROOT):
    env = dict(os.environ, HOME=str(home))
    env.pop("CLAUDE_CONFIG_DIR", None)
    env.pop("XDG_CONFIG_HOME", None)
    env.update(extra_env or {})
    return subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "eos_sync.py"), "sync", "--target", target,
         "--engine", str(engine), "--data", str(home / "data"), "--python", "/usr/bin/python3",
         "--claude-cli", ""],
        capture_output=True, text=True, env=env)


def fake_opencode(bindir, version):
    bindir.mkdir(parents=True, exist_ok=True)
    exe = bindir / "opencode"
    exe.write_text(f"#!/bin/sh\necho 'opencode v{version}'\n")
    exe.chmod(0o755)
    return {"PATH": f"{bindir}:/usr/bin:/bin"}


print("test_adapters: parser")
check("parses quoted keys and nested maps",
      parse_frontmatter('---\na:\n  "x *": allow\n  b: deny\n---\nB\n')[0] == {"a": {"x *": "allow", "b": "deny"}})
check("folded block", parse_frontmatter("---\nd: >-\n  one\n  two\n---\n")[0]["d"] == "one two")
check("inline comment stripped", parse_frontmatter("---\na: deny  # c\n---\n")[0]["a"] == "deny")
check("body preserved byte-for-byte", parse_frontmatter("---\na: b\n---\n\n# T\n  x\n")[1] == "\n# T\n  x\n")
check("lists rejected loudly", "lists are not supported" in (raises(lambda: parse_frontmatter("---\na:\n  - x\n---\n", "f.md")) or ""))
check("tabs rejected", raises(lambda: parse_frontmatter("---\na:\n\tb: c\n---\n", "f.md")) is not None)
check("flow collections rejected", raises(lambda: parse_frontmatter("---\na: [x, y]\n---\n", "f.md")) is not None)
check("unclosed frontmatter rejected", raises(lambda: parse_frontmatter("---\na: b\n", "f.md")) is not None)
check("duplicate key rejected", raises(lambda: parse_frontmatter("---\na: b\na: c\n---\n", "f.md")) is not None)
check("quoted value with trailing comment", parse_frontmatter('---\nm: "a/b" # c\n---\n')[0]["m"] == "a/b")
check("bad escape rejected", raises(lambda: parse_frontmatter('---\nm: "a\\qb"\n---\n', "f.md")) is not None)
check("text after quoted value rejected", raises(lambda: parse_frontmatter('---\nm: "a" b\n---\n', "f.md")) is not None)
check("YAML-special words emitted quoted", emit_yaml({"a": "True", "b": "NULL", "c": "yes"}) == 'a: "True"\nb: "NULL"\nc: "yes"')
check("JSONC trailing commas accepted", json.loads(strip_jsonc('{"a": [1, 2,], // c\n "b": "x,}",}')) == {"a": [1, 2], "b": "x,}"})
err = raises(lambda: parse_frontmatter("---\nok: 1\nbad:\n  - x\n---\n", "agents/x.md")) or ""
check("error carries file:line", "agents/x.md:4" in err, err)

print("test_adapters: emitter round trip on every source file")
src = load_source(ROOT)
bad = []
for item in src.agents + src.commands + src.skills:
    fm = item.fm
    back, _ = parse_frontmatter("---\n" + emit_yaml(fm) + "\n---\n")
    if ordered(back) != ordered(fm):
        bad.append(item.path.name)
check("emit -> parse preserves values and key order", not bad, bad)
check("numbers and booleans emitted unquoted", emit_yaml({"t": "0.1", "s": "false"}) == "t: 0.1\ns: false")

print("test_adapters: source validation")
check("source loads", len(src.agents) == 9 and len(src.commands) == 6 and len(src.skills) >= 17,
      (len(src.agents), len(src.commands), len(src.skills)))
check("exactly one primary agent (lead)", [a.name for a in src.primary()] == ["lead"])
check("no editor-specific keys at top level",
      all(not ({"mode", "permission", "temperature", "model", "agent", "subtask"} & set(i.fm)) for i in src.agents + src.commands))

with tempfile.TemporaryDirectory() as t:
    eng = Path(t) / "engine"
    for d in ("agents", "skills", "commands"):
        shutil.copytree(ROOT / d, eng / d)
    bad_agent = eng / "agents" / "explorer.md"
    bad_agent.write_text(bad_agent.read_text().replace("role: subagent", "mode: subagent", 1))
    check("unknown key rejected", "unknown frontmatter keys" in (raises(lambda: load_source(eng)) or ""))
    bad_agent.write_text(bad_agent.read_text().replace("mode: subagent", "role: helper", 1))
    check("bad role rejected", "'role' must be one of" in (raises(lambda: load_source(eng)) or ""))
    bad_agent.write_text(bad_agent.read_text().replace("role: helper", "role: subagent", 1).replace("name: explorer", "name: other", 1))
    check("name/file mismatch rejected", "must equal the file name" in (raises(lambda: load_source(eng)) or ""))
    bad_agent.write_text(bad_agent.read_text().replace("name: other", "name: explorer", 1).replace(
        '    "*": deny\n    "git status *": allow', '    "git status *": allow\n    "*": deny', 1))
    check("'*' default must be the first rule", "must be the first rule" in (raises(lambda: load_source(eng)) or ""))

print("test_adapters: OpenCode golden (vs pre-migration opencode/ files)")
# Intended changes since the fixtures were captured. The golden compares each
# rendered agent with its fixture after applying exactly these edits, so any
# other drift (a dropped rule, a reorder, a stray prompt edit) still fails.
# bash: rules removed in place, then new rules appended in order.
GIT_BRANCH_READ = ["git branch", "git branch -a", "git branch -r", "git branch -v", "git branch -vv",
                   "git branch --show-current", "git branch --list *", "git branch --contains *",
                   "git branch --merged *", "git branch --no-merged *"]
GIT_REMOTE_READ = ["git remote", "git remote -v", "git remote get-url *"]


def no_git_writes(*subs):
    return [(f"git {s} *{flag}*", "deny") for s in subs for flag in ("--output", "--ext-diff")]


def allows(*keys):
    return [(k, "allow") for k in keys]


EXPLORER_TOOLS_OLD = "(`status`, `rev-parse`, `log`, `branch`, `remote`, `ls-files`)."
EXPLORER_TOOLS_NEW = ("(`status`, `rev-parse`, `log`, `ls-files`, listing forms of `branch` such as "
                      "`git branch -a` / `git branch --list <pattern>`, and `git remote -v` / "
                      "`git remote get-url <name>`). Anything that changes branches, remotes, or writes "
                      "files (e.g. `git branch -D`, `git remote set-url`, `git log --output`) is denied.")
RESEARCHER_RISKS = "- Identify risks and limitations, not just answers.\n"
RESEARCHER_TOOLS = (
    "- TOOL RESTRICTIONS (by design): `bash` is limited to read-only git inspection of local repos "
    "(`log`, `show`, `diff`, `status`, `rev-parse`, `ls-files`, `describe`, listing forms of "
    "`branch`/`tag`, `git remote -v`) and `opencode mcp`. Do not clone, fetch, or change any repo; "
    "read upstream source through `webfetch` (e.g. raw GitHub files) instead.\n")
FIXTURE_DELTAS = {  # 2026-10-10: read-only agents get read-only git in OpenCode too
    "explorer": {"bash_remove": ["git branch *", "git remote *"],
                 "bash_add": allows(*GIT_BRANCH_READ, *GIT_REMOTE_READ) + no_git_writes("log"),
                 "body": [(EXPLORER_TOOLS_OLD, EXPLORER_TOOLS_NEW)]},
    "reviewer": {"bash_remove": ["git branch *"],
                 "bash_add": allows(*GIT_BRANCH_READ) + no_git_writes("diff", "log", "show")},
    "security": {"bash_add": no_git_writes("diff", "log", "show")},
    "researcher": {"bash_remove": ["git *"],
                   "bash_add": allows("git status *", "git rev-parse *", "git log *", "git show *",
                                      "git diff *", "git ls-files *", "git describe *", "git tag",
                                      "git tag --list *", "git tag -l *", *GIT_BRANCH_READ,
                                      *GIT_REMOTE_READ) + no_git_writes("diff", "log", "show"),
                   "body": [(RESEARCHER_RISKS, RESEARCHER_RISKS + RESEARCHER_TOOLS)]},
    "architect": {"bash_add": no_git_writes("log")},
}


def apply_delta(name, fm, body, problems):
    d = FIXTURE_DELTAS.get(name)
    if not d:
        return fm, body
    bash = dict(fm["permission"]["bash"])
    for k in d.get("bash_remove", []):
        if k not in bash:
            problems.append(f"delta for {name}: {k!r} not in fixture")
        bash.pop(k, None)
    for k, v in d.get("bash_add", []):
        if k in bash:
            problems.append(f"delta for {name}: {k!r} already in fixture")
        bash[k] = v
    fm = dict(fm, permission=dict(fm["permission"], bash=bash))
    for a, b in d.get("body", []):
        if body.count(a) != 1:
            problems.append(f"delta for {name}: body text not found exactly once: {a[:40]!r}")
        body = body.replace(a, b, 1)
    return fm, body


mism, delta_problems = [], []
for a in src.agents:
    # typed=True: 0.1 / false must stay number / bool, not become "0.1" / "false"
    new = parse_frontmatter(oc.render_agent(a), typed=True)
    old = parse_frontmatter((FIXTURES / "agents" / f"{a.name}.md").read_text(), typed=True)
    old = apply_delta(a.name, *old, delta_problems)
    if ordered(new[0]) != ordered(old[0]) or new[1] != old[1]:
        mism.append(f"agents/{a.name}")
for c in src.commands:
    new = parse_frontmatter(oc.render_command(c), typed=True)
    old = parse_frontmatter((FIXTURES / "commands" / f"{c.name}.md").read_text(), typed=True)
    if ordered(new[0]) != ordered(old[0]) or new[1] != old[1]:
        mism.append(f"commands/{c.name}")
for s in src.skills:
    fx = FIXTURES / "skills" / s.name / "SKILL.md"
    if fx.exists() and oc.render_skill(s) != fx.read_bytes():
        mism.append(f"skills/{s.name}")
check("fixture deltas apply cleanly", not delta_problems, delta_problems)
check("every agent, command and skill matches the fixture + declared deltas (typed, order-sensitive)", not mism, mism)
check("deltas only touch existing agents", set(FIXTURE_DELTAS) <= {a.name for a in src.agents}, set(FIXTURE_DELTAS))


def oc_match(cmd, pattern):
    """OpenCode wildcard: '*' is any run of characters; a trailing ' *' is optional."""
    rx = "".join(".*" if c == "*" else re.escape(c) for c in pattern)
    if pattern.endswith(" *"):
        rx = rx[:-len(re.escape(" ") + ".*")] + "( .*)?"
    return re.fullmatch(rx, cmd, re.S) is not None


def oc_bash(rules, cmd):
    """OpenCode resolves a permission map by the last matching rule."""
    if isinstance(rules, str):
        return rules
    hits = [v for k, v in rules.items() if oc_match(cmd, k)]
    return hits[-1] if hits else "ask"


print("test_adapters: read-only agents cannot write through git (OpenCode semantics)")
check("matcher: trailing ' *' optional", oc_match("git log", "git log *") and oc_match("git log -1", "git log *"))
check("matcher: exact rule is exact", oc_match("git branch -a", "git branch -a") and not oc_match("git branch -a x", "git branch -a"))
MUTATING_GIT = ["git push", "git push origin main", "git reset --hard", "git clean -fdx", "git clone https://x/y",
                "git fetch", "git pull", "git checkout .", "git commit -m x", "git stash", "git config user.name x",
                "git branch newb", "git branch -D main", "git branch -m a b", "git branch -f main HEAD~1",
                "git branch --delete main", "git branch -u origin/x", "git remote add x https://x",
                "git remote set-url origin https://x", "git remote remove origin", "git remote rename origin x",
                "git tag v9", "git tag -d v1", "git log --output=/tmp/x", "git log -p --output /tmp/x",
                "git show --output=/tmp/x HEAD", "git diff --output=/tmp/x", "git diff --ext-diff",
                "git -c alias.x=!sh x", "git -C /tmp push"]
READ_ONLY = ["explorer", "reviewer", "security", "researcher", "architect"]


def git_leaks(maps):
    return [f"{n}: {c}" for n in READ_ONLY for c in MUTATING_GIT if oc_bash(maps[n], c) == "allow"]


old_maps = {n: parse_frontmatter((FIXTURES / "agents" / f"{n}.md").read_text())[0]["permission"]["bash"]
            for n in READ_ONLY}
check("simulation flags the pre-change maps (researcher git *, explorer git branch *)",
      {"researcher: git push", "explorer: git branch -D main", "explorer: git remote set-url origin https://x",
       "explorer: git log --output=/tmp/x"} <= set(git_leaks(old_maps)))
leaks = git_leaks({a.name: a.fm["permissions"]["bash"] for a in src.agents})
check("no read-only agent may run a mutating git command", not leaks, leaks)
by_name = {a.name: a.fm["permissions"]["bash"] for a in src.agents}
want = {"explorer": ["git status", "git log --oneline -5", "git branch -a", "git branch --list 'feat/*'",
                     "git remote -v", "git remote get-url origin", "git ls-files src"],
        "reviewer": ["git diff main...HEAD", "git show HEAD", "git branch --contains HEAD"],
        "researcher": ["git log -3", "git tag --list 'v*'", "git describe --tags", "opencode mcp list"],
        "architect": ["git log --oneline"],
        "security": ["git diff", "npm audit"]}
lost = [f"{n}: {c}" for n, cs in want.items() for c in cs if oc_bash(by_name[n], c) != "allow"]
check("read-only git inspection still allowed", not lost, lost)
check("typed golden would catch quoting drift",
      parse_frontmatter("---\nt: 0.1\n---\n", typed=True)[0] != parse_frontmatter('---\nt: "0.1"\n---\n', typed=True)[0])

print("test_adapters: OpenCode install (sandbox HOME)")
with tempfile.TemporaryDirectory() as t:
    home = Path(t)
    env = fake_opencode(home / "bin", "2.0.18")
    ocdir = home / ".config" / "opencode"
    (ocdir / "agents").mkdir(parents=True)
    # Legacy copy-based install (no manifest) + a user's own agent.
    shutil.copy(FIXTURES / "agents" / "explorer.md", ocdir / "agents" / "explorer.md")
    (ocdir / "agents" / "mine.md").write_text("---\ndescription: mine\nmode: subagent\n---\nkeep\n")
    (ocdir / "opencode.jsonc").write_text(
        '{\n  // user comment\n  "default_agent": "build",\n  "mcp": {\n'
        '    "engineering-memory": {"type": "local", "command": ["/usr/bin/python3", "' + str(ROOT) +
        '/mcp/engineering-memory/server.py"], "timeout": 10000},\n'
        '    "servers": {\n      "neon": {"type": "remote", "url": "https://mcp.neon.tech/mcp"},\n'
        '      "engineering-memory": {"type": "local", "command": ["x"], "timeout": {"catalog": 5000, "execution": 6000}}\n'
        '    }\n  }\n}\n')
    r = run_sync(home, "opencode", env)
    check("sync succeeds", r.returncode == 0, r.stderr or r.stdout)
    check("legacy file adopted, not skipped", "SKIPPED" not in r.stdout, r.stdout)
    check("all agents installed", all((ocdir / "agents" / f"{a.name}.md").is_file() for a in src.agents))
    check("user agent untouched", (ocdir / "agents" / "mine.md").read_text().endswith("keep\n"))
    cfg = json.loads(strip_jsonc((ocdir / "opencode.jsonc").read_text()))
    mem = cfg["mcp"]["servers"]["engineering-memory"]
    check("MCP written in v2 shape", mem["command"][1].endswith("mcp/engineering-memory/server.py") and mem["type"] == "local")
    check("v2 timeout object preserved", mem["timeout"] == {"catalog": 5000, "execution": 6000}, mem.get("timeout"))
    check("data dir passed", mem["environment"]["ENGINEERING_OS_DATA"] == str(home / "data"))
    check("stale v1 entry (ours) removed", "engineering-memory" not in cfg["mcp"])
    check("other MCP servers kept", "neon" in cfg["mcp"]["servers"])
    check("user default_agent respected", cfg["default_agent"] == "build")
    bak = ocdir / "opencode.jsonc.engineeringos.bak"
    check("backup keeps the user's original (with comments)", "// user comment" in bak.read_text())
    check("shape choice is logged", "MCP config shape v2 (config already uses mcp.servers)" in r.stdout, r.stdout)
    r2 = run_sync(home, "opencode", env)
    check("second sync is a no-op", "(0 files changed)" in r2.stdout and "already configured" in r2.stdout, r2.stdout)
    cfgp = ocdir / "opencode.jsonc"
    cfgp.write_text(cfgp.read_text().replace('"default_agent": "build"', '"default_agent": "plan"'))
    run_sync(home, "opencode", env)
    check("first backup is never overwritten", "// user comment" in bak.read_text())
    # After the manifest exists, a file we do not own is never overwritten.
    man = ocdir / ".engineeringos-manifest.json"
    m = json.loads(man.read_text())
    target = str(ocdir / "commands" / "feature.md")
    m["files"].remove(target)
    man.write_text(json.dumps(m))
    Path(target).write_text("user edit\n")
    r3 = run_sync(home, "opencode", env)
    check("unowned file reported SKIPPED", f"SKIPPED {target}" in r3.stdout, r3.stdout)
    check("unowned file untouched", Path(target).read_text() == "user edit\n")

def shape_for(version_line, cfg_text=None):
    with tempfile.TemporaryDirectory() as t:
        home = Path(t)
        env = fake_opencode(home / "bin", "0") if version_line is not None else {"PATH": "/usr/bin:/bin"}
        if version_line is not None:
            (home / "bin" / "opencode").write_text(f"#!/bin/sh\nprintf '%s\\n' \"{version_line}\"\n")
        if cfg_text is not None:
            (home / ".config" / "opencode").mkdir(parents=True)
            (home / ".config" / "opencode" / "opencode.jsonc").write_text(cfg_text)
        r = run_sync(home, "opencode", env)
        cfg = json.loads(strip_jsonc((home / ".config" / "opencode" / "opencode.jsonc").read_text()))
        return ("v2" if "servers" in cfg.get("mcp", {}) else "v1"), r.stdout


check("update notice on later line ignored", shape_for("opencode v1.9.3\nupdate available 2.1.0")[0] == "v1")
check("no CLI + no config defaults to v2", shape_for(None)[0] == "v2")
v1cfg = '{"mcp": {"engineering-memory": {"type": "local", "command": ["/usr/bin/python3", "' + str(ROOT) + '/mcp/engineering-memory/server.py"]}}}'
check("no CLI + existing v1 entry keeps v1", shape_for(None, v1cfg)[0] == "v1")
with tempfile.TemporaryDirectory() as t:
    home = Path(t)
    (home / ".config" / "opencode").mkdir(parents=True)
    (home / ".config" / "opencode" / "opencode.jsonc").write_text('{"mcp": "nope"}')
    r = run_sync(home, "opencode", {"PATH": "/usr/bin:/bin"})
    check("non-object mcp fails cleanly", r.returncode != 0 and "is not an object" in (r.stdout + r.stderr) and "Traceback" not in r.stderr, r.stderr)

with tempfile.TemporaryDirectory() as t:
    home = Path(t)
    env = fake_opencode(home / "bin", "1.4.0")
    r = run_sync(home, "opencode", env)
    cfg = json.loads(strip_jsonc((home / ".config" / "opencode" / "opencode.jsonc").read_text()))
    check("v1 OpenCode gets v1 MCP shape", cfg.get("mcp", {}).get("engineering-memory", {}).get("timeout") == 10000, cfg)
    check("fresh install defaults to lead", cfg.get("default_agent") == "lead")

print("test_adapters: invalid source aborts before writing")
with tempfile.TemporaryDirectory() as t:
    home, eng = Path(t) / "home", Path(t) / "engine"
    for d in ("agents", "skills", "commands", "adapters", "scripts", "mcp"):
        shutil.copytree(ROOT / d, eng / d)
    p = eng / "agents" / "builder.md"
    p.write_text(p.read_text().replace("role: subagent", "role: subagent\nextra:\n  - nope", 1))
    r = run_sync(home, "all", fake_opencode(Path(t) / "bin", "2.0.0"), engine=eng)
    check("sync fails with file:line", r.returncode != 0 and "agents/builder.md:" in (r.stderr + r.stdout), r.stderr)
    check("nothing written", not (home / ".config").exists() and not (home / ".claude").exists())

print(f"\ntest_adapters: {passed} passed, {failed} failed")
sys.exit(1 if failed else 0)
