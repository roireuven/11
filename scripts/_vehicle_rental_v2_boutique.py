"""Boutique car rental v2 — calendar, conflict prevention, messaging, locations, contract, expenses."""

VEHICLE_V2_CSS = """
    .rent-tabs { display: flex; gap: 0.35rem; flex-wrap: wrap; margin-bottom: 0.75rem; }
    .rent-tab { padding: 0.35rem 0.75rem; border-radius: 999px; border: 1px solid var(--border); background: var(--card-bg); cursor: pointer; font-size: 0.82rem; font-weight: 600; }
    .rent-tab.active { background: var(--primary); color: #fff; border-color: var(--primary); }
    .rent-floor-summary { display: flex; flex-wrap: wrap; gap: 0.5rem 1rem; font-size: 0.78rem; color: var(--text-light); margin: 0 0 0.5rem; }
    .rent-floor-summary span { display: inline-flex; align-items: center; gap: 0.3rem; }
    .rent-legend-dot { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
    .rent-cal-wrap { overflow-x: auto; margin-bottom: 0.75rem; }
    .rent-cal-grid { width: 100%; border-collapse: collapse; font-size: 0.72rem; min-width: 520px; }
    .rent-cal-grid th, .rent-cal-grid td { border: 1px solid var(--border); padding: 0.35rem 0.25rem; text-align: center; }
    .rent-cal-grid th:first-child, .rent-cal-grid td:first-child { text-align: left; min-width: 5.5rem; font-weight: 700; }
    .rent-cal-free { background: rgba(76,175,80,0.12); }
    .rent-cal-booked { background: rgba(244,67,54,0.35); font-weight: 700; color: #b71c1c; }
    .rent-cal-maint { background: rgba(120,144,156,0.35); }
    .rent-cal-done { background: rgba(33,150,243,0.2); }
    .rent-pnl-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.65rem; }
    .rent-pnl-card { border: 1px solid var(--border); border-radius: 12px; padding: 0.65rem 0.75rem; background: var(--card-bg); }
    .rent-pnl-card h4 { margin: 0 0 0.35rem; font-size: 0.9rem; }
    .rent-pnl-row { display: flex; justify-content: space-between; font-size: 0.78rem; margin: 0.15rem 0; }
    .rent-pnl-net { font-weight: 800; margin-top: 0.35rem; padding-top: 0.35rem; border-top: 1px dashed var(--border); }
    .rent-conflict-warn { background: #fff3e0; border: 1px solid #ffb74d; border-radius: 8px; padding: 0.5rem 0.65rem; font-size: 0.82rem; color: #e65100; margin: 0.5rem 0; }
    .rent-sig-wrap { border: 1px dashed var(--border); border-radius: 8px; padding: 0.35rem; margin: 0.5rem 0; }
    .rent-sig-wrap canvas { width: 100%; max-width: 320px; height: 80px; background: #fff; border-radius: 6px; touch-action: none; cursor: crosshair; }
    body.dark-mode .rent-sig-wrap canvas { background: #1e293b; }
    .rent-comm-btns { display: flex; flex-wrap: wrap; gap: 0.35rem; margin-top: 0.5rem; }
    .rent-guest-search { margin-bottom: 0.5rem; }
"""

VEHICLE_V2_DATA = """
let vehicleExpenses = load('vehicleExpenses', null);
if (vehicleExpenses == null || !Array.isArray(vehicleExpenses)) { vehicleExpenses = []; save('vehicleExpenses', vehicleExpenses); }
let vehicleMaintBlocks = load('vehicleMaintBlocks', null);
if (vehicleMaintBlocks == null || !Array.isArray(vehicleMaintBlocks)) { vehicleMaintBlocks = []; save('vehicleMaintBlocks', vehicleMaintBlocks); }
let rentLocations = load('rentLocations', null);
if (rentLocations == null || !Array.isArray(rentLocations)) {
  rentLocations = [
    { id: 'hotel', name: 'Hotel front desk', address: 'On-site pickup', mapsUrl: '', deliveryFee: 0, visible: true },
    { id: 'airport', name: 'Airport', address: 'Airport terminal', mapsUrl: 'https://maps.google.com/?q=airport', deliveryFee: 15, visible: true },
    { id: 'station', name: 'Train station', address: 'Central station', mapsUrl: 'https://maps.google.com/?q=train+station', deliveryFee: 10, visible: true },
    { id: 'custom', name: 'Custom delivery', address: 'Agreed location', mapsUrl: '', deliveryFee: 20, visible: true }
  ];
  save('rentLocations', rentLocations);
}
window.rentViewMode = window.rentViewMode || 'floor';
window.rentCalStart = window.rentCalStart || null;
window.rentGuestSearch = window.rentGuestSearch || '';
"""
