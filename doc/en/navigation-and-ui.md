# Navigation & UI

This guide explains how to move around **HotelRestaurantMini-MartManagement** on desktop, tablet, and phone.

## Layout overview

The app is a **single-page application (SPA)** with:

- **Top bar** — page title, **Documentation** button, language picker, dark mode, user menu, logout
- **Sidebar** (☰ Menu) — full module list grouped by section
- **Main content** — active module (or **embedded documentation** viewer)
- **Bottom navigation** (mobile) — Dashboard, POS, Bookings, **Docs**, Menu

![Dashboard — top bar, shifts, and bottom navigation](assets/screenshots/02-dashboard.png)

---

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

### Opening the sidebar

| Device | Action |
|--------|--------|
| Desktop | Click **☰** (hamburger) top-left |
| Mobile | Tap **Menu** in bottom nav |

![Help section at top of sidebar — Documentation link](assets/screenshots/03-help-menu.png)

---

## Mobile bottom nav

| Button | Action |
|--------|--------|
| **Dashboard** | Open dashboard |
| **POS** | Opens **Inventory POS** (or Mini-Mart if POS not in your role) |
| **Bookings** | Open bookings |
| **Docs** | Open in-app documentation (embedded viewer) |
| **Menu** | Toggle sidebar |

Kitchen role may see a reduced bottom nav (Restaurant + Docs + Menu).

> **Documentation tip:** Links at the bottom of the docs sidebar (Live web app, APK landing) open in a **new browser tab** so they do not replace the embedded help panel.

---

## Documentation (embedded in the app)

Documentation is **inside the software** — not a separate website tab.

| Location | Label | Action |
|----------|-------|--------|
| **Top bar** | Documentation | Opens embedded help panel |
| **Hamburger menu (☰)** | Help → Documentation | First section at top of sidebar |
| **Bottom bar** | Docs | Bottom navigation (mobile) |
| **Login screen** | Hint text | Help available after sign-in via ☰ Menu → Help |

![Documentation embedded inside the app](assets/screenshots/04-documentation-embed.png)

- Opens in your **current app language** (21 locales)
- See [Multilingual documentation](multilingual-documentation.md) and [Visual guide](visual-guide.md)

---

## Top bar controls

| Control | Purpose |
|---------|---------|
| **← Back** | Return from drill-down views |
| **Documentation** | In-app help |
| **Localization / language** | Change UI language |
| **🌙 / ☀** | Dark / light mode |
| **User avatar** | Shows role name |
| **Logout** | End session |

---

## Dark mode

Toggle with the **🌙 / ☀** button. Preference is saved in settings and `localStorage`.

---

## Language selection

| When | How |
|------|-----|
| Before login | Interface language dropdown on sign-in screen |
| After login | Top bar locale selector |

See [Localization](localization.md).

---

## Kitchen vs Restaurant label

**Kitchen** role sees the Restaurant module labeled **Kitchen** — same queue, restricted payment actions.

---

## Shift indicators (Dashboard)

| Shift | Action |
|-------|--------|
| Restaurant / Mini-mart / Hotel | OPEN SHIFT / CLOSE SHIFT on Dashboard |

See [Reports](reports.md).

---

## Printing

Print-friendly CSS hides navigation chrome when printing invoices or reports.

---

## Related

- [Visual guide (screenshots)](visual-guide.md)
- [User roles & permissions](user-roles-and-permissions.md)
- [Getting started](getting-started.md)
