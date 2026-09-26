#!/usr/bin/env python3
"""engineering-memory MCP server (stdlib only, no pip dependencies).

Exposes the EngineeringOS *data* directory + SQLite memory over MCP stdio
(newline-delimited JSON-RPC).

The engine (this repo) and your data are separate: engine code is public and
contains no personal data; all knowledge/projects/research/decisions/memory live
under the data directory so it can be version-controlled privately.

Data directory resolution (first match wins):
  1. $ENGINEERING_OS_DATA
  2. <repo>/data   (i.e. next to this server's repo root)
DB: <data>/memory/engineering_memory.db (auto-created, FTS5).
"""
import json
import os
import re
import sqlite3
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get(
    "ENGINEERING_OS_DATA",
    str(Path(__file__).resolve().parents[2] / "data"),
))
DB_PATH = ROOT / "memory" / "engineering_memory.db"

TOOLS = [
    {"name": "search_knowledge", "description": "Full-text search over EngineeringOS knowledge/, decisions/, research/ and project docs. Returns ranked snippets.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 8}}, "required": ["query"]}},
    {"name": "get_project_context", "description": "Get full project context: context.md, architecture.md, state.md, recent decisions/research/tasks.",
     "inputSchema": {"type": "object", "properties": {"project": {"type": "string"}}, "required": ["project"]}},
    {"name": "get_project_state", "description": "Get current state.md for a project plus open tasks.",
     "inputSchema": {"type": "object", "properties": {"project": {"type": "string"}}, "required": ["project"]}},
    {"name": "update_project_state", "description": "Update project state (appends timestamped entry to state.md and DB). Creates project dir if missing.",
     "inputSchema": {"type": "object", "properties": {"project": {"type": "string"}, "state": {"type": "string"}, "status": {"type": "string"}}, "required": ["project", "state"]}},
    {"name": "search_decisions", "description": "Search Architecture Decision Records.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 8}}, "required": ["query"]}},
    {"name": "get_decision", "description": "Get a single decision by id.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}},
    {"name": "record_decision", "description": "Record an ADR: writes decisions/<date>-<slug>.md (or projects/<p>/decisions/) + DB row. Returns id and path.",
     "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}, "context": {"type": "string", "default": ""}, "decision": {"type": "string"}, "alternatives": {"type": "string", "default": ""}, "project": {"type": "string", "default": ""}}, "required": ["title", "decision"]}},
    {"name": "search_research", "description": "Search persisted technical research.",
     "inputSchema": {"type": "object", "properties": {"query": {"type": "string"}, "limit": {"type": "integer", "default": 8}}, "required": ["query"]}},
    {"name": "get_research", "description": "Get a single research record by id.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "integer"}}, "required": ["id"]}},
    {"name": "record_research", "description": "Persist research: writes research/<date>-<slug>.md + DB row. Returns id and path.",
     "inputSchema": {"type": "object", "properties": {"question": {"type": "string"}, "findings": {"type": "string"}, "recommendation": {"type": "string", "default": ""}, "sources": {"type": "string", "default": ""}, "project": {"type": "string", "default": ""}}, "required": ["question", "findings"]}},
    {"name": "get_active_tasks", "description": "List open tasks across all projects (or one project). Blackboard index.",
     "inputSchema": {"type": "object", "properties": {"project": {"type": "string", "default": ""}, "limit": {"type": "integer", "default": 20}}}},
    {"name": "record_task", "description": "Create a task on the blackboard (tasks/ + DB).",
     "inputSchema": {"type": "object", "properties": {"title": {"type": "string"}, "project": {"type": "string", "default": ""}, "owner": {"type": "string", "default": ""}, "status": {"type": "string", "default": "open"}, "details": {"type": "string", "default": ""}}, "required": ["title"]}},
    {"name": "update_task", "description": "Update task status/details by id.",
     "inputSchema": {"type": "object", "properties": {"id": {"type": "integer"}, "status": {"type": "string"}, "details": {"type": "string", "default": ""}}, "required": ["id", "status"]}},
]


def db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(DB_PATH))
    con.row_factory = sqlite3.Row
    con.execute("""CREATE TABLE IF NOT EXISTS decisions(
        id INTEGER PRIMARY KEY, title TEXT NOT NULL, context TEXT DEFAULT '',
        decision TEXT NOT NULL, alternatives TEXT DEFAULT '', project TEXT DEFAULT '',
        path TEXT DEFAULT '', created_at TEXT NOT NULL)""")
    con.execute("""CREATE TABLE IF NOT EXISTS research(
        id INTEGER PRIMARY KEY, question TEXT NOT NULL, findings TEXT NOT NULL,
        recommendation TEXT DEFAULT '', sources TEXT DEFAULT '', project TEXT DEFAULT '',
        path TEXT DEFAULT '', created_at TEXT NOT NULL)""")
    con.execute("""CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY, title TEXT NOT NULL, project TEXT DEFAULT '',
        owner TEXT DEFAULT '', status TEXT DEFAULT 'open', details TEXT DEFAULT '',
        updated_at TEXT NOT NULL, created_at TEXT NOT NULL)""")
    con.execute("""CREATE TABLE IF NOT EXISTS project_state(
        project TEXT PRIMARY KEY, status TEXT DEFAULT '', state TEXT DEFAULT '',
        updated_at TEXT NOT NULL)""")
    for tbl, col in (("decisions_fts", "decisions"), ("research_fts", "research")):
        try:
            con.execute(f"CREATE VIRTUAL TABLE IF NOT EXISTS {tbl} USING fts5(title, body)")
        except sqlite3.OperationalError:
            pass  # FTS5 unavailable; fall back to LIKE
    con.commit()
    return con


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def slug(s, n=50):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return (s[:n] or "untitled")


def fts_available(con, tbl):
    try:
        con.execute(f"SELECT * FROM {tbl} LIMIT 0")
        return True
    except sqlite3.OperationalError:
        return False


def md_search(query, limit=8):
    """Rank markdown files under knowledge/, decisions/, research/, projects/."""
    terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 1]
    if not terms:
        return []
    roots = [ROOT / "knowledge", ROOT / "decisions", ROOT / "research", ROOT / "projects"]
    hits = []
    for base in roots:
        if not base.is_dir():
            continue
        for p in base.rglob("*.md"):
            try:
                text = p.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            low = text.lower()
            score = sum(low.count(t) for t in terms)
            if score > 0:
                idx = min((low.find(t) for t in terms if t in low))
                snippet = text[max(0, idx - 200):idx + 400].replace("\n", " ").strip()
                hits.append({"path": str(p.relative_to(ROOT)), "score": score, "snippet": snippet[:600]})
    hits.sort(key=lambda h: -h["score"])
    return hits[:limit]


def do_search_knowledge(a):
    con = db()
    q, lim = a["query"], int(a.get("limit", 8))
    out = []
    if fts_available(con, "decisions_fts"):
        for r in con.execute("SELECT title FROM decisions_fts WHERE decisions_fts MATCH ? LIMIT ?", (q, lim)):
            out.append({"source": "decisions_db", "title": r["title"]})
    if fts_available(con, "research_fts"):
        for r in con.execute("SELECT title FROM research_fts WHERE research_fts MATCH ? LIMIT ?", (q, lim)):
            out.append({"source": "research_db", "title": r["title"]})
    for h in md_search(q, lim):
        out.append({"source": "file", **h})
    con.close()
    return {"query": q, "results": out[:max(lim, len(out))]}


def read_proj_file(project, name):
    p = ROOT / "projects" / project / name
    return p.read_text(encoding="utf-8", errors="replace") if p.is_file() else ""


def do_get_project_context(a):
    project = a["project"]
    con = db()
    base = ROOT / "projects" / project
    if not base.is_dir():
        con.close()
        return {"project": project, "registered": False, "hint": "Run /init-project in the repo to register it."}
    decisions = [dict(r) for r in con.execute(
        "SELECT id,title,created_at FROM decisions WHERE project=? ORDER BY id DESC LIMIT 10", (project,))]
    research = [dict(r) for r in con.execute(
        "SELECT id,question,created_at FROM research WHERE project=? ORDER BY id DESC LIMIT 10", (project,))]
    tasks = [dict(r) for r in con.execute(
        "SELECT id,title,owner,status,updated_at FROM tasks WHERE project=? AND status!='done' ORDER BY id DESC LIMIT 20", (project,))]
    con.close()
    return {"project": project, "registered": True,
            "context": read_proj_file(project, "context.md"),
            "architecture": read_proj_file(project, "architecture.md"),
            "state": read_proj_file(project, "state.md"),
            "recent_decisions": decisions, "recent_research": research, "open_tasks": tasks}


def do_get_project_state(a):
    project = a["project"]
    con = db()
    row = con.execute("SELECT * FROM project_state WHERE project=?", (project,)).fetchone()
    tasks = [dict(r) for r in con.execute(
        "SELECT id,title,owner,status,updated_at FROM tasks WHERE project=? AND status!='done' ORDER BY id", (project,))]
    con.close()
    return {"project": project, "state_file": read_proj_file(project, "state.md"),
            "db": dict(row) if row else None, "open_tasks": tasks}


def do_update_project_state(a):
    project, entry, status = a["project"], a["state"], a.get("status", "")
    pdir = ROOT / "projects" / project
    pdir.mkdir(parents=True, exist_ok=True)
    for f, tpl in (("context.md", f"# {project} — Context\n"), ("architecture.md", f"# {project} — Architecture\n"),
                   ("state.md", f"# {project} — State\n")):
        if not (pdir / f).is_file():
            (pdir / f).write_text(tpl, encoding="utf-8")
    sp = pdir / "state.md"
    sp.write_text(sp.read_text(encoding="utf-8") + f"\n## {now()} UTC\n{entry}\n", encoding="utf-8")
    con = db()
    prev = con.execute("SELECT state FROM project_state WHERE project=?", (project,)).fetchone()
    full = ((prev["state"] + "\n" if prev else "") + f"[{now()}] {entry}")[-8000:]
    con.execute("INSERT INTO project_state(project,status,state,updated_at) VALUES(?,?,?,?) "
                "ON CONFLICT(project) DO UPDATE SET status=excluded.status,state=excluded.state,updated_at=excluded.updated_at",
                (project, status or (prev and "" or ""), full, now()))
    con.commit()
    con.close()
    return {"project": project, "path": str(sp.relative_to(ROOT)), "ok": True}


def do_search_decisions(a):
    con = db()
    q, lim = a["query"], int(a.get("limit", 8))
    like = f"%{q}%"
    rows = [dict(r) for r in con.execute(
        "SELECT id,title,project,created_at FROM decisions WHERE title LIKE ? OR decision LIKE ? OR context LIKE ? ORDER BY id DESC LIMIT ?",
        (like, like, like, lim))]
    con.close()
    for h in md_search(a["query"], lim):
        if h["path"].startswith("decisions/") or "/decisions/" in h["path"]:
            rows.append(h)
    return {"results": rows}


def do_get_decision(a):
    con = db()
    r = con.execute("SELECT * FROM decisions WHERE id=?", (a["id"],)).fetchone()
    con.close()
    return {"decision": dict(r) if r else None}


def do_record_decision(a):
    con = db()
    ts = now()
    title = a["title"]
    proj = a.get("project", "")
    fname = f"{datetime.now().date().isoformat()}-{slug(title)}.md"
    dest = ROOT / ("projects/" + proj + "/decisions" if proj else "decisions") / fname
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"# {title}\n\nDate: {ts}\nProject: {proj or 'global'}\n\n## Context\n{a.get('context','')}\n\n## Decision\n{a['decision']}\n\n## Alternatives\n{a.get('alternatives','')}\n", encoding="utf-8")
    cur = con.execute("INSERT INTO decisions(title,context,decision,alternatives,project,path,created_at) VALUES(?,?,?,?,?,?,?)",
                      (title, a.get("context", ""), a["decision"], a.get("alternatives", ""), proj, str(dest.relative_to(ROOT)), ts))
    did = cur.lastrowid
    if fts_available(con, "decisions_fts"):
        con.execute("INSERT INTO decisions_fts(title,body) VALUES(?,?)", (title, f"{a.get('context','')} {a['decision']} {a.get('alternatives','')}"))
    con.commit()
    con.close()
    return {"id": did, "path": str(dest.relative_to(ROOT))}


def do_search_research(a):
    con = db()
    q, lim = a["query"], int(a.get("limit", 8))
    like = f"%{q}%"
    rows = [dict(r) for r in con.execute(
        "SELECT id,question,project,created_at FROM research WHERE question LIKE ? OR findings LIKE ? ORDER BY id DESC LIMIT ?",
        (like, like, lim))]
    con.close()
    for h in md_search(a["query"], lim):
        if h["path"].startswith("research/") or "/research/" in h["path"]:
            rows.append(h)
    return {"results": rows}


def do_get_research(a):
    con = db()
    r = con.execute("SELECT * FROM research WHERE id=?", (a["id"],)).fetchone()
    con.close()
    return {"research": dict(r) if r else None}


def do_record_research(a):
    con = db()
    ts = now()
    fname = f"{datetime.now().date().isoformat()}-{slug(a['question'])}.md"
    dest = ROOT / "research" / fname
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(f"# {a['question']}\n\nDate: {ts}\nProject: {a.get('project','') or 'global'}\n\n## Findings\n{a['findings']}\n\n## Recommendation\n{a.get('recommendation','')}\n\n## Sources\n{a.get('sources','')}\n", encoding="utf-8")
    cur = con.execute("INSERT INTO research(question,findings,recommendation,sources,project,path,created_at) VALUES(?,?,?,?,?,?,?)",
                      (a["question"], a["findings"], a.get("recommendation", ""), a.get("sources", ""), a.get("project", ""), str(dest.relative_to(ROOT)), ts))
    rid = cur.lastrowid
    if fts_available(con, "research_fts"):
        con.execute("INSERT INTO research_fts(title,body) VALUES(?,?)", (a["question"], f"{a['findings']} {a.get('recommendation','')}"))
    con.commit()
    con.close()
    return {"id": rid, "path": str(dest.relative_to(ROOT))}


def do_get_active_tasks(a):
    con = db()
    proj, lim = a.get("project", ""), int(a.get("limit", 20))
    if proj:
        rows = con.execute("SELECT * FROM tasks WHERE project=? AND status NOT IN ('done','cancelled') ORDER BY id", (proj,))
    else:
        rows = con.execute("SELECT * FROM tasks WHERE status NOT IN ('done','cancelled') ORDER BY id LIMIT ?", (lim,))
    out = [dict(r) for r in rows]
    con.close()
    return {"tasks": out}


def do_record_task(a):
    con = db()
    ts = now()
    cur = con.execute("INSERT INTO tasks(title,project,owner,status,details,updated_at,created_at) VALUES(?,?,?,?,?,?,?)",
                      (a["title"], a.get("project", ""), a.get("owner", ""), a.get("status", "open"), a.get("details", ""), ts, ts))
    tid = cur.lastrowid
    con.commit()
    con.close()
    return {"id": tid}


def do_update_task(a):
    con = db()
    con.execute("UPDATE tasks SET status=?, details=COALESCE(NULLIF(?,''),details), updated_at=? WHERE id=?",
                (a["status"], a.get("details", ""), now(), a["id"]))
    con.commit()
    row = con.execute("SELECT * FROM tasks WHERE id=?", (a["id"],)).fetchone()
    con.close()
    return {"task": dict(row) if row else None}


HANDLERS = {"search_knowledge": do_search_knowledge, "get_project_context": do_get_project_context,
            "get_project_state": do_get_project_state, "update_project_state": do_update_project_state,
            "search_decisions": do_search_decisions, "get_decision": do_get_decision,
            "record_decision": do_record_decision, "search_research": do_search_research,
            "get_research": do_get_research, "record_research": do_record_research,
            "get_active_tasks": do_get_active_tasks, "record_task": do_record_task,
            "update_task": do_update_task}


def text_result(data):
    return {"content": [{"type": "text", "text": json.dumps(data, indent=2)[:12000]}]}


def handle(req):
    method, rid, params = req.get("method"), req.get("id"), req.get("params", {}) or {}
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": rid, "result": {
            "protocolVersion": "2024-11-05", "capabilities": {"tools": {}},
            "serverInfo": {"name": "engineering-memory", "version": "0.1.0"}}}
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return {"jsonrpc": "2.0", "id": rid, "result": {}}
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": rid, "result": {"tools": TOOLS}}
    if method == "tools/call":
        name, args = params.get("name"), params.get("arguments", {}) or {}
        if name not in HANDLERS:
            return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32602, "message": f"unknown tool: {name}"}}
        try:
            return {"jsonrpc": "2.0", "id": rid, "result": text_result(HANDLERS[name](args))}
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
            return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32603, "message": f"{e}"}}
    if rid is None:
        return None
    return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"unknown method: {method}"}}


def main():
    db().close()  # ensure schema exists
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            resp = handle(json.loads(line))
        except Exception as e:
            resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
        if resp is not None:
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
