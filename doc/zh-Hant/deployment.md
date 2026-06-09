# Deployment

## Firebase Hosting (web app + docs)

### Production URLs

| URL | Role |
|-----|------|
| [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) | **Development** — latest build from `npm run deploy` |
| [hotel-restaurant-minimart.firebaseapp.com](https://hotel-restaurant-minimart.firebaseapp.com/) | Same as development (alternate domain) |
| [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) | **Stable v2.3** — for daily use; update with `npm run deploy:2.3` |
| [hotel-restaurant-minimart2-3.firebaseapp.com](https://hotel-restaurant-minimart2-3.firebaseapp.com/) | Stable v2.3 (alternate domain) |

Documentation is embedded in the app on every site (`/doc/`).

**Project ID:** `hotel-restaurant-minimart` (both hosting sites live in this Firebase project)

### Which deploy command?

| Command | Deploys to | When to use |
|---------|------------|-------------|
| `npm run deploy` | Development site + Firestore rules | Day-to-day development |
| `npm run deploy:2.3` | Stable v2.3 site only | Publish a tested snapshot for staff |
| `npm run deploy:all` | Both sites + Firestore rules | Refresh everything at once |

### What gets deployed

The deploy bundle (`public/`) contains:

| Path | Source |
|------|--------|
| `/` (app) | Synced from live Firebase, then patched for in-app docs |
| `/doc/` | Docsify site from repo `doc/` folder (26 guides) |

The build patches `public/index.html` to **embed documentation inside the app**:

- Top bar **Documentation** button
- Sidebar **Help → Documentation**
- Bottom nav **Docs** button
- Embedded iframe page at `#page-documentation` → `/doc/#/README`

Build command merges both:

```bash
npm run build       # → public/index.html + public/doc/*
npm run deploy      # development site + Firestore rules
npm run deploy:2.3  # stable v2.3 site only
```

### Deploy steps

From repository root ([roireuven/11](https://github.com/roireuven/11)):

```bash
npm install
firebase login
npm run deploy
```

**Windows (PowerShell):**

```powershell
cd C:\Users\roire\11
.\firebase-fix.bat deploy
```

Or step by step: `npx firebase login` then `npm run deploy`. Sign in as the Google account that owns project **hotel-restaurant-minimart**.

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
