#!/usr/bin/env python3
"""Generate multilingual documentation folders for all 21 app UI locales."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "doc"
I18N = DOC / "i18n"
EN = DOC / "en"

# Sidebar page slugs (English source files in doc/en/)
PAGES = {
    "sec_getting_started": [
        ("whats-new-v2.md", "page_whats_new_v2"),
        ("overview.md", "page_overview"),
        ("getting-started.md", "page_getting_started"),
        ("visual-guide.md", "page_visual_guide"),
        ("installation.md", "page_installation"),
        ("first-time-setup.md", "page_first_time_setup"),
        ("demo-credentials.md", "page_demo_credentials"),
    ],
    "sec_using": [
        ("user-roles-and-permissions.md", "page_user_roles"),
        ("navigation-and-ui.md", "page_navigation"),
        ("hotel-operations.md", "page_hotel"),
        ("services-and-billing.md", "page_services"),
        ("restaurant-and-kitchen.md", "page_restaurant"),
        ("minimart-and-pos.md", "page_minimart"),
        ("guest-qr-orders.md", "page_guest_qr_orders"),
        ("inventory-and-catalog.md", "page_inventory"),
        ("guest-portal.md", "page_guest_portal"),
        ("reports.md", "page_reports"),
        ("accounts-and-audit.md", "page_accounts"),
    ],
    "sec_admin": [
        ("settings-and-configuration.md", "page_settings"),
        ("backup-restore-and-data.md", "page_backup"),
        ("localization.md", "page_localization"),
        ("multilingual-documentation.md", "page_multilingual_docs"),
        ("data-model.md", "page_data_model"),
    ],
    "sec_technical": [
        ("architecture.md", "page_architecture"),
        ("deployment.md", "page_deployment"),
        ("development.md", "page_development"),
        ("troubleshooting-faq.md", "page_troubleshooting"),
        ("glossary.md", "page_glossary"),
    ],
}

TRANSLATED_PAGES = {
    "getting-started.md",
    "overview.md",
    "navigation-and-ui.md",
    "localization.md",
    "whats-new-v2.md",
}


def load_messages() -> dict:
    path = I18N / "messages.json"
    if not path.is_file():
        raise SystemExit(f"Missing {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def msg(messages: dict, locale: str, key: str) -> str:
    block = messages.get(locale) or messages["en"]
    return block.get(key) or messages["en"].get(key) or key


def en_doc_href(slug: str) -> str:
    base = slug.replace(".md", "")
    return f"https://hotel-restaurant-minimart.firebaseapp.com/doc/?lang=en#/{base}"


def all_page_slugs() -> list[str]:
    slugs: list[str] = []
    for pages in PAGES.values():
        for slug, _ in pages:
            if slug not in slugs:
                slugs.append(slug)
    return slugs


def write_readme(locale: str, messages: dict, dest: Path) -> None:
    m = lambda k: msg(messages, locale, k)
    en_note = "" if locale == "en" else f"\n> {m('english_fallback_note')}\n"
    text = f"""# {m('home_title')}

{m('home_subtitle')}{en_note}

