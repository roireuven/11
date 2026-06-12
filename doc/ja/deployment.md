# Deployment

## Firebase Hosting (web app + docs)

### Production URLs

| URL | Role |
|-----|------|
| [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) | **Stable v2.4** — **production** (default deploy target) |
| [hotel-restaurant-minimart2-4.firebaseapp.com](https://hotel-restaurant-minimart2-4.firebaseapp.com/) | Stable v2.4 (alternate domain) |
| [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) | **Stable v2.3** — legacy snapshot (not updated by default) |
| [hotel-restaurant-minimart2-3.firebaseapp.com](https://hotel-restaurant-minimart2-3.firebaseapp.com/) | Stable v2.3 (alternate domain) |
| [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) | **Development** — manual deploy only (`npm run deploy:dev`) |
| [hotel-restaurant-minimart.firebaseapp.com](https://hotel-restaurant-minimart.firebaseapp.com/) | Development (alternate domain) |

Documentation is embedded in the app on every site (`/doc/`).

**Project ID:** `hotel-restaurant-minimart` (all hosting sites live in this Firebase project)

### Which deploy command?

| Command | Deploys to | When to use |
|---------|------------|-------------|
| `npm run deploy` | **Stable v2.4 only** | **Default** — publish staff-facing production |
| `npm run deploy:2.4` | Same as `npm run deploy` | Explicit alias |
| `npm run deploy:2.3` | Stable v2.3 site only | Legacy pin (manual) |
| `npm run deploy:dev` | Development site + Firestore rules | Internal testing (manual) |
| `npm run deploy:all` | Development + both stable sites + Firestore | Full refresh (manual, rare) |

**Policy:** routine releases go to **v2.4 only**. Do not deploy to development or v2.3 unless you intentionally need those URLs updated.

Stable site URLs use hyphens (Firebase naming): `hotel-restaurant-minimart2-3.web.app`, `hotel-restaurant-minimart2-4.web.app`.

### What gets deployed

The deploy bundle (`public/`) contains:

| Path | Source |
|------|--------|
| `/` (app) | Synced from live Firebase, then patched for i18n and features |
| `/doc/` | Docsify site from repo `doc/` folder (30 guides, 21 locales) |

The build patches `public/index.html` to **embed documentation inside the app**:

- Top bar **Documentation** button
- Sidebar **Help → Documentation**
- Bottom nav **Docs** button
- Embedded iframe page at `#page-documentation` → `/doc/#/README`

Build command merges both:

```bash
npm run build    # → public/index.html + public/doc/*
npm run deploy   # stable v2.4 (production)
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
npm run deploy
```

Requires Firebase project **Editor** or **Firebase Hosting Admin** role.

### Local preview

```bash
npm run serve
```

- App: [http://127.0.0.1:5000/](http://127.0.0.1:5000/)
- Docs: [http://127.0.0.1:5000/doc/](http://127.0.0.1:5000/doc/)
- What's new: [http://127.0.0.1:5000/doc/#/whats-new-v2](http://127.0.0.1:5000/doc/#/whats-new-v2)

### Hosting configuration

Two stable targets plus development share the same `public/` folder:

```json
{
  "hosting": [
    { "target": "production", "public": "public" },
    { "target": "stable23", "public": "public" },
    { "target": "stable24", "public": "public" }
  ]
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
- [ ] Deploy: `npm run deploy` (stable v2.4)
- [ ] Train staff per [User roles](user-roles-and-permissions.md) and [What's new](whats-new-v2.md)

## Related

- [Development](development.md)
- [Architecture](architecture.md)
- [What's new in v2.3 / v2.4](whats-new-v2.md)
