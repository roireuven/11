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

1. Merge/push so `.github/workflows/deploy-pages.yml` is on `main`
2. **Settings** → **Pages** → **Source**: **GitHub Actions** (not “Deploy from a branch”)
3. **Actions** tab → run **Deploy GitHub Pages** (or push a commit to trigger it)
4. When the workflow is green, open the site URL again

## APK

Add your signed build as **`app-release.apk`** in this repository root (next to `index.html`). Download buttons on the site link to that file.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
