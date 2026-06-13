# Vehicle rental (cars & motorbikes)

The **Vehicle Rental** module is a boutique fleet system for small-scale car and motorbike operations. It combines a visual **fleet floor** (like restaurant tables), **conflict-free scheduling**, **guest/booking linking**, **WhatsApp/SMS messaging**, **pick-up/drop-off locations**, **digital contracts**, and **per-vehicle profit tracking**.

## Who can access it

| Role | Access |
|------|--------|
| **Admin** | Full access |
| **Manager** | Full access |
| **Reception** | Full access |
| **Other roles** | Module hidden |

Open from the sidebar: **Services → Vehicle Rental** (🚗 icon).

## Three views (tabs)

| Tab | Purpose |
|-----|---------|
| **Fleet floor** | Color-coded tiles — tap to check out or open rental details |
| **Schedule grid** | 7-day calendar per vehicle — prevents overbooking visually |
| **Fleet P&L** | Revenue vs expenses per vehicle, maintenance scheduling |

## Conflict prevention (no overbooking)

Before checkout, the system checks whether the vehicle is already:

- Rented for overlapping dates
- Blocked for **maintenance** in that window

If there is a conflict, checkout is **blocked** and a warning appears. The **Schedule grid** tab shows booked days (red), maintenance (grey), and completed rentals (blue).

## Guest & booking linking

Use the **searchable guest card grid** (same pattern as restaurant room service):

- Tap an **in-house booking** card to pre-fill guest, room, and booking reference
- Tap a **CRM guest** card for walk-in customers

Phone and email are pulled from the guest profile when available.

## Pick-up / drop-off locations

At checkout, choose **pick-up** and **drop-off** locations:

| Preset | Delivery fee |
|--------|----------------|
| Hotel front desk | Free |
| Airport | +$15 |
| Train station | +$10 |
| Custom delivery | +$20 |

Delivery fees are added to the rental total automatically. Use **Open map** in the rental detail modal for Google Maps links.

## Checkout flow

1. Select guest/booking from the card grid (optional).
2. Tap an **available** (green) vehicle on the fleet floor.
3. Confirm dates, locations, fuel/odometer, deposit, and payment method.
4. Guest signs on the **digital signature pad** and enters printed name.
5. Tap **Check out** — rental posts to transactions if paid or charged to room.

## Customer messaging (WhatsApp / SMS / Email)

From the **Rental details** modal or active rentals grid:

| Button | Action |
|--------|--------|
| **WhatsApp** | Opens WhatsApp with booking confirmation text |
| **SMS** | Opens SMS app with return reminder |
| **Email contract** | Opens email client with agreement summary |
| **Send location** | WhatsApp with pick-up location and map link |

Requires guest **phone** (WhatsApp/SMS) or **email** on the rental record.

## Return

1. Tap an occupied vehicle or use **Return** on the active rentals grid.
2. Enter return date, fuel/mileage in, and **extra charges** (fuel, damage, late fee).
3. Settle payment if still pending.

## Digital contract & PDF

- Signature and printed name stored on the rental record
- **Print contract** generates a printable rental agreement (browser print → save as PDF)
- **Email contract** sends summary via the guest's email app

## Fleet P&L & maintenance

On the **Fleet P&L** tab, each vehicle shows:

- **Revenue** from completed rentals
- **Expenses** (insurance, registration, repair, fuel, other)
- **Net profit**

Actions per vehicle:

- **+ Add expense** — log cost against that vehicle
- **Schedule maintenance** — block dates on the calendar and mark vehicle as maintenance (grey tile)

## Active rentals & history

- **Active rentals** grid — view details, return, or send WhatsApp
- **Rental history** — completed rentals with revenue totals
- Export fleet data via **Settings → Backup** (vehicles, rentals, expenses CSV)

## Integration

- **Transactions** — `source: Vehicle Rental`
- **Dashboard** — rental revenue in hotel totals
- **Audit log** — checkout and return events

## Related guides

- [Hotel operations](hotel-operations.md) — bookings and guests
- [Restaurant & kitchen](restaurant-and-kitchen.md) — similar floor and guest-picker patterns
- [Guest QR orders](guest-qr-orders.md) — guest messaging patterns
- [Reports](reports.md) — revenue reporting
- [Data model](data-model.md) — entities
