# Services & billing

## Services catalog

**Path:** Sidebar → **Services**

Define sellable services (spa, laundry, airport transfer, etc.):

- Service name, category, price
- Linked to guest stays and invoices

### Order service on a booking

From a booking, open **Order service**:

1. Select service
2. Set quantity
3. Add line items to the stay bill

## Invoices

**Path:** Sidebar → **Invoices**

View and manage invoices generated from:

- Check-in / check-out
- Room services
- Taxes and surcharges

Invoice fields follow hotel settings (default tax %, service tax %, currency).

## Check-in / check-out billing

| Event | Billing behavior |
|-------|------------------|
| **Check-in** | May create or link opening invoice |
| **During stay** | Restaurant/mini-mart can charge to room |
| **Check-out** | Final invoice with all room charges |

Messages confirm actions, e.g. *"{guest} checked out. Invoice {inv} generated."*

## Discounts

From booking/invoice flows:

- Apply **discount %** with reason
- **Waive fee** for penalties or adjustments

Default discount reason in settings: *Manager discount*

## Payment methods

Configured under **Dropdown Lists → Payment methods / Payment types**.

Used across POS, restaurant, mini-mart, and invoice settlement.

## Room charges from F&B and shop

Restaurant **room service** and mini-mart **Put bill on customer** add charges to the guest's active folio before final checkout payment.

Department breakdown in reports:

> Restaurant · Mini-Mart · Hotel (PMS) · POS

## Related

- [Hotel operations](hotel-operations.md)
- [Restaurant & kitchen](restaurant-and-kitchen.md)
- [Mini-mart & POS](minimart-and-pos.md)
- [Settings & configuration](settings-and-configuration.md) — tax rates
