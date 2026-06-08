# Development

Guide for developers working on HotelRestaurantMini-MartManagement.

## Repository layout

When the dev environment is present in [roireuven/11](https://github.com/roireuven/11):

```
hotel-restaurant-minimart/
├── public/                 # Static files deployed to Firebase
│   ├── index.html          # Full SPA
│   └── assets/
│       ├── locales/
│       └── data/
├── firebase.json
├── .firebaserc
├── package.json
└── scripts/
    └── sync-from-production.sh
```

Documentation lives in `/doc/` at repository root.

## Prerequisites

- Node.js 18+
- npm
- Firebase CLI (via `npm install` in project)

## Local development

```bash
cd hotel-restaurant-minimart
npm install
npm run dev      # Firebase Hosting emulator → http://127.0.0.1:5000
npm run serve    # Alternative static server
```

If port 5000 is busy, the Firebase emulator may use **5002**.

## Sync from production

Refresh local `public/` from live site:

```bash
npm run sync
```

Downloads:

- `index.html`
- `assets/data/*.js`
- All 21 locale JSON files

## Firebase packages

| Package | Purpose |
|---------|---------|
| `firebase-tools@15.x` | CLI — emulators, deploy |
| `serve` | Simple static server |

Upgrade:

```bash
npm install firebase-tools@latest --save-dev
```

## Editing the app

The production app is a **monolithic `index.html`**. Typical workflow:

1. `npm run sync` — get latest production
2. Edit `public/index.html` or locale JSON files
3. Test with `npm run serve`
4. `npm run deploy` — push to Firebase (with credentials)

For large refactors, consider splitting modules in a build step (not currently in repo).

## Localization development

Edit `public/assets/locales/en.json` first, then mirror keys to other locale files.

Test RTL with `ar` or `he` locale.

## Testing checklist

- [ ] First-time setup (`?newsetup=1` in dev only)
- [ ] Each demo role login
- [ ] Restaurant → Kitchen queue update
- [ ] Mini-mart sale cash + room charge
- [ ] Export / import round-trip
- [ ] Dark mode + language switch

## Firebase project access

Deploy requires login:

```bash
firebase login
firebase projects:list
```

Project: `hotel-restaurant-minimart`

## Related

- [Architecture](architecture.md)
- [Deployment](deployment.md)
- [Localization](localization.md)
