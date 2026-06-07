# Restaurant & kitchen

Unified F&B module for dine-in, room service, and kitchen display.

**Path:** Sidebar → **Restaurant** (or **Kitchen** for kitchen role)

![Restaurant — table floor and order queue](/doc/en/assets/screenshots/08-restaurant.png)

## Order types

| Type | Use case |
|------|----------|
| **Table / Walk-in** | Restaurant floor, cash guests |
| **Room Service** | Charge to checked-in guest room |

For room service, select guest from checked-in list (search by room, name, email, phone, booking ID).

## Table floor

Visual **table tiles** show status at a glance:

| Color | Meaning |
|-------|---------|
| Green | Free seat |
| Red | Open order / kitchen active |
| Amber | Served — payment pending |

Legend labels: **free**, **live**, **pay**

## Order workflow

```
Create order → Send to Kitchen → New → Preparing → Ready → Served → Payment
```

| Action | Description |
|--------|-------------|
| **Send to Kitchen** | Sends ticket to kitchen queue |
| **Send to Room** | Creates order already at Ready (room service shortcut) |
| Advance status | Kitchen moves tickets through queue |

Kitchen queue sorts **oldest first**.

## Kitchen queue

Shared live queue between Restaurant and Kitchen tabs:

- Updates when orders change in any tab or device on same storage
- Banner: *"Synced with Restaurant — everyone uses the same saved orders"*

Kitchen role sees **All active orders** without payment buttons.

## Menu integration

- Add items from **Menu Items** catalog
- Stock checks against **Inventory** when linked
- Shortcuts to Menu Items and Inventory from restaurant screen (role permitting)

## Payments

Restaurant staff can settle:

- **Cash** — table or room cart
- **Card** — as configured
- **Room charge** — posts to guest folio

Kitchen **cannot** take payment or close tabs.

## Order history

**Path:** Sidebar → **Order History** (Admin/Manager)

- Past restaurant orders
- **Void order** when needed
- Change log for compliance

## Sample menu data

Production ships optional dataset `nisha1-menu-dataset.js` (Indian restaurant sample, LAK pricing). New setups may load catalog templates; see Settings export/reload options.

## Restrictions by role

| Action | Restaurant | Kitchen |
|--------|:----------:|:-------:|
| Create orders | ✓ | ✗ |
| Kitchen queue | ✓ | ✓ |
| Payment | ✓ | ✗ |
| Menu Items | ✓ | ✗ |

## Related

- [Inventory & catalog](inventory-and-catalog.md)
- [User roles & permissions](user-roles-and-permissions.md)
- [Mini-mart & POS](minimart-and-pos.md)
