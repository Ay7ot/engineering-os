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

from adapters.common import (Item, SourceError, Writer, emit_yaml, load_source,  # noqa: E402
                             parse_frontmatter, render_frontmatter, strip_jsonc)
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
check("lists of maps parse", parse_frontmatter('---\np:\n  - action: read\n    resource: "*"\n  - action: shell\n    resource: "git log *"\n---\n')[0]
      == {"p": [{"action": "read", "resource": "*"}, {"action": "shell", "resource": "git log *"}]})
check("lists of scalars parse", parse_frontmatter("---\np:\n  - a\n  - b\n---\n")[0] == {"p": ["a", "b"]})
check("list item with a nested map", parse_frontmatter("---\np:\n  - action: read\n    where:\n      a: b\n---\n")[0]
      == {"p": [{"action": "read", "where": {"a": "b"}}]})
check("a list cannot sit beside a mapping key", raises(lambda: parse_frontmatter("---\n- x\n---\n", "f.md")) is not None)
check("scalar list item cannot nest", raises(lambda: parse_frontmatter("---\np:\n  - x\n    y: z\n---\n", "f.md")) is not None)
check("list item continuation must line up with the item",
      "list item" in (raises(lambda: parse_frontmatter("---\np:\n  - action: shell\n   effect: deny\n---\n", "f.md")) or ""))
check("quoted first key in a list item parses",
      parse_frontmatter('---\np:\n  - "x y": 1\n    b: 2\n---\n')[0] == {"p": [{"x y": "1", "b": "2"}]})
check("a comment before a list is skipped, not treated as a map",
      parse_frontmatter("---\np:\n  # why\n  - a\n---\n")[0] == {"p": ["a"]})
