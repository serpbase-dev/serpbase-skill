# SerpBase API Reference

## Authentication

Send the API key in the `X-API-Key` header.

The helper script also sends `X-SerpBase-Source: serpbase-skill`.

## Endpoints

| Script type | HTTP path | Required input | Main result field | Credits |
| --- | --- | --- | --- | --- |
| `search` | `/google/search` | `q` | `organic` | 1 |
| `images` | `/google/images` | `q` | `images` | 2 |
| `news` | `/google/news` | `q` | `news` | 1 |
| `videos` | `/google/videos` | `q` | `videos` | 1 |
| `maps_search` | `/google/maps/search` | `q` | `places` | 2 |
| `maps_detail` | `/google/maps/detail` | `feature_id` | `place` | 2 |

## Shared Query Parameters

- `q`: query string.
- `hl`: Google language code. Default `en`.
- `gl`: Google country code. Default `us`.
- `page`: 1-based page number. Default `1`.

## Maps Parameters

`maps_search` accepts optional `lat`, `lng`, and `zoom`.

- Send `lat` and `lng` together.
- `zoom` is valid only when coordinates are sent.
- Default zoom is `14`.

`maps_detail` accepts:

- `feature_id`: required. Use the value returned by `maps_search`.
- `hl` and `gl`.

## Response Conventions

Successful responses include `status: 0`, `request_id`, `elapsed_ms`, `credits_charged`, `search_type`, and endpoint-specific result fields.

Common result fields:

- Link-like results: `rank`, `position`, `title`, `link`, `url`, `display_url`, `snippet`.
- News/video results: `source`, `time`, `published_at`, `thumbnail_url`.
- Image results: `image_url`, `thumbnail_url`, `source`, `domain`.
- Maps search: `name`, `title`, `feature_id`, `place_id`, `rating`, `types`, `address`, `phone`, `website`, `google_maps_url`, `latitude`, `longitude`, `hours`.
- Maps detail: `place` object with richer place metadata, photos, category, open status, and normalized URLs when available.

Errors generally include nonzero `status` and `error`. Important statuses include:

- `1000`: invalid request.
- `1001`: unauthorized.
- `1020`: insufficient credits.
- `1029`: rate limited.
- `1502`, `1503`, `1504`: upstream or availability failures.
