# Troubleshooting & FAQ

## Login & setup

### "Please enter email and password"
Both fields are required. Password is case-sensitive.

### "App is still loading"
Wait a few seconds for the large SPA to finish parsing, then retry setup.

### "Storage blocked"
Browser blocked `localStorage`. Allow cookies/site data for the Firebase domain or install Android app.

### Setup screen keeps appearing
Storage was cleared or you are in a new browser profile. Restore from backup import or run setup again.

### Demo login does not work
Use password `1234`. Ensure setup is complete or demo accounts exist. Try `admin@hotel.com`.

### Login screen blank or "Sign In" does nothing
Hard refresh (**Ctrl+Shift+R** / **Cmd+Shift+R**). An old cached bundle could block JavaScript from loading. Deploy v2.1+ includes quote-escape fixes for Restaurant QR buttons.

## Guest QR orders

### Order number dropdown does not open
The QR modal uses a **native browser dropdown** for order numbers 1–60 (custom select picker sits below full-screen modals). Hard refresh if you still see no list.

### QR code area empty
Select an **order number** first. QR and link generate only after a slot 1–60 is chosen.

### Guest scan opens blank page
Confirm menu items (restaurant) or store items (mini-mart) exist and are **available**. Test with **Open order screen** from the staff QR modal.

### QR Orders Report shows no rows
No guest QR orders yet — complete a test scan and submit from a phone.

See [Guest QR orders](guest-qr-orders.md).

## Data & sync

### Changes not visible on another computer
Web uses **localStorage per browser**. Export from device A, import on device B.

### Kitchen not seeing new orders
Same browser/device storage must be shared. Kitchen and Restaurant on different browsers will **not** sync on web.

### Lost all data after browser update
Restore from **Settings export** if available. Otherwise data may be unrecoverable on web.

## Roles & navigation

### "Menu Items page is not available for this role"
Expected for Kitchen/Housekeeper. Sign in as Restaurant, Reception, Manager, or Admin.

### Kitchen cannot take payment
By design. Use Restaurant or Reception role to close tabs.

### Missing Settings or Accounts
Admin role only. Sign in as setup email or Admin account.

## Restaurant & mini-mart

### "Not enough stock"
Increase inventory quantity or reduce cart quantity.

### "Cart is empty"
Add store/menu items before payment or room charge.

### "No unpaid bill to settle"
Use **Put bill on customer** first for room charges, or pay cart with Cash/Card.

### Room service guest not listed
Guest must be **checked in**. Verify booking status on Bookings page.

## Housekeeping

### Cannot change room status
Room may be **Out of Service** — resolve maintenance ticket first.

## Currency & locale

### Wrong currency symbol
Update **Settings → Currency** and currency labels in Dropdown Lists.

### LAK missing
Add LAK under **Dropdown Lists → Currencies** (Settings shows hint for Lao UI).

## Firebase / hosting

### 404 on Firebase URL
Verify project hosting is deployed. Try [web.app](https://hotel-restaurant-minimart.web.app/) mirror.

### Old version after deploy
Hard refresh (Ctrl+Shift+R) — `index.html` uses no-cache headers but CDN/browser may cache aggressively on first load. After v2.1, verify bottom nav shows **Restaurant QR** and **Mini-Mart QR** labels.

## Android

### APK install blocked
Enable **Install unknown apps** for Chrome/Files (see landing page install guide).

### Data after reinstall
SQLite cleared on uninstall. Restore from export backup.

## Getting help

1. Check [Getting started](getting-started.md)
2. Review [User roles & permissions](user-roles-and-permissions.md)
3. Export logs/data before **Factory reset**
4. Full doc index: [README](README.md)
