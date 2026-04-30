# DocMagic

**Your repo is lying to your AI agent. DocMagic finds where.**

DocMagic is a repo-level causality and documentation repair tool for AI-coded systems.

It is not a README generator, docstring generator, or "AI documentation assistant." Those tools explain what code appears to do. DocMagic exists because AI agents fail when they cannot see what code *actually participates in*: hidden calls, hooks, generated files, state writes, config paths, background daemons, and stale explanatory surfaces.

> AI agents do not only need more context. They need admissible context.

## The Problem

Most AI coding failures come from structural blindness:

1. **Stale explanatory surfaces** — A docstring says `X`, but the code now does `Y`. The LLM reads the docstring and believes it.

2. **Hidden nonlocal behavior** — A function looks simple locally, but it is called through a registry, hook, decorator, generated file, CLI entrypoint, or background process. The LLM edits it as if it is local.

3. **Search ≠ reading** — The model sees search results and assumes the execution boundary is known. But search does not prove the true entrypoint, hidden callers, or downstream consumers were found.

4. **Execution boundaries are not closed before editing** — The agent edits before it understands the path from runtime entrypoint to terminal behavior.

5. **Agent action causality is invisible** — The agent's own tool calls trigger hooks, state writes, memory updates, index changes, and downstream behavior. The agent thinks it "edited a file," but the environment propagated that action through hidden machinery.

## Install

```bash
pip install docmagic
```

## Usage

### As a Claude Code skill (recommended)

Copy `.claude/skills/docmagic/` from this repo into your project. Claude reads the skill, becomes Doctor Magic, and scans before editing.

### As scripts

```bash
# Full scan — hidden connections + annotation score
python3 .claude/skills/docmagic/scripts/scan.py /path/to/repo

# Detailed hidden connection breakdown
python3 .claude/skills/docmagic/scripts/hidden.py /path/to/repo

# Generate # DOCMAGIC: annotations (dry run)
python3 .claude/skills/docmagic/scripts/annotate.py /path/to/repo

# Apply annotations
python3 .claude/skills/docmagic/scripts/annotate.py /path/to/repo --apply
```

### As an MCP server

Add to your Claude Code config (`.claude.json`):

```json
{
  "mcpServers": {
    "docmagic": {
      "command": "python3",
      "args": ["-m", "docmagic.server"]
    }
  }
}
```

### As a CLI

```bash
docmagic scan /path/to/repo
docmagic hidden /path/to/repo
docmagic annotate /path/to/repo --apply
docmagic serve  # start MCP server
```

## What It Detects

DocMagic scans for 7 categories of invisible coupling:

| Category | What it finds |
|----------|--------------|
| **HTTP calls** | Cross-service calls to localhost ports, API endpoints between microservices |
| **File triggers** | Daemon processes watching directories for file changes |
| **Hook bridges** | Code registered to fire on events (pre/post hooks, signals) |
| **MCP references** | Tool calls embedded in strings that route through MCP servers |
| **Cross-imports** | Imports that reach across package boundaries |
| **State files** | Shared mutable state via temp files, lock files, config writes |
| **Multi-write drift** | Multiple writers to the same file without coordination |

## What It Produces

```python
# DOCMAGIC: HTTP → localhost:8080/hook/posttooluse (CAVE_sancrev)
# Contract: POST JSON with tool_name, tool_input, tool_response
# Sync-with: omnisanc_logic.py, paia_posttooluse.py
def _post_to_cave_hook(tool_name, tool_input, response):
    ...
```

Every hidden connection gets a local, searchable, agent-readable breadcrumb.

## The Core Invariant

> Every nonlocal behavior that can affect an AI edit must have a local, searchable, agent-readable breadcrumb.

## Architecture

```
docmagic/
├── scanner/          # AST parsing + hidden connection detection
├── graph/            # networkx (default) or Neo4j (optional) backend
├── repair/           # annotation generator
├── core.py           # plain functions (library layer)
├── server.py         # MCP server (thin wrappers)
└── cli.py            # CLI (thin wrappers)
```

Onion architecture: scanner → core → server/CLI. All three surfaces call the same functions.

## License

MIT

---

Built by [Isaac](https://aisaac.pages.dev) — AI Transformation consulting.
