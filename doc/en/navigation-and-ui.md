# Navigation & UI

This guide explains how to move around **HotelRestaurantMini-MartManagement** on desktop, tablet, and phone.

## Layout overview

The app is a **single-page application (SPA)** with:

- **Top bar** — page title, **Documentation**, **Settings**, language, dark mode, user menu, logout (on phones: two rows with **⋮ More** overflow)
- **Sidebar** (☰ Menu) — full module list grouped by section
- **Main content** — active module (or **embedded documentation** viewer)
- **Bottom navigation** (mobile) — two rows: Dashboard, POS, Bookings on row 1; **Restaurant QR**, **Mini-Mart QR** on row 2; **Docs** and **Settings** in **⋮ More**; **Menu** toggles sidebar

![Dashboard — top bar, shifts, and bottom navigation](assets/screenshots/02-dashboard.png)

### Dashboard quick actions (PMS grid)

Below the welcome bar, the dashboard shows a grid of **+** buttons for common add actions (all labels follow your UI language):

Add Room, Add Booking, Add Guest, Add Task, Add Service, Add Invoice, Add Stock, Add Menu, Add Shop Item, Add User.

Housekeeping and Transactions are available from the **sidebar** (not on this grid as of v2.4). See [What's new in v2.4](whats-new-v2.md).

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

## Mobile bottom nav (v2.4)

On phones the bottom bar is **double-height** (two rows of buttons):

| Row | Buttons |
|-----|---------|
| **Row 1** | Dashboard, POS, Bookings |
| **Row 2** | **Restaurant QR**, **Mini-Mart QR** (always visible) |
| **⋮ More** | Docs, Settings |
| **Menu** | Toggle sidebar (☰) |

| Button | Action |
|--------|--------|
| **Dashboard** | Open dashboard |
| **POS** | Opens **Inventory POS** (or Mini-Mart if POS not in your role) |
| **Bookings** | Open bookings |
| **Restaurant QR** | Open guest restaurant order QR modal (order # 1–60) |
| **Mini-Mart QR** | Open guest mini-mart order QR modal |
| **⋮ More → Docs** | Open in-app documentation (embedded viewer) |
| **⋮ More → Settings** | Open settings (Admin) or settings page for your role |
| **Menu** | Toggle sidebar |

Kitchen role may see a reduced bottom nav (Restaurant + Docs in More + Menu).

## Mobile top bar (v2.4)

On narrow screens the top bar is also **double-height**:

| Row | Controls |
|-----|----------|
| **Row 1** | Back, page title, user avatar |
| **Row 2** | Documentation, Settings, language, dark mode, logout — or **⋮ More** when space is tight |

### Language picker on phone

Tap **⋮ More** → **Localization** to open a popup list of all **21 languages**. Select a language to switch the UI immediately. This works on phones where the desktop language dropdown is hidden.

QR modals and the **QR Orders Report** open **full screen** on phone and desktop for easier scanning and review.

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
| **Settings** | Quick access to Settings (Admin) |
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
