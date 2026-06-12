# What's new in v2.3 / v2.4

This guide summarizes major features added in **stable v2.3** and **stable v2.4** of HotelRestaurantMini-MartManagement.

**Live stable sites:**

| Version | URL |
|---------|-----|
| **v2.3** | [hotel-restaurant-minimart2-3.web.app](https://hotel-restaurant-minimart2-3.web.app/) |
| **v2.4** | [hotel-restaurant-minimart2-4.web.app](https://hotel-restaurant-minimart2-4.web.app/) |
| **Development** | [hotel-restaurant-minimart.web.app](https://hotel-restaurant-minimart.web.app/) |

---

## Full interface in 21 languages

The web app UI is available in **21 locales**: English, Spanish, French, German, Japanese, Korean, Arabic, Hindi, Thai, Vietnamese, Indonesian, Turkish, Russian, Italian, Dutch, Polish, Hebrew, Lao, Portuguese (Brazil), Chinese (Simplified), and Chinese (Traditional).

### Where to change language

| Screen | How |
|--------|-----|
| **Login / setup** | Language dropdown in the header (before sign-in) |
| **After login** | Top bar locale selector or **Localization** in the menu |
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

## Documentation

- This **What's new** guide is available in all 21 documentation languages.
- Open docs from the app: **top bar → Documentation**, **☰ Help → Documentation**, or **bottom nav → Docs**.
- Standalone URL: `/doc/?lang={code}#/whats-new-v2`

---

## For administrators

| Task | Where |
|------|--------|
| Train staff on language switch | [Localization](localization.md) |
| Configure property after upgrade | [Settings & configuration](settings-and-configuration.md) |
| Deploy updates | [Deployment](deployment.md) — `npm run deploy:stable` publishes to v2.3 and v2.4 |

---

## Related guides

- [Localization](localization.md) — languages, RTL, locale files
- [First-time setup](first-time-setup.md) — initial configuration
- [Navigation & UI](navigation-and-ui.md) — dashboard, sidebar, mobile nav
- [Hotel operations](hotel-operations.md) — bookings and guests
- [Deployment](deployment.md) — development vs stable v2.3 / v2.4
