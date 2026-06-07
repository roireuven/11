#!/usr/bin/env node
import { spawnSync } from "node:child_process";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

function pythonCmd() {
  for (const cmd of process.platform === "win32" ? ["python", "py", "python3"] : ["python3", "python"]) {
    const r = spawnSync(cmd, ["--version"], { encoding: "utf8", shell: process.platform === "win32" });
    if (r.status === 0) return cmd;
  }
  throw new Error("Python not found.");
}

const py = pythonCmd();
for (const script of ["scripts/patch-app-mobile-menu.py", "scripts/patch-app-embed-docs.py"]) {
  const r = spawnSync(py, [join(ROOT, script)], { stdio: "inherit", cwd: ROOT, shell: process.platform === "win32" });
  if (r.status !== 0) process.exit(r.status ?? 1);
}
