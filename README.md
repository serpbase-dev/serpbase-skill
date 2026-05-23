# SerpBase Skill

[中文文档](README.zh-CN.md)

SerpBase Skill lets Codex and other AI agents call the [SerpBase](https://serpbase.dev) Google Search, Images, News, Videos, and Maps APIs.

If your agent supports MCP, prefer [serpbase-mcp](https://github.com/serpbase-dev/serpbase-mcp). Use this skill when you want a skill-native workflow or a lightweight script fallback without running an MCP server.

## What it does

- Ground agent answers with real-time Google Search results from SerpBase.
- Fetch structured Google Search results, related searches, knowledge graph data, and other SERP modules.
- Fetch Google Images, News, and Videos results.
- Search Google Maps local places and fetch place details by `feature_id`.
- Call SerpBase directly from the bundled Python script when MCP is unavailable.

## File layout

```text
serpbase-skill/
├── SKILL.md                 # Main skill instructions loaded by agents
├── agents/openai.yaml       # Codex UI metadata
├── references/api.md        # SerpBase API parameters and response field reference
└── scripts/serpbase_search.py
```

## Get an API key

1. Open [SerpBase API Keys](https://serpbase.dev/dashboard/api-keys).
2. Create or copy an API key.
3. Set it as an environment variable:

macOS / Linux:

```bash
export SERPBASE_API_KEY=your_serpbase_api_key
```

Windows PowerShell:

```powershell
$env:SERPBASE_API_KEY = "your_serpbase_api_key"
```

Do not commit API keys to public files.

## Install in Codex

### Option 1: copy into the Codex skills directory

Copy the entire `serpbase-skill` directory into your Codex skills directory.

macOS / Linux:

```bash
mkdir -p ~/.codex/skills
cp -R serpbase-skill ~/.codex/skills/
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force $env:USERPROFILE\.codex\skills
Copy-Item -Recurse .\serpbase-skill $env:USERPROFILE\.codex\skills\
```

Restart Codex, then use:

```text
Use $serpbase-skill to search Google through SerpBase and return cited structured results.
```

### Option 2: use it from a project directory

If this folder already exists in your workspace, point the agent to it:

```text
Use $serpbase-skill at ./serpbase-skill to search for "OpenAI API updates" and cite sources.
```

## Run the script directly

The script uses only the Python standard library.

### Google Search

```bash
python scripts/serpbase_search.py --type search --query "python asyncio" --hl en --gl us --page 1
```

### Google Images

```bash
python scripts/serpbase_search.py --type images --query "iphone 15 pro blue" --hl en --gl us
```

### Google News

```bash
python scripts/serpbase_search.py --type news --query "apple event" --hl en --gl us
```

### Google Videos

```bash
python scripts/serpbase_search.py --type videos --query "python asyncio tutorial" --hl en --gl us
```

### Google Maps local search

```bash
python scripts/serpbase_search.py \
  --type maps_search \
  --query "coffee" \
  --lat 37.7749 \
  --lng -122.4194 \
  --zoom 14
```

`--lat` and `--lng` must be sent together. `--zoom` is valid only with coordinates.

### Google Maps place detail

First get a `feature_id` from `maps_search`, then call:

```bash
python scripts/serpbase_search.py \
  --type maps_detail \
  --feature-id "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123"
```

### Compact JSON output

```bash
python scripts/serpbase_search.py --type search --query "serp api" --compact
```

## CLI options

| Option | Description |
| --- | --- |
| `--type` | `search`, `images`, `news`, `videos`, `maps_search`, or `maps_detail` |
| `--query` | Search query. Required except for `maps_detail` |
| `--feature-id` | `feature_id` for Maps detail lookup |
| `--hl` | Google language code. Default: `en` |
| `--gl` | Google country/region code. Default: `us` |
| `--page` | Page number. Default: `1` |
| `--lat` / `--lng` | Maps coordinates. Must be sent together |
| `--zoom` | Maps zoom. Default: `14` when coordinates are used |
| `--api-key` | Manual API key override. Defaults to `SERPBASE_API_KEY` |
| `--base-url` | Defaults to `SERPBASE_BASE_URL` or `https://api.serpbase.dev` |
| `--timeout` | Request timeout in seconds. Default: `30` |
| `--compact` | Print one-line compact JSON |

## Agent prompt examples

General search:

```text
Use $serpbase-skill to search Google for "best SERP API for AI agents". Summarize the top 5 results and include source links.
```

News monitoring:

```text
Use $serpbase-skill to search recent news about "Apple event". Return title, source, time, link, and one-sentence summary.
```

Local businesses:

```text
Use $serpbase-skill to search Google Maps for coffee shops near 37.7749,-122.4194. Return name, rating, address, website, and feature_id.
```

Place detail:

```text
Use $serpbase-skill to fetch Maps detail for this feature_id and extract phone, website, opening status, photos, and Google Maps URL.
```

## Response fields

Common fields:

- Search: `organic[]`, `people_also_ask`, `related_searches`, `knowledge_graph`
- Images: `images[].image_url`, `thumbnail_url`, `link`, `domain`
- News: `news[].title`, `source`, `time`, `published_at`, `snippet`, `link`
- Videos: `videos[].title`, `source`, `duration`, `time`, `thumbnail_url`, `link`
- Maps Search: `places[].name`, `feature_id`, `rating`, `address`, `phone`, `website`, `google_maps_url`
- Maps Detail: address, contact, open status, photos, categories, and other fields inside `place`

See [references/api.md](references/api.md) for more details.

## Troubleshooting

### `SERPBASE_API_KEY is not set`

Set the environment variable:

```bash
export SERPBASE_API_KEY=your_serpbase_api_key
```

Windows PowerShell:

```powershell
$env:SERPBASE_API_KEY = "your_serpbase_api_key"
```

### `status: 1020`

The account does not have enough SerpBase credits. Add credits or use another valid key.

### Where do I get `feature_id` for Maps detail?

Call `maps_search` first, then use `places[].feature_id`.

### The agent answers without source links

Ask the agent to cite `link`, `url`, `display_url`, or `google_maps_url` from the returned data.

## License

MIT
