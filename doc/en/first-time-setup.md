# First-time setup

## When setup appears

The **First-Time Setup** screen shows when:

- No prior setup exists in this browser/device storage
- You open the URL with `?newsetup=1` (forces new setup — **one browser only**)

Screen title: **Welcome to HotelRestaurantMini-MartManagement — v2.0 — First-Time Setup**

![First-time setup — email, password, Create Account](/doc/en/assets/screenshots/01-login.png)

## What you create

| Field | Purpose |
|-------|---------|
| **Email** | Primary system login; also defines your **data namespace** |
| **Password** | Login password (minimum 4 characters) |

After setup, the app:

1. Saves `setupEmail`, `setupPassword`, `setupDone` in storage
2. Sets `hotel_mgr_dataNamespace` from your email (isolates your data)
3. Creates an **Admin** account for that email
4. May load bundled sample catalog data (menu/minimart templates) for new namespaces

## Setup wizard messaging

The setup screen explains three principles:

1. **Sign in anywhere** — use email + password on any device (with export/import for web sync)
2. **Sync across devices** — same email on multiple installs shares data when storage is synced (Android SQLite per device; web requires manual import/export)
3. **Role-based access** — assign staff roles after first login

## After setup

1. You are signed in as **Admin**
2. Go to **Settings** and configure hotel details
3. Open **Accounts** to add staff with roles Reception, Restaurant, Kitchen, etc.

## Reset setup

To start completely fresh:

**Settings → Danger zone → Full wipe and new setup**

This removes:

- All business data (rooms, bookings, orders, etc.)
- System email and password
- Data namespace

You will return to the first-time setup screen.

## URL parameters

| Parameter | Effect |
|-----------|--------|
| `?newsetup=1` | Show setup even if setup was done (use carefully) |

Example: `https://hotel-restaurant-minimart.firebaseapp.com/?newsetup=1`

## Validation rules

- Email must contain `@`
- Password must be at least **4 characters**
- Storage must be available (not blocked by browser privacy settings)

If storage is blocked, the app shows an error asking you to allow site data/cookies.

## Android vs web

Both platforms run the same setup flow. On Android, credentials and settings are also written to SQLite via `HotelDB`.

## Related

- [Demo credentials](demo-credentials.md) — skip setup and use demo users
- [Backup, restore & data](backup-restore-and-data.md) — export before reset
