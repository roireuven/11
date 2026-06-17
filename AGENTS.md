## Cursor Cloud specific instructions

- This repository hosts a **web-only** sales landing page (`index.html`) on GitHub Pages and a Firebase-hosted SPA (`hotel-restaurant-minimart/` build via `npm run build`).
- Standard project details and deployment options are documented in `README.md`; avoid duplicating them here.
- For local landing preview, serve the repository root with a static server such as `python3 -m http.server 8000` and open `http://localhost:8000`.
- **Firebase web app dev:** run `npm install && npm run build && npm run serve` from repo root, or see `hotel-restaurant-minimart/README.md` if present. Production URL: `https://hotel-restaurant-minimart2-4.web.app/`. Licensed trial: `/paid`.
- **Full product documentation** is in [`doc/`](doc/). Browse on Firebase: [https://hotel-restaurant-minimart2-4.web.app/doc/](https://hotel-restaurant-minimart2-4.web.app/doc/) (stable v2.4). Deploy with `npm run deploy` after `firebase login`.
