#!/usr/bin/env python3
"""Generate whats-new-v2.md documentation in all 21 app locales."""
from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "doc"
EN_SRC = DOC / "en" / "whats-new-v2.md"
MESSAGES = DOC / "i18n" / "messages.json"

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

LINK_RE = re.compile(r"(\[[^\]]*\]\([^)]+\)|`[^`]+`|\{[^}]+\})")
CHUNK_MAX = 2800


def protect_inline(text: str) -> tuple[str, list[str]]:
    tokens: list[str] = []

    def repl(m: re.Match[str]) -> str:
        tokens.append(m.group(1))
        return f"⟦T{len(tokens) - 1}⟧"

    return LINK_RE.sub(repl, text), tokens


def restore_inline(text: str, tokens: list[str]) -> str:
    for i, tok in enumerate(tokens):
        text = text.replace(f"⟦T{i}⟧", tok)
    return text


def translate_chunk(text: str, target: str, translator_cls) -> str:
    if not text.strip():
        return text
    protected, tokens = protect_inline(text)
    for attempt in range(4):
        try:
            out = translator_cls(source="en", target=target).translate(protected)
            return restore_inline(out, tokens)
        except Exception:
            time.sleep(1.5 * (attempt + 1))
    return text


def chunk_paragraphs(text: str) -> list[str]:
    parts: list[str] = []
    buf: list[str] = []
    size = 0
    for line in text.splitlines(keepends=True):
        if size + len(line) > CHUNK_MAX and buf:
            parts.append("".join(buf))
            buf = []
            size = 0
        buf.append(line)
        size += len(line)
    if buf:
        parts.append("".join(buf))
    return parts


def translate_markdown(text: str, locale: str, translator_cls) -> str:
    if locale == "en":
        return text
    target = LOCALE_TARGETS.get(locale, locale)
    chunks = chunk_paragraphs(text)
    return "".join(translate_chunk(c, target, translator_cls) for c in chunks)


def patch_messages_title() -> None:
    data = json.loads(MESSAGES.read_text(encoding="utf-8"))
    en_title = "What's new in v2.3 / v2.4"
    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        GoogleTranslator = None  # type: ignore
    for code in data:
        if code == "en":
            data[code]["page_whats_new_v2"] = en_title
            continue
        title = en_title
        if GoogleTranslator:
            try:
                target = LOCALE_TARGETS.get(code, code)
                title = GoogleTranslator(source="en", target=target).translate(en_title)
            except Exception:
                pass
        data[code]["page_whats_new_v2"] = title
    MESSAGES.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if not EN_SRC.is_file():
        print(f"Missing {EN_SRC}", file=sys.stderr)
        return 1

    locales = json.loads((DOC / "i18n" / "locales.json").read_text(encoding="utf-8"))
    src_mtime = EN_SRC.stat().st_mtime
    all_present = all((DOC / loc["code"] / "whats-new-v2.md").is_file() for loc in locales)
    msgs = json.loads(MESSAGES.read_text(encoding="utf-8")) if MESSAGES.is_file() else {}
    titles_ok = all(msgs.get(loc["code"], {}).get("page_whats_new_v2") for loc in locales)
    if all_present and titles_ok and not os.environ.get("FORCE_WHATS_NEW_DOCS"):
        newest = max((DOC / loc["code"] / "whats-new-v2.md").stat().st_mtime for loc in locales)
        if newest >= src_mtime:
            print("What's new v2 docs up to date — skipping translation")
            return 0

    try:
        from deep_translator import GoogleTranslator
    except ImportError:
        print("deep-translator required: pip install deep-translator", file=sys.stderr)
        return 1

    source = EN_SRC.read_text(encoding="utf-8")
    count = 0
    for loc in locales:
        code = loc["code"]
        dest_dir = DOC / code
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / "whats-new-v2.md"
        translated = translate_markdown(source, code, GoogleTranslator)
        dest.write_text(translated, encoding="utf-8")
        count += 1
        print(f"Wrote {dest}")

    patch_messages_title()
    print(f"Generated whats-new-v2 docs for {count} locales")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
