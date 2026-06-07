# Guest portal

**Path:** Sidebar → **Guest Portal**

Staff-facing module to manage **in-stay guest communication**, service requests, and portal activity. Available to **Admin**, **Manager**, and **Reception**.

---

## Purpose

The guest portal bridges front desk operations and guests during an active stay:

| Function | Description |
|----------|-------------|
| **Service requests** | Guest asks for housekeeping, amenities, maintenance |
| **Messages** | Two-way communication log with guest |
| **Activity tracking** | Portal events recorded for audit |

Use alongside **Services**, **Messages**, and **Bookings** for a complete guest journey.

---

## Typical workflow

```
Guest checks in (Bookings)
    → Guest portal entry linked to stay
    → Guest/staff message or request
    → Reception assigns to Services / Housekeeping
    → Fulfillment logged → Audit trail updated
```

### Step-by-step (Reception)

1. Confirm guest has an **active booking** (checked in).
2. Open **Guest Portal** from the sidebar.
3. Select or create the portal session for the guest/room.
4. Record requests (extra towels, late checkout inquiry, etc.).
5. Cross-reference **Services** for billable items or **Housekeeping** for room tasks.
6. Review **Messages** for ongoing conversation history.

---

## Access control

| Role | Guest Portal |
|------|:------------:|
| Admin | ✓ |
| Manager | ✓ |
| Reception | ✓ |
| Housekeeper | — |
| Restaurant / Kitchen | — |

Kitchen and housekeeping staff use their own modules; portal is a **front-office** tool.

---

## Data and audit

Guest portal actions appear in **Audit Log / change logs** under category `guestportal`:

- Who made the change
- Timestamp
- Action type

Export audit data via **Settings → Export all data (CSV ZIP)** for compliance reviews.

---

## Integration map

| Module | Connection |
|--------|------------|
| **Bookings** | Active stay — room and guest context |
| **Guests** | Guest profile, VIP flags, contact info |
| **Services** | Billable spa, laundry, transport, etc. |
| **Messages** | Staff ↔ guest communication |
| **Invoices** | Charges from services may appear on checkout invoice |
| **Housekeeping** | Room status after guest requests |

---

## Best practices

1. **Link every request to a booking** when possible — avoids orphan charges.
2. **Use Messages** for anything that needs a paper trail.
3. **Train reception** to check portal at shift handover.
4. **Export backups** weekly if portal volume is high.

---

## Troubleshooting

| Issue | Check |
|-------|--------|
| Portal empty | Guest must be **checked in** |
| Cannot see module | Role must be Admin, Manager, or Reception |
| Missing history | Audit log filters; verify export includes `guestportal` |

---

## Related

- [Hotel operations](hotel-operations.md)
- [Services & billing](services-and-billing.md)
- [Accounts & audit](accounts-and-audit.md)
- [Visual guide](visual-guide.md)
