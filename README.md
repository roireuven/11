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

## APK download (v9.0)

The landing page promotes **v9.0** on the right-hand **New release** card and in every **Download** button. The file must exist on GitHub:

`https://github.com/roireuven/hotel-management-v2/releases/download/v9.0/HotelManager-v9.0-release.apk`

### Publish this version (upload the new APK)

On repo **roireuven/hotel-management-v2**:

1. Build a signed release APK from your current sources and name it **`HotelManager-v9.0-release.apk`** (exact name).
2. **Releases** → **Draft a new release** → choose tag **`v9.0`** (create new tag on your default branch).
3. Title e.g. `Hotel Manager v9.0`, attach **`HotelManager-v9.0-release.apk`**, publish.
4. Mark **v9.0** as **Set as the latest release** if it should be the default on GitHub.

Or with [GitHub CLI](https://cli.github.com/): `gh release create v9.0 HotelManager-v9.0-release.apk --title "Hotel Manager v9.0" --generate-notes`

To ship a different version later, change **`v9.0`** and **`HotelManager-v9.0-release.apk`** everywhere in `index.html` (search/replace) to match the new tag and filename.

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
