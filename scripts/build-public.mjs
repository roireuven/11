#!/usr/bin/env node
/** Build public/ for Firebase deploy — works on Windows without bash. */
import { cp, mkdir, readdir, rm, stat, readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PUBLIC = join(ROOT, "public");
const DOC_SRC = join(ROOT, "doc");

function pythonCmd() {
  for (const cmd of process.platform === "win32" ? ["python", "py", "python3"] : ["python3", "python"]) {
    const r = spawnSync(cmd, ["--version"], { encoding: "utf8", shell: process.platform === "win32" });
    if (r.status === 0) return cmd;
  }
  throw new Error("Python not found. Install Python 3 from https://python.org/downloads/");
}

function runNodeScript(rel) {
  const r = spawnSync(process.execPath, [join(ROOT, rel)], { stdio: "inherit", cwd: ROOT });
  if (r.status !== 0) process.exit(r.status ?? 1);
}

function runPython(rel) {
  const py = pythonCmd();
  const r = spawnSync(py, [join(ROOT, rel)], { stdio: "inherit", cwd: ROOT, shell: process.platform === "win32" });
  if (r.status !== 0) process.exit(r.status ?? 1);
}

async function copyDir(src, dest) {
  await mkdir(dest, { recursive: true });
  for (const name of await readdir(src)) {
    const s = join(src, name);
    const d = join(dest, name);
    if ((await stat(s)).isDirectory()) await copyDir(s, d);
    else await cp(s, d);
  }
}

runNodeScript("scripts/sync-from-production.mjs");

console.log("Patching mobile top bar...");
runPython("scripts/patch-app-mobile-menu.py");

console.log("Embedding documentation into app...");
runPython("scripts/patch-app-embed-docs.py");

console.log("Patching sell flows, audit log, POS nav...");
runPython("scripts/patch-app-features.py");

console.log("Adding Settings shortcut to top bar...");
runPython("scripts/patch-app-topbar-settings.py");

console.log("Patching invoice items table and logo...");
runPython("scripts/patch-app-invoice.py");

console.log("Patching shifts to start closed by default...");
runPython("scripts/patch-app-shifts.py");

console.log("Adding guest QR restaurant self-order...");
runPython("scripts/patch-app-guest-qr-order.py");

console.log("Adding guest QR order reports...");
runPython("scripts/patch-app-guest-qr-reports.py");

console.log("Adding guest QR cloud sync (Firestore)...");
runPython("scripts/patch-app-guest-qr-cloud.py");

console.log("Adding restaurant QR order numbers floor...");
runPython("scripts/patch-app-rest-qr-orders-floor.py");

console.log("Adding Mini-Mart + POS QR order numbers floor...");
runPython("scripts/patch-app-mart-pos-qr-orders-floor.py");

console.log("Invoice bills: bank payment QR + logo only...");
runPython("scripts/patch-app-invoice-payment-qr-only.py");

console.log("Restricting invoice edits to Admin...");
runPython("scripts/patch-app-invoice-admin-edit.py");

console.log("Adding pay for QR scan orders...");
runPython("scripts/patch-app-qr-order-pay.py");

console.log("Completing backup export/import (all CSV + JSON)...");
runPython("scripts/patch-app-backup-complete.py");

console.log("Patching full-screen modals...");
runPython("scripts/patch-app-shell-modal.py");

console.log("Fixing small-phone layout (scroll, buttons, safe areas)...");
runPython("scripts/patch-app-mobile-small-screens.py");

console.log("Login/setup language dropdown (21 locales)...");
runPython("scripts/patch-app-login-lang-header.py");

console.log("Wiring setup screen i18n...");
runPython("scripts/patch-app-setup-i18n.py");

console.log("Adding setup business/admin form fields...");
runPython("scripts/patch-app-setup-form.py");

console.log("Auth screens RTL + small-phone layout...");
runPython("scripts/patch-app-auth-rtl-mobile.py");

console.log("Syncing setup/login locale across auth screens...");
runPython("scripts/patch-app-auth-locale-sync.py");

console.log("Applying core i18n fixes (uiT, bottom nav, embedded locales)...");
runPython("scripts/patch-app-i18n-fixes.py");

console.log("Generating guest order locale keys...");
runPython("scripts/generate-guest-order-locale-keys.py");

console.log("Adding invoice i18n keys to app locale files...");
runPython("scripts/patch-locale-invoice-keys.py");

console.log("Adding documentation keys to app locale files...");
runPython("scripts/patch-locale-doc-keys.py");

console.log("Adding guest order / QR report keys to app locale files...");
runPython("scripts/patch-locale-guest-order-keys.py");

console.log("Adding restaurant QR order floor keys to app locale files...");
runPython("scripts/patch-locale-rest-qr-floor-keys.py");

console.log("Adding login/setup i18n keys to app locale files...");
runPython("scripts/patch-locale-login-keys.py");

console.log("Adding setup screen i18n keys to app locale files...");
runPython("scripts/patch-locale-setup-keys.py");

console.log("Adding setup form + gap i18n keys to app locale files...");
runPython("scripts/patch-locale-setup-form-keys.py");
runPython("scripts/patch-locale-gap-keys.py");

console.log("Generating multilingual documentation (21 locales)...");
runPython("scripts/generate-doc-locales.py");

console.log("Copying documentation site to public/doc/...");
await rm(join(PUBLIC, "doc"), { recursive: true, force: true });
await mkdir(join(PUBLIC, "doc"), { recursive: true });
await cp(join(DOC_SRC, "index.html"), join(PUBLIC, "doc", "index.html"));
await copyDir(join(DOC_SRC, "i18n"), join(PUBLIC, "doc", "i18n"));
await copyDir(join(DOC_SRC, "en"), join(PUBLIC, "doc", "en"));
try {
  await stat(join(DOC_SRC, "en", "assets"));
  await copyDir(join(DOC_SRC, "en", "assets"), join(PUBLIC, "doc", "en", "assets"));
} catch {
  console.warn("  warn: no doc/en/assets/ — run npm run capture:screenshots for screenshots");
}

const locales = JSON.parse(await readFile(join(DOC_SRC, "i18n", "locales.json"), "utf8"));
for (const loc of locales) {
  if (loc.code === "en") continue;
  const src = join(DOC_SRC, loc.code);
  try {
    await stat(src);
    await copyDir(src, join(PUBLIC, "doc", loc.code));
  } catch {
    console.warn(`  warn: missing doc locale folder ${loc.code}`);
  }
}

const enMd = (await readdir(join(PUBLIC, "doc", "en"))).filter((f) => f.endsWith(".md")).length;
console.log("Build complete.");
console.log(`  App:  ${join(PUBLIC, "index.html")} (Documentation in Help menu, top bar, bottom nav)`);
console.log(`  Docs: ${join(PUBLIC, "doc")} (${locales.length} locales, ${enMd} English guides)`);
console.log("");
console.log("  npm run verify   — check bundle");
console.log("  npm run deploy   — build + verify + upload to Firebase");
