#!/usr/bin/env node
/** Build public/ for Firebase deploy — works on Windows without bash. */
import { cp, mkdir, readdir, rm } from "node:fs/promises";
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

runNodeScript("scripts/sync-from-production.mjs");

console.log("Patching mobile top bar...");
runPython("scripts/patch-app-mobile-menu.py");

console.log("Embedding documentation into app...");
runPython("scripts/patch-app-embed-docs.py");

console.log("Copying documentation site to public/doc/...");
await rm(join(PUBLIC, "doc"), { recursive: true, force: true });
await mkdir(join(PUBLIC, "doc"), { recursive: true });
await cp(join(DOC_SRC, "index.html"), join(PUBLIC, "doc", "index.html"));
await cp(join(DOC_SRC, "_sidebar.md"), join(PUBLIC, "doc", "_sidebar.md"));
const mdFiles = (await readdir(DOC_SRC)).filter((f) => f.endsWith(".md"));
for (const f of mdFiles) {
  await cp(join(DOC_SRC, f), join(PUBLIC, "doc", f));
}

const docCount = mdFiles.length + 2;
console.log("Build complete.");
console.log(`  App:  ${join(PUBLIC, "index.html")} (Documentation in Help menu, top bar, bottom nav)`);
console.log(`  Docs: ${join(PUBLIC, "doc")} (${docCount} files at /doc/)`);
console.log("");
console.log("  npm run verify   — check bundle");
console.log("  npm run deploy   — build + verify + upload to Firebase");
