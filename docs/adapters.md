# Editor adapters

EngineeringOS keeps one **editor-neutral** source of agents, skills and
commands (`agents/`, `skills/`, `commands/`). An **adapter** renders that source
into one editor's format, installs it, and registers the `engineering-memory`
MCP server there. `eng sync` runs every adapter whose editor is installed.

| Adapter | Installs into | Notes |
|---|---|---|
| `opencode` | `~/.config/opencode/` (`XDG_CONFIG_HOME`) | MCP in v2 (`mcp.servers`) or v1 shape, matching your OpenCode |
| `claude` | `~/.claude/`, `~/.claude.json` (`CLAUDE_CONFIG_DIR`) | Lead becomes the default output style; guard hook enforces permissions |

## Neutral source format

Frontmatter is a small YAML subset: nested maps and scalars. Lists, flow
collections (`[...]`, `{...}`), anchors and tabs are rejected with `file:line`,
and sync aborts before writing anything.

**Agent** (`agents/<name>.md`)

| Key | Required | Meaning |
|---|---|---|
| `name` | yes | Must equal the file name |
| `description` | yes | When to use this agent |
| `role` | yes | `primary` (the orchestrating mode) or `subagent` |
| `model_tier` | no | `deep`, `standard` or `fast`; each adapter maps it to a model |
| `permissions` | no | `read`, `edit`, `bash`, `webfetch`, `websearch`, `task`, ...: `allow` / `deny` / `ask`, or a map of patterns. In a map, the `"*"` default must come first (`"*": deny`, then `"git log *": allow`); the loader rejects other orders because editors resolve precedence differently. Adapters must never grant more than the most restrictive reading (Claude: denies win over allows). To carve a write form out of an allow wildcard, put the deny after the allow it narrows (`"git log *": allow`, then `"git log *--output*": deny`): OpenCode applies the last matching rule, the Claude guard checks denies first, so both read it the same way |
| `targets.<editor>` | no | Settings only that editor understands (e.g. `targets.opencode.temperature`, `targets.claude.model`) |

**Command** (`commands/<name>.md`): `description`, optional `targets.<editor>`
(e.g. `targets.opencode.agent: lead`). Use `$ARGUMENTS` for user input.

**Skill** (`skills/<name>/SKILL.md`): `name` (= directory), `description`,
optional `metadata`, optional `targets.<editor>`. Extra files in the skill
directory are installed alongside it.

Bodies are passed through as written. They use OpenCode-style tool words
(`read`, `glob`, `todowrite`, ...); adapters for other editors prepend a short
tool-name mapping note.

## Writing an adapter

1. Create `adapters/<editor>/__init__.py` (empty) and `adapters/<editor>/adapter.py`:

   ```python
   from adapters.common import Writer, log, grants, load_json, atomic_write_json, MCP_NAME

   NAME = "<editor>"

   def detect(ctx):            # is the editor installed? (CLI on PATH or config dir exists)
       ...

   def sync(ctx, source):      # render, install, register MCP
       w = Writer(config_root, NAME)
       for agent in source.agents:          # or source.subagents() / source.primary()
           w.write(path, render(agent))
       w.finish()                            # prunes stale owned files, saves manifest
       ...                                   # register MCP in the editor's native shape

   def health(ctx, source):    # print "[eng]   <Editor> ...: ok/missing" lines
       ...
   ```

2. Add the name to `REGISTRY` in `adapters/__init__.py`.
3. Add tests (hermetic: temp `HOME`, fake CLI on `PATH`), wire them into
   `.github/workflows/ci.yml` and `py_compile`.
4. Document it in the table above and in `README.md`.

### Rules every adapter follows

- **Fail closed on permissions.** Use `grants(value)`: only the exact value
  `allow` grants a capability. If the editor cannot express a rule, deny the
  capability (or enforce it with a hook, as the Claude adapter does). Never
  silently widen access.
- **Never clobber user files.** Always write through `Writer`. Use
  `adopt_legacy=True` only when migrating from an older install of ours.
- **Merge shared configs, do not replace them.** `load_json` (with `jsonc=True`
  where needed) then `atomic_write_json`, which keeps a `.engineeringos.bak`.
  Touch only the keys you own. Prefer the editor's own CLI when it can register
  MCP servers, so you do not race a running editor.
- **Idempotent.** A second `eng sync` reports `(0 files changed)` and
  "already configured".
- **Stdlib only.** No `pip install`.
- **Collisions.** If generated names collide with the editor's built-ins, rename
  inside the adapter (see `SKILL_RENAMES` in the Claude adapter) and rewrite
  references. Hyphenated names (`code-review`) are rewritten wherever they
  appear; one-word names (`simplify`, `dataviz`) only when written in backticks,
  so ordinary prose is untouched. Sources must therefore reference skills in
  backticks; `tests/test_adapters.py` flags un-backticked mentions.

### Candidate next adapters (not implemented)

- **Codex**: `AGENTS.md`-based instructions; MCP servers in `~/.codex/config.toml`.
- **Cursor**: rules in `.cursor/rules/*.mdc`; MCP in `~/.cursor/mcp.json`.
- **Gemini CLI**: `GEMINI.md` context; MCP in `~/.gemini/settings.json`.

Check each editor's current docs before building; these formats change.
