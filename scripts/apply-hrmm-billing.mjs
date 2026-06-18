#!/usr/bin/env node
/** Inject PayPal / pricing from config/hrmm-billing.json into sales landing pages. */
import { readFile, writeFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CONFIG = join(ROOT, "config/hrmm-billing.json");

async function loadBilling() {
  try {
    const raw = await readFile(CONFIG, "utf8");
    const data = JSON.parse(raw);
    return {
      paypalUrl: String(data.paypalUrl || "").trim(),
      licensePriceUsd: Number(data.licensePriceUsd) || 100,
      trialDays: Number(data.trialDays) || 30,
    };
  } catch {
    return { paypalUrl: "", licensePriceUsd: 100, trialDays: 30 };
  }
}

function patchPaypalLine(html, paypalUrl) {
  const escaped = paypalUrl.replace(/\\/g, "\\\\").replace(/'/g, "\\'");
  return html.replace(/paypal:\s*'[^']*'/, `paypal: '${escaped}'`);
}

async function patchFile(rel) {
  const path = join(ROOT, rel);
  try {
    let html = await readFile(path, "utf8");
    html = patchPaypalLine(html, billing.paypalUrl);
    await writeFile(path, html, "utf8");
  } catch {
    /* optional during partial builds */
  }
}

const billing = await loadBilling();
await patchFile("index.html");
await patchFile("public/sales.html");

if (billing.paypalUrl) {
  console.log(`Billing config applied (PayPal: ${billing.paypalUrl})`);
} else {
  console.log("Billing config applied (PayPal URL empty — edit config/hrmm-billing.json)");
}
