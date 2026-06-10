# Services & billing

Guest folios, extra services, taxes, discounts, and payment settlement across hotel, restaurant, and mini-mart.

**Paths:** Sidebar → **Services** · **Invoices**

---

## Services catalog

**Path:** Sidebar → **Services**

Define sellable add-ons (spa, laundry, airport transfer, minibar restock, etc.):

| Field | Purpose |
|-------|---------|
| Service name | Display on invoice |
| Category | Grouping in reports |
| Price | Default charge (hotel currency) |
| Active flag | Hide discontinued services |

### Walk-in sale (cash at desk)

For guests **without** an active booking folio:

1. Open **Services** → service catalog grid
2. Click **Pay** on the service row (green button)
3. Confirm cash in the payment modal
4. Sale posts to **All Transactions** and **Audit Log** (`Sale` / `Service`)

Use this for spa day passes, walk-in laundry, or amenity purchases paid immediately.

### Order service on a booking (room charge)

From an active **Booking**:

1. Open the booking detail
2. Click **Order service**
3. Select service from catalog
4. Set **quantity**
5. Confirm — line posts to the guest folio

Charges appear on **Invoices** and at **check-out**.

### Service requests (operations queue)

The **Service Requests** grid handles room-service workflows:

| Status | Billing |
|--------|---------|
| **Pending / In Progress** | No charge yet |
| **Completed (with booking)** | Room charge via `processSale` |
| **Completed (walk-in, no booking)** | Cash payment modal → immediate sale |

---

## Invoices

**Path:** Sidebar → **Invoices**

Central billing view for stays and posted charges.

![Invoices — guest folios and line items](assets/screenshots/10-invoices.png)

### Invoice payment QR (bank)

Invoices show your **bank payment QR** and optional **logo** only — not restaurant or mini-mart guest-order QRs (those live on the bottom nav **Restaurant QR** / **Mini-Mart QR** shortcuts).

| Setting (Settings) | Effect |
|--------------------|--------|
| Payment QR text or URL | Payload encoded in the QR (bank link or EMV string) |
| Payment QR image | Upload bank-provided QR image |
| Include invoice number & total in payment QR | Appends INV/TOTAL to the payment payload when enabled |

Per-invoice overrides: logo browse and payment QR browse on the invoice payment overlay.

Guest self-order uses **order numbers 1–60** from staff QR modals — see [Guest QR orders](guest-qr-orders.md).

### Pay QR orders from the floor

Staff can **pay** guest QR orders from:

- Restaurant / Mini-Mart / POS **QR bill modals** (Cash or Card)
- **QR Orders Report** — tap a slot or use the Pay column

Paid orders update local records and the audit log.

### Pay invoice (cash)

1. Open **Invoices**
2. Click **Pay** on an unpaid row
3. Enter cash received in the modal
4. Invoice marked **Fully Paid**
5. A **Hotel** transaction is created and linked in **All Transactions**
6. **Audit Log** records `Payment` with transaction id

### Edit invoice (Admin only)

After an invoice is created, **only Admin** can:

- Open **Edit** on the invoice grid
- Import invoice CSV rows
- Change logo or payment QR on the bill overlay
- Delete (hide) an invoice row

Manager, Reception, and other roles can still **view**, **pay**, and **print** invoices.

### Invoice sources

| Source | Example |
|--------|---------|
| **Check-in / check-out** | Room nights, taxes |
| **Services** | Spa, laundry ordered from booking |
| **Restaurant** | Room service charged to room |
| **Mini-mart** | Shop items on **Put bill on customer** |
| **Manual adjustments** | Discounts, waivers |

---

## Where selling happens in the app

| Module | Sell action | Payment |
|--------|-------------|---------|
| **Mini-Mart** | Cart checkout | Cash, Card, Room charge |
| **Inventory POS** | Sidebar → Inventory POS | Cash, Card, Room charge |
| **Restaurant** | Table / walk-in checkout | Cash, Card, Room, Table |
| **Services catalog** | **Pay** button on row | Cash (walk-in) |
| **Service requests** | Complete request | Cash or Room charge |
| **Invoices** | **Pay** button | Cash |
| **Bookings** | Prepay / check-out | Cash, Card |

All completed sales flow through the shared transaction engine and appear in **Reports** by department.

---

## Check-in / check-out billing

| Event | Billing behavior |
|-------|------------------|
| **Check-in** | Opens or links guest folio; room becomes **Occupied** |
| **During stay** | Restaurant and mini-mart post to active folio |
| **Check-out** | Final invoice; room returns to housekeeping workflow |

---

## Related

- [Hotel operations](hotel-operations.md)
- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Accounts & audit](accounts-and-audit.md)
- [Visual guide](visual-guide.md)
