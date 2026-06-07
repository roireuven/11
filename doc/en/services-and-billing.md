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

### Order service on a booking

From an active **Booking**:

1. Open the booking detail
2. Click **Order service**
3. Select service from catalog
4. Set **quantity**
5. Confirm — line posts to the guest folio

Charges appear on **Invoices** and at **check-out**.

---

## Invoices

**Path:** Sidebar → **Invoices**

Central billing view for stays and posted charges.

![Invoices — guest folios and line items](assets/screenshots/10-invoices.png)

### Invoice sources

| Source | Example |
|--------|---------|
| **Check-in / check-out** | Room nights, taxes |
| **Services** | Spa, laundry ordered from booking |
| **Restaurant** | Room service charged to room |
| **Mini-mart** | Shop items on **Put bill on customer** |
| **Manual adjustments** | Discounts, waivers |

### Typical invoice fields

- Guest name, room, booking reference
- Line items with quantity and unit price
- **Default tax %** and **service tax %** from Settings
- Currency from hotel profile
- Payment status (open / paid)

---

## Check-in / check-out billing

| Event | Billing behavior |
|-------|------------------|
| **Check-in** | Opens or links guest folio; room becomes **Occupied** |
| **During stay** | Restaurant and mini-mart post to active folio |
| **Check-out** | Final invoice; room returns to housekeeping workflow |

Confirmation messages include guest name and invoice id, e.g. *"{guest} checked out. Invoice {inv} generated."*

### End-of-stay checklist (Reception)

1. Review **Invoices** for open line items
2. Settle restaurant/shop room charges if still on active orders
3. Apply discounts if approved by manager
4. **Check out** booking
5. Print or email invoice if your process requires

---

## Discounts and waivers

| Action | When to use |
|--------|-------------|
| **Discount %** | Promotions, loyalty, manager approval |
| **Waive fee** | Late checkout penalty, service recovery |

Default discount reason in Settings: *Manager discount* — customize in **Dropdown Lists** if needed.

---

## Payment methods

Configure under **Dropdown Lists → Payment methods / Payment types**.

Used for:

- POS walk-in sales (cash/card)
- Restaurant table payment
- Invoice settlement at checkout

Ensure methods match your property (cash, card, bank transfer, room charge, etc.).

---

## Room charges from F&B and shop

| Module | Flow |
|--------|------|
| **Restaurant room service** | Select checked-in guest → order → charge to folio |
| **Mini-mart Put bill on customer** | Guest picker → cart → bill on active orders → pay at checkout |

Department breakdown in **Reports**:

> Restaurant · Mini-Mart · Hotel (PMS) · POS

---

## Shift and tax context

- **Tax rates** — Settings → default tax %, service tax %
- **Season multipliers** — Settings → peak/off season (room rates)
- **Shifts** — Dashboard OPEN/CLOSE shift affects POS reporting

See [Reports](reports.md) and [Settings & configuration](settings-and-configuration.md).

---

## Related

- [Hotel operations](hotel-operations.md)
- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Visual guide](visual-guide.md)
