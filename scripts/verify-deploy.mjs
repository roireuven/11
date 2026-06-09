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
if (!html.includes("getInvoiceLineItems") || !html.includes("refreshInvoiceQrDisplay") || !html.includes("HRMM-INVOICE-v7")) {
  fail("app missing invoice items table, logo, and QR patch (HRMM-INVOICE-v7)");
}
if (!html.includes("function invoiceT") || !html.includes("refreshOpenInvoiceOverlayI18n")) {
  fail("app missing invoice i18n helpers (HRMM-INVOICE-v7)");
}
if (!html.includes("HRMM-INVOICE-PRINT-v6")) {
  fail("app missing invoice print layout fix");
}
if (!html.includes("hrmmInvoicePrintFrame") || !html.includes("buildInvoicePrintBodyHtml")) {
  fail("app missing iframe invoice print (HRMM-INVOICE-PRINT-v6)");
}
if (!html.includes("HRMM-SHIFTS-v1") || !html.includes("migrateShiftsClosedByDefault")) {
  fail("app missing shifts-closed-by-default patch (HRMM-SHIFTS-v1)");
}
if (!html.includes("HRMM-MOBILE-MENU-v4") || !html.includes("window.closeLangMenu") || !html.includes('id="langMenuBackdrop"')) {
  fail("app missing mobile phone UI patch (HRMM-MOBILE-MENU-v4)");
}
if (!html.includes("HRMM-GUEST-QR-ORDER-v12") || !html.includes("function guestOrderQrBuildUrl") || !html.includes('data-bnav="guestorder-rest"')) {
  fail("app missing guest QR order patch (HRMM-GUEST-QR-ORDER-v12)");
}
if (!html.includes("guestOrderQrSetPickMode") || !html.includes("guestOrderQrTablePick")) {
  fail("app missing restaurant QR table pick mode (HRMM-GUEST-QR-ORDER-v12)");
}
if (!html.includes("guestRestFindTableMergeTarget") || !html.includes("function restTableLabelsMatch")) {
  fail("app missing table QR → restaurant active orders link (HRMM-GUEST-QR-ORDER-v12)");
}
if (!html.includes("HRMM-GUEST-QR-CLOUD-v1") || !html.includes("guestQrCloudStartStaffSync")) {
  fail("app missing guest QR cloud sync (HRMM-GUEST-QR-CLOUD-v1)");
}
if (!html.includes("params.set('propertyNs'") || !html.includes("guestQrCloudPushRestaurantOrder")) {
  fail("app missing guest QR Firestore push (HRMM-GUEST-QR-CLOUD-v1)");
}
const cloudInStyle = html.indexOf("/* HRMM guest QR cloud sync v13 */");
const styleClose = html.indexOf("</style>");
if (cloudInStyle >= 0 && styleClose >= 0 && cloudInStyle < styleClose) {
  fail("guest QR cloud JS must not be inside <style> (breaks fullscreen guest menu)");
}
if (!html.includes("guestRestGetMenuCategories") || !html.includes("nisha1DefaultMenuItems")) {
  fail("app missing guest order menu load helpers (guestRestGetMenuCategories)");
}
if (!html.includes("HRMM-GUEST-QR-REPORTS-v3") || !html.includes("openGuestQrOrdersReport")) {
  fail("app missing guest QR orders report (HRMM-GUEST-QR-REPORTS-v3)");
}
if (!html.includes("HRMM-REST-QR-ORDERS-FLOOR-v1") || !html.includes("restRenderOrderNumFloorHtml")) {
  fail("app missing restaurant QR order numbers floor (HRMM-REST-QR-ORDERS-FLOOR-v1)");
}
if ((html.match(/let restOrderNum = '';/g) || []).length !== 1) {
  fail("duplicate let restOrderNum breaks login JS");
}
if (!html.includes("HRMM-MART-POS-QR-ORDERS-FLOOR-v1") || !html.includes("martSetOrderType")) {
  fail("app missing Mini-Mart + POS QR order numbers floor (HRMM-MART-POS-QR-ORDERS-FLOOR-v1)");
}
if ((html.match(/let martOrderType = 'Room Service';/g) || []).length !== 1) {
  fail("duplicate let martOrderType breaks login JS");
}
if (html.includes("restFocusAllOrderNums=true;restOrderNum='';renderRestaurant()")) {
  fail("unescaped restOrderNum='' in Show all onclick breaks login JS");
}
if (html.includes("martFocusAllOrderNums=true;martOrderNum='';renderMiniMart()")) {
  fail("unescaped martOrderNum='' in Show all onclick breaks login JS");
}
if (!html.includes("HRMM-I18N-FIXES-v2") || !html.includes("function uiT")) {
  fail("app missing core i18n fixes (HRMM-I18N-FIXES-v2)");
}
if (!html.includes("sel.closest('#modalOverlay')")) {
  fail("modal selects must use native dropdown (isLocaleOrNativeSelect fix)");
}
if (!html.includes('id="guestOrderQrOrderNumPick" data-native-select="1"')) {
  fail("guest QR order number select must use native dropdown");
}
if (!html.includes("uiT('guestOrder.qrReportBtn'") || !html.includes("uiT('guestQrReport.titleRest'")) {
  fail("app missing guest order / QR report i18n wiring");
}
if (!html.includes("guestQrBuildChartsHtml") || !html.includes("guest-qr-report-btn")) {
  fail("app missing QR order charts and report toolbar buttons");
}
if (html.includes("openGuestQrOrdersReport('restaurant')")) {
  fail("renderRestaurant QR button has unescaped quotes (breaks login JS)");
}
if (!html.includes("openGuestQrOrdersReport(\\'restaurant\\')")) {
  fail("renderRestaurant QR button missing escaped restaurant onclick");
}
if (!html.includes("HRMM-FULLSCREEN-MODAL-v3") || !html.includes("modal-overlay--fullscreen") || !html.includes("modal--fullscreen")) {
  fail("app missing full-screen modal patch (HRMM-FULLSCREEN-MODAL-v3)");
}
if (!html.includes(".csel-overlay.active { z-index: 10100")) {
  fail("custom select picker must sit above fullscreen modals (z-index 10100)");
}
if (!html.includes("openShellModal(html, { wide: true })") || !html.includes("openShellModal(html);\n  guestOrderQrRefreshPreview()")) {
  fail("QR modals must route through openShellModal/openModal fullscreen helpers");
}
if (!html.includes("guestOrderQrPickOrderNum") || !html.includes("guestOrderQrOrderNumPick")) {
  fail("app missing mini-mart order number QR picker (HRMM-GUEST-QR-ORDER-v8)");
}
if (!html.includes("buildGuestOrderUrl") || !html.includes("guestMartSubmitOrder") || !html.includes("var guestOrderQrStaffCtx")) {
  fail("app missing guest order QR staff helpers");
}
if (!html.includes("HRMM-INVOICE-PAYMENT-QR-ONLY-v1")) {
  fail("app missing invoice payment-QR-only patch (HRMM-INVOICE-PAYMENT-QR-ONLY-v1)");
}
if (html.includes("sInvoiceQrGuestOrderRest") || html.includes("sInvoiceQrGuestOrderMart")) {
  fail("invoice settings must not expose guest order QR toggles (payment QR only on bills)");
}
if (!html.includes("function buildInvoiceGuestOrderQrsHtml(inv) {\n  return '';")) {
  fail("buildInvoiceGuestOrderQrsHtml must be disabled on invoices");
}
if (!html.includes("invoiceModalLogoBrowseChanged") || !html.includes("Browse payment QR")) {
  fail("invoice bill overlay must expose logo and payment QR browse controls");
}
if (!html.includes("HRMM-QR-ORDER-PAY-v1")) {
  fail("app missing QR order pay patch (HRMM-QR-ORDER-PAY-v1)");
}
if (!html.includes("guestQrOpenSlotPayModal") || !html.includes("guestQrPayMartOpenBill")) {
  fail("app missing QR order pay helpers");
}
if (!html.includes("guest-qr-slot-payable")) {
  fail("QR orders report slots must be tappable to pay");
}
if (html.includes("restPayActiveOrdersTotal('Cash')") || html.includes("martPayTotalBar('Cash')")) {
  fail("unescaped pay-total onclick strings break login JS");
}
if (html.includes("guestQrPayMartOpenBill('' + idS + ''")) {
  fail("unescaped guestQrPayMartOpenBill onclick breaks login JS");
}
if (!html.includes("HRMM-BACKUP-COMPLETE-v1") || !html.includes("messages.csv") || !html.includes("onclick=\"exportAllData()\"")) {
  fail("app missing complete backup export/import patch (HRMM-BACKUP-COMPLETE-v1)");
}
if (!html.includes("assembleBackupFromZipEntries") || !html.includes("settings.json")) {
  fail("backup ZIP must include settings.json and CSV fallback import");
}
if (!html.includes("HRMM-SMALL-PHONE-v1") || !html.includes("HRMM small-phone layout")) {
  fail("app missing small-phone layout patch (HRMM-SMALL-PHONE-v1)");
}
const martChunk = html.split("function renderGuestMiniMartOrder()")[1] || "";
if (!martChunk.includes("Search items") || !martChunk.includes("guestRestMobileBarHtml")) {
  fail("app missing complete mini-mart guest order UI");
}
if (html.includes("parseGuestRestaurantOrderParams();") && html.includes("window.tryBootGuestOrderFromUrl = function()") && html.includes("var params = parseGuestRestaurantOrderParams();")) {
  fail("app has stale duplicate guest QR boot block");
}
if (!html.includes('data-bnav="guestorder"')) {
  fail("app missing bottom nav Order QR button for guest restaurant ordering");
}
if (!html.includes('id="guestRestOrderOverlay"') || !html.includes("guestRestSubmitOrder")) {
  fail("app missing guest restaurant order overlay UI");
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
