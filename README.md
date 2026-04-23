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

## APK download (v6.9 — *Hotel Manager v6.9 — Reorder from Past Orders*)

Every **Download** button points at the **latest** release asset named:

**`HotelManager-v6.9-release.apk`**

URL pattern:

`https://github.com/roireuven/hotel-management-v2/releases/latest/download/HotelManager-v6.9-release.apk`

### Publish this build from your *current* code

1. Build a signed (or release) `.apk` from the **commit you want to ship** (e.g. current `master` with latest `docs/` and locales). Run `node docs/scripts/sync-embedded-locales.cjs` in **hotel-management-v2** before building if the app bundles `docs/index.html`.
2. Name the file **`HotelManager-v6.9-release.apk`**.
3. On [Releases](https://github.com/roireuven/hotel-management-v2/releases) → **Draft a new release**:
   - Tag: **`v6.9`**
   - Title: **Hotel Manager v6.9 — Reorder from Past Orders**
   - Upload **`HotelManager-v6.9-release.apk`**
4. Check **Set as the latest release** so `/latest/download/...` matches the landing page.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
