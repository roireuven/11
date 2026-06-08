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

![Invoices — guest folios and line items](../en/assets/screenshots/10-invoices.png)

### Invoice QR codes and guest ordering

Invoices can show QR codes that link guests to **self-order** screens:

| Setting (Settings) | Effect |
|------------------|--------|
| Include restaurant guest order on invoice QR | QR opens restaurant guest menu |
| Include mini-mart guest order on invoice QR | QR opens mini-mart guest cart |
| Include invoice details in QR | Text payload (invoice #, total) when guest-order QR is disabled |

Per-invoice QR can be edited in the invoice overlay (custom URL/image). Guest orders use **order numbers 1–60** when generated from the staff QR modal.

See [Guest QR orders](guest-qr-orders.md).

### Pay invoice (cash)

1. Open **Invoices**
2. Click **Pay** on an unpaid row
3. Enter cash received in the modal
4. Invoice marked **Fully Paid**
5. A **Hotel** transaction is created and linked in **All Transactions**
6. **Audit Log** records `Payment` with transaction id

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
