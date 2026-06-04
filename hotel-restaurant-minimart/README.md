# Hotel Restaurant Mini-Mart — Development

Local development environment for the web app hosted at:

**Production:** [https://hotel-restaurant-minimart.firebaseapp.com/](https://hotel-restaurant-minimart.firebaseapp.com/)

Firebase project: `hotel-restaurant-minimart`

Requires **firebase-tools 15.19.1+** (Firebase CLI; installed via `npm install`).

## Quick start

```bash
cd hotel-restaurant-minimart
npm install
npm run dev
```

Open **http://127.0.0.1:5000** (Firebase Hosting emulator).

Alternative without Firebase CLI:

```bash
npm run serve
```

Open **http://localhost:5000**.

## First-time setup in the app

1. Open the app locally.
2. Use **first-time setup** (`?newsetup=1` in the URL) to create your admin email and password, **or**
3. Sign in with demo credentials:

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@hotel.com | 1234 |
| Manager | mike@hotel.com | 1234 |
| Reception | jane@hotel.com | 1234 |
| Housekeeper | tom@hotel.com | 1234 |
| Restaurant | restaurant@hotel.com | 1234 |
| Kitchen | kitchen@hotel.com | 1234 |

**Note:** Data is stored in **browser localStorage** per browser. Local dev data is separate from production unless you export/import via Settings.

## Sync from production

To refresh `public/` from the live Firebase site:

```bash
npm run sync
```

## Deploy to Firebase

Requires Firebase login and project access:

```bash
firebase login
npm run deploy
```

Preview channel (7-day URL):

```bash
npm run deploy:preview
```

## Project layout

| Path | Purpose |
|------|---------|
| `public/index.html` | Full SPA (~1.1 MB single file) |
| `public/assets/locales/*.json` | i18n strings (22 languages) |
| `public/assets/data/*.js` | Sample menu datasets |
| `firebase.json` | Hosting config (SPA rewrites) |
| `.firebaserc` | Firebase project ID |
| `scripts/sync-from-production.sh` | Pull latest from production |

## Firebase config (production)

```json
{
  "projectId": "hotel-restaurant-minimart",
  "authDomain": "hotel-restaurant-minimart.firebaseapp.com",
  "storageBucket": "hotel-restaurant-minimart.firebasestorage.app"
}
```

The app runs client-side with localStorage; Firebase Hosting serves static files only.
