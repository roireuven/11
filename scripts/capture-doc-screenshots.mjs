#!/usr/bin/env node
/** Capture real app screenshots from production for documentation. */
import { chromium } from "playwright";
import { mkdir, rm } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const OUT = join(ROOT, "doc/en/assets/screenshots");
const BASE = "https://hotel-restaurant-minimart.firebaseapp.com/";

async function dismissOverlays(page) {
  await page.evaluate(() => {
    ["setupOverlay", "loginOverlay"].forEach((id) => {
      const el = document.getElementById(id);
      if (el) el.classList.add("hidden");
    });
  });
  await page.waitForTimeout(500);
}

async function login(page) {
  await page.goto(BASE, { waitUntil: "domcontentloaded", timeout: 90000 });
  await page.waitForTimeout(1500);
  await page.evaluate(() => {
    const s = document.getElementById("setupOverlay");
    const l = document.getElementById("loginOverlay");
    if (s && !s.classList.contains("hidden")) {
      const btn = document.getElementById("linkBackToSignIn");
      if (btn) btn.click();
    }
  });
  await page.waitForTimeout(800);
  const email = page.locator("#loginEmail").first();
  if (!(await email.isVisible({ timeout: 8000 }).catch(() => false))) {
    await dismissOverlays(page);
    return;
  }
  await page.locator(".demo-cred-row, [data-demo-email], .demo-row").first().click({ timeout: 3000 }).catch(async () => {
    await email.fill("admin@hotel.com");
    await page.locator("#loginPassword").fill("1234");
  });
  await page.locator("#btnLogin").click();
  await page.waitForTimeout(3000);
  await dismissOverlays(page);
  await page.waitForSelector("#pageTitle, #mainApp", { timeout: 15000 }).catch(() => {});
  await page.waitForTimeout(1000);
}

async function openSidebar(page) {
  await dismissOverlays(page);
  await page.locator("#menuToggle").click({ force: true, timeout: 5000 }).catch(() => {});
  await page.waitForTimeout(500);
}

async function goPage(page, pageId) {
  await page.evaluate((id) => {
    if (typeof navToPage === "function") navToPage(id);
  }, pageId);
  await page.waitForTimeout(1500);
  const title = await page.locator("#pageTitle").textContent().catch(() => "");
  if (!title || title.trim().length === 0) {
    await openSidebar(page);
    await page.locator(`a[data-page="${pageId}"]`).first().click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(1500);
  }
}

async function shot(page, file, fn) {
  await fn();
  await page.screenshot({ path: join(OUT, file), fullPage: false });
  console.log("OK", file);
}

async function main() {
  await mkdir(OUT, { recursive: true });
  for (const f of ["dashboard.png", "bookings.png", "help-menu.png", "documentation-embed.png",
    "first-time-setup.png", "minimart-pos.png", "restaurant.png", "settings.png"]) {
    await rm(join(OUT, f), { force: true });
  }

  const browser = await chromium.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox", "--window-size=1280,800"],
  });
  const page = await (await browser.newContext({ viewport: { width: 1280, height: 800 } })).newPage();

  await shot(page, "01-login.png", async () => {
    await page.goto(BASE, { waitUntil: "domcontentloaded" });
    await page.waitForTimeout(2000);
  });

  await login(page);

  await shot(page, "02-dashboard.png", async () => { await goPage(page, "dashboard"); });
  await shot(page, "03-help-menu.png", async () => {
    await goPage(page, "dashboard");
    await openSidebar(page);
    await page.waitForTimeout(600);
  });
  await shot(page, "04-documentation-embed.png", async () => { await goPage(page, "documentation"); });
  await shot(page, "05-rooms.png", async () => { await goPage(page, "rooms"); });
  await shot(page, "06-bookings.png", async () => { await goPage(page, "bookings"); });
  await shot(page, "07-housekeeping.png", async () => { await goPage(page, "housekeeping"); });
  await shot(page, "08-restaurant.png", async () => { await goPage(page, "restaurant"); });
  await shot(page, "09-minimart-pos.png", async () => { await goPage(page, "minimart"); });
  await shot(page, "10-invoices.png", async () => { await goPage(page, "invoices"); });
  await shot(page, "11-settings.png", async () => { await goPage(page, "settings"); });
  await shot(page, "12-reports.png", async () => { await goPage(page, "reports"); });
  await shot(page, "13-accounts.png", async () => { await goPage(page, "accounts"); });
  await shot(page, "14-guest-portal.png", async () => { await goPage(page, "guestportal"); });

  await page.setViewportSize({ width: 390, height: 844 });
  await goPage(page, "dashboard");
  await page.waitForTimeout(800);
  await page.screenshot({ path: join(OUT, "15-mobile-bottom-nav.png") });
  console.log("OK 15-mobile-bottom-nav.png");

  await browser.close();
  console.log("Screenshots saved to", OUT);
}

main().catch((e) => { console.error(e); process.exit(1); });
