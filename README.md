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

The site’s **Download** buttons point to release **v8.4** on the main app repo:

`https://github.com/roireuven/hotel-management-v2/releases/download/v8.4/HotelManager-v8.4-release.apk`

When you ship a **new** Android build from current sources: on **hotel-management-v2**, create a GitHub Release tagged **`v8.4`** (or bump the tag in `index.html`) and attach a signed APK named **`HotelManager-v8.4-release.apk`** so the link above works. Mark that release as **Latest** if you want it to be the default download.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
