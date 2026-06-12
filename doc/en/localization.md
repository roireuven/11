# Localization

HotelRestaurantMini-MartManagement supports **21 interface languages** with optional RTL layout.

## Supported locales

| Code | Language |
|------|----------|
| `en` | English |
| `es` | Spanish |
| `fr` | French |
| `de` | German |
| `ja` | Japanese |
| `ko` | Korean |
| `ar` | Arabic (RTL) |
| `hi` | Hindi |
| `th` | Thai |
| `vi` | Vietnamese |
| `id` | Indonesian |
| `tr` | Turkish |
| `ru` | Russian |
| `it` | Italian |
| `nl` | Dutch |
| `pl` | Polish |
| `he` | Hebrew (RTL) |
| `lo` | Lao |
| `pt-BR` | Portuguese (Brazil) |
| `zh-Hans` | Chinese (Simplified) |
| `zh-Hant` | Chinese (Traditional) |

Locale files live at `assets/locales/{code}.json` in the deployed bundle.

## Changing language

1. **Before login:** Interface language dropdown on sign-in screen
2. **After login:** Top bar locale selector or Localization menu
3. **Settings:** App language section (mirrors top bar)

Preference stored in `hotel_mgr_uiLocale` (or namespaced variant per account).

## RTL languages

**Arabic** and **Hebrew** set `dir="rtl"` on the document root:

- Sidebar opens from the right
- Text alignment follows start/end logical properties

## Fonts

Google Noto Sans family loaded for Arabic, CJK, Hebrew, Thai, Lao, Devanagari, etc.

## Currency vs language

Interface language is independent of **hotel currency** in Settings. For Lao language UI, Settings may prompt to set currency to **LAK (₭)**.

Add LAK under **Dropdown Lists → Currencies** if missing.

## Adding or editing translations

In production, locale JSON files are static assets. Developers edit `assets/locales/*.json` and redeploy Firebase Hosting.

Keys follow module structure: `nav.*`, `settings.*`, `restaurant.*`, `msg.*`, etc.

### Guest QR order keys (v2.1+)

Additional sections in locale JSON files:

| Section | Examples |
|---------|----------|
| `bnav` | `guestOrderRest`, `guestOrderMart` — bottom nav QR labels |
| `guestOrder` | Modal titles, order number picker, guest self-order screen, submit buttons |
| `guestQrReport` | QR Orders Report stats, chart labels, grid columns, CSV export |

### Setup, PMS, and modal keys (v2.3 / v2.4)

| Section | Examples |
|---------|----------|
| `setup` | Business name, admin username/email/password on first-time setup |
| `pms` | Dashboard quick-action button labels (`btnAddRoom`, `btnAddBk`, …) |
| `modal` | Add/edit forms: invoice, inventory, menu, store, maintenance ticket, user |
| `guest` / `msg` | Booking **New guest** modal, nationality picker, `addGuestReturn` |

All **21 locales** include these keys (built from `doc/i18n/*.json` patch scripts at deploy time).

Modal forms use **RTL-safe alignment** (`text-align: start`) so English and other LTR languages display correctly when Arabic or Hebrew UI is active.

Embedded fallback blocks in `index.html` cover en, fr, es, he, th, lo; other languages load `/assets/locales/{code}.json`.

## Related

- [Guest QR orders](guest-qr-orders.md)
- [Settings & configuration](settings-and-configuration.md)
- [Navigation & UI](navigation-and-ui.md)
- [Development](development.md)
