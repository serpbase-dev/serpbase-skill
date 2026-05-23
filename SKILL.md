---
name: serpbase-skill
description: Call SerpBase Google SERP APIs from Codex or other AI agents. Use when an agent needs current Google Search, Images, News, Videos, Google Maps local search, or Google Maps place detail results through serpbase.dev; when configuring search grounding through SerpBase; or when a user asks to use a SerpBase API key directly from a skill instead of MCP.
---

# SerpBase Skill

## Overview

Use SerpBase as the structured Google SERP data source for current web discovery, grounding, SEO checks, image/news/video discovery, and local Maps enrichment.

Prefer an installed SerpBase MCP server when available. If no MCP tool is available, run `scripts/serpbase_search.py` from this skill.

## Configuration

Require `SERPBASE_API_KEY` in the environment, or pass `--api-key` to the script. Use `SERPBASE_BASE_URL` only for staging or self-hosted gateway testing; it defaults to `https://api.serpbase.dev`.

Never print or reveal the API key. If the key is missing, tell the user to create one at `https://serpbase.dev/dashboard/api-keys`.

## Endpoint Selection

- General web search: `search`
- Image URLs, thumbnails, and source pages: `images`
- Recent publisher/article discovery: `news`
- Video links and metadata: `videos`
- Local businesses or places: `maps_search`
- Details for one Maps result: `maps_detail`

Read `references/api.md` when you need endpoint fields, parameters, or response shape details.

## Script Usage

From the skill directory:

```bash
python scripts/serpbase_search.py --type search --query "python asyncio" --hl en --gl us --page 1
```

Maps local search:

```bash
python scripts/serpbase_search.py --type maps_search --query "coffee" --lat 37.7749 --lng -122.4194 --zoom 14
```

Maps detail:

```bash
python scripts/serpbase_search.py --type maps_detail --feature-id "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123"
```

## Workflow

1. Translate the user request into the narrowest endpoint. Use `search` for broad discovery; use media-specific endpoints only when the user asks for images, news, or videos; use Maps endpoints only for local/place tasks.
2. Send `q`, `hl`, `gl`, and `page` for query endpoints. Use `hl=en`, `gl=us`, `page=1` unless the task or user location calls for something else.
3. For `maps_search`, send `lat` and `lng` together when geo-targeting matters; include `zoom` only with coordinates.
4. For `maps_detail`, first obtain a `feature_id` from `maps_search`; then call detail with that `feature_id`.
5. When answering from results, cite result URLs where available, mention result freshness from returned metadata when relevant, and separate extracted facts from inference.
6. If SerpBase returns an error status, report the status and error message. Do not retry in a loop unless the user explicitly asks.

## Output Guidance

For search/news/video answers, prioritize title, URL, source/display URL, snippet, and published/date fields. For images, include image URL, thumbnail, source page, and domain. For Maps, include name, feature_id, rating, address, phone, website, coordinates, and Google Maps URL when present.

Do not invent missing fields. State that a field was not returned if it matters to the user's task.
