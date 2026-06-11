#!/usr/bin/env python3
"""Fix modal form alignment for LTR and RTL locales."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-MODAL-RTL-v1"
INDEX = Path("public/index.html")

CSS_ANCHOR = "    .modal-body .form-group label { font-size: 0.8rem; font-weight: 600; color: #1a3a5c; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.35rem; }"
CSS_NEW = """    .modal-body .form-group label { font-size: 0.8rem; font-weight: 600; color: #1a3a5c; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 0.25rem; display: flex; align-items: center; gap: 0.35rem; text-align: start; justify-content: flex-start; }
    .modal-body .form-group small { text-align: start; display: block; }
    .modal-header { flex-direction: row; }
    .modal-header h2 { text-align: start; flex: 1; min-width: 0; }
    .modal-body .form-control,
    .modal-body textarea,
    .modal-body select { text-align: start; }
    [dir="rtl"] .modal-body input[type="email"],
    [dir="rtl"] .modal-body input[type="number"],
    [dir="rtl"] .modal-body input[type="date"],
    [dir="rtl"] .modal-body input[type="url"],
    [dir="rtl"] .modal-body input[type="password"],
    [dir="rtl"] .modal-body input[inputmode="email"],
    [dir="rtl"] .modal-body input[inputmode="numeric"] { direction: ltr; text-align: left; }
    .modal-footer { justify-content: flex-start; gap: 0.5rem; }"""


def patch(content: str) -> str:
    if MARKER in content and "text-align: start; justify-content: flex-start" in content:
        return content
    if CSS_ANCHOR not in content:
        print("Modal label CSS anchor missing", file=sys.stderr)
        return content
    content = content.replace(CSS_ANCHOR, CSS_NEW, 1)
    if MARKER not in content:
        content = content.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)
    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    patched = patch(text)
    if patched == text:
        print("No modal RTL changes applied.")
        return 0
    INDEX.write_text(patched, encoding="utf-8")
    print(f"Patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