check("tabs rejected", raises(lambda: parse_frontmatter("---\na:\n\tb: c\n---\n", "f.md")) is not None)
check("flow collections rejected", raises(lambda: parse_frontmatter("---\na: [x, y]\n---\n", "f.md")) is not None)
check("unclosed frontmatter rejected", raises(lambda: parse_frontmatter("---\na: b\n", "f.md")) is not None)
check("duplicate key rejected", raises(lambda: parse_frontmatter("---\na: b\na: c\n---\n", "f.md")) is not None)
check("quoted value with trailing comment", parse_frontmatter('---\nm: "a/b" # c\n---\n')[0]["m"] == "a/b")
check("bad escape rejected", raises(lambda: parse_frontmatter('---\nm: "a\\qb"\n---\n', "f.md")) is not None)
check("text after quoted value rejected", raises(lambda: parse_frontmatter('---\nm: "a" b\n---\n', "f.md")) is not None)
check("YAML-special words emitted quoted", emit_yaml({"a": "True", "b": "NULL", "c": "yes"}) == 'a: "True"\nb: "NULL"\nc: "yes"')
check("JSONC trailing commas accepted", json.loads(strip_jsonc('{"a": [1, 2,], // c\n "b": "x,}",}')) == {"a": [1, 2], "b": "x,}"})
err = raises(lambda: parse_frontmatter("---\nok: 1\nbad:\n  x: y\n   z: q\n---\n", "agents/x.md")) or ""
check("error carries file:line", "agents/x.md:5" in err, err)
list_fm = {"permissions": [{"action": "read", "resource": "*", "effect": "allow"}], "tags": ["a", "b"]}
check("lists emit and parse back unchanged",
      parse_frontmatter(render_frontmatter(list_fm, ""))[0] == list_fm
      and emit_yaml(list_fm) == 'permissions:\n  - action: read\n    resource: "*"\n    effect: allow\ntags:\n  - a\n  - b')

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
check("source loads", len(src.agents) == 8 and len(src.commands) == 6 and len(src.skills) >= 17,
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
    good = (ROOT / "agents" / "explorer.md").read_text()
    bad_agent.write_text(good.replace('    "git status *": allow', '    "git status *": maybe', 1))
    check("unknown effect rejected", "must be one of" in (raises(lambda: load_source(eng)) or ""))
    bad_agent.write_text(good.replace('    "git status *": allow', '    "git status *":\n      - allow', 1))
    check("a list-valued permission rule is rejected, not stringified",
          "must be one of" in (raises(lambda: load_source(eng)) or ""))
    (eng / "agents" / "builder.md").write_text(
        (ROOT / "agents" / "builder.md").read_text().replace("  opencode:\n    temperature:", "  opencode:\n    - temperature:", 1))
    check("a non-map targets entry rejected", "map of editor" in (raises(lambda: load_source(eng)) or ""))

print("test_adapters: skill structure (see skills/skill-authoring)")
from adapters.claude.adapter import SKILL_RENAMES  # noqa: E402

TRIGGER = re.compile(r"(^|[.!?]\s+)Use (when|whenever|for|after|before|periodically)\b")
EDITOR_SPECIFIC = ("mcp__", ".claude/", "CLAUDE_CONFIG_DIR", ".config/opencode", ".opencode/",
                   "TodoWrite", "AskUserQuestion", "WebFetch", "WebSearch", "NotebookEdit")
ONE_WORD_RENAMED = [n for n in SKILL_RENAMES if "-" not in n]
bad = []
for s in src.skills:
    desc = s.fm.get("description", "")
    texts = [desc, s.body] + [f.read_text(errors="ignore") for _, f in s.files]
    problems = []
    if not TRIGGER.search(desc):
        problems.append("description lacks a 'Use when/for/after/before ...' sentence")
    if len(desc) > 300:
        problems.append(f"description too long ({len(desc)} > 300 chars)")
    for heading in ("When to use", "Checklist"):
        if not re.search(rf"^## {heading}\s*$", s.body, re.M):
            problems.append(f"missing '## {heading}'")
    for word in EDITOR_SPECIFIC:
        if any(word in t for t in texts):
            problems.append(f"editor-specific reference {word!r}")
    if problems:
        bad.append(f"{s.name}: {'; '.join(problems)}")
check("every skill has a trigger sentence, When to use, Checklist, and is editor-neutral", not bad, bad)

# One-word renamed skills are only rewritten for editors when written as `name`.
loose = []
for item in src.skills + src.agents + src.commands:
    texts = [item.fm.get("description", ""), item.body]
    for name in ONE_WORD_RENAMED:
        for t in texts:
            if re.search(rf"(?<![`\w-]){re.escape(name)}(?![`\w-])\s+skill", t):
                loose.append(f"{item.path.relative_to(ROOT)}: '{name} skill' without backticks")
check("renamed one-word skills are referenced in backticks", not loose, loose)
check("all expected skills present",
      {"simplify", "memory-hygiene", "skill-authoring", "dataviz", "code-review", "testing", "technical-research"}
      <= {s.name for s in src.skills})

print("test_adapters: OpenCode golden (agents/commands vs pre-migration files; skills pass through)")
# Intended changes since the fixtures were captured. The golden pins the
# translated frontmatter (mode, model, permission, request) after applying
# exactly these edits. The body is asserted to pass through verbatim; prompt
# content is deliberately not pinned. Prompt drift is caught in review plus the
# REQUIRED_SKILLS checks, not here.
# bash: rules removed in place, then new rules appended in order.
GIT_BRANCH_READ = ["git branch", "git branch -a", "git branch -r", "git branch -v", "git branch -vv",
                   "git branch --show-current", "git branch --list *", "git branch --contains *",
                   "git branch --merged *", "git branch --no-merged *"]
GIT_REMOTE_READ = ["git remote", "git remote -v", "git remote get-url *"]


def no_git_writes(*subs):
    return [(f"git {s} *{flag}*", "deny") for s in subs for flag in ("--output", "--ext-diff")]


def allows(*keys):
    return [(k, "allow") for k in keys]


# 2026-10-25: agent bodies are no longer compared to the frozen fixture. The
# fixture still pins the v1 permission map each agent must render; the body is
# asserted to pass through verbatim. Procedure now lives in skills, so the
# requirement checks below point at the skill each agent must reference.
REQUIRED_SKILLS = {
    "lead": ["project-planning", "architecture-analysis", "memory-hygiene", "diagrams"],
    "builder": ["test-driven-development", "simplify", "verification-before-completion"],
    "explorer": ["repository-exploration"],
    "researcher": ["technical-research"],
    "architect": ["architecture-analysis", "diagrams"],
    "reviewer": ["code-review", "security-review"],
    "security": ["security-review"],
    "tester": ["testing", "verification-before-completion"],
}
FIXTURE_DELTAS = {  # 2026-10-10: read-only agents get read-only git in OpenCode too
    "explorer": {"bash_remove": ["git branch *", "git remote *"],
                 "bash_add": allows(*GIT_BRANCH_READ, *GIT_REMOTE_READ) + no_git_writes("log")},
    "reviewer": {"bash_remove": ["git branch *"],
                 "bash_add": allows(*GIT_BRANCH_READ) + no_git_writes("diff", "log", "show")},
    "security": {"bash_add": no_git_writes("diff", "log", "show")},
    "researcher": {"bash_remove": ["git *"],
                   "bash_add": allows("git status *", "git rev-parse *", "git log *", "git show *",
                                      "git diff *", "git ls-files *", "git describe *", "git tag",
                                      "git tag --list *", "git tag -l *", *GIT_BRANCH_READ,
                                      *GIT_REMOTE_READ) + no_git_writes("diff", "log", "show")},
    "architect": {"bash_add": no_git_writes("log")},
}

# 2026-10-21: model_tier resolves to an OpenCode selector. The fixture golden
# compares the v1 dialect, which has no `#variant`.
TIER_MODEL = {
    "deep": "opencode-go/deepseek-v4.1-flash#max",
    "standard": "opencode-go/deepseek-v4.1-flash#high",
    "fast": "opencode-go/mimo-v2.6-flash",
}


def legacy(selector):
    return selector.split("#", 1)[0]


MODEL_DELTAS = {name: legacy(model) for name, model in {
    "lead": TIER_MODEL["deep"], "architect": TIER_MODEL["deep"],
    "reviewer": TIER_MODEL["deep"], "security": TIER_MODEL["deep"],
    "builder": TIER_MODEL["standard"],
    "researcher": TIER_MODEL["standard"], "tester": TIER_MODEL["standard"],
    "explorer": TIER_MODEL["fast"],
}.items()}


def with_model(fm, model):
    """Fixture fm plus 'model', where the renderer emits it (before permission)."""
    out, placed = {}, False
    for k, v in fm.items():
        if k == "model":
            continue
        if k == "permission" and not placed:
            out["model"] = model
            placed = True
        out[k] = v
    if not placed:
        out["model"] = model
    return out


# 2026-10-22: OpenCode's `.env` prompt is restored after a blanket read allow in
# both dialects (agent rules are appended after the editor's base policy).
READ_POLICY = {"*": "allow", "*.env": "ask", "*.env.*": "ask", "*.env.example": "allow"}


def with_read_policy(fm):
    perms = dict(fm["permission"])
    perms["read"] = READ_POLICY
    return dict(fm, permission=perms)


def apply_delta(name, fm, problems):
    d = FIXTURE_DELTAS.get(name)
    if not d:
        return fm
    if d.get("bash_remove") or d.get("bash_add"):
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
    return fm


mism, delta_problems = [], []
for a in src.agents:
    # typed=True: 0.1 / false must stay number / bool, not become "0.1" / "false"
    new_fm, new_body = parse_frontmatter(oc.render_agent(a, v2=False), typed=True)
    old_fm, _ = parse_frontmatter((FIXTURES / "agents" / f"{a.name}.md").read_text(), typed=True)
    # `description` is source text passed through verbatim, like the body. The
    # fixture pins the translated fields (mode, model, permission, request).
    new_desc, old_desc = new_fm.pop("description"), old_fm.pop("description")
    old_fm = apply_delta(a.name, old_fm, delta_problems)
    if a.name in MODEL_DELTAS:
        old_fm = with_model(old_fm, MODEL_DELTAS[a.name])
    old_fm = with_read_policy(old_fm)
    if (ordered(new_fm) != ordered(old_fm) or new_body != a.body
            or new_desc != a.fm["description"]):
        mism.append(f"agents/{a.name}")
for c in src.commands:
    new_fm, new_body = parse_frontmatter(oc.render_command(c, v2=False), typed=True)
    old_fm, _ = parse_frontmatter((FIXTURES / "commands" / f"{c.name}.md").read_text(), typed=True)
    new_desc, old_desc = new_fm.pop("description"), old_fm.pop("description")
    if (ordered(new_fm) != ordered(old_fm) or new_body != c.body
            or new_desc != c.fm["description"]):
        mism.append(f"commands/{c.name}")
check("fixture deltas apply cleanly", not delta_problems, delta_problems)
check("agent and command frontmatter matches its fixture + deltas; bodies pass through verbatim",
      not mism, mism)
by_name = {a.name: a for a in src.agents}
check("each agent references the skill that holds its procedure",
      not any(f"`{x}`" not in a.body for a in src.agents for x in REQUIRED_SKILLS.get(a.name, [])),
      {a.name: [x for x in REQUIRED_SKILLS.get(a.name, []) if f"`{x}`" not in a.body] for a in src.agents})
check("every agent is covered by REQUIRED_SKILLS",
      set(REQUIRED_SKILLS) == set(by_name), sorted(set(REQUIRED_SKILLS) ^ set(by_name)))
known_skills = {s.name for s in src.skills}
check("every skill an agent points at exists",
      not any(s not in known_skills for ss in REQUIRED_SKILLS.values() for s in ss),
      {n: [s for s in ss if s not in known_skills] for n, ss in REQUIRED_SKILLS.items()})
check("every agent has a fixture and every fixture has an agent",
      {p.stem for p in (FIXTURES / "agents").glob("*.md")} == set(by_name),
      sorted({p.stem for p in (FIXTURES / "agents").glob("*.md")} ^ set(by_name)))
check("planner is folded into the lead loop",
      "planner" not in by_name and "`project-planning`" in by_name["lead"].body, sorted(by_name))
check("no current skill uses targets (pass-through below is exercised)", all("targets" not in s.fm for s in src.skills))
with tempfile.TemporaryDirectory() as t:
    eng = Path(t)
    for d in ("agents", "commands"):
        shutil.copytree(ROOT / d, eng / d)
    sk = eng / "skills" / "demo"
    sk.mkdir(parents=True)
    plain = "---\nname: demo\ndescription: Demo. Use when testing.\n---\n# Demo\nbody\n"
    (sk / "SKILL.md").write_text(plain)
    demo = load_source(eng).skills[0]
    check("skill without targets installs byte-for-byte", oc.render_skill(demo) == plain.encode())
    (sk / "SKILL.md").write_text("---\nname: demo\ndescription: Demo. Use when testing.\n"
                                 "targets:\n  opencode:\n    license: MIT\n  claude:\n    x: y\n---\n# Demo\nbody\n")
    demo = load_source(eng).skills[0]
    out = oc.render_skill(demo)
    out = out.decode() if isinstance(out, bytes) else out
    fm, body = parse_frontmatter(out)
    check("skill with targets: own target merged, others dropped, body kept",
          fm.get("license") == "MIT" and "targets" not in fm and "x" not in fm and body == "# Demo\nbody\n", (fm, body))
check("deltas only touch existing agents", set(FIXTURE_DELTAS) <= {a.name for a in src.agents}, set(FIXTURE_DELTAS))

print("test_adapters: OpenCode model tiers")
check("adapter tier map matches the pinned expectation", oc.TIER_MODELS == TIER_MODEL, oc.TIER_MODELS)
check("every tier is used by at least one agent",
      set(TIER_MODEL) == {a.fm.get("model_tier") for a in src.agents},
      {a.fm.get("model_tier") for a in src.agents})
SELECTOR = re.compile(r"^[a-z0-9-]+/[a-z0-9./-]+(?:#[a-z]+)?$")
bad = []
for a in src.agents:
    got = parse_frontmatter(oc.render_agent(a, v2=False))[0].get("model")
    want = MODEL_DELTAS[a.name]
    if got != want:
        bad.append(f"{a.name}: {got!r} != {want!r}")
    elif not SELECTOR.match(want):
        bad.append(f"{a.name}: malformed selector {want!r}")
check("every agent renders its tier's selector", not bad, bad)
lead = next(a for a in src.agents if a.name == "lead")
check("lead resolves through the tier map now that its explicit target is gone",
      parse_frontmatter(oc.render_agent(lead, v2=False))[0].get("model") == legacy(TIER_MODEL["deep"]))
check("'#variant' would round-trip if we emit one (effort is a follow-up, not lost)",
      parse_frontmatter('---\nm: "opencode-go/deepseek-v4.1-flash#max"\n---\n')[0]["m"]
      == "opencode-go/deepseek-v4.1-flash#max")
tiered = Item("x", {"name": "x", "description": "d", "role": "subagent", "model_tier": "fast"}, "", ROOT / "agents" / "x.md")
overridden = Item("y", {"name": "y", "description": "d", "role": "subagent", "model_tier": "fast",
                        "targets": {"opencode": {"model": "opencode-go/kimi-k3#low"}}}, "", ROOT / "agents" / "y.md")
untiered = Item("z", {"name": "z", "description": "d", "role": "subagent"}, "", ROOT / "agents" / "z.md")
check("model_tier maps when no target override", oc.model_for(tiered) == TIER_MODEL["fast"])
check("targets.opencode.model beats model_tier", oc.model_for(overridden) == "opencode-go/kimi-k3#low")
check("v1 strips #variant from an explicit target model",
      parse_frontmatter(oc.render_agent(overridden, v2=False))[0]["model"] == "opencode-go/kimi-k3")
check("v2 keeps #variant from an explicit target model",
      parse_frontmatter(oc.render_agent(overridden, v2=True))[0]["model"] == "opencode-go/kimi-k3#low")
check("no tier and no override inherits (None)", oc.model_for(untiered) is None)
check("untiered agent renders no model line", "model" not in parse_frontmatter(oc.render_agent(untiered, v2=False))[0])


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

print("test_adapters: OpenCode v2 agent dialect")


def v2_effect(rules, action, value):
    """OpenCode v2: ordered rules, last match wins; `*` matches any action."""
    hit = None
    for r in rules:
        if r["action"] in (action, "*") and oc_match(value, r["resource"]):
            hit = r["effect"]
    return hit if hit is not None else "ask"


shape_bad = []
for a in src.agents:
    text = oc.render_agent(a, v2=True)
    fm, body = parse_frontmatter(text)
    if "\npermission:" in text or "\ntemperature:" in text:
        shape_bad.append(f"{a.name}: legacy field emitted")
    if not isinstance(fm.get("permissions"), list):
        shape_bad.append(f"{a.name}: permissions is not a list")
    if body != a.body:
        shape_bad.append(f"{a.name}: body changed")
    actions = [r["action"] for r in fm.get("permissions", [])]
    if {"bash", "task"} & set(actions):
        shape_bad.append(f"{a.name}: v1 action name")
    if set(actions) & oc.V2_RETIRED_ACTIONS:
        shape_bad.append(f"{a.name}: retired action emitted")
    if not all(set(r) == {"action", "resource", "effect"} for r in fm.get("permissions", [])):
        shape_bad.append(f"{a.name}: rule with extra/missing keys")
    temp = a.target("opencode").get("temperature")
    if temp is not None and fm.get("request", {}).get("body", {}).get("temperature") != temp:
        shape_bad.append(f"{a.name}: temperature not moved into request.body")
check("every agent renders a V2 permissions list with no legacy fields", not shape_bad, shape_bad)

PROBES = MUTATING_GIT + ["npm test", "rm -rf /tmp/x", "python3 -m pytest", "ls", "cat ~/.ssh/id_rsa"]
disagree = [f"{a.name}: {c}"
            for a in src.agents
            for c in PROBES
            if oc_bash(a.fm["permissions"]["bash"], c)
            != v2_effect(parse_frontmatter(oc.render_agent(a, v2=True))[0]["permissions"], "shell", c)]
check("v2 list resolves exactly like the v1 map (shell)", not disagree, disagree)
read_disagree = []
for a in src.agents:
    v1_read = parse_frontmatter(oc.render_agent(a, v2=False))[0]["permission"]["read"]
    v2_rules = parse_frontmatter(oc.render_agent(a, v2=True))[0]["permissions"]
    for p in ("*.env", "*.env.local", "*.env.example", "src/app.py", "/etc/passwd"):
        if oc_bash(v1_read, p) != v2_effect(v2_rules, "read", p):
            read_disagree.append(f"{a.name}: {p}")
check("v2 list resolves exactly like the v1 map (read)", not read_disagree, read_disagree)
env_bad = [a.name for a in src.agents
           if v2_effect(parse_frontmatter(oc.render_agent(a, v2=True))[0]["permissions"], "read", ".env") != "ask"
           or v2_effect(parse_frontmatter(oc.render_agent(a, v2=True))[0]["permissions"], "read", ".env.example") != "allow"
           or oc_bash(parse_frontmatter(oc.render_agent(a, v2=False))[0]["permission"]["read"], ".env") != "ask"]
check("reading .env asks and .env.example is allowed, in both dialects", not env_bad, env_bad)
edit_disagree = [f"{a.name}: {p}"
                 for a in src.agents
                 for p in ("src/app.py", "docs/adr.md", "package.json")
                 if oc_bash(a.fm["permissions"]["edit"], p)
                 != v2_effect(parse_frontmatter(oc.render_agent(a, v2=True))[0]["permissions"], "edit", p)]
check("v2 list resolves exactly like the v1 map (edit)", not edit_disagree, edit_disagree)
try:
    oc.permission_rules({"todowrite": "deny"}, True)
    retired_deny = ""
except SystemExit as exc:
    retired_deny = str(exc)
check("a deny on a retired V2 action fails instead of vanishing silently",
      "cannot be expressed" in retired_deny, retired_deny)
check("v2 denies mutating git for read-only agents through the list",
      not [f"{n}: {c}" for n in READ_ONLY
           for c in MUTATING_GIT
           if v2_effect(parse_frontmatter(oc.render_agent(next(a for a in src.agents if a.name == n), v2=True))[0]["permissions"],
                        "shell", c) == "allow"])
check("v2 keeps read-only git inspection through the list",
      not [f"{n}: {c}" for n in READ_ONLY for c in want[n]
           if v2_effect(parse_frontmatter(oc.render_agent(next(a for a in src.agents if a.name == n), v2=True))[0]["permissions"],
                        "shell", c) != "allow"])

cmd_bad = [c.name for c in src.commands
           if "subtask" in parse_frontmatter(oc.render_command(c, v2=True))[0]
           or parse_frontmatter(oc.render_command(c, v2=True))[0].get("subagent")
           != parse_frontmatter(oc.render_command(c, v2=False))[0].get("subtask")]
check("commands use `subagent` in v2 and keep `subtask` in v1", not cmd_bad, cmd_bad)
check("v2 keeps the effort variant, v1 strips it",
      parse_frontmatter(oc.render_agent(next(a for a in src.agents if a.name == "builder"), v2=True))[0]["model"]
      == TIER_MODEL["standard"]
      and parse_frontmatter(oc.render_agent(next(a for a in src.agents if a.name == "builder"), v2=False))[0]["model"]
      == legacy(TIER_MODEL["standard"]))

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
    ex = (ocdir / "agents" / "explorer.md").read_text()
    check("agents installed in the v2 dialect",
          "\npermissions:" in ex and "\npermission:" not in ex and "\nrequest:" in ex, ex[:200])
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
    ex = (home / ".config" / "opencode" / "agents" / "explorer.md").read_text()
    check("v1 install keeps the legacy agent dialect",
          "\npermission:" in ex and "\npermissions:" not in ex and "\ntemperature:" in ex, ex[:200])
    check("fresh install defaults to lead", cfg.get("default_agent") == "lead")

# A v1 binary decides the dialect even when the config already uses the v2 MCP
# shape (downgrade, copied dotfiles). V1 cannot read `permissions:` lists, so
# guessing v2 here would silently drop every rule.
with tempfile.TemporaryDirectory() as t:
    home = Path(t)
    (home / ".config" / "opencode").mkdir(parents=True)
    (home / ".config" / "opencode" / "opencode.jsonc").write_text(
        '{"mcp": {"servers": {"neon": {"type": "remote", "url": "https://mcp.neon.tech/mcp"}}}}')
    r = run_sync(home, "opencode", fake_opencode(home / "bin", "1.9.3"))
    ex = (home / ".config" / "opencode" / "agents" / "explorer.md").read_text()
    check("v1 CLI + v2-shaped config still renders the legacy dialect",
          r.returncode == 0 and "\npermission:" in ex and "\npermissions:" not in ex, ex[:200])

# No CLI and no config: V2 reads V1 agents, so the unknown case takes V1.
with tempfile.TemporaryDirectory() as t:
    home = Path(t)
    r = run_sync(home, "opencode", {"PATH": "/usr/bin:/bin"})
    ex = (home / ".config" / "opencode" / "agents" / "explorer.md").read_text()
    check("no CLI + no config falls back to the legacy dialect",
          r.returncode == 0 and "\npermission:" in ex and "\npermissions:" not in ex, ex[:200])

# A v2 binary upgrades a v1-shaped config to the v2 dialect.
with tempfile.TemporaryDirectory() as t:
    home = Path(t)
    (home / ".config" / "opencode").mkdir(parents=True)
    (home / ".config" / "opencode" / "opencode.jsonc").write_text(
        '{"mcp": {"engineering-memory": {"type": "local", "command": ["/usr/bin/python3", "'
        + str(ROOT) + '/mcp/engineering-memory/server.py"], "timeout": 10000}}}')
    r = run_sync(home, "opencode", fake_opencode(home / "bin", "2.0.27"))
    ex = (home / ".config" / "opencode" / "agents" / "explorer.md").read_text()
    check("v2 CLI + v1-shaped config renders the v2 dialect",
          r.returncode == 0 and "\npermissions:" in ex and "\npermission:" not in ex, ex[:200])

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
