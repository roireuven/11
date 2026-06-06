# Inventory & catalog

Stock and product management across F&B and retail.

## Inventory

**Path:** Sidebar → **Inventory**

Central stock for:

- F&B ingredients and supplies
- Mini-mart products (when linked)
- Hotel operational supplies

Features:

- Add/edit inventory items
- Categories from dropdown lists
- Stock counts and adjustments
- Audit log (Inventory audit log)

Restaurant and mini-mart decrement stock on sale when items are linked.

## Menu Items

**Path:** Sidebar → **Menu Items**

Restaurant catalog:

- Dish name, category, price
- Optional image URL
- Recipe / inventory link (catalog-inventory migration links items at setup)

Accessible to Admin, Manager, Reception, Restaurant — **not** Kitchen or Housekeeper.

## Store Items

**Path:** Sidebar → **Store Items**

Mini-mart / shop catalog:

- Product name, category, price, barcode
- Stock on hand
- Store categories from dropdown lists

Typically Admin/Manager only in sidebar (Reception may use mini-mart without editing store catalog).

## Dropdown list dependencies

Configure under **Dropdown Lists**:

| List | Used by |
|------|---------|
| Menu categories | Menu Items |
| Store categories | Store Items |
| Inventory categories | Inventory |
| Order statuses | Restaurant queue |
| Payment types | POS / restaurant |

## Sample datasets

Production includes optional bundled data:

| File | Content |
|------|---------|
| `assets/data/nisha1-menu-dataset.js` | Sample Indian restaurant menu (LAK) |
| `assets/data/embedded-sample.js` | Empty by default in new browsers |

Reload sample data from **Settings → Reload built-in demo sample** (destructive — see backup docs).

## CSV export

Export individual tables from Settings:

- Inventory, Menu, Store, Restaurant, Mini-mart open bills, etc.

## Related

- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Settings & configuration](settings-and-configuration.md)
- [Data model](data-model.md)
