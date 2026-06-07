#!/usr/bin/env node
/** Verify public/ is ready for Firebase deploy (Windows + Linux). */
import { readFile, readdir, stat } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PUBLIC = join(ROOT, "public");
const INDEX = join(PUBLIC, "index.html");
const DOC = join(PUBLIC, "doc");

function fail(msg) {
  console.error(`verify-deploy: ${msg}`);
  process.exit(1);
}

try {
  await stat(join(DOC, "index.html"));
  await stat(join(DOC, "en", "README.md"));
  await stat(join(DOC, "i18n", "ui.json"));
  await stat(join(DOC, "i18n", "locales.json"));
} catch {
  fail("missing multilingual doc site under public/doc/");
}

let html;
try {
  html = await readFile(INDEX, "utf8");
} catch {
  fail("missing public/index.html");
}

const checks = [
  ['id="topbarDocBtn"', "app missing top bar Documentation button"],
  ['id="topbarSettingsBtn"', "app missing top bar Settings button"],
  ['data-bnav="documentation"', "app missing bottom nav Documentation link"],
  ['data-bnav="settings"', "app missing bottom nav Settings link"],
  ['class="hrmm-doc-nav"', "app missing hamburger menu Documentation link"],
  ['embed=1', "app missing in-app embedded documentation (embed=1)"],
  ["'/doc/?lang='", "app iframe must use absolute /doc/ path (Firebase rewrite bug)"],
  ["renderDocumentation", "app missing documentation page"],
  ['data-page="documentation"', "app missing sidebar Documentation link"],
];

for (const [needle, msg] of checks) {
  if (!html.includes(needle)) fail(msg);
}

if (/\n}\n  var bnavSettings = document\.querySelector\('#bottomNav \[data-bnav="settings"\]'\);/.test(html)) {
  fail("applyRBAC has broken Settings tail (orphaned bnavSettings breaks login)");
}
if (!html.includes("HRMM-TOPBAR-SETTINGS-v3")) {
  fail("app missing fixed Settings patch marker (HRMM-TOPBAR-SETTINGS-v3)");
}
if (!html.includes("getInvoiceLineItems") || !html.includes("refreshInvoiceQrDisplay") || !html.includes("HRMM-INVOICE-v4")) {
  fail("app missing invoice items table, logo, and QR patch (HRMM-INVOICE-v4)");
}
if (!html.includes("HRMM-INVOICE-PRINT-v5")) {
  fail("app missing invoice print layout fix");
}
if (!html.includes("printPostPaymentInvoice") || !html.includes("buildInvoicePrintBodyHtml")) {
  fail("app missing dedicated invoice print window");
}
if (!html.includes("HRMM-SHIFTS-v1") || !html.includes("migrateShiftsClosedByDefault")) {
  fail("app missing shifts-closed-by-default patch (HRMM-SHIFTS-v1)");
}

let docHtml;
try {
  docHtml = await readFile(join(DOC, "index.html"), "utf8");
} catch {
  fail("missing public/doc/index.html");
}
if (!docHtml.includes("basePath: DOC_ROOT + '/' + DOC_LANG + '/'")) {
  fail("doc site must use absolute DOC_ROOT basePath (prevents SPA HTML in docs panel)");
}
if (!docHtml.includes("fixDocAssetUrl")) {
  fail("doc site missing image URL fix plugin");
}

let enGuide;
try {
  enGuide = await readFile(join(DOC, "en", "getting-started.md"), "utf8");
} catch {
  fail("missing public/doc/en/getting-started.md");
}
if (enGuide.includes("/doc/en/assets/")) {
  fail("English docs must use relative assets/ paths (Docsify double-prefix bug)");
}

let esInstall;
try {
  esInstall = await readFile(join(DOC, "es", "installation.md"), "utf8");
} catch {
  fail("missing public/doc/es/installation.md — locale fallback pages required for Firebase");
}
if (esInstall.startsWith("<!DOCTYPE html>")) {
  fail("public/doc/es/installation.md must be markdown, not SPA HTML");
}

const enMd = (await readdir(join(DOC, "en"))).filter((f) => f.endsWith(".md")).length;
if (enMd < 20) fail(`expected 20+ English doc files, found ${enMd}`);

let locales;
try {
  locales = JSON.parse(await readFile(join(DOC, "i18n", "locales.json"), "utf8"));
} catch {
  fail("invalid doc/i18n/locales.json");
}

let localeDirs = 0;
for (const loc of locales) {
  try {
    await stat(join(DOC, loc.code, "README.md"));
    localeDirs++;
  } catch {
    fail(`missing public/doc/${loc.code}/README.md`);
  }
}

console.log("Deploy bundle OK — app + multilingual documentation ready for Firebase Hosting");
console.log(`  App:  ${INDEX}`);
console.log(`  Docs: ${DOC} (${localeDirs} locales, ${enMd} English guides)`);
