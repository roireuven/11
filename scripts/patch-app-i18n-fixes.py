#!/usr/bin/env python3
"""Core i18n fixes: invoiceT/uiT helpers, bottom-nav race, embedded locale sync."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "public" / "index.html"
KEYS_FILE = ROOT / "doc" / "i18n" / "guest-order-app-keys.json"
MARKER = "HRMM-I18N-FIXES-v2"
EMBEDDED_LOCALES = ("en", "fr", "es", "he", "th", "lo")

INVOICE_T_OLD = """function invoiceT(key, fallback) {
  var v = (typeof t === 'function' ? t(key) : '');
  return v || fallback;
}"""

INVOICE_T_NEW = """function invoiceT(key, fallback) {
  var v = (typeof t === 'function' ? t(key) : '');
  if (!v || v === key) return fallback;
  return v;
}
function uiT(key, fallback, params) {
  var v = (typeof t === 'function' ? t(key, params) : '');
  if (!v || v === key) {
    if (params && fallback) {
      return fallback.replace(/\\{(\\w+)\\}/g, function(_, w) { return params[w] != null ? String(params[w]) : '{' + w + '}'; });
    }
    return fallback || key;
  }
  return v;
}"""

BNAV_TAIL_OLD = """  document.body.appendChild(nav);
})();"""

BNAV_TAIL_NEW = """  document.body.appendChild(nav);
  if (typeof applyShellI18n === 'function') applyShellI18n();
})();"""

IS_LOCALE_SELECT_OLD = """function isLocaleOrNativeSelect(sel) {
  if (!sel || sel.tagName !== 'SELECT') return false;
  if (sel.id === 'settingsLocaleSelect' || sel.id === 'topbarLocaleSelect' || sel.id === 'loginLocaleSelect' || sel.getAttribute('data-locale-select') === '1' || sel.getAttribute('data-native-select') === '1') return true;
  return false;
}"""

IS_LOCALE_SELECT_NEW = """function isLocaleOrNativeSelect(sel) {
  if (!sel || sel.tagName !== 'SELECT') return false;
  if (sel.id === 'settingsLocaleSelect' || sel.id === 'topbarLocaleSelect' || sel.id === 'loginLocaleSelect' || sel.getAttribute('data-locale-select') === '1' || sel.getAttribute('data-native-select') === '1') return true;
  if (sel.closest && sel.closest('#modalOverlay')) return true;
  return false;
}"""


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def _sync_embedded_locales(content: str, all_keys: dict) -> str:
    for code in EMBEDDED_LOCALES:
        block = all_keys.get(code) or all_keys["en"]
        merge_sections = {}
        for section in ("bnav", "guestOrder", "guestQrReport"):
            if block.get(section):
                merge_sections[section] = block[section]
        if not merge_sections:
            continue

        pattern = rf'(<script type="application/json" id="i18n-{re.escape(code)}-embedded">\s*)(\{{.*?\}})(\s*</script>)'
        match = re.search(pattern, content, flags=re.DOTALL)
        if not match:
            continue
        try:
            data = json.loads(match.group(2))
        except json.JSONDecodeError:
            continue
        for section, entries in merge_sections.items():
            data[section] = _deep_merge(data.get(section) or {}, entries)
        new_json = json.dumps(data, ensure_ascii=False, indent=2)
        content = content[: match.start()] + match.group(1) + new_json + match.group(3) + content[match.end() :]
    return content


def patch(content: str) -> str:
    if INVOICE_T_OLD in content and "function uiT" not in content:
        content = content.replace(INVOICE_T_OLD, INVOICE_T_NEW, 1)
    elif "function uiT" not in content and "function invoiceT" in content:
        content = content.replace(
            "function invoiceT(key, fallback) {",
            INVOICE_T_NEW.split("function translateInvoicePaymentStatus")[0].rstrip() + "\nfunction translateInvoicePaymentStatus",
            1,
        )

    if BNAV_TAIL_OLD in content and "applyShellI18n" not in content.split(BNAV_TAIL_OLD, 1)[1][:80]:
        content = content.replace(BNAV_TAIL_OLD, BNAV_TAIL_NEW, 1)

    if IS_LOCALE_SELECT_OLD in content:
        content = content.replace(IS_LOCALE_SELECT_OLD, IS_LOCALE_SELECT_NEW, 1)
    elif "sel.closest('#modalOverlay')" not in content and "function isLocaleOrNativeSelect" in content:
        content = content.replace(
            "  if (sel.id === 'settingsLocaleSelect' || sel.id === 'topbarLocaleSelect' || sel.id === 'loginLocaleSelect' || sel.getAttribute('data-locale-select') === '1' || sel.getAttribute('data-native-select') === '1') return true;\n  return false;",
            "  if (sel.id === 'settingsLocaleSelect' || sel.id === 'topbarLocaleSelect' || sel.id === 'loginLocaleSelect' || sel.getAttribute('data-locale-select') === '1' || sel.getAttribute('data-native-select') === '1') return true;\n  if (sel.closest && sel.closest('#modalOverlay')) return true;\n  return false;",
            1,
        )

    if KEYS_FILE.is_file():
        all_keys = json.loads(KEYS_FILE.read_text(encoding="utf-8"))
        content = _sync_embedded_locales(content, all_keys)

    content = re.sub(r"HRMM-I18N-FIXES-v\d+", MARKER, content)
    if f"<!-- {MARKER} -->" not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    INDEX.write_text(patch(text), encoding="utf-8")
    print(f"Patched {INDEX} — {MARKER} (invoiceT, uiT, bnav i18n, embedded locales)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
