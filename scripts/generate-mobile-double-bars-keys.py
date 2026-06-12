#!/usr/bin/env python3
"""Generate mobile double-bars i18n keys for all 21 locales."""
from __future__ import annotations

import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "doc" / "i18n" / "mobile-double-bars-keys.json"
LOCALES = [
    "ar", "de", "en", "es", "fr", "he", "hi", "id", "it", "ja", "ko", "lo",
    "nl", "pl", "pt-BR", "ru", "th", "tr", "vi", "zh-Hans", "zh-Hant",
]
TARGETS = {
    "ar": "ar", "de": "de", "es": "es", "fr": "fr", "he": "iw", "hi": "hi",
    "id": "id", "it": "it", "ja": "ja", "ko": "ko", "lo": "lo", "nl": "nl",
    "pl": "pl", "pt-BR": "pt", "ru": "ru", "th": "th", "tr": "tr", "vi": "vi",
    "zh-Hans": "zh-CN", "zh-Hant": "zh-TW",
}


def main() -> int:
    from deep_translator import GoogleTranslator

    en = {"topbar.more": "More", "bnav.more": "More"}
    data: dict = {"en": en}
    for code in LOCALES:
        if code == "en":
            continue
        block = {}
        tgt = TARGETS.get(code, code)
        tr = GoogleTranslator(source="en", target=tgt)
        for k, v in en.items():
            for attempt in range(4):
                try:
                    block[k] = tr.translate(v)
                    break
                except Exception:
                    time.sleep(1.0 * (attempt + 1))
            else:
                block[k] = v
            time.sleep(0.05)
        data[code] = block
        print(f"Translated {code}")
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
