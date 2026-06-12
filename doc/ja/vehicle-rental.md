# Vehicle rental (cars & motorbikes)

The **Vehicle Rental** module lets front desk and management staff rent **cars** and **motorbikes** to hotel guests and walk-in customers. It uses a visual **fleet floor** (similar to restaurant table tiles), links rentals to **guests** and **bookings**, records **checkout/return**, and posts revenue to **transactions** and the **dashboard**.

## Who can access it

| Role | Access |
|------|--------|
| **Admin** | Full access |
| **Manager** | Full access |
| **Reception** | Full access |
| **Other roles** | Module hidden |

Open from the sidebar: **Services → Vehicle Rental** (🚗 icon).

## Fleet floor

The main screen shows a grid of vehicle tiles:

| Tile color | Meaning |
|------------|---------|
| **Green** | Available — tap to start checkout |
| **Red** | Rented out (active rental) — tap to process return |
| **Amber** | Due / payment pending |
| **Grey** | Maintenance — not rentable |

Each tile shows the vehicle type icon (🚗 car or 🏍️ motorbike), **plate number**, and status label.

On phones the grid uses three columns; on desktop, five columns.

## Checkout (rent out)

1. Optionally select a **booking** or **guest** from the pickers at the top (fills guest name, room, booking reference).
2. Tap an **available** (green) vehicle.
3. In the checkout modal, confirm or edit:
   - Guest name, room number, booking reference
   - Start and end date/time
   - Fuel level out, odometer out
   - Daily rate (from vehicle profile)
   - Deposit and payment method
   - Notes
4. Tap **Check out** — the rental is created, the vehicle tile turns red, and a **transaction** is recorded with source **Vehicle Rental**.

Rental numbers use the format `RNT-1001`, `RNT-1002`, etc.

## Return

1. Tap an **occupied** (red) or **pending** (amber) vehicle.
2. In the return modal, enter:
   - Return date/time
   - Fuel level in, odometer in
   - Extra charges (fuel, damage, late fee) if any
   - Final payment / balance
3. Tap **Complete return** — rental status becomes **Completed**, vehicle returns to **Available**, and any balance posts to transactions.

## Active rentals & history

Below the fleet floor:

- **Active rentals** — grid of open rentals with guest, vehicle, dates, and total
- **Rental history** — completed and cancelled rentals

Use **Export CSV** on the module header to back up rental data.

## Vehicle management

Use **+ Add vehicle** to register fleet items:

| Field | Description |
|-------|-------------|
| Type | Car or Motorbike |
| Brand / Model | e.g. Toyota Yaris |
| Plate number | Unique ID on the floor |
| Daily rate / Hourly rate | Pricing |
| Status | Available or Maintenance |
| Sort order | Tile position on the floor |

Edit or hide vehicles with the row actions. Hidden vehicles respect the same visibility rules as other data rows.

## Integration with hotel & billing

- **Guest picker** — link rental to an existing guest profile
- **Booking picker** — pre-fill guest, room, and booking ID from an active reservation
- **Transactions** — checkout and return create rows with `source: Vehicle Rental`
- **Dashboard** — vehicle rental revenue included in shift and daily totals
- **Audit log** — checkout and return actions logged

## Reports

Vehicle rental revenue appears in:

- **Dashboard** shift summaries
- **Reports** — filter transactions by source **Vehicle Rental**
- **All Transactions** (Admin) — full ledger

## Default demo fleet

On first use, the app seeds sample vehicles (two cars, two motorbikes) if the fleet is empty. Replace these with your property's real fleet in production.

## Related guides

- [Hotel operations](hotel-operations.md) — bookings and guests
- [Services & billing](services-and-billing.md) — invoices and charges
- [Reports](reports.md) — revenue reporting
- [Navigation & UI](navigation-and-ui.md) — sidebar and mobile layout
- [Data model](data-model.md) — `vehicles` and `vehicleRentals` entities
