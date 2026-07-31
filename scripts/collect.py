#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

API_URL = "https://open.maimemo.com/open/api/v1/study/get_today_items"
TZ = ZoneInfo("Asia/Taipei")


def fetch_today_items(token: str) -> dict:
    payload = json.dumps({"limit": 1000}).encode("utf-8")
    request = urllib.request.Request(
        API_URL,
        data=payload,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": "maimemo-daily/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"墨墨 API 返回 HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"无法连接墨墨 API: {exc}") from exc


def main() -> int:
    token = os.getenv("MAIMEMO_TOKEN", "").strip()
    if not token:
        print("缺少环境变量 MAIMEMO_TOKEN", file=sys.stderr)
        return 2

    now = datetime.now(TZ)
    date_str = now.strftime("%Y-%m-%d")
    raw = fetch_today_items(token)
    print("RAW_RESPONSE_START")
    print(json.dumps(raw, ensure_ascii=False, indent=2))
    print("RAW_RESPONSE_END")
    
    print("墨墨 API 原始响应：")
    print(json.dumps(raw, ensure_ascii=False, indent=2))
    
    items = raw.get("today_items", [])

    cleaned = []
    for item in items:
        cleaned.append(
            {
                "word": item.get("voc_spelling"),
                "first_response": item.get("first_response"),
                "is_new": bool(item.get("is_new")),
                "is_finished": bool(item.get("is_finished")),
                "order": item.get("order"),
            }
        )

    cleaned.sort(key=lambda x: (x["order"] is None, x["order"] or 0))

    result = {
        "date": date_str,
        "timezone": "Asia/Taipei",
        "collected_at": now.isoformat(),
        "count": len(cleaned),
        "items": cleaned,
    }

    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    (data_dir / f"{date_str}.json").write_text(text, encoding="utf-8")
    (data_dir / "latest.json").write_text(text, encoding="utf-8")

    print(f"已保存 {len(cleaned)} 个单词：{date_str}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
