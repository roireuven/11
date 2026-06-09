# Guest QR orders

Let customers **self-order** from the restaurant or mini-mart by scanning a QR code on their phone — no login required. Staff assign either an **order number (1–60)** or a **restaurant table** — you choose which mode fits your floor.

**Paths:**

- Mobile bottom nav → **Restaurant QR** or **Mini-Mart QR**
- Restaurant → **QR Orders Report** (New Order card and Active Orders header)
- Mini-Mart → **QR Orders Report** (New Order card and Active Orders header)

---

## How it works

```
Staff picks order #1–60 → QR generated → Guest scans → Self-order screen → Kitchen / shop queue
```

| Step | Who | Action |
|------|-----|--------|
| 1 | Staff | Open QR modal, choose **Restaurant** or **Mini-Mart**, then pick **Order number** (1–60) or **Table** (restaurant only) |
| 2 | Staff | Print or display QR (or copy link / open preview) |
| 3 | Guest | Scan QR with phone camera → opens guest order screen |
| 4 | Guest | Browse menu or store items, add to cart, submit |
| 5 | Staff | Order appears on the **table active orders** (table QR) or in the queue tagged with that **order number** |

**Table QR:** guest items are added to that table’s active bill in Restaurant → Table view (floor tile, active orders list, and open-bill modal). Multiple guest submissions merge into the same open kitchen order when the table already has one in progress.

**Order number QR:** numbers **1–60** replace room/guest context. Each slot can hold one active QR order at a time (see **QR Orders Report** board).

**Cloud sync (v2.2+):** New QR links include a `propertyNs` key. When a guest orders from their **phone**, the order is saved to **Firestore** and staff devices **pull it automatically** into Restaurant / Mini-Mart (active orders, QR report, and table floor). Regenerate QR codes after updating — old links without `propertyNs` cannot sync from guest phones.

---

## Staff: Restaurant QR modal

**Open:** Bottom nav → **Restaurant QR** (or **Mini-Mart QR** for shop).

The QR screen opens **full screen** with:

| Control | Purpose |
|---------|---------|
| **Restaurant QR / Mini-Mart QR** | Switch department |
| **Order number / Table** | Restaurant: toggle pick mode, then select **1–60** or a **table** from your floor |
| **Order number** (mini-mart) | Pick slot **1–60** (required before QR generates) |
| QR preview | Scannable code once a number is selected |
| **Order link** | Read-only URL for sharing |
| **Open order screen** | Preview guest view on this device |
| **Copy link** | Copy URL to clipboard |

**Tip:** After selecting an order number, the QR image and link update immediately. Caption shows *Scan to order*.

### Invoice QR codes (optional)

On **Invoices**, printed/emailed QR codes can link to guest ordering when enabled in **Settings**:

| Setting | Effect |
|---------|--------|
| Include restaurant guest order on invoice QR | Restaurant self-order link on invoice |
| Include mini-mart guest order on invoice QR | Mini-mart self-order link on invoice |
| Include invoice details in QR | Legacy text payload (INV/TOTAL) when guest order QR is off |

Staff can still override QR text per invoice in the invoice editor.

---

## Guest self-order screen

After scanning, guests see a **mobile-friendly** order page (no staff login):

### Restaurant

- **Full-screen** order overlay (hides staff dashboard; close with × when previewing on staff device)
- Search and category tabs for menu items (includes built-in **NISHA 1** menu when the device has no local menu yet)
- Cart with quantities, tax, and notes
- **Send to kitchen** submits the order
- Success message confirms submission

### Mini-mart

- Search and category tabs for store items
- Cart checkout
- **Submit order** sends to staff queue

Guest UI is translated in all **21 app languages** (follows browser/device; staff app language does not affect guest scan URL).

---

## QR Orders Report

**Open:**

- Restaurant → **QR Orders Report** on the **New Order** card or **Active Orders** toolbar
- Mini-Mart → same buttons on equivalent cards

Report opens **full screen** and includes:

| Section | Content |
|---------|---------|
| **Summary stats** | Total QR orders, slots used (of 60), open count, revenue |
| **Charts** | Status breakdown (paid/open/other), revenue by order #, orders by hour |
| **Order numbers 1–60** | Color-coded slot board (free vs occupied, amount, status) |
| **Spreadsheet** | Filterable grid of all QR scan orders |
| **Export Excel (CSV)** | Download `restaurant-qr-orders.csv` or `minimart-qr-orders.csv` |

Use the report for shift handover, busy-hour planning, and reconciling counter/table pickups.

---

## Navigation shortcuts

| Location | Label | Action |
|----------|-------|--------|
| Bottom nav | **Restaurant QR** | Open restaurant QR modal |
| Bottom nav | **Mini-Mart QR** | Open mini-mart QR modal |
| Bottom nav | **Docs** | In-app documentation |
| Top bar | **Settings** | Admin settings (gear icon) |
| Top bar | **Documentation** | Embedded help |

Kitchen role may have a reduced bottom nav; Restaurant and Manager roles see both QR buttons.

---

## Localization

Guest QR flows use dedicated translation keys (`guestOrder.*`, `guestQrReport.*`, `bnav.guestOrderRest`, etc.) in all **21 locales**.

| Area | Translated |
|------|------------|
| Bottom nav QR labels | ✓ |
| QR modal (titles, order number, buttons) | ✓ |
| Guest self-order screens | ✓ |
| QR Orders Report (stats, charts, columns) | ✓ |

Change staff UI language via top bar locale picker; guest scan page uses the same locale files when loaded.

See [Localization](localization.md).

---

## Full-screen modals

QR modals, QR Orders Report, and most pop-ups open **full screen** (entire viewport) for phone and tablet use. Close with **×** top-right or tap outside where supported.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Order number dropdown does nothing | Hard refresh (Ctrl+F5). Modal selects use the native browser dropdown. |
| QR image blank | Select an order number **1–60** first |
| Guest link does not open menu | Confirm menu/store items exist and are marked available |
| Cannot sign in / blank app | Hard refresh; ensure latest deploy (broken quote in old bundles was fixed) |
| QR report empty | No guest QR orders yet — scan and submit a test order |
| Wrong language on guest phone | Guest page uses URL + device locale; staff language picker affects staff UI only |

More: [Troubleshooting & FAQ](troubleshooting-faq.md)

---

## Related

- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Services & billing](services-and-billing.md) — invoice QR settings
- [Reports](reports.md) — department sales and shifts
- [Navigation & UI](navigation-and-ui.md) — bottom nav and modals
- [Localization](localization.md)
