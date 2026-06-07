#!/usr/bin/env node
/** Download the live app from Firebase Hosting into public/ (Windows + Linux). */
import { mkdir, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PUBLIC = join(ROOT, "public");
const BASE = "https://hotel-restaurant-minimart.firebaseapp.com";

const LOCALES = [
  "en", "es", "fr", "de", "ja", "ko", "ar", "hi", "th", "vi", "id", "tr", "ru",
  "it", "nl", "pl", "he", "lo", "pt-BR", "zh-Hans", "zh-Hant",
];

async function fetchText(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Failed to fetch ${url}: ${res.status}`);
  return res.text();
}

async function download(url, dest) {
  const text = await fetchText(url);
  await mkdir(dirname(dest), { recursive: true });
  await writeFile(dest, text, "utf8");
}

console.log("Syncing app index.html...");
await download(`${BASE}/`, join(PUBLIC, "index.html"));

console.log("Syncing data assets...");
await download(`${BASE}/assets/data/embedded-sample.js`, join(PUBLIC, "assets/data/embedded-sample.js"));
await download(`${BASE}/assets/data/nisha1-menu-dataset.js`, join(PUBLIC, "assets/data/nisha1-menu-dataset.js"));

console.log(`Syncing ${LOCALES.length} locale files...`);
for (const loc of LOCALES) {
  await download(`${BASE}/assets/locales/${loc}.json`, join(PUBLIC, "assets/locales", `${loc}.json`));
}

console.log("App sync done.");
