# Demo credentials

Built-in demo users for **training and evaluation** without running first-time setup.

![Sign-in screen — demo credential rows](../en/assets/screenshots/01-login.png)

> Tap a demo **email row** to auto-fill the username. Password for all demo users: **`1234`**

---

## Demo user table

| Role | Email (username) | Password | Lands on |
|------|------------------|----------|----------|
| **Admin** | admin@hotel.com | 1234 | Dashboard (full access) |
| **Manager** | mike@hotel.com | 1234 | Reports |
| **Reception** | jane@hotel.com | 1234 | Rooms |
| **Housekeeper** | tom@hotel.com | 1234 | Housekeeping |
| **Restaurant** | restaurant@hotel.com | 1234 | Restaurant |
| **Kitchen** | kitchen@hotel.com | 1234 | Restaurant (as **Kitchen**) |

---

## What each role sees

| Role | Sidebar highlights | Restrictions |
|------|-------------------|--------------|
| **Admin** | All modules incl. Settings, Accounts, Audit | — |
| **Manager** | Reports, inventory, operations | No Settings/Accounts |
| **Reception** | Rooms, bookings, guests, invoices, F&B sales | No admin modules |
| **Housekeeper** | Housekeeping, maintenance | No billing |
| **Restaurant** | Restaurant, menu, inventory | No room management |
| **Kitchen** | Kitchen queue only | No payments |

See full matrix: [User roles & permissions](user-roles-and-permissions.md).

---

## Training workflow

1. Open [live app (v2.4)](https://hotel-restaurant-minimart2-4.web.app/)
2. Select **interface language** on login screen
3. Tap demo row → enter password **1234** → **Sign in**
4. Explore role-specific menus
5. Open **☰ Help → Documentation** for guides and [Visual guide](visual-guide.md)

Try each role in separate browser profiles to compare menus side by side.

---

## Demo data notes

- Demo accounts may be **auto-created** on first login if missing
- Sample rooms, bookings, and catalog data may load with demo namespace
- Demo data shares browser storage with your property — **Factory reset** before production
- For a clean property, use [First-time setup](first-time-setup.md) instead

---

## Interface language

Choose language **before** sign-in on the login screen. Applies to labels and in-app documentation (21 locales).

See [Localization](localization.md).

---

## Related

- [Getting started](getting-started.md)
- [First-time setup](first-time-setup.md)
- [Visual guide](visual-guide.md)
