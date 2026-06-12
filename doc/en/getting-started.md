# Getting started

This guide gets a new property from zero to daily operations in the minimum number of steps.

## Step 1 — Open the app

**Web (v2.4 production):** [https://hotel-restaurant-minimart2-4.web.app/](https://hotel-restaurant-minimart2-4.web.app/)

**Android:** Install the APK from the [Hotel Manager landing page](https://roireuven.github.io/11/).

Use a modern browser (Chrome, Edge, Safari, Firefox) or Android 8+ for the mobile app.

![Dashboard after login — shifts and analytics](assets/screenshots/02-dashboard.png)

> **Tip:** Open **☰ Menu → Help → Documentation** anytime for in-app help in your language.

## Step 2 — First-time setup

On first visit you see **v2.0 — First-Time Setup**.

![First-time setup screen](assets/screenshots/01-login.png)

1. Enter your **system email** (this becomes the primary admin login).
2. Enter a **password** (minimum 4 characters).
3. Click **Create Account & Get Started**.

The app creates a **data namespace** from your email so your property data is isolated from other setups on the same browser.

**Alternative URL:** append `?newsetup=1` to force the setup screen (use only in one browser — see [First-time setup](first-time-setup.md)).

See [First-time setup](first-time-setup.md) for details.

## Step 3 — Configure the hotel

Sign in as Admin and open **Settings**:

![Settings — hotel profile and taxes](assets/screenshots/11-settings.png)

1. Set **hotel name**, address, phone, contact email
2. Choose **currency** (use **LAK** if operating in Laos — see localization hints in Settings)
3. Set **check-in / check-out times**, tax rates, peak season rules
4. Click **Save settings**

## Step 4 — Add rooms and staff

1. **Rooms** — add room numbers, types, floors, nightly rates
2. **Bookings** — create a test reservation (see screenshot below)
3. **Accounts** — create staff users and assign roles (Reception, Restaurant, Kitchen, etc.)
4. **Dropdown lists** — review room types, payment methods, currencies
5. **Guest QR** — test bottom nav **Restaurant QR** / **Mini-Mart QR**, pick order #1, scan from a phone (see [Guest QR orders](guest-qr-orders.md))

![Bookings — reservations and check-in/out](assets/screenshots/06-bookings.png)

See [Hotel operations](hotel-operations.md) and [User roles & permissions](user-roles-and-permissions.md).

## Step 5 — Set up F&B and shop

1. **Menu Items** — restaurant dishes and prices
2. **Store Items** — mini-mart products and stock
3. **Inventory** — shared F&B and supply stock (optional link from menu)

![Restaurant — tables and orders](assets/screenshots/08-restaurant.png)

![Mini-mart POS — cart and payment](assets/screenshots/09-minimart-pos.png)

See [Restaurant & kitchen](restaurant-and-kitchen.md) and [Mini-mart & POS](minimart-and-pos.md).

## Step 6 — Train staff by role

| Role | Start here |
|------|------------|
| Reception | Dashboard → Rooms → Bookings |
| Housekeeper | Housekeeping board |
| Restaurant | Restaurant → table floor / room service |
| Kitchen | Restaurant (labeled **Kitchen** in sidebar) |
| Manager | Reports → Inventory |

Each role lands on a **default page** after login (see [User roles & permissions](user-roles-and-permissions.md)).

## Step 7 — Back up before go-live

In **Settings → Backup and restore**:

- **Export all data (CSV ZIP)** — archive before production use
- Keep exports in a safe location off the device

See [Backup, restore & data](backup-restore-and-data.md).

## Demo mode

For training without your own setup, use the built-in demo accounts in [Demo credentials](demo-credentials.md). Demo logins work on the sign-in screen without running first-time setup.

## Daily workflow (summary)

```
Guest arrives     → Booking → Check-in → Room occupied
Housekeeping      → Dirty → Clean → Inspected
Restaurant        → Order → Kitchen queue → Served → Payment
Mini-mart         → Cart → Cash/Card OR charge to room
Guest departs     → Check-out → Invoice
Manager end of day → Reports
```

## Next steps

- [Installation](installation.md) — browsers, Android, offline notes
- [Navigation & UI](navigation-and-ui.md) — sidebar, mobile nav, languages
- [Troubleshooting & FAQ](troubleshooting-faq.md) — if something does not work
