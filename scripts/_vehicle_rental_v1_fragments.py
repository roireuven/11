"""JS/CSS fragments for vehicle rental module (cars & motorbikes)."""

VEHICLE_CSS = """
    .rent-vehicle-floor { display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.6rem; margin-bottom: 0.5rem; padding: 0.5rem; border-radius: 14px; background: linear-gradient(180deg, rgba(26,115,232,0.04) 0%, rgba(0,0,0,0.02) 100%); border: 1px solid rgba(26,115,232,0.12); }
    body.dark-mode .rent-vehicle-floor { background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.08); }
    .rent-vehicle-tile { border-radius: 14px; padding: 0.45rem 0.3rem 0.5rem; text-align: center; cursor: pointer; border: 3px solid transparent; font-weight: 700; font-size: 0.72rem; transition: transform 0.14s ease, box-shadow 0.14s ease; min-height: 96px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 0.06rem; font-family: inherit; position: relative; overflow: hidden; }
    .rent-vehicle-tile .rvt-icon { font-size: 1.5rem; line-height: 1; }
    .rent-vehicle-tile .rvt-plate { font-size: 0.78rem; font-weight: 900; letter-spacing: 0.02em; }
    .rent-vehicle-tile .rvt-tag { font-size: 0.55rem; font-weight: 900; letter-spacing: 0.1em; text-transform: uppercase; opacity: 0.92; }
    .rent-vehicle-tile .rvt-sub { font-size: 0.58rem; font-weight: 600; opacity: 0.88; line-height: 1.15; max-width: 100%; padding: 0 0.15rem; }
    .rent-vehicle-tile.available { background: linear-gradient(160deg, #a5d6a7 0%, #66bb6a 45%, #43a047 100%); color: #0d3d12; border-color: #2e7d32; }
    .rent-vehicle-tile.occupied { background: linear-gradient(160deg, #ff8a80 0%, #ef5350 40%, #c62828 100%); color: #3e0a0a; border-color: #b71c1c; }
    .rent-vehicle-tile.pending { background: linear-gradient(160deg, #ffd54f 0%, #ffb300 45%, #f57c00 100%); color: #4e2500; border-color: #ef6c00; animation: rest-tile-pulse 2.2s ease-in-out infinite; }
    .rent-vehicle-tile.maintenance { background: linear-gradient(160deg, #b0bec5 0%, #78909c 100%); color: #263238; border-color: #546e7a; opacity: 0.85; }
    @media (max-width: 640px) { .rent-vehicle-floor { grid-template-columns: repeat(3, 1fr); } }
"""

VEHICLE_DATA_INIT = """
let vehicles = load('vehicles', null);
if (vehicles == null || !Array.isArray(vehicles)) {
  vehicles = [
    { id: genId(), type: 'Car', brand: 'Toyota', model: 'Yaris', plateNumber: 'CAR-101', dailyRate: 45, hourlyRate: 8, status: 'Available', sortOrder: 1, visible: true },
    { id: genId(), type: 'Car', brand: 'Honda', model: 'City', plateNumber: 'CAR-102', dailyRate: 50, hourlyRate: 9, status: 'Available', sortOrder: 2, visible: true },
    { id: genId(), type: 'Motorbike', brand: 'Honda', model: 'PCX', plateNumber: 'MB-201', dailyRate: 18, hourlyRate: 4, status: 'Available', sortOrder: 3, visible: true },
    { id: genId(), type: 'Motorbike', brand: 'Yamaha', model: 'NMAX', plateNumber: 'MB-202', dailyRate: 20, hourlyRate: 4.5, status: 'Available', sortOrder: 4, visible: true }
  ];
  save('vehicles', vehicles);
}
let vehicleRentals = load('vehicleRentals', null);
if (vehicleRentals == null || !Array.isArray(vehicleRentals)) { vehicleRentals = []; save('vehicleRentals', vehicleRentals); }
let rentSelectedBooking = null;
let rentCrmGuestId = null;
"""

