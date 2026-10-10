#!/usr/bin/env python3
"""EngineeringOS sync/health entry point. Called by `eng`. Stdlib only.

  eos_sync.py sync   [--target all|<editor>[,<editor>]] --engine DIR --data DIR [--python PY]
  eos_sync.py health [--target ...] ...

`all` syncs every registered editor that is installed (detect()); naming a
target syncs it even if not detected. Health reports every requested target.
"""
import argparse
import os
import sys
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("action", choices=["sync", "health", "targets"])
    p.add_argument("--target", default="all")
    p.add_argument("--engine", required=True)
    p.add_argument("--data", required=True)
    p.add_argument("--python", default=sys.executable)
    p.add_argument("--claude-cli", default=None,
                   help="claude CLI path for MCP registration ('' forces a direct ~/.claude.json edit)")
    p.add_argument("--claude-json", default=None)
    a = p.parse_args()

    engine = Path(os.path.abspath(a.engine))  # no symlink resolution: generated paths must match eng's
    sys.path.insert(0, str(engine))
    import adapters
    from adapters.common import Context, SourceError, load_source

    ctx = Context(engine=engine, data=Path(a.data), python=a.python, home=Path.home(),
                  env=dict(os.environ), options={"claude_cli": a.claude_cli, "claude_json": a.claude_json})
    if a.action == "targets":
        for name in adapters.REGISTRY:
            print(f"{name}\t{'installed' if adapters.load(name).detect(ctx) else 'not found'}")
        return
    try:
        source = load_source(engine)
    except SourceError as exc:
        sys.exit(f"[eng]   FAIL: invalid source: {exc}")

    explicit = a.target != "all"
    names = adapters.REGISTRY if not explicit else [t.strip() for t in a.target.split(",") if t.strip()]
    for name in names:
        mod = adapters.load(name)
        if a.action == "sync":
            if not explicit and not mod.detect(ctx):
                print(f"[eng]   {name}: not installed, skipped")
                continue
            print(f"[eng] Syncing {name} ...")
            mod.sync(ctx, source)
        else:
            mod.health(ctx, source)


if __name__ == "__main__":
    main()
