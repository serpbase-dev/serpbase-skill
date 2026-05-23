# SerpBase Skill For OpenClaw-Style Agents

Use `AGENTS.md` as the canonical project instruction file.

When current Google Search, Images, News, Videos, or Maps data is needed, call SerpBase with:

```bash
python scripts/serpbase_search.py --type search --query "query here"
```

Require `SERPBASE_API_KEY` in the environment. Do not print, log, commit, or reveal API keys.

For endpoint routing, response fields, and citation rules, follow `AGENTS.md` and `references/api.md`.
