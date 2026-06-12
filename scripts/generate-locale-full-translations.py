#!/usr/bin/env python3
"""Generate translations for locale keys still identical to English (resumable, parallel)."""
from __future__ import annotations

import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCALES_DIR = ROOT / "public" / "assets" / "locales"
OUT_FILE = ROOT / "doc" / "i18n" / "locale-full-translations.json"
CACHE_FILE = ROOT / "doc" / "i18n" / "locale-translation-cache.json"
MAX_WORKERS = 6

LOCALE_TARGETS = {
    "ar": "ar",
    "de": "de",
    "es": "es",
    "fr": "fr",
    "he": "iw",
    "hi": "hi",
    "id": "id",
    "it": "it",
    "ja": "ja",
    "ko": "ko",
    "lo": "lo",
    "nl": "nl",
    "pl": "pl",
    "pt-BR": "pt",
    "ru": "ru",
    "th": "th",
    "tr": "tr",
    "vi": "vi",
    "zh-Hans": "zh-CN",
    "zh-Hant": "zh-TW",
}

PLACEHOLDER_RE = re.compile(r"(\{[a-zA-Z0-9_]+\})")
TOKEN_PREFIX = "⟦PH"
TOKEN_SUFFIX = "⟧"


def flatten(data: dict, prefix: str = "") -> dict[str, str]:
    out: dict[str, str] = {}
    for key, val in data.items():
        if key == "_meta":
            continue
        full = f"{prefix}.{key}" if prefix else key
        if isinstance(val, dict):
            out.update(flatten(val, full))
        elif isinstance(val, str):
            out[full] = val
    return out


def protect_placeholders(text: str) -> tuple[str, list[str]]:
    placeholders: list[str] = []

    def repl(m: re.Match[str]) -> str:
        placeholders.append(m.group(1))
        return f"{TOKEN_PREFIX}{len(placeholders) - 1}{TOKEN_SUFFIX}"

    return PLACEHOLDER_RE.sub(repl, text), placeholders


def restore_placeholders(text: str, placeholders: list[str]) -> str:
    for i, ph in enumerate(placeholders):
        text = text.replace(f"{TOKEN_PREFIX}{i}{TOKEN_SUFFIX}", ph)
    return text


def translate_text(text: str, target: str, translator_cls, retries: int = 4) -> str:
    if not text or not text.strip():
        return text
    protected, placeholders = protect_placeholders(text)
    for attempt in range(retries):
        try:
            result = translator_cls(source="en", target=target).translate(protected)
            if result:
                return restore_placeholders(result, placeholders)
        except Exception:
            time.sleep(1.2 * (attempt + 1))
    return text


def load_json(path: Path, default):
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def process_locale(
    locale: str,
    target: str,
    en_flat: dict[str, str],
    loc_flat: dict[str, str],
    locale_cache: dict[str, str],
    translator_cls,
) -> tuple[str, dict, dict[str, str], int]:
    pending_keys = [k for k in en_flat if loc_flat.get(k) == en_flat[k]]
    unique_strings = sorted({en_flat[k] for k in pending_keys}, key=len)
    locale_block: dict = {}
    api_calls = 0
    missing = [s for s in unique_strings if s not in locale_cache]

    def do_one(en_text: str) -> tuple[str, str]:
        return en_text, translate_text(en_text, target, translator_cls)

    if missing:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {pool.submit(do_one, s): s for s in missing}
            for fut in as_completed(futures):
                en_text, tr = fut.result()
                locale_cache[en_text] = tr
                api_calls += 1

    for full_key in pending_keys:
        section, _, subkey = full_key.partition(".")
        if not subkey:
            continue
        locale_block.setdefault(section, {})[subkey] = locale_cache.get(en_flat[full_key], en_flat[full_key])

    return locale, locale_block, locale_cache, api_calls


def main() -> int:
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("Install deep-translator: pip install deep-translator", file=sys.stderr)
        return 1

    if not LOCALES_DIR.is_dir():
        print(f"Run npm run build first — missing {LOCALES_DIR}", file=sys.stderr)
        return 1

    en_flat = flatten(json.loads((LOCALES_DIR / "en.json").read_text(encoding="utf-8")))
    out = load_json(OUT_FILE, {})
    cache = load_json(CACHE_FILE, {})
    total_api = 0

    for locale, target in LOCALE_TARGETS.items():
        path = LOCALES_DIR / f"{locale}.json"
        if not path.is_file():
            continue
        loc_flat = flatten(json.loads(path.read_text(encoding="utf-8")))
        locale_cache = cache.setdefault(locale, {})
        pending = sum(1 for k in en_flat if loc_flat.get(k) == en_flat[k])
        print(f"{locale}: {pending} keys pending, {len(locale_cache)} cached strings")

        code, block, locale_cache, api_calls = process_locale(
            locale, target, en_flat, loc_flat, locale_cache, GoogleTranslator
        )
        cache[code] = locale_cache
        out[code] = block
        total_api += api_calls
        save_json(CACHE_FILE, cache)
        save_json(OUT_FILE, out)
        print(f"  ✓ {code} — {api_calls} API calls")

    print(f"Complete — {total_api} new API translations → {OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
