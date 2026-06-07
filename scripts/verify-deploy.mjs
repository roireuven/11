#!/usr/bin/env node
/** Verify public/ is ready for Firebase deploy (Windows + Linux). */
import { readFile } from "node:fs/promises";
import { readdir } from "node:fs/promises";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const PUBLIC = join(ROOT, "public");
const INDEX = join(PUBLIC, "index.html");

function fail(msg) {
  console.error(`verify-deploy: ${msg}`);
  process.exit(1);
}

try {
  await readFile(join(PUBLIC, "doc", "index.html"));
} catch {
  fail("missing public/doc/index.html");
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
  ["renderDocumentation", "app missing documentation page"],
  ['data-page="documentation"', "app missing sidebar Documentation link"],
];

for (const [needle, msg] of checks) {
  if (!html.includes(needle)) fail(msg);
}

const docFiles = (await readdir(join(PUBLIC, "doc"))).filter((f) => f.endsWith(".md"));
if (docFiles.length < 20) fail(`expected 20+ doc files, found ${docFiles.length}`);

console.log("Deploy bundle OK — app + documentation ready for Firebase Hosting");
console.log(`  App:  ${INDEX}`);
console.log(`  Docs: ${join(PUBLIC, "doc")} (${docFiles.length} guides)`);