VEHICLE_MODULE_JS = r"""
function rentVehicleIcon(type) {
  return String(type || '').toLowerCase().indexOf('motor') >= 0 ? '🏍️' : '🚗';
}
function rentSortedVehicles() {
  return (vehicles || []).filter(rowDataVisible).slice().sort(function(a, b) {
    return (parseInt(a.sortOrder, 10) || 0) - (parseInt(b.sortOrder, 10) || 0);
  });
}
function rentGetActiveRentalForVehicle(vehicleId) {
  return (vehicleRentals || []).find(function(r) {
    return rowDataVisible(r) && r.vehicleId === vehicleId && r.status !== 'Completed' && r.status !== 'Cancelled';
  }) || null;
}
function rentGetVehicleFloorState(v) {
  if (!v || v.status === 'Maintenance') return 'maintenance';
  const active = rentGetActiveRentalForVehicle(v.id);
  if (!active) return 'available';
  if (active.paymentStatus === 'Pending' || active.status === 'Due') return 'pending';
  return 'occupied';
}
function rentFillContextFromSelection() {
  if (rentSelectedBooking) {
    const b = bookings.find(function(x) { return x.id === rentSelectedBooking; });
    if (b) {
      return {
        guestId: b.guestId || '',
        roomNumber: String(b.roomNumber != null ? b.roomNumber : ''),
        guestName: String(b.guestName != null ? b.guestName : ''),
        bookingId: (b.bookingId != null && b.bookingId !== '') ? String(b.bookingId) : String(b.id || '')
      };
    }
  }
  if (rentCrmGuestId) {
    const g = (guests || []).find(function(x) { return x.id === rentCrmGuestId; });
    if (g) {
      return { guestId: g.id, roomNumber: '—', guestName: String(guestDisplayNameFromProfile(g) || ''), bookingId: '' };
    }
  }
  return { guestId: '', roomNumber: '', guestName: '', bookingId: '' };
}
function rentCalcTotalPrice(vehicle, startIso, endIso) {
  const daily = parseFloat(vehicle && vehicle.dailyRate) || 0;
  if (!startIso || !endIso) return daily;
  try {
    const a = new Date(startIso);
    const b = new Date(endIso);
    if (isNaN(a.getTime()) || isNaN(b.getTime()) || b <= a) return daily;
    const hours = (b.getTime() - a.getTime()) / 3600000;
    const days = Math.max(1, Math.ceil(hours / 24));
    return Math.round(days * daily * 100) / 100;
  } catch (e) { return daily; }
}
function rentNextRentalNumber() {
  const nums = (vehicleRentals || []).map(function(r) {
    const m = String(r.rentalNumber || '').match(/(\d+)/);
    return m ? parseInt(m[1], 10) : 0;
  });
  const n = nums.length ? Math.max.apply(null, nums) + 1 : 1001;
  return 'RNT-' + n;
}
window.rentFloorClick = function(vehicleId) {
  const v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return;
  if (v.status === 'Maintenance') { toast(t('rental.inMaintenance')); return; }
  const active = rentGetActiveRentalForVehicle(vehicleId);
  if (active) rentOpenReturnModal(active.id);
  else rentOpenCheckoutModal(vehicleId);
};
window.rentOpenCheckoutModal = function(vehicleId) {
  const v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return;
  const ctx = rentFillContextFromSelection();
  const now = new Date();
  const end = new Date(now.getTime() + 86400000);
  const startVal = now.toISOString().slice(0, 16);
  const endVal = end.toISOString().slice(0, 16);
  openModal('<div class="modal-header"><h2>' + t('rental.checkoutTitle') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body">' +
    '<p style="font-size:0.85rem;margin:0 0 0.75rem;"><strong>' + rentVehicleIcon(v.type) + ' ' + escAttr(v.brand + ' ' + v.model) + '</strong> · ' + escAttr(v.plateNumber) + ' · ' + fmt$(v.dailyRate) + '/' + t('rental.perDay') + '</p>' +
    '<div class="form-group"><label>' + t('g.guest') + '</label><input type="text" class="form-control" id="rCkGuest" value="' + escAttr(ctx.guestName) + '" placeholder="' + t('rental.phGuest') + '"></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.roomNumber') + '</label><input type="text" class="form-control" id="rCkRoom" value="' + escAttr(ctx.roomNumber) + '"></div>' +
    '<div class="form-group"><label>' + t('rental.bookingRef') + '</label><input type="text" class="form-control" id="rCkBk" value="' + escAttr(ctx.bookingId) + '"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.startDate') + '</label><input type="datetime-local" class="form-control" id="rCkStart" value="' + startVal + '"></div>' +
    '<div class="form-group"><label>' + t('rental.endDate') + '</label><input type="datetime-local" class="form-control" id="rCkEnd" value="' + endVal + '"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.fuelOut') + '</label><select class="form-control" id="rCkFuel"><option>Full</option><option>3/4</option><option>1/2</option><option>1/4</option></select></div>' +
    '<div class="form-group"><label>' + t('rental.mileageOut') + '</label><input type="number" class="form-control" id="rCkMile" value="0" min="0"></div></div>' +
    '<div class="form-group"><label>' + t('g.total') + '</label><input type="number" class="form-control" id="rCkTotal" step="0.01" value="' + rentCalcTotalPrice(v, startVal, endVal) + '"></div>' +
    '<div class="form-group"><label>' + t('g.payment') + '</label><select class="form-control" id="rCkPay"><option value="Pending">' + t('rental.payPending') + '</option><option value="Charged to Room">' + t('rental.payRoom') + '</option><option value="Paid">' + t('rental.payPaid') + '</option></select></div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button><button class="btn btn-primary" onclick="rentSaveCheckout(\'' + v.id + '\')">' + t('rental.checkoutBtn') + '</button></div>');
};
window.rentSaveCheckout = function(vehicleId) {
  const v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return;
  const guestName = (document.getElementById('rCkGuest') && document.getElementById('rCkGuest').value.trim()) || '';
  if (!guestName) { toast(t('rental.needGuest')); return; }
  const total = parseFloat(document.getElementById('rCkTotal').value) || 0;
  const pay = document.getElementById('rCkPay').value;
  const rental = {
    id: genId(), rentalNumber: rentNextRentalNumber(), vehicleId: v.id,
    vehicleLabel: v.plateNumber + ' ' + v.brand + ' ' + v.model, vehicleType: v.type,
    guestId: rentCrmGuestId || '', guestName: guestName,
    roomNumber: document.getElementById('rCkRoom').value.trim(),
    bookingId: document.getElementById('rCkBk').value.trim(),
    startDate: document.getElementById('rCkStart').value,
    endDate: document.getElementById('rCkEnd').value,
    actualReturnDate: null, initialFuelLevel: document.getElementById('rCkFuel').value,
    returnFuelLevel: null, initialMileage: parseInt(document.getElementById('rCkMile').value, 10) || 0,
    returnMileage: null, totalPrice: total, paymentStatus: pay, status: 'Out',
    timestamp: new Date().toISOString(), staffName: currentUser ? currentUser.name : currentRole, visible: true
  };
  vehicleRentals.push(rental);
  v.status = 'Rented';
  save('vehicleRentals', vehicleRentals); save('vehicles', vehicles);
  if (pay === 'Paid' || pay === 'Charged to Room') {
    const txn = processSale({
      source: 'Vehicle Rental', orderId: rental.rentalNumber, guestName: rental.guestName,
      roomNumber: rental.roomNumber, bookingId: rental.bookingId,
      paymentMethod: pay === 'Charged to Room' ? 'Room Charge' : 'Cash',
      items: [{ name: rental.vehicleLabel + ' rental', qty: 1, unitPrice: total }],
      taxRate: parseFloat(settings.serviceTax || settings.taxRate) || 7
    });
    if (txn) { rental.transactionId = txn.transactionId; rental.paymentStatus = pay; }
  }
  save('vehicleRentals', vehicleRentals);
  logAudit('Checkout', 'Vehicle Rental', rental.rentalNumber, 'Checked out ' + v.plateNumber + ' to ' + guestName);
  closeModal(); renderVehicleRental(); toast(t('rental.checkedOut', { num: rental.rentalNumber }));
};
window.rentOpenReturnModal = function(rentalId) {
  const r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  const now = new Date().toISOString().slice(0, 16);
  openModal('<div class="modal-header"><h2>' + t('rental.returnTitle') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body">' +
    '<p style="font-size:0.85rem;">' + escAttr(r.rentalNumber) + ' · ' + escAttr(r.guestName) + ' · ' + escAttr(r.vehicleLabel) + '</p>' +
    '<div class="form-group"><label>' + t('rental.returnDate') + '</label><input type="datetime-local" class="form-control" id="rRtDate" value="' + now + '"></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.fuelIn') + '</label><select class="form-control" id="rRtFuel"><option>Full</option><option>3/4</option><option>1/2</option><option>1/4</option></select></div>' +
    '<div class="form-group"><label>' + t('rental.mileageIn') + '</label><input type="number" class="form-control" id="rRtMile" value="' + (r.initialMileage || 0) + '" min="0"></div></div>' +
    '<div class="form-group"><label>' + t('g.payment') + '</label><select class="form-control" id="rRtPay"><option value="Pending" ' + (r.paymentStatus === 'Pending' ? 'selected' : '') + '>' + t('rental.payPending') + '</option><option value="Charged to Room">' + t('rental.payRoom') + '</option><option value="Paid">' + t('rental.payPaid') + '</option></select></div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button><button class="btn btn-primary" onclick="rentCompleteReturn(\'' + r.id + '\')">' + t('rental.returnBtn') + '</button></div>');
};
window.rentCompleteReturn = function(rentalId) {
  const r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  r.actualReturnDate = document.getElementById('rRtDate').value;
  r.returnFuelLevel = document.getElementById('rRtFuel').value;
  r.returnMileage = parseInt(document.getElementById('rRtMile').value, 10) || 0;
  const pay = document.getElementById('rRtPay').value;
  r.status = 'Completed';
  const v = vehicles.find(function(x) { return x.id === r.vehicleId; });
  if (v) { v.status = 'Available'; save('vehicles', vehicles); }
  if (pay !== 'Pending' && !r.transactionId) {
    const txn = processSale({
      source: 'Vehicle Rental', orderId: r.rentalNumber, guestName: r.guestName,
      roomNumber: r.roomNumber, bookingId: r.bookingId,
      paymentMethod: pay === 'Charged to Room' ? 'Room Charge' : 'Cash',
      items: [{ name: r.vehicleLabel + ' rental', qty: 1, unitPrice: r.totalPrice }],
      taxRate: parseFloat(settings.serviceTax || settings.taxRate) || 7
    });
    if (txn) r.transactionId = txn.transactionId;
  }
  r.paymentStatus = pay;
  save('vehicleRentals', vehicleRentals);
  logAudit('Return', 'Vehicle Rental', r.rentalNumber, 'Returned ' + r.vehicleLabel);
  closeModal(); renderVehicleRental(); toast(t('rental.returned', { num: r.rentalNumber }));
};
window.showAddVehicle = function() {
  openModal('<div class="modal-header"><h2>' + t('rental.addVehicleTitle') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.type') + '</label><select class="form-control" id="mVType"><option>Car</option><option>Motorbike</option></select></div>' +
    '<div class="form-group"><label>' + t('rental.plate') + '</label><input type="text" class="form-control" id="mVPlate" placeholder="ABC-123"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.brand') + '</label><input type="text" class="form-control" id="mVBrand"></div>' +
    '<div class="form-group"><label>' + t('rental.model') + '</label><input type="text" class="form-control" id="mVModel"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.dailyRate') + '</label><input type="number" class="form-control" id="mVDaily" step="0.01" value="25"></div>' +
    '<div class="form-group"><label>' + t('rental.hourlyRate') + '</label><input type="number" class="form-control" id="mVHourly" step="0.01" value="5"></div></div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button><button class="btn btn-primary" onclick="addVehicle()">' + t('common.add') + '</button></div>');
};
window.addVehicle = function() {
  const plate = document.getElementById('mVPlate').value.trim();
  if (!plate) { toast(t('rental.needPlate')); return; }
  const maxSort = rentSortedVehicles().reduce(function(m, v) { return Math.max(m, parseInt(v.sortOrder, 10) || 0); }, 0);
  vehicles.push({
    id: genId(), type: document.getElementById('mVType').value, brand: document.getElementById('mVBrand').value.trim(),
    model: document.getElementById('mVModel').value.trim(), plateNumber: plate,
    dailyRate: parseFloat(document.getElementById('mVDaily').value) || 0,
    hourlyRate: parseFloat(document.getElementById('mVHourly').value) || null,
    status: 'Available', sortOrder: maxSort + 1, visible: true
  });
  save('vehicles', vehicles); closeModal(); renderVehicleRental(); toast(t('rental.vehicleAdded'));
};
function renderVehicleRental() {
  const pg = document.getElementById('page-vehiclerental');
  if (!pg) return;
  const list = rentSortedVehicles();
  const active = (vehicleRentals || []).filter(function(r) { return rowDataVisible(r) && r.status !== 'Completed' && r.status !== 'Cancelled'; });
  const avail = list.filter(function(v) { return rentGetVehicleFloorState(v) === 'available'; }).length;
  const out = active.length;
  const due = active.filter(function(r) { return r.status === 'Due' || r.paymentStatus === 'Pending'; }).length;
  let tiles = '';
  list.forEach(function(v) {
    const st = rentGetVehicleFloorState(v);
    const ar = rentGetActiveRentalForVehicle(v.id);
    const tag = st === 'available' ? t('rental.stAvailable') : st === 'occupied' ? t('rental.stOut') : st === 'pending' ? t('rental.stDue') : t('rental.stMaint');
    const sub = ar ? (ar.guestName || '') : (v.brand + ' ' + v.model);
    tiles += '<button type="button" class="rent-vehicle-tile ' + st + '" onclick="rentFloorClick(\'' + v.id + '\')">' +
      '<span class="rvt-icon">' + rentVehicleIcon(v.type) + '</span>' +
      '<span class="rvt-plate">' + escAttr(v.plateNumber) + '</span>' +
      '<span class="rvt-tag">' + tag + '</span>' +
      '<span class="rvt-sub">' + escAttr(sub) + '</span></button>';
  });
  const bkOpts = getBookingsForGuestPicker().map(function(b) {
    return '<option value="' + b.id + '"' + (rentSelectedBooking === b.id ? ' selected' : '') + '>' + escAttr(b.roomNumber + ' — ' + b.guestName) + '</option>';
  }).join('');
  const gstOpts = getGuestDirectoryOnlyForPicker().map(function(g) {
    return '<option value="' + g.id + '"' + (rentCrmGuestId === g.id ? ' selected' : '') + '>' + escAttr(guestDisplayNameFromProfile(g)) + '</option>';
  }).join('');
  pg.innerHTML =
    '<div class="card"><div class="card-header" style="flex-wrap:wrap;gap:0.5rem;"><h2>' + t('pageTitle.vehiclerental') + '</h2>' +
    '<div style="display:flex;gap:0.35rem;flex-wrap:wrap;"><button type="button" class="btn btn-sm btn-primary" onclick="showAddVehicle()">+ ' + t('rental.addVehicle') + '</button></div></div>' +
    '<div class="card-body">' +
    '<div class="stats-grid" style="margin-bottom:0.75rem;">' +
    '<div class="stat-card"><div class="stat-info"><h3>' + avail + '</h3><p>' + t('rental.stAvailable') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + out + '</h3><p>' + t('rental.stOut') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + due + '</h3><p>' + t('rental.stDue') + '</p></div></div></div>' +
    '<div class="form-row" style="margin-bottom:0.75rem;"><div class="form-group"><label>' + t('rental.linkBooking') + '</label><select class="form-control" id="rentBkSel" onchange="rentSelectedBooking=this.value||null;rentCrmGuestId=null;renderVehicleRental()"><option value="">' + t('rental.pickBooking') + '</option>' + bkOpts + '</select></div>' +
    '<div class="form-group"><label>' + t('rental.linkGuest') + '</label><select class="form-control" id="rentGstSel" onchange="rentCrmGuestId=this.value||null;rentSelectedBooking=null;renderVehicleRental()"><option value="">' + t('rental.pickGuest') + '</option>' + gstOpts + '</select></div></div>' +
    '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.5rem;">' + t('rental.floorHint') + '</p>' +
    '<div class="rent-vehicle-floor">' + (tiles || '<p>' + t('rental.noVehicles') + '</p>') + '</div></div></div>' +
    '<div class="card"><div class="card-header"><h2>' + t('rental.activeRentals') + '</h2></div><div class="card-body"><div id="rentActiveGrid"></div></div></div>' +
    '<div class="card"><div class="card-header"><h2>' + t('rental.reportTitle') + '</h2></div><div class="card-body"><div id="rentReportGrid"></div></div></div>';
  new XGrid('rentActiveGrid', {
    columns: [
      {field:'rentalNumber',label:t('rental.rentalNum'),filterable:true,width:'95px'},
      {field:'vehicleLabel',label:t('rental.vehicle'),filterable:true},
      {field:'guestName',label:t('g.guest'),filterable:true},
      {field:'roomNumber',label:t('g.roomNumber'),width:'75px'},
      {field:'startDate',label:t('rental.startDate'),width:'130px'},
      {field:'endDate',label:t('rental.endDate'),width:'130px'},
      {field:'totalPrice',label:t('g.total'),format:function(v){return fmt$(v);},width:'85px'},
      {field:'paymentStatus',label:t('g.payment'),filterable:true,width:'110px'},
      {field:'status',label:t('g.status'),filterable:true,width:'90px'}
    ],
    data: active,
    showSearch: true,
    emptyMessage: t('rental.noActive'),
    actions: [
      {name:'return',label:t('rental.returnBtn'),cls:'btn-primary',handler:function(id){ rentOpenReturnModal(id); }},
      {name:'view',label:t('common.view'),cls:'btn-outline',handler:function(id){
        const r = vehicleRentals.find(function(x){return x.id===id;});
        if(r) toast(r.rentalNumber + ' · ' + r.guestName);
      }}
    ]
  });
  const completed = (vehicleRentals || []).filter(rowDataVisible).slice().reverse();
  new XGrid('rentReportGrid', {
    columns: [
      {field:'rentalNumber',label:t('rental.rentalNum'),filterable:true},
      {field:'vehicleType',label:t('rental.type'),filterable:true,width:'90px'},
      {field:'guestName',label:t('g.guest'),filterable:true},
      {field:'totalPrice',label:t('g.total'),format:function(v){return fmt$(v);}},
      {field:'paymentStatus',label:t('g.payment'),filterable:true},
      {field:'status',label:t('g.status'),filterable:true},
      {field:'timestamp',label:t('g.date'),format:function(v){try{return new Date(v).toLocaleString();}catch(e){return v;}},width:'140px'}
    ],
    data: completed,
    showSearch: true,
    summaryRow: {totalPrice:'sum'},
    emptyMessage: t('rental.noHistory')
  });
}
"""
