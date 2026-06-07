# Installation

## Web application (recommended for front desk)

### Requirements

- Modern browser with JavaScript enabled
- Cookies / site data allowed (required for `localStorage`)
- Internet connection for initial load (app runs offline after first load)

### Install as shortcut (optional)

**Android Chrome:** Menu → **Add to Home screen**

**iOS Safari:** Share → **Add to Home Screen**

**Desktop Chrome/Edge:** Install icon in address bar (if offered) or bookmark the URL.

### URLs

| URL | Notes |
|-----|-------|
| [hotel-restaurant-minimart.firebaseapp.com](https://hotel-restaurant-minimart.firebaseapp.com/) | Primary Firebase Hosting URL |
| [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) | Firebase alternate domain |

## Android application

The Android build uses **SQLite** on device instead of browser storage.

1. Download `app-debug.apk` from [roireuven.github.io/11](https://roireuven.github.io/11/)
2. Enable **Install unknown apps** for your browser or Files app
3. Open the APK and install
4. Launch **Hotel Manager** and complete first-time setup

APK source: [HotelManager-v7.4.1-release.apk](https://github.com/roireuven/HotelManager-v7.4.1-release.apk)

## Local development

For developers mirroring production:

```bash
git clone https://github.com/roireuven/11.git
cd 11/hotel-restaurant-minimart   # when dev folder is merged
npm install
npm run dev    # Firebase Hosting emulator → http://127.0.0.1:5000
# or
npm run serve  # static server → http://localhost:5000
```

See [Development](development.md) for sync, deploy, and Firebase CLI.

## Storage by platform

| Platform | Backend | Persists after close? |
|----------|---------|------------------------|
| Web | Browser `localStorage` | Yes, same browser only |
| Android | SQLite `hotel_manager.db` | Yes, on device |

**Important:** Web data does **not** sync to other browsers or devices automatically. Use **export/import** in Settings to move data.

## Browser privacy modes

Private/incognito windows may clear data when closed. Do not use incognito for production front-desk work.

## Firewall / corporate networks

The app loads fonts from Google Fonts CDN. If blocked, the UI still works but typography may fall back to system fonts.

## Uninstall / remove data

**Web:** Settings → **Factory reset** or **Full wipe and new setup** (see [Backup, restore & data](backup-restore-and-data.md))

**Android:** App settings → Clear storage, or uninstall the app
