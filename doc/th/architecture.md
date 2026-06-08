# Architecture

## High-level design

```
┌─────────────────────────────────────────────────────────┐
│  Browser / WebView (Android)                             │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Single HTML SPA (~1.1 MB index.html)              │  │
│  │  • UI + business logic (JavaScript)                │  │
│  │  • i18n via embedded + assets/locales/*.json       │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│            ┌─────────────┴─────────────┐                │
│            ▼                           ▼                │
│   localStorage (web)          HotelDB / SQLite (Android)│
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  Firebase Hosting (static CDN only)                      │
│  hotel-restaurant-minimart.firebaseapp.com               │
└─────────────────────────────────────────────────────────┘
```

## Single-page application

The entire app ships as one **`index.html`** file containing:

- CSS (design tokens, dark mode, RTL)
- Embedded locale fallbacks
- All module renderers (`renderPage`, RBAC, restaurant, mini-mart, etc.)

Additional static assets:

```
public/
├── index.html
└── assets/
    ├── locales/{code}.json
    └── data/
        ├── embedded-sample.js
        └── nisha1-menu-dataset.js
```

## No server-side business API

Firebase Hosting serves **static files only**. There is no Firestore/Realtime Database sync for hotel data in the current web build.

Client-side storage:

| Environment | API | Persistence |
|-------------|-----|-------------|
| Web | `localStorage` | Per browser profile |
| Android | `HotelDB` (SQLite) | Per device file |

## Authentication model

- Email + password checked against local `accounts` table and setup credentials
- Session stored as `currentUser` JSON in storage
- Not OAuth/cloud auth — credentials are property-managed

## Multi-tenant isolation

Each property setup uses a **data namespace** derived from the system email:

```
hotel_mgr_{namespace}_*
```

Prevents collision when multiple setups use the same browser (still prefer separate profiles for production).

## Role-based access

`applyRBAC()` hides sidebar links based on `currentRole`. See [User roles & permissions](user-roles-and-permissions.md).

## Real-time kitchen sync

Restaurant and Kitchen views read/write the **same local order store**. Updates reflect across tabs on the same browser/device via in-app refresh — not cloud pub/sub.

## Migrations

`appDataEpoch` and setup version flags trigger in-app migrations (e.g. catalog-inventory linking) on load.

## Firebase project (hosting only)

```json
{
  "projectId": "hotel-restaurant-minimart",
  "authDomain": "hotel-restaurant-minimart.firebaseapp.com",
  "storageBucket": "hotel-restaurant-minimart.firebasestorage.app"
}
```

Public config available at `/__/firebase/init.json` — used for analytics/hosting metadata, not app data.

## Android bridge

When `typeof HotelDB !== 'undefined'`:

- `isAndroid = true`
- Reads/writes map to SQLite tables
- Same UI code paths with storage adapters

## Related

- [Deployment](deployment.md)
- [Development](development.md)
- [Backup, restore & data](backup-restore-and-data.md)
