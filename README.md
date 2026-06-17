# Integrated Business Solutions — Landing (GitHub Pages)

Static sales landing page for the **web suite** (hotel, restaurant, mini-mart, car rental). No mobile app download — web only.

## Firebase addresses (production v2.4)

| Purpose | URL |
|--------|-----|
| **30-day trial & licensed app** | [https://hotel-restaurant-minimart2-4.web.app/paid](https://hotel-restaurant-minimart2-4.web.app/paid) |
| **Free web app** (no license gate) | [https://hotel-restaurant-minimart2-4.web.app/](https://hotel-restaurant-minimart2-4.web.app/) |
| **Sales / pricing landing** | [https://hotel-restaurant-minimart2-4.web.app/sales](https://hotel-restaurant-minimart2-4.web.app/sales) |
| **Documentation** (21 languages) | [https://hotel-restaurant-minimart2-4.web.app/doc/](https://hotel-restaurant-minimart2-4.web.app/doc/) |
| **Alternate domain** (same v2.4) | [https://hotel-restaurant-minimart2-4.firebaseapp.com/](https://hotel-restaurant-minimart2-4.firebaseapp.com/) |
| **Development** (manual deploy) | [https://hotel-restaurant-minimart.firebaseapp.com/](https://hotel-restaurant-minimart.firebaseapp.com/) |
| **Legacy v2.3 snapshot** | [https://hotel-restaurant-minimart2-3.web.app/](https://hotel-restaurant-minimart2-3.web.app/) |

GitHub Pages mirror of the sales landing: [https://roireuven.github.io/11/](https://roireuven.github.io/11/)

## Documentation

Full documentation for **HotelRestaurantMini-MartManagement** (hotel, restaurant, mini-mart, vehicle rental web app):

| Format | URL |
|--------|-----|
| **Docs site (Firebase v2.4)** | [https://hotel-restaurant-minimart2-4.web.app/doc/](https://hotel-restaurant-minimart2-4.web.app/doc/) |
| **Docs site (GitHub Pages)** | [https://roireuven.github.io/11/doc/](https://roireuven.github.io/11/doc/) |
| **Markdown source** | [doc/README.md](doc/README.md) |

Deploy **app + documentation** to Firebase from repo root:

```bash
npm install
firebase login
npm run deploy        # stable v2.4 only (default — staff production URL)
npm run deploy:2.4    # same as npm run deploy
npm run deploy:2.3    # legacy v2.3 only (manual)
npm run deploy:dev    # development site + Firestore (manual)
npm run deploy:all    # every hosting target + Firestore (manual)
```

This builds `public/` with the app (Documentation button in top bar), embeds docs in the app, and uploads `/doc/` (30 guides, 21 locales). See [What's new in v2.3 / v2.4](doc/en/whats-new-v2.md). CI: add `FIREBASE_TOKEN` secret and push to `main`, or run **Actions → Deploy Firebase Hosting → Run workflow**.

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

## Files

| File | Purpose |
|------|--------|
| `index.html` | Landing page (Tailwind + Font Awesome CDN) |
