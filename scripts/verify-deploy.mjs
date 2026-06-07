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
  ['data-bnav="documentation"', "app missing bottom nav Documentation link"],
  ['class="hrmm-doc-nav"', "app missing hamburger menu Documentation link"],
  ["getDocUiLocale", "app missing locale-aware documentation embed"],
  ["renderDocumentation", "app missing documentation page"],
  ['data-page="documentation"', "app missing sidebar Documentation link"],
];

for (const [needle, msg] of checks) {
  if (!html.includes(needle)) fail(msg);
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
