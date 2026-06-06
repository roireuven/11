# Deployment

## Firebase Hosting (web app + docs)

### Production URLs

| URL | Content |
|-----|---------|
| [hotel-restaurant-minimart.firebaseapp.com](https://hotel-restaurant-minimart.firebaseapp.com/) | Main app (PMS) |
| [hotel-restaurant-minimart.firebaseapp.com/doc/](https://hotel-restaurant-minimart.firebaseapp.com/doc/) | **Documentation site** |
| [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) | Alternate domain (same content) |

**Project ID:** `hotel-restaurant-minimart`

### What gets deployed

The deploy bundle (`public/`) contains:

| Path | Source |
|------|--------|
| `/` (app) | Synced from live Firebase (`scripts/sync-from-production.sh`) |
| `/doc/` | Docsify site from repo `doc/` folder |

Build command merges both:

```bash
npm run build    # → public/index.html + public/doc/*
npm run deploy   # build + firebase deploy --only hosting
```

### Deploy steps

From repository root ([roireuven/11](https://github.com/roireuven/11)):

```bash
npm install
firebase login
npm run deploy
```

Requires Firebase project **Editor** or **Firebase Hosting Admin** role.

### Local preview

```bash
npm run serve
```

- App: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Docs: [http://127.0.0.1:5000/doc/](http://127.0.0.1:5000/doc/)

### Hosting configuration

```json
{
  "hosting": {
    "public": "public",
    "rewrites": [{ "source": "**", "destination": "/index.html" }]
  }
}
```

Static files under `/doc/` and `/assets/` are served directly; the catch-all rewrite applies to the main SPA only when no file matches.

### Cache headers

- `/index.html` — no-cache
- `/doc/**` and `/assets/**` — 1 hour cache

## GitHub Pages

| URL | Content |
|-----|---------|
| [roireuven.github.io/11](https://roireuven.github.io/11/) | APK download landing |
| [roireuven.github.io/11/doc](https://roireuven.github.io/11/doc/) | Docs mirror (same markdown + Docsify) |

GitHub Pages deploys via `.github/workflows/deploy-pages.yml` on push to `main`.

## Android APK

```
https://raw.githubusercontent.com/roireuven/HotelManager-v7.4.1-release.apk/main/app-debug.apk
```

Linked from the GitHub Pages landing page.

## Go-live checklist

- [ ] Complete [First-time setup](first-time-setup.md)
- [ ] Configure [Settings](settings-and-configuration.md)
- [ ] Create staff [Accounts](accounts-and-audit.md)
- [ ] [Export backup](backup-restore-and-data.md)
- [ ] Deploy docs: `npm run deploy`
- [ ] Train staff per [User roles](user-roles-and-permissions.md)

## Related

- [Development](development.md)
- [Architecture](architecture.md)
