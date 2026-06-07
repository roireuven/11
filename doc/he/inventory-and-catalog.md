# Inventory & catalog

Stock and product management across **restaurant**, **mini-mart**, and shared **inventory**.

![Mini-mart POS — store items linked to inventory](../en/assets/screenshots/09-minimart-pos.png)

![Restaurant — menu items and stock checks](../en/assets/screenshots/08-restaurant.png)

---

## Inventory (central stock)

**Path:** Sidebar → **Inventory**

| Feature | Description |
|---------|-------------|
| **Items** | Ingredients, supplies, retail stock |
| **Categories** | From Dropdown Lists |
| **Adjustments** | Manual stock in/out |
| **Audit log** | Inventory change history |

Restaurant and mini-mart **decrement stock on sale** when menu/store items link to inventory rows.

### Stock validation

- Mini-mart shows *"Not enough stock"* if cart exceeds on-hand quantity
- Restaurant may block items when recipe link requires stock

---

## Menu Items (restaurant catalog)

**Path:** Sidebar → **Menu Items**

| Field | Purpose |
|-------|---------|
| Name, category | Menu organization |
| Price | Restaurant currency |
| Image URL | Optional photo on POS |
| Recipe / inventory link | Deduct stock on order |

**Roles:** Admin, Manager, Reception, Restaurant — not Kitchen/Housekeeper.

Configure categories: **Dropdown Lists → Menu categories**.

---

## Store Items (mini-mart catalog)

**Path:** Sidebar → **Store Items**

| Field | Purpose |
|-------|---------|
| Name, category, barcode | SKU identification |
| Price | Shop shelf price |
| Stock on hand | Linked to inventory |

**Roles:** Typically Admin/Manager edit catalog; Reception sells via Mini-mart.

Configure categories: **Dropdown Lists → Store categories**.

---

## How catalogs connect

```
Menu Items ──► Restaurant orders ──► Inventory (deduct)
Store Items  ──► Mini-mart POS    ──► Inventory (deduct)
Inventory    ──► Reports / export / audit
```

---

## Dropdown list dependencies

| List | Used by |
|------|---------|
| Menu categories | Menu Items |
| Store categories | Store Items |
| Inventory categories | Inventory |
| Order statuses | Restaurant kitchen queue |
| Payment types | POS, restaurant, invoices |

**Path:** Sidebar → **Dropdown Lists** (Admin)

---

## Sample datasets

| Asset | Content |
|-------|---------|
| `nisha1-menu-dataset.js` | Sample Indian restaurant menu (LAK) |
| `embedded-sample.js` | Bundled demo data loader |

Reload: **Settings → Reload built-in demo sample** (destructive — [backup first](backup-restore-and-data.md)).

---

## Export

**Settings → Export all data (CSV ZIP)** or per-table CSV:

- Inventory, Menu, Store, Restaurant sales, Mini-mart bills

---

## Related

- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Data model](data-model.md)
- [Visual guide](visual-guide.md)