> **{m('browse_online')}:** [https://hotel-restaurant-minimart.firebaseapp.com/doc/?lang={locale}](https://hotel-restaurant-minimart.firebaseapp.com/doc/?lang={locale})  
> **{m('inside_app')}:** {m('inside_app_detail')}  
> **{m('mirror')}:** [GitHub Pages doc](https://roireuven.github.io/11/doc/?lang={locale})

## {m('live_app_heading')}

| {m('table_platform')} | URL |
|----------|-----|
| **{m('web_firebase')}** | [hotel-restaurant-minimart.firebaseapp.com](https://hotel-restaurant-minimart.firebaseapp.com/) |
| **{m('alt_domain')}** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

## {m('doc_index_heading')}

{m('doc_index_intro')}

## {m('version_heading')}

- **{m('app_version')}:** v2.4
- **{m('doc_source')}:** hotel-restaurant-minimart.firebaseapp.com

## {m('support_heading')}

1. {m('support_step1')}
2. {m('support_step2')}
3. {m('support_step3')}
"""
    dest.write_text(text, encoding="utf-8")


def write_sidebar(locale: str, messages: dict, dest: Path) -> None:
    lines = ["* [Home](README.md)", ""]
    for sec_key, pages in PAGES.items():
        lines.append(f"* **{msg(messages, locale, sec_key)}**")
        for slug, page_key in pages:
            title = msg(messages, locale, page_key)
            lines.append(f"  * [{title}]({slug})")
        lines.append("")
    lines.append(f"* **{msg(messages, locale, 'sec_links')}**")
    lines.append("  * [Live web app ↗](https://hotel-restaurant-minimart.firebaseapp.com/)")
    lines.append("  * [APK landing (GitHub) ↗](https://roireuven.github.io/11/)")
    dest.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_getting_started(locale: str, messages: dict, dest: Path) -> None:
    if locale == "en":
        src = EN / "getting-started.md"
        if src.is_file():
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
        return
    m = lambda k: msg(messages, locale, k)
    body = "\n".join(f"- {m(k)}" for k in [
        "gs_bullet1", "gs_bullet2", "gs_bullet3", "gs_bullet4", "gs_bullet5",
    ])
    text = f"""# {m('page_getting_started')}

{m('gs_intro')}

## {m('gs_steps_heading')}

{body}

## {m('gs_full_guide')}

{m('gs_full_guide_text')} [English getting started guide]({en_doc_href('getting-started.md')}).
"""
    dest.write_text(text, encoding="utf-8")


def write_overview(locale: str, messages: dict, dest: Path) -> None:
    if locale == "en":
        dest.write_text((EN / "overview.md").read_text(encoding="utf-8"), encoding="utf-8")
        return
    m = lambda k: msg(messages, locale, k)
    text = f"""# {m('page_overview')}

{m('overview_intro')}

## {m('overview_modules')}

- **{m('module_hotel')}** — {m('module_hotel_desc')}
- **{m('module_restaurant')}** — {m('module_restaurant_desc')}
- **{m('module_minimart')}** — {m('module_minimart_desc')}
- **{m('module_admin')}** — {m('module_admin_desc')}

{m('overview_full')} [English overview]({en_doc_href('overview.md')}).
"""
    dest.write_text(text, encoding="utf-8")


def write_navigation(locale: str, messages: dict, dest: Path) -> None:
    if locale == "en":
        dest.write_text((EN / "navigation-and-ui.md").read_text(encoding="utf-8"), encoding="utf-8")
        return
    m = lambda k: msg(messages, locale, k)
    text = f"""# {m('page_navigation')}

{m('nav_intro')}

## {m('nav_doc_heading')}

| {m('nav_location')} | {m('nav_label')} | {m('nav_action')} |
|----------|-------|--------|
| **{m('nav_topbar')}** | {m('doc_label')} | {m('nav_topbar_action')} |
| **{m('nav_hamburger')}** | {m('nav_help')} → {m('doc_label')} | {m('nav_hamburger_action')} |
| **{m('nav_bottom')}** | {m('bnav_docs')} | {m('nav_bottom_action')} |

{m('nav_full')} [English navigation guide]({en_doc_href('navigation-and-ui.md')}).
"""
    dest.write_text(text, encoding="utf-8")


def write_localization(locale: str, messages: dict, dest: Path) -> None:
    if locale == "en":
        dest.write_text((EN / "localization.md").read_text(encoding="utf-8"), encoding="utf-8")
        return
    m = lambda k: msg(messages, locale, k)
    locales = json.loads((I18N / "locales.json").read_text(encoding="utf-8"))
    rows = "\n".join(f"| `{L['code']}` | {L['native']} |" for L in locales)
    text = f"""# {m('page_localization')}

{m('loc_intro')}

## {m('loc_supported')}

| Code | {m('loc_language')} |
|------|----------|
{rows}

{m('loc_docs_note')}

{m('loc_full')} [English localization guide]({en_doc_href('localization.md')}).
"""
    dest.write_text(text, encoding="utf-8")


def copy_english_fallback(locale: str, slug: str) -> None:
    """Copy English guides for pages without a locale translation (Firebase must serve real .md files)."""
    if locale == "en" or slug in TRANSLATED_PAGES:
        return
    src = EN / slug
    if not src.is_file():
        return
    text = src.read_text(encoding="utf-8")
    text = re.sub(r"!\[([^\]]*)\]\(assets/", r"![\1](../en/assets/", text)
    text = re.sub(r"(?<!!)\]\(assets/", "](../en/assets/", text)
    (DOC / locale / slug).write_text(text, encoding="utf-8")


def write_ui_json(messages: dict) -> None:
    ui = {}
    for locale in messages:
        ui[locale] = {
            "loading": msg(messages, locale, "ui_loading"),
            "search_placeholder": msg(messages, locale, "ui_search"),
            "search_no_data": msg(messages, locale, "ui_no_results"),
            "language": msg(messages, locale, "ui_language"),
            "open_new_tab": msg(messages, locale, "ui_open_tab"),
        }
    (I18N / "ui.json").write_text(json.dumps(ui, ensure_ascii=False, indent=2), encoding="utf-8")


def generate() -> None:
    messages = load_messages()
    locales = json.loads((I18N / "locales.json").read_text(encoding="utf-8"))
    slugs = all_page_slugs()

    for loc in locales:
        code = loc["code"]
        dest_dir = DOC / code
        if code != "en":
            dest_dir.mkdir(parents=True, exist_ok=True)

        if code == "en":
            dest_dir = EN
        else:
            write_readme(code, messages, dest_dir / "README.md")
            write_sidebar(code, messages, dest_dir / "_sidebar.md")
            write_getting_started(code, messages, dest_dir / "getting-started.md")
            write_overview(code, messages, dest_dir / "overview.md")
            write_navigation(code, messages, dest_dir / "navigation-and-ui.md")
            write_localization(code, messages, dest_dir / "localization.md")
            for slug in slugs:
                copy_english_fallback(code, slug)

    write_ui_json(messages)
    print(f"Generated documentation for {len(locales)} locales in {DOC}/")


def main() -> int:
    if not EN.is_dir():
        print(f"Missing {EN}", file=sys.stderr)
        return 1
    generate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
