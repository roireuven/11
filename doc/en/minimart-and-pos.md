# Mini-mart & POS

Retail sales for on-site shop items, snacks, and amenities — with walk-in or room-charge payment.

**Paths:** Sidebar → **Mini-Mart** · **Inventory POS** · bottom nav **POS**

![Mini-mart POS — products, cart, charge to room](assets/screenshots/09-minimart-pos.png)

---

## Two POS modes

| Mode | Path | Best for |
|------|------|----------|
| **Mini-Mart** | Sidebar → **Mini-Mart** | Store items (SKU catalog), guest picker, room bills |
| **Inventory POS** | Sidebar → **Inventory POS** | Direct sales from **Inventory** items marked POS-available |

Mobile bottom nav **POS** opens **Inventory POS** when your role has access; otherwise it opens **Mini-Mart**.

---

## Mini-Mart (store items)

### Guest-attached sales

| Mode | Description |
|------|-------------|
| **Walk-in / no guest** | Cash or card sale at till |
| **Checked-in guest** | Search by room, name, email, phone, booking ID |

### Payment options

| Method | When to use |
|--------|-------------|
| **Cash / Card** | Immediate sale |
| **Put bill on customer** | Add to guest's active orders — settle at checkout |

---

## Inventory POS

**Path:** Sidebar → **Inventory POS** (Admin, Manager, Receptionist)

Sell items directly from the **Inventory** table:

1. Open **Inventory POS**
2. Tap items to add to cart (only items with POS enabled)
3. Choose **Cash**, **Card**, or **Charge to room**
4. Sale deducts stock and posts to **All Transactions**

Use Inventory POS for front-desk sundries, minibar top-ups, or items not in the Store Items catalog.

---

## Store items vs inventory

| Catalog | Module | Used by |
|---------|--------|---------|
| **Store Items** | Mini-Mart | Retail SKUs, barcodes, linked inventory |
| **Inventory** | Inventory POS | Raw stock items with `posAvailable` flag |

Configure store items under **Store Items**; enable POS on inventory rows under **Inventory**.

---

## Reports

Sales roll into **Reports** by department:

- Mini-Mart
- Restaurant
- Hotel (PMS)
- POS

---

## Related

- [Inventory & catalog](inventory-and-catalog.md)
- [Services & billing](services-and-billing.md)
- [Accounts & audit](accounts-and-audit.md)
