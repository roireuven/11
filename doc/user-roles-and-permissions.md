# User roles & permissions

The app uses **role-based access control (RBAC)**. After login, the sidebar hides pages your role cannot access.

**Note:** The internal role name for front desk is `Receptionist`; the UI displays **Reception**.

## Roles summary

| Role | Default landing page | Access level |
|------|---------------------|--------------|
| **Admin** | Dashboard | **All pages** |
| **Manager** | Reports | Operations + F&B + reports (no accounts/settings/audit admin) |
| **Reception** | Rooms | Front office + guest services + F&B sales |
| **Housekeeper** | Housekeeping | Housekeeping + maintenance only |
| **Restaurant** | Restaurant | Restaurant, menu items, inventory |
| **Kitchen** | Restaurant (as **Kitchen**) | Restaurant view — kitchen queue only |

## Page access matrix

Pages listed below are **visible** for each role. All others are hidden.

| Page | Admin | Manager | Reception | Housekeeper | Restaurant | Kitchen |
|------|:-----:|:-------:|:---------:|:-----------:|:----------:|:-------:|
| Dashboard | ✓ | ✓ | ✓ | ✓ | — | — |
| Rooms | ✓ | ✓ | ✓ | — | — | — |
| Bookings | ✓ | ✓ | ✓ | — | — | — |
| Guests | ✓ | ✓ | ✓ | — | — | — |
| Housekeeping | ✓ | ✓ | — | ✓ | — | — |
| Maintenance | ✓ | ✓ | — | ✓ | — | — |
| Services | ✓ | ✓ | ✓ | — | — | — |
| Invoices | ✓ | ✓ | ✓ | — | — | — |
| Inventory | ✓ | ✓ | ✓ | — | ✓ | — |
| Mini-Mart | ✓ | ✓ | ✓ | — | — | — |
| Restaurant | ✓ | ✓ | ✓ | — | ✓ | ✓* |
| Menu Items | ✓ | ✓ | ✓ | — | ✓ | — |
| Store Items | ✓ | ✓ | — | — | — | — |
| Order History | ✓ | ✓ | — | — | — | — |
| Guest Portal | ✓ | ✓ | ✓ | — | — | — |
| Reports | ✓ | ✓ | — | — | — | — |
| Accounts | ✓ | — | — | — | — | — |
| Transactions | ✓ | — | — | — | — | — |
| Messages | ✓ | — | — | — | — | — |
| Audit Log | ✓ | — | — | — | — | — |
| Dropdown Lists | ✓ | — | — | — | — | — |
| Settings | ✓ | — | — | — | — | — |

\* **Kitchen** sees the Restaurant page relabeled **Kitchen** — payment and order-creation actions are restricted.

## Kitchen restrictions

Kitchen staff **cannot**:

- Create new orders (use Restaurant login)
- Take payment
- Close paid tabs

Kitchen **can**:

- View the live kitchen queue (New → Preparing → Ready)
- Advance order status as food is prepared

## Restaurant restrictions

Restaurant staff **cannot**:

- Access room management, bookings admin, accounts, or settings
- See **Store Items** or **Order History** in sidebar (Manager/Admin only for store items)

If Restaurant tries to open Menu Items or Inventory via shortcuts without permission, a toast explains the page is unavailable.

## Managing accounts

Only **Admin** can open **Accounts** to:

- Add/edit/deactivate users
- Assign roles
- Control who sees which modules

## Best practices

1. Give each staff member their own email/login
2. Use **Kitchen** role on kitchen tablets, **Restaurant** on waitstaff devices
3. Reserve **Admin** for owners and IT
4. Use **Manager** for supervisors who need reports but not system config

## Related

- [Demo credentials](demo-credentials.md)
- [Accounts & audit](accounts-and-audit.md)
- [Navigation & UI](navigation-and-ui.md)
