# SerpBase Skill

[English](README.md)

这是一个给 Codex / Agent 使用的 SerpBase skill，用来通过 [SerpBase](https://serpbase.dev) 调用 Google Search、Images、News、Videos 和 Maps API。

如果你的 Agent 支持 MCP，优先使用 [serpbase-mcp](https://github.com/serpbase-dev/serpbase-mcp)。如果你想用 skill 方式，把这份目录安装到 Codex skills 里即可。

## 能做什么

- 让 Agent 使用 SerpBase 做实时 Google 搜索 grounding
- 获取结构化 Google Search 结果、相关搜索、知识图谱等 SERP 数据
- 获取 Google Images / News / Videos 的结构化结果
- 搜索 Google Maps 本地地点，并用 `feature_id` 查询地点详情
- 在没有 MCP server 的环境里，用附带脚本直接调用 SerpBase API

## 文件结构

```text
serpbase-skill/
├── SKILL.md                 # skill 主说明，Agent 会读取这里的工作流
├── agents/openai.yaml       # Codex UI 元数据
├── references/api.md        # SerpBase API 参数和返回字段速查
└── scripts/serpbase_search.py
```

## 准备 API Key

1. 打开 [SerpBase API Keys](https://serpbase.dev/dashboard/api-keys)
2. 创建或复制一个 API key
3. 在本地设置环境变量：

macOS / Linux:

```bash
export SERPBASE_API_KEY=your_serpbase_api_key
```

Windows PowerShell:

```powershell
$env:SERPBASE_API_KEY = "your_serpbase_api_key"
```

不要把 API key 写进公开文件。

## 安装到 Codex

### 方法一：复制到 Codex skills 目录

把整个 `serpbase-skill` 目录复制到 Codex skills 目录：

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

重启 Codex 后即可使用：

```text
Use $serpbase-skill to search Google through SerpBase and return cited structured results.
```

### 方法二：直接从项目目录使用

如果你在一个工作区里已经有这个目录，也可以让 Agent 明确使用：

```text
Use $serpbase-skill at ./serpbase-skill to search for "OpenAI API updates" and cite sources.
```

## 直接运行脚本

脚本不依赖第三方包，使用 Python 标准库即可。

### 普通 Google 搜索

```bash
python scripts/serpbase_search.py --type search --query "python asyncio" --hl en --gl us --page 1
```

### 图片搜索

```bash
python scripts/serpbase_search.py --type images --query "iphone 15 pro blue" --hl en --gl us
```

### 新闻搜索

```bash
python scripts/serpbase_search.py --type news --query "apple event" --hl en --gl us
```

### 视频搜索

```bash
python scripts/serpbase_search.py --type videos --query "python asyncio tutorial" --hl en --gl us
```

### Google Maps 本地搜索

```bash
python scripts/serpbase_search.py \
  --type maps_search \
  --query "coffee" \
  --lat 37.7749 \
  --lng -122.4194 \
  --zoom 14
```

`--lat` 和 `--lng` 必须一起传；`--zoom` 只有在传坐标时有效。

### Google Maps 地点详情

先用 `maps_search` 拿到 `feature_id`，再调用：

```bash
python scripts/serpbase_search.py \
  --type maps_detail \
  --feature-id "0x8085809c2c6fdc63:0x4b3f2d70e4f5a123"
```

### 输出紧凑 JSON

```bash
python scripts/serpbase_search.py --type search --query "serp api" --compact
```

## 参数说明

| 参数 | 说明 |
| --- | --- |
| `--type` | `search`、`images`、`news`、`videos`、`maps_search`、`maps_detail` |
| `--query` | 搜索关键词，除 `maps_detail` 外都需要 |
| `--feature-id` | Maps 详情查询所需的 `feature_id` |
| `--hl` | Google 语言代码，默认 `en` |
| `--gl` | Google 国家/地区代码，默认 `us` |
| `--page` | 页码，默认 `1` |
| `--lat` / `--lng` | Maps 搜索坐标，需要成对传入 |
| `--zoom` | Maps zoom，默认 `14` |
| `--api-key` | 手动传 API key；默认读取 `SERPBASE_API_KEY` |
| `--base-url` | 默认读取 `SERPBASE_BASE_URL` 或使用 `https://api.serpbase.dev` |
| `--timeout` | 请求超时秒数，默认 `30` |
| `--compact` | 输出单行紧凑 JSON |

## Agent 使用提示词示例

普通搜索：

```text
Use $serpbase-skill to search Google for "best SERP API for AI agents". Summarize the top 5 results and include source links.
```

新闻监控：

```text
Use $serpbase-skill to search recent news about "Apple event". Return title, source, time, link, and one-sentence summary.
```

本地商家：

```text
Use $serpbase-skill to search Google Maps for coffee shops near 37.7749,-122.4194. Return name, rating, address, website, and feature_id.
```

地点详情：

```text
Use $serpbase-skill to fetch Maps detail for this feature_id and extract phone, website, opening status, photos, and Google Maps URL.
```

## 返回字段怎么看

常用字段：

- Search: `organic[]`, `people_also_ask`, `related_searches`, `knowledge_graph`
- Images: `images[].image_url`, `thumbnail_url`, `link`, `domain`
- News: `news[].title`, `source`, `time`, `published_at`, `snippet`, `link`
- Videos: `videos[].title`, `source`, `duration`, `time`, `thumbnail_url`, `link`
- Maps Search: `places[].name`, `feature_id`, `rating`, `address`, `phone`, `website`, `google_maps_url`
- Maps Detail: `place` 对象里的地址、联系方式、营业状态、照片、分类等详情

更详细字段见 [references/api.md](references/api.md)。

## 常见问题

### 1. 提示 `SERPBASE_API_KEY is not set`

设置环境变量：

```bash
export SERPBASE_API_KEY=your_serpbase_api_key
```

Windows PowerShell:

```powershell
$env:SERPBASE_API_KEY = "your_serpbase_api_key"
```

### 2. 返回 `status: 1020`

SerpBase credits 不足，需要充值或换一个有余额的 key。

### 3. Maps detail 不知道 `feature_id` 从哪里来

先调用 `maps_search`，从 `places[].feature_id` 里取。

### 4. Agent 回答没有引用来源

提示 Agent 使用结果里的 `link`、`url`、`display_url`、`google_maps_url` 作为来源链接。

## License

MIT
