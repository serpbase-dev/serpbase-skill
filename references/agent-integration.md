# Agent Integration

Use this reference when installing SerpBase Skill into agents that do not load Codex `SKILL.md` files directly.

## Universal Shell Fallback

Any agent with shell access can use:

```bash
python /path/to/serpbase-skill/scripts/serpbase_search.py --type search --query "your query"
```

Set `SERPBASE_API_KEY` in the agent process environment.

## Codex

Copy this folder to the Codex skills directory, or reference it explicitly:

```text
Use $serpbase-skill to search Google through SerpBase and cite sources.
```

Codex reads `SKILL.md` and `agents/openai.yaml`.

## Claude Code

Claude Code can use `CLAUDE.md` as project memory. Copy or symlink `CLAUDE.md` into the project root where Claude Code is running, or keep this repository open and ask Claude Code to follow it.

Recommended prompt:

```text
Use the SerpBase instructions in CLAUDE.md to search current Google results and cite source links.
```

## opencode / OpenClaw / Generic Agents

For agents that support project rule files, use `AGENTS.md`.

If the agent does not automatically load `AGENTS.md`, paste the relevant section into its project instructions and tell it where `scripts/serpbase_search.py` lives.

Recommended prompt:

```text
Follow AGENTS.md in the serpbase-skill folder. Use SerpBase for current Google SERP data and cite links.
```

## MCP-capable Agents

If the agent supports MCP, prefer `serpbase-mcp` for lower-friction tool calls:

```text
https://github.com/serpbase-dev/serpbase-mcp
```

Use this skill as the fallback for agents that cannot run MCP or when a script-based integration is easier.
