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

The site links to a **public file in a separate repository** (not a GitHub Release on the main app repo):

`https://raw.githubusercontent.com/roireuven/HotelManager-v7.4.1-release.apk/main/app-debug.apk`

That is the direct **raw** URL for `app-debug.apk` on branch `main` (same file as `github.com/.../raw/main/...`). If the link 404s, the default branch may be `master` — use `.../master/app-debug.apk` in the path.

**Alternative:** create a [Release](https://github.com/roireuven/hotel-management-v2/releases) on the main app repo and point `index.html` at `.../releases/download/TAG/filename.apk` for a cleaner, versioned download URL.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
