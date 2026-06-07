# Navigation & UI

## Layout

The app is a **single-page application (SPA)** with:

- **Top bar** — page title, Documentation button, language picker, dark mode, user menu, logout
- **Sidebar** (☰ Menu) — full module list grouped by section
- **Main content** — active module (or embedded documentation viewer)
- **Bottom navigation** (mobile) — Dashboard, POS, Bookings, Docs, Menu

## Sidebar sections

| Section | Modules |
|---------|---------|
| **Help** | Documentation (embedded user guide) |
| **Main** | Dashboard, Rooms, Bookings, Guests |
| **Operations** | Housekeeping, Maintenance |
| **Services** | Services, Invoices, Inventory, Mini-Mart |
| **F&B** | Restaurant, Menu Items, Store Items, Order History |
| **Guest** | Guest Portal |
| **Admin** | Reports, Accounts, Transactions, Messages, Audit Log, Dropdown Lists, Settings |

Hidden sections collapse automatically when no visible links remain for your role.

## Mobile bottom nav

| Button | Action |
|--------|--------|
| **Dashboard** | Open dashboard |
| **POS** | Opens Mini-Mart POS-style view |
| **Bookings** | Open bookings |
| **Docs** | Open in-app documentation (embedded `/doc/` viewer) |
| **Menu** | Toggle sidebar |

## Documentation (in-app)

Documentation is **inside the app** — full guides open in an embedded viewer.

| Location | Label | Action |
|----------|-------|--------|
| **Top bar** | Documentation | Opens embedded docs page (`navToPage('documentation')`) |
| **Hamburger menu (☰)** | Help → Documentation | First section at top of sidebar |
| **Bottom bar** | Docs | Bottom navigation (mobile) |
| **Login screen** | Documentation ↗ | Opens `/doc/` in a new tab before sign-in |

Available to **all roles**. Use **Open in new tab ↗** inside the docs page for `/doc/`.

Standalone URL: [https://hotel-restaurant-minimart.firebaseapp.com/doc/](https://hotel-restaurant-minimart.firebaseapp.com/doc/)

The POS bottom-nav button routes to the mini-mart/sales interface for quick till operations.

## Dark mode

Toggle with the **🌙 / ☀** button in the top bar. Preference is saved in settings and `localStorage`.

## Language selection

Two ways to change language:

1. **Login screen** — Interface language dropdown
2. **Top bar** — locale selector (also under Localization menu)

Language applies to menus, labels, and common UI text. RTL layout is used for **Arabic** and **Hebrew**.

See [Localization](localization.md) for the full language list.

## Kitchen vs Restaurant label

When signed in as **Kitchen**, the sidebar link `restaurant` displays as **Kitchen** with a kitchen icon, but uses the same underlying order queue as Restaurant.

## Printing

Print-friendly CSS hides sidebar, top bar, and bottom nav when printing invoices or reports.

## Accessibility

- Skip links and ARIA labels on key controls
- `.visually-hidden` class for screen-reader-only text
- Large touch targets on housekeeping buttons for tablet use

## Tips

- Use **← back** in the top bar when drilling into sub-views
- **Badge** on Rooms shows open maintenance ticket count
- Active sidebar item is highlighted in blue

## Related

- [User roles & permissions](user-roles-and-permissions.md)
- [Localization](localization.md)
