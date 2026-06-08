# Multilingual documentation

HotelRestaurantMini-MartManagement ships user documentation in **21 languages**, matching the app UI locales.

## Supported documentation languages

Same codes as the app interface — see [Localization](localization.md) for the full list (`en`, `es`, `fr`, `de`, `ja`, `ko`, `ar`, `hi`, `th`, `vi`, `id`, `tr`, `ru`, `it`, `nl`, `pl`, `he`, `lo`, `pt-BR`, `zh-Hans`, `zh-Hant`).

## How it works

| Layer | Behavior |
|-------|----------|
| **English (`doc/en/`)** | Full guides — 25+ topics (hotel, restaurant, mini-mart, admin, technical) |
| **Other locales (`doc/{code}/`)** | Translated home, sidebar, getting started, overview, navigation, and localization pages |
| **Fallback** | Sidebar links to English guides for pages not yet translated in your language |
| **Docsify** | Language switcher on `/doc/` — choice stored in `hrmm_doc_lang` |
| **In-app embed** | Documentation iframe uses your current **app UI language** (`?lang=` parameter) |

## In the app

Documentation is combined inside the SPA:

1. **Top bar** — Documentation button  
2. **☰ menu** — **Help → Documentation**  
3. **Bottom nav (mobile)** — **Docs**  
4. **Embedded viewer** — loads `/doc/?lang={your locale}#/README`  

Doc chrome labels (Help, Documentation, Docs, toolbar) use the same locale JSON as the rest of the UI.

## Standalone docs URL

```
https://hotel-restaurant-minimart.firebaseapp.com/doc/?lang=es#/README
```

Change `lang=` to any supported code. Use the language dropdown on the docs site to switch.

## For developers

| Path | Purpose |
|------|---------|
| `doc/en/*.md` | English source guides |
| `doc/i18n/messages.json` | Translated strings for all locales |
| `doc/i18n/locales.json` | Locale metadata (code, native name, RTL) |
| `scripts/generate-doc-locales.py` | Generates locale folders before deploy |
| `scripts/patch-locale-doc-keys.py` | Adds doc keys to app `assets/locales/*.json` |
| `scripts/patch-app-embed-docs.py` | Embeds docs page + locale-aware iframe |

Build: `npm run build` → sync app, patch embed, generate locales, copy to `public/doc/`.

## Related

- [Localization](localization.md)
- [Navigation & UI](navigation-and-ui.md)
- [Deployment](deployment.md)
