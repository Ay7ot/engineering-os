"""EngineeringOS editor adapters.

Each adapter module exposes: NAME, detect(ctx), sync(ctx, source), health(ctx, source).
To add an editor, create adapters/<name>/adapter.py and register it below.
See docs/adapters.md.
"""
import importlib

REGISTRY = ("opencode", "claude")


def load(name):
    if name not in REGISTRY:
        raise SystemExit(f"[eng] unknown target {name!r} (known: {', '.join(REGISTRY)})")
    return importlib.import_module(f"adapters.{name}.adapter")
