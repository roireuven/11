# Mini-mart & POS

Retail sales for on-site shop items, snacks, and amenities — with walk-in or room-charge payment.

**Path:** Sidebar → **Mini-Mart** or bottom nav **POS**

## Guest-attached sales

Before scanning items, choose who the order is for:

| Mode | Description |
|------|-------------|
| **Walk-in / no guest** | Cash or card sale at till |
| **Checked-in guest** | Search by room, name, email, phone, booking ID |

Guest picker shows checked-in guests only for room charges.

### Quick add guest

Add a guest profile from the picker if they are not in the directory yet.

## Cart operations

- Add **Store Items** to cart
- Adjust quantities (+ / −)
- Stock validation — *"Not enough stock"* if quantity exceeds inventory

## Payment options

| Method | When to use |
|--------|-------------|
| **Cash / Card** | Immediate sale — *"Sale completed"* |
| **Put bill on customer** | Add to guest's **active orders** (unpaid) — settle later |

### Room bill flow

1. Select checked-in guest
2. Add items to cart
3. **Put bill on customer** — bill moves to active orders (not paid yet)
4. Settle via **Pay total** on room bill or pay cart with Cash/Card

Toast messages guide each step if cart state is invalid.

## Mini-mart cash title

Walk-in sales display as **Mini-Mart — Cash** on receipts/transactions.

## POS bottom navigation

On mobile, the **POS** bottom-nav button opens the mini-mart interface optimized for quick sales (same underlying module).

## Store items

**Path:** Sidebar → **Store Items** (Admin/Manager)

Manage SKUs:

- Name, category, price, barcode
- Stock quantity
- Linked to inventory tables

## Open bills

Unpaid mini-mart room charges appear in data exports as **Mini-mart open bills** until settled at checkout or pay total.

## Reports

Sales roll into **Reports** by department:

- Mini-Mart
- Restaurant
- Hotel (PMS)
- POS

## Related

- [Inventory & catalog](inventory-and-catalog.md)
- [Services & billing](services-and-billing.md)
- [Hotel operations](hotel-operations.md) — checked-in guests
