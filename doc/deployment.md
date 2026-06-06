# Deployment

## Firebase Hosting (web)

### Production

| URL | Role |
|-----|------|
| [hotel-restaurant-minimart.firebaseapp.com](https://hotel-restaurant-minimart.firebaseapp.com/) | Primary |
| [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) | Alternate |

**Project ID:** `hotel-restaurant-minimart`

### Hosting configuration

```json
{
  "hosting": {
    "public": "public",
    "rewrites": [{ "source": "**", "destination": "/index.html" }]
  }
}
```

SPA rewrite sends unknown paths to `index.html` (note: requests like `/manifest.json` also resolve to the SPA unless a physical file exists).

### Deploy steps

```bash
cd hotel-restaurant-minimart
npm install
firebase login
npm run deploy
```

Preview channel (7-day URL):

```bash
npm run deploy:preview
```

Requires Firebase project **Editor** or **Firebase Hosting Admin** role.

### Cache headers

- `index.html` — no-cache (users get updates quickly)
- `/assets/**` — 1 hour cache

## GitHub Pages (APK landing)

Separate repo **[roireuven/11](https://github.com/roireuven/11)** hosts the Android APK download page at [roireuven.github.io/11](https://roireuven.github.io/11/).

Not used for the main web PMS app.

## Android APK

Distributed via raw GitHub file:

```
https://raw.githubusercontent.com/roireuven/HotelManager-v7.4.1-release.apk/main/app-debug.apk
```

Build pipeline is outside this documentation repo; APK is a prebuilt artifact.

## Environment checklist

Before go-live:

- [ ] Complete [First-time setup](first-time-setup.md) on production URL
- [ ] Configure [Settings](settings-and-configuration.md)
- [ ] Create staff [Accounts](accounts-and-audit.md)
- [ ] [Export backup](backup-restore-and-data.md)
- [ ] Train staff per [User roles](user-roles-and-permissions.md)

## Related

- [Development](development.md)
- [Architecture](architecture.md)
