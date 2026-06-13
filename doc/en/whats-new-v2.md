# What's new in v2.4

**v2.4** is the **current production release** of HotelRestaurantMini-MartManagement. Routine deploys (`npm run deploy`) publish **only** to the v2.4 site.

| Site | URL | Role |
|------|-----|------|
| **v2.4 (production)** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) | **Current** — staff-facing stable |
| v2.3 (legacy) | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) | Frozen snapshot — manual deploy only |
| Development | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) | Internal testing — manual deploy only |

---

## Vehicle rental (cars & motorbikes)

New **Vehicle Rental** module for properties that rent cars and motorbikes to guests:

- Visual **fleet floor** with color-coded tiles (available, rented, pending, maintenance)
- **Checkout** and **return** flows with fuel/odometer tracking
- Link rentals to **guests** and **bookings**
- Revenue posts to **transactions** and **dashboard** (`source: Vehicle Rental`)
- Active rentals grid, history, and CSV export
- Available to **Admin**, **Manager**, and **Reception**

See [Vehicle rental](vehicle-rental.md).

---

## Mobile UI — double-height bars

On small phones the top and bottom bars are **taller** (two rows) for easier tapping:

| Bar | Row 1 | Row 2 |
|-----|-------|-------|
| **Top** | Back, title, user | Documentation, Settings, language, dark mode, logout — overflow in **⋮ More** |
| **Bottom** | Dashboard, POS, Bookings | **Restaurant QR**, **Mini-Mart QR** always visible; Docs + Settings in **⋮ More** |

### Language on phone

Tap **⋮ More** (top bar) → **Localization** opens a **language picker popup** with all 21 locales. This replaces the desktop dropdown that was hard to use on narrow screens.

### QR always visible

**Restaurant QR** and **Mini-Mart QR** stay on the bottom bar (not hidden in More) so staff can open guest order QR codes quickly.

See [Navigation & UI](navigation-and-ui.md).

---

## Full interface in 21 languages

The web app UI is available in **21 locales**: English, Spanish, French, German, Japanese, Korean, Arabic, Hindi, Thai, Vietnamese, Indonesian, Turkish, Russian, Italian, Dutch, Polish, Hebrew, Lao, Portuguese (Brazil), Chinese (Simplified), and Chinese (Traditional).

### Where to change language

| Screen | How |
|--------|-----|
| **Login / setup** | Language dropdown in the header (before sign-in) |
| **After login (desktop)** | Top bar locale selector |
| **After login (phone)** | Top bar **⋮ More → Localization** popup |
| **Settings** | App language section |

Preference is saved in browser storage (`hotel_mgr_uiLocale`).

### RTL (right-to-left)

**Arabic** and **Hebrew** enable RTL layout for the whole app. Modal forms use improved alignment so labels and inputs read correctly in both LTR and RTL languages.

---

## First-time setup (translated)

The setup wizard is fully localized:

- Business / hotel name
- System header text
- Admin username, email, and password fields
- All buttons and validation messages

After setup, the hotel name is stored and shown in the app header where configured.

---

## Dashboard quick actions (PMS grid)

The **Dashboard** shows a grid of blue **+** buttons for common tasks:

| Button | Opens |
|--------|--------|
| Add Room | New room form |
| Add Booking | New booking form |
| Add Guest | New guest form |
| Add Task | New maintenance ticket |
| Add Service | New service request |
| Add Invoice | New invoice form |
| Add Stock | New inventory item |
| Add Menu | New menu item |
| Add Shop Item | New store / mini-mart item |
| Add User | New staff account |

**Note:** *Add Cleaning* and *Add Transaction* were removed from this grid (v2.4). Use the sidebar for **Housekeeping** and **Transactions** when needed.

---

## Translated modal forms

Add and edit dialogs are localized in all 21 languages, including:

- **Maintenance** — new ticket (room, priority, issue, notes)
- **Invoice** — add / edit (guest, room, dates, amounts, payment status)
- **Inventory** — add / edit item (name, barcode, category, quantity, POS availability)
- **Menu item** — add / edit (name, icon, price, category, image, stock link)
- **Store item** — add / edit (name, price, category, shelf icon, barcode, stock)
- **User account** — add / edit (name, email, password, role)

Image upload labels (“from device”, “or image URL”) follow the active language.

---

## Booking → New guest

When creating a **booking**, if the guest is not in the directory yet:

1. Tap **+ New guest** (or equivalent) on the booking form.
2. Fill in the **New Guest** modal (name, passport, nationality, date of birth, payment method, contact, notes).
3. Tap **Add guest & return** — you return to the booking with the new guest selected.

The nationality picker (search list) is also translated.

---

## Documentation (v2.4)

- User guides updated for **v2.4** production URLs and new modules.
- Available in all **21 documentation languages** at `/doc/?lang={code}`.
- Open from the app: **top bar → Documentation**, **☰ Help → Documentation**, or **bottom nav → ⋮ More → Docs**.
- Standalone URL: [https://hotel-restaurant-minimart2-4.web.app/doc/?lang=en#/whats-new-v2](https://hotel-restaurant-minimart2-4.web.app/doc/?lang=en#/whats-new-v2)

---

## For administrators

| Task | Where |
|------|--------|
| Train staff on language switch | [Localization](localization.md) |
| Configure vehicle fleet | [Vehicle rental](vehicle-rental.md) |
| Configure property after upgrade | [Settings & configuration](settings-and-configuration.md) |
| Deploy updates | [Deployment](deployment.md) — `npm run deploy` publishes to **v2.4 only** |

---

## Related guides

- [Vehicle rental](vehicle-rental.md) — fleet floor, checkout, return
- [Localization](localization.md) — languages, RTL, locale files
- [First-time setup](first-time-setup.md) — initial configuration
- [Navigation & UI](navigation-and-ui.md) — dashboard, sidebar, mobile nav
- [Hotel operations](hotel-operations.md) — bookings and guests
- [Deployment](deployment.md) — v2.4 production deploy
