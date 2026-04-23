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

**Download buttons** use a **pinned** link to the v6.8 asset (reliable 404 fix):

`https://github.com/roireuven/hotel-management-v2/releases/download/v6.8/HotelManager-v2.0-release.apk`

**Why not `/releases/latest/download/...`?** If GitHub’s **Latest** release is empty, mistagged, or the asset name does not match, that URL **404s**. Your repo’s **Latest** was a tag like `v6,9` with **no `.apk` uploaded** — so “direct latest” failed.

**Why not `HotelManager-v6.9-release.apk`?** That file is **not** on [Releases](https://github.com/roireuven/hotel-management-v2/releases) until you build it and upload it. Until then, links to it return **404**.

### When you publish v6.9

1. Build from your current sources; optionally name the output **`HotelManager-v6.9-release.apk`**.
2. Create a release with tag **v6.9**, attach that file, and set it as **Latest** (or edit `index.html` to use a tagged URL and matching filename).
3. Update `index.html` so every `href` + `download="..."` point at the new asset, then push this repo so Pages updates.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
