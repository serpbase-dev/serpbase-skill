# SerpBase Agent Instructions

Use this file for agents that read project-level instructions such as Codex, opencode, OpenClaw-style agents, and other coding/research agents.

## Capability

Use SerpBase for current Google SERP data:

- Google Search: web results and SERP modules
- Google Images: image URLs, thumbnails, and source pages
- Google News: articles, publishers, timestamps, and snippets
- Google Videos: video links, sources, durations, and thumbnails
- Google Maps Search: local places
- Google Maps Detail: place detail by `feature_id`

## Authentication

Require `SERPBASE_API_KEY` in the environment, or pass `--api-key` to `scripts/serpbase_search.py`.

Never print, log, commit, or reveal API keys. If the key is missing, ask the user to create one at `https://serpbase.dev/dashboard/api-keys`.

## How To Call

Prefer a SerpBase MCP server if one is available. Otherwise run the bundled script from this folder:

```bash
python scripts/serpbase_search.py --type search --query "python asyncio" --hl en --gl us --page 1
```

Maps search:

```bash
python scripts/serpbase_search.py --type maps_search --query "coffee" --lat 37.7749 --lng -122.4194 --zoom 14
```

Maps detail:

```bash
python scripts/serpbase_search.py --type maps_detail --feature-id "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123"
```

## Routing

- Broad web discovery: `search`
- Images: `images`
- News/current publisher discovery: `news`
- Videos/tutorial/media discovery: `videos`
- Local businesses or places: `maps_search`
- Details for one Maps result: `maps_detail`

Use `hl=en`, `gl=us`, `page=1` unless the task or user explicitly calls for another locale. For Maps geo-targeting, send `lat` and `lng` together.

## Answering

Cite result URLs where available. Use `link`, `url`, `display_url`, or `google_maps_url` as source fields. Separate facts returned by SerpBase from your inference. Do not invent missing fields.
