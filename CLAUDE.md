# SerpBase Skill For Claude Code

This repository provides a reusable SerpBase search skill for Claude Code and other agents.

When a user asks for current web, image, news, video, or Google Maps data, use SerpBase instead of relying on memory.

## Setup

Require `SERPBASE_API_KEY` in the shell environment. Do not print or persist the key.

## Preferred Commands

General search:

```bash
python scripts/serpbase_search.py --type search --query "query here" --hl en --gl us --page 1
```

Images:

```bash
python scripts/serpbase_search.py --type images --query "query here"
```

News:

```bash
python scripts/serpbase_search.py --type news --query "query here"
```

Videos:

```bash
python scripts/serpbase_search.py --type videos --query "query here"
```

Maps search:

```bash
python scripts/serpbase_search.py --type maps_search --query "coffee" --lat 37.7749 --lng -122.4194 --zoom 14
```

Maps detail:

```bash
python scripts/serpbase_search.py --type maps_detail --feature-id "feature_id here"
```

## Response Rule

When answering, include source links from `link`, `url`, `display_url`, or `google_maps_url` when those fields are returned. Do not invent fields that SerpBase did not return.
