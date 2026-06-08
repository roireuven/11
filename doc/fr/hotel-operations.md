# Hotel operations

This guide covers the **hotel / PMS** modules: rooms, bookings, guests, housekeeping, and maintenance.

## Rooms

**Path:** Sidebar → **Rooms**

![Rooms grid — occupancy and housekeeping status](../en/assets/screenshots/05-rooms.png)

### Room overview

Grid/list of all rooms showing:

- Room number, floor, type
- Nightly rate
- Occupancy status: Available, Occupied, Reserved, Out of Service
- Housekeeping status

### Add / edit room

Fields include:

- Room number, floor, room type, bed configuration
- Max adults / children
- Price per night (hotel currency)
- Amenities (comma-separated)
- Housekeeping and occupancy status

### Room statuses

| Occupancy | Meaning |
|-----------|---------|
| Available | Ready to sell |
| Occupied | Guest in house |
| Reserved | Held for upcoming booking |
| Out of Service | Not sellable (maintenance) |

## Bookings

**Path:** Sidebar → **Bookings**

![Bookings module — guest stays and actions](../en/assets/screenshots/06-bookings.png)

### Create booking

1. Click **Add New Booking**
2. Enter guest name (or select from guest directory)
3. Choose check-in / check-out dates and times
4. Select an available room
5. Save — system may generate booking ID and invoice

### Booking actions

| Action | Description |
|--------|-------------|
| **Check In** | Mark guest arrived; room becomes occupied |
| **Check Out** | End stay; generates checkout invoice |
| **Invoice** | View or open related invoice |
| **Discount / Waive fee** | Manager-style adjustments |
| **Order service** | Add spa, laundry, etc. to stay |

Validation: check-out date must be after check-in.

## Guests

**Path:** Sidebar → **Guests**

Central guest directory:

- First/last name, passport, nationality, phone, email
- Date of birth, notes (allergies, preferences)
- VIP, frequent guest, blacklist flags
- Visit history

Guests link to bookings and room charges across restaurant and mini-mart.

## Housekeeping

**Path:** Sidebar → **Housekeeping**

![Housekeeping board by floor](../en/assets/screenshots/07-housekeeping.png)

### Housekeeping board

Visual board grouped by floor. **Tap a room card** to cycle status:

```
Dirty → In Progress → Clean → Inspected → (back to Dirty)
```

Out-of-service rooms may block status changes until maintenance is resolved.

### Report issue

From a room card, submit a **maintenance ticket** with description and priority.

## Maintenance

**Path:** Sidebar → **Maintenance**

Track tickets created from housekeeping or manual entry:

- Room, issue description, priority, status
- Resolve tickets before returning rooms to service

## Dashboard (hotel view)

Reception and Admin dashboards show:

- Room counts: available, occupied, dirty, out of service
- Tasks today (dirty rooms, OOS rooms)
- Bookings and invoices for selected date range
- Link to housekeeping board

## Typical front-desk flow

```
1. Create booking (or walk-in check-in)
2. Check in guest → room Occupied
3. Add services / room charges during stay
4. Check out → final invoice
5. Housekeeping sets room Dirty → Clean → Inspected → Available
```

## Related

- [Services & billing](services-and-billing.md)
- [User roles & permissions](user-roles-and-permissions.md) — Reception access
- [Reports](reports.md) — occupancy reporting
