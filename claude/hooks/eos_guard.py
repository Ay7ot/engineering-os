#!/usr/bin/env python3
"""Compatibility shim: the guard moved to adapters/claude/hooks/eos_guard.py.

Claude Code sessions that were already running when `eng sync` moved the guard
still call this path until they restart. Forward to the real guard; if it is
missing, block (exit 2) so the shim can never fail open. Remove after one
release, once every running session has been restarted.
"""
import os
import sys

REAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "adapters", "claude", "hooks", "eos_guard.py")
REAL = os.path.normpath(REAL)
if not os.path.isfile(REAL):
    sys.stderr.write("EngineeringOS guard: blocked (guard not found; run 'eng sync claude' and restart Claude Code)\n")
    sys.exit(2)
try:
    os.execv(sys.executable, [sys.executable, REAL] + sys.argv[1:])
except OSError:
    sys.stderr.write("EngineeringOS guard: blocked (could not start guard)\n")
    sys.exit(2)
