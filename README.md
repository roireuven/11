# Hotel Manager — Landing (GitHub Pages)

Static landing page for the Android app.

## Live site

**URL:** [https://roireuven.github.io/11/](https://roireuven.github.io/11/)

### If you see “404 — There isn’t a GitHub Pages site here”

GitHub Pages is not turned on yet, or the wrong **source** is selected. Do **one** of these:

#### Option A — Deploy from branch (simplest)

1. Repo **Settings** → **Pages**
2. **Build and deployment** → **Source**: **Deploy from a branch**
3. **Branch**: `main`, folder **`/ (root)`** → **Save**
4. Wait 1–3 minutes, then open [https://roireuven.github.io/11/](https://roireuven.github.io/11/) again

#### Option B — GitHub Actions (this repo includes a workflow)

1. **Settings** → **Pages** → **Source**: **GitHub Actions** → Save  
2. Push to `main` (or **Actions** → **Deploy GitHub Pages** → **Run workflow**)  
3. **Actions** tab → wait until **Deploy GitHub Pages** is green (approve **github-pages** environment the first time if GitHub asks).  
4. Reload [https://roireuven.github.io/11/](https://roireuven.github.io/11/)

**Easier:** If Actions fails, use **Option A** (branch `main`, folder **`/ (root)`**) — no workflow needed.

## APK download

**Current links** target **v7.4.0** (localization / i18n) and this asset name:

`https://github.com/roireuven/hotel-management-v2/releases/download/v7.4.0/HotelManager-v7.4.0-release.apk`

1. In [Releases](https://github.com/roireuven/hotel-management-v2/releases), create a release with tag **v7.4.0** and upload **`HotelManager-v7.4.0-release.apk`** (exact name). Set it as **Latest** if you want the default to point at this build.
2. The older **v6.8** file remains available for archive downloads if you need it.

**Why not `/releases/latest/download/...`?** It only works when your **Latest** release includes an `.apk` whose filename matches the URL. A tagged link (`.../download/v7.4.0/...`) stays predictable after you create that release and attach the file.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
