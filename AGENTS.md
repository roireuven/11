## Cursor Cloud specific instructions

- This repository is a static GitHub Pages landing page for the Hotel Manager Android APK. There is no backend, database, package manager manifest, or local build step.
- Standard project details and deployment options are documented in `README.md`; avoid duplicating them here.
- For local development preview, serve the repository root with a static server such as `python3 -m http.server 8000` and open `http://localhost:8000`.
- The "Download APK" flow depends on an external public GitHub raw URL in the separate `roireuven/HotelManager-v7.4.1-release.apk` repository; this repository does not contain the Android app source or APK build pipeline.
- A useful sanity check is to request the local page and verify the APK URL resolves, since CDN assets and the download target are remote dependencies.
