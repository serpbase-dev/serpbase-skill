#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any


ENDPOINTS = {
    "search": "/google/search",
    "images": "/google/images",
    "news": "/google/news",
    "videos": "/google/videos",
    "maps_search": "/google/maps/search",
    "maps_detail": "/google/maps/detail",
}


def compact_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def build_payload(args: argparse.Namespace) -> dict[str, Any]:
    hl = args.hl.strip() or "en"
    gl = args.gl.strip() or "us"
    if args.type == "maps_detail":
        feature_id = (args.feature_id or "").strip()
        if not feature_id:
            raise SystemExit("--feature-id is required for maps_detail")
        return {"feature_id": feature_id, "hl": hl, "gl": gl}

    query = (args.query or "").strip()
    if not query:
        raise SystemExit("--query is required")
    if args.page < 1:
        raise SystemExit("--page must be >= 1")

    payload: dict[str, Any] = {
        "q": query,
        "hl": hl,
        "gl": gl,
        "page": args.page,
    }
    if args.type == "maps_search":
        has_lat = args.lat is not None
        has_lng = args.lng is not None
        if has_lat != has_lng:
            raise SystemExit("--lat and --lng must be provided together")
        if args.zoom is not None and not (has_lat and has_lng):
            raise SystemExit("--zoom requires --lat and --lng")
        if has_lat and has_lng:
            if not -90 <= args.lat <= 90:
                raise SystemExit("--lat must be between -90 and 90")
            if not -180 <= args.lng <= 180:
                raise SystemExit("--lng must be between -180 and 180")
            payload["lat"] = args.lat
            payload["lng"] = args.lng
            payload["zoom"] = args.zoom or 14
    return compact_payload(payload)


def call_serpbase(args: argparse.Namespace) -> dict[str, Any]:
    request_payload = build_payload(args)
    api_key = args.api_key or os.getenv("SERPBASE_API_KEY", "")
    if not api_key:
        raise SystemExit(
            "SERPBASE_API_KEY is not set. Create a key at https://serpbase.dev/dashboard/api-keys."
        )
    base_url = (args.base_url or os.getenv("SERPBASE_BASE_URL", "https://api.serpbase.dev")).rstrip("/")
    url = f"{base_url}{ENDPOINTS[args.type]}"
    payload = json.dumps(request_payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "User-Agent": "serpbase-skill/0.1 (+https://github.com/serpbase-dev/serpbase-skill)",
            "X-API-Key": api_key,
            "X-SerpBase-Source": "serpbase-skill",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            raise SystemExit(f"HTTP {exc.code}: {body}") from exc
        raise SystemExit(json.dumps(data, ensure_ascii=True, indent=2)) from exc
    except urllib.error.URLError as exc:
        raise SystemExit(f"Network error: {exc.reason}") from exc

    data = json.loads(body)
    if data.get("status") not in (0, None):
        raise SystemExit(json.dumps(data, ensure_ascii=True, indent=2))
    return data


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Call SerpBase Google SERP APIs.")
    parser.add_argument("--type", choices=sorted(ENDPOINTS), default="search")
    parser.add_argument("--query", help="Search query for all query endpoints.")
    parser.add_argument("--feature-id", help="Google Maps feature_id for maps_detail.")
    parser.add_argument("--hl", default="en", help="Google language code.")
    parser.add_argument("--gl", default="us", help="Google country code.")
    parser.add_argument("--page", type=int, default=1, help="1-based page number.")
    parser.add_argument("--lat", type=float, help="Maps latitude.")
    parser.add_argument("--lng", type=float, help="Maps longitude.")
    parser.add_argument("--zoom", type=int, help="Maps zoom, valid with lat/lng.")
    parser.add_argument("--api-key", help="SerpBase API key. Defaults to SERPBASE_API_KEY.")
    parser.add_argument("--base-url", help="Defaults to SERPBASE_BASE_URL or https://api.serpbase.dev.")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--compact", action="store_true", help="Print compact JSON.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    data = call_serpbase(args)
    if args.compact:
        print(json.dumps(data, ensure_ascii=True, separators=(",", ":")))
    else:
        print(json.dumps(data, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
