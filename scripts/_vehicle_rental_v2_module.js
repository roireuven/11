/* Boutique car rental v2 — loaded by patch-app-vehicle-rental.py */

function rentVehicleIcon(type) {
  return String(type || '').toLowerCase().indexOf('motor') >= 0 ? '🏍️' : '🚗';
}
function rentParseDt(v) {
  if (!v) return null;
  try {
    var d = new Date(String(v).length <= 10 ? String(v) + 'T12:00:00' : v);
    return isNaN(d.getTime()) ? null : d;
  } catch (e) { return null; }
}
function rentRangesOverlap(a0, a1, b0, b1) {
  if (!a0 || !a1 || !b0 || !b1) return false;
  return a0 < b1 && b0 < a1;
}
function rentHasConflict(vehicleId, startIso, endIso, excludeRentalId) {
  var a0 = rentParseDt(startIso);
  var a1 = rentParseDt(endIso);
  if (!a0 || !a1 || a1 <= a0) return true;
  var hit = false;
  (vehicleMaintBlocks || []).forEach(function(b) {
    if (hit || !rowDataVisible(b) || b.vehicleId !== vehicleId) return;
    if (rentRangesOverlap(a0, a1, rentParseDt(b.startDate), rentParseDt(b.endDate))) hit = true;
  });
  if (hit) return true;
  (vehicleRentals || []).forEach(function(r) {
    if (hit || !rowDataVisible(r) || r.vehicleId !== vehicleId) return;
    if (excludeRentalId && r.id === excludeRentalId) return;
    if (r.status === 'Completed' || r.status === 'Cancelled') return;
    var re = rentParseDt(r.actualReturnDate) || rentParseDt(r.endDate);
    if (rentRangesOverlap(a0, a1, rentParseDt(r.startDate), re || rentParseDt(r.endDate))) hit = true;
  });
  return hit;
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
function rentSyncOverdueRentals() {
  var now = new Date();
  var changed = false;
  (vehicleRentals || []).forEach(function(r) {
    if (!rowDataVisible(r) || r.status === 'Completed' || r.status === 'Cancelled') return;
    var end = rentParseDt(r.endDate);
    if (end && end < now && r.status !== 'Due') { r.status = 'Due'; changed = true; }
  });
  if (changed) save('vehicleRentals', vehicleRentals);
}
function rentGetVehicleFloorState(v) {
  if (!v || v.status === 'Maintenance') return 'maintenance';
  var active = rentGetActiveRentalForVehicle(v.id);
  if (!active) return 'available';
  if (active.paymentStatus === 'Pending' || active.status === 'Due') return 'pending';
  return 'occupied';
}
function rentGetFleetStats() {
  rentSyncOverdueRentals();
  var list = rentSortedVehicles();
  var active = (vehicleRentals || []).filter(function(r) { return rowDataVisible(r) && r.status !== 'Completed' && r.status !== 'Cancelled'; });
  var today = (typeof dashYmd === 'function') ? dashYmd(new Date()) : new Date().toISOString().slice(0, 10);
  var todayRev = 0;
  (transactions || []).forEach(function(tx) {
    if (!rowDataVisible(tx) || tx.source !== 'Vehicle Rental') return;
    if (typeof dashTimestampDay === 'function' && dashTimestampDay(tx.timestamp) === today) todayRev += parseFloat(tx.grandTotal) || 0;
  });
  return {
    total: list.length,
    avail: list.filter(function(v) { return rentGetVehicleFloorState(v) === 'available'; }).length,
    out: active.length,
    due: active.filter(function(r) { return r.status === 'Due' || r.paymentStatus === 'Pending'; }).length,
    todayRev: rentRoundMoney(todayRev)
  };
}
function rentEnsureShiftOpen() {
  if (typeof getActiveWorkPeriod !== 'function') return true;
  if (getActiveWorkPeriod('Vehicle Rental')) return true;
  if (typeof toast === 'function') toast(typeof t === 'function' ? t('msg.workPeriodNoActive') : 'Open a shift on the dashboard first.');
  return false;
}
function rentRenderShiftNoticeHtml() {
  if (typeof getActiveWorkPeriod !== 'function') return '';
  var wp = getActiveWorkPeriod('Vehicle Rental');
  if (wp) return '';
  return '<div class="work-period-bar card rent-shift-notice" style="border-left:4px solid #c62828;margin-bottom:0.75rem;box-shadow:0 2px 8px rgba(0,0,0,0.06);">' +
    '<div class="card-body" style="display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:0.75rem;">' +
    '<div><strong style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;color:var(--text-light);">' +
    (typeof t === 'function' ? t('dashboard.rentalShift') : 'Vehicle rental shift') + '</strong> ' +
    '<span style="color:#c62828;">' + (typeof t === 'function' ? t('dashboard.workPeriodNoShift') : 'No open shift') + '</span></div>' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="showPage(\'dashboard\')">' +
    (typeof t === 'function' ? t('dashboard.workPeriodOpen') : 'Open shift') + '</button></div></div>';
}
function rentRenderDashboardCardHtml() {
  if (typeof currentRole !== 'undefined' && currentRole === 'Housekeeper') return '';
  var s = rentGetFleetStats();
  var alert = s.due > 0 ? '<p class="rent-dash-alert">' + t('rental.dueAlert', { n: String(s.due) }) + '</p>' : '';
  return '<div class="card rent-dash-card" style="margin-bottom:0.85rem;cursor:pointer;" onclick="showPage(\'vehiclerental\')">' +
    '<div class="card-header" style="flex-wrap:wrap;gap:0.5rem;"><h2>🚗 ' + t('pageTitle.vehiclerental') + '</h2>' +
    '<span style="font-size:0.78rem;color:var(--text-light);">' + t('rental.viewFleet') + ' →</span></div>' +
    '<div class="card-body"><div class="stats-grid" style="margin-bottom:0.5rem;">' +
    '<div class="stat-card"><div class="stat-info"><h3>' + s.avail + '</h3><p>' + t('rental.stAvailable') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + s.out + '</h3><p>' + t('rental.stOut') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + s.due + '</h3><p>' + t('rental.stDue') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + fmt$(s.todayRev) + '</h3><p>' + t('rental.todayRevenue') + '</p></div></div></div>' +
    alert + '</div></div>';
}
function rentRefreshRelatedViews() {
  rentSyncOverdueRentals();
  var dashPg = document.getElementById('page-dashboard');
  if (dashPg && dashPg.classList.contains('active') && typeof renderDashboard === 'function') {
    renderDashboard();
  } else {
    if (typeof updateDashChart === 'function' && document.getElementById('dashChartArea')) updateDashChart();
    var card = document.querySelector('.rent-dash-card');
    if (card && typeof rentRenderDashboardCardHtml === 'function') {
      var wrap = document.createElement('div');
      wrap.innerHTML = rentRenderDashboardCardHtml();
      if (wrap.firstElementChild) card.replaceWith(wrap.firstElementChild);
    }
  }
  if (document.getElementById('page-vehiclerental')) renderVehicleRental();
}
function rentGetRentalsForDay(ymd) {
  return (vehicleRentals || []).filter(function(r) {
    if (!rowDataVisible(r)) return false;
    if (r.timestamp && typeof dashTimestampDay === 'function' && dashTimestampDay(r.timestamp) === ymd) return true;
    if (r.startDate && String(r.startDate).slice(0, 10) === ymd) return true;
    if (r.endDate && String(r.endDate).slice(0, 10) === ymd) return true;
    if (r.actualReturnDate && String(r.actualReturnDate).slice(0, 10) === ymd) return true;
    return false;
  });
}
function rentRenderDayDetailSection(dateStr) {
  var rentDay = rentGetRentalsForDay(dateStr);
  var html = '<p style="font-size:0.85rem;font-weight:600;margin:0.75rem 0 0.5rem;">' + t('dashboard.rentalsCount', { n: String(rentDay.length) }) + '</p>';
  if (rentDay.length) {
    html += '<div class="table-wrap"><table style="font-size:0.8rem;"><thead><tr><th>' + t('rental.rentalNum') + '</th><th>' + t('rental.vehicle') + '</th><th>' + t('g.guest') + '</th><th>' + t('g.total') + '</th><th>' + t('g.status') + '</th></tr></thead><tbody>';
    rentDay.forEach(function(r) {
      rentApplyBillToRental(r);
      html += '<tr style="cursor:pointer" onclick="showPage(\'vehiclerental\');rentOpenRentalDetail(\'' + escAttr(r.id) + '\')"><td>' + escAttr(r.rentalNumber) + '</td><td>' + escAttr(r.vehicleLabel) + '</td><td>' + escAttr(r.guestName) + '</td><td>' + fmt$(r.grandTotal) + '</td><td>' + escAttr(r.status) + '</td></tr>';
    });
    html += '</tbody></table></div>';
  } else {
    html += '<p style="color:var(--text-light);font-size:0.85rem;">—</p>';
  }
  return html;
}
function rentFillContextFromSelection() {
  if (rentSelectedBooking) {
    var b = bookings.find(function(x) { return x.id === rentSelectedBooking; });
    if (b) {
      var g = b.guestId ? (guests || []).find(function(x) { return x.id === b.guestId; }) : null;
      return {
        guestId: b.guestId || '',
        roomNumber: String(b.roomNumber != null ? b.roomNumber : ''),
        guestName: String(b.guestName != null ? b.guestName : ''),
        bookingId: (b.bookingId != null && b.bookingId !== '') ? String(b.bookingId) : String(b.id || ''),
        guestPhone: g ? String(g.phone || g.mobile || '') : '',
        guestEmail: g ? String(g.email || '') : ''
      };
    }
  }
  if (rentCrmGuestId) {
    var g2 = (guests || []).find(function(x) { return x.id === rentCrmGuestId; });
    if (g2) {
      return {
        guestId: g2.id, roomNumber: '—',
        guestName: String(guestDisplayNameFromProfile(g2) || ''),
        bookingId: '',
        guestPhone: String(g2.phone || g2.mobile || ''),
        guestEmail: String(g2.email || '')
      };
    }
  }
  return { guestId: '', roomNumber: '', guestName: '', bookingId: '', guestPhone: '', guestEmail: '' };
}
function rentCalcTotalPrice(vehicle, startIso, endIso, deliveryFee) {
  var daily = parseFloat(vehicle && vehicle.dailyRate) || 0;
  var base = daily;
  if (startIso && endIso) {
    try {
      var a = new Date(startIso);
      var b = new Date(endIso);
      if (!isNaN(a.getTime()) && !isNaN(b.getTime()) && b > a) {
        var hours = (b.getTime() - a.getTime()) / 3600000;
        var days = Math.max(1, Math.ceil(hours / 24));
        base = rentRoundMoney(days * daily);
      }
    } catch (e) {}
  }
  return rentRoundMoney(base + (parseFloat(deliveryFee) || 0));
}
function rentRoundMoney(v) {
  return Math.round((parseFloat(v) || 0) * 100) / 100;
}
function rentGetTaxRate() {
  return parseFloat(settings && (settings.serviceTax || settings.taxRate)) || 7;
}
function rentCalcRentalDays(startIso, endIso) {
  if (!startIso || !endIso) return 1;
  try {
    var a = new Date(startIso);
    var b = new Date(endIso);
    if (isNaN(a.getTime()) || isNaN(b.getTime()) || b <= a) return 1;
    return Math.max(1, Math.ceil((b.getTime() - a.getTime()) / 86400000));
  } catch (e) { return 1; }
}
function rentBuildSaleItems(rental) {
  var items = [];
  var del = rentRoundMoney(rental.deliveryFee || 0);
  var extra = rentRoundMoney(rental.extraCharges || 0);
  var base = rentRoundMoney(rental.baseSubtotal);
  if (isNaN(base) || base < 0) {
    base = rentRoundMoney((parseFloat(rental.subtotal) || parseFloat(rental.totalPrice) || 0) - del - extra);
  }
  if (base > 0) items.push({ name: (rental.vehicleLabel || 'Vehicle') + ' rental', qty: 1, unitPrice: base });
  if (del > 0) items.push({ name: 'Delivery / location fee', qty: 1, unitPrice: del });
  if (extra > 0) items.push({ name: 'Extra charges (fuel / damage / late)', qty: 1, unitPrice: extra });
  if (!items.length) {
    items.push({ name: (rental.vehicleLabel || 'Vehicle') + ' rental', qty: 1, unitPrice: rentRoundMoney(rental.subtotal || rental.totalPrice || 0) });
  }
  return items;
}
function rentComputeBill(rental) {
  var items = rentBuildSaleItems(rental || {});
  return computeLineTotalsFromRawLineItems(items, rentGetTaxRate());
}
function rentApplyBillToRental(rental) {
  var bill = rentComputeBill(rental);
  rental.baseSubtotal = rental.baseSubtotal != null ? rental.baseSubtotal : rentRoundMoney(bill.subtotal - (rental.deliveryFee || 0) - (rental.extraCharges || 0));
  rental.subtotal = bill.subtotal;
  rental.taxAmount = bill.taxAmount;
  rental.grandTotal = bill.grandTotal;
  rental.taxRate = bill.taxRate;
  rental.totalPrice = bill.subtotal;
  return bill;
}
function rentGetPostedGrandTotal(r) {
  var sum = 0;
  [r.transactionId, r.extraTransactionId].forEach(function(tid) {
    if (!tid) return;
    var tx = (transactions || []).find(function(x) { return x && String(x.transactionId) === String(tid); });
    if (tx && rowDataVisible(tx)) sum += parseFloat(tx.grandTotal) || 0;
  });
  return rentRoundMoney(sum);
}
function rentGetDisplayGrandTotal(r) {
  if (!r) return 0;
  rentApplyBillToRental(r);
  return r.grandTotal || 0;
}
function rentMapPayMethod(payMethod) {
  if (payMethod === 'Charged to Room' || payMethod === 'Room Charge') return 'Room Charge';
  if (payMethod === 'Credit Card') return 'Credit Card';
  if (payMethod === 'Pending') return 'Pending';
  return 'Cash';
}
function rentPaymentStatusFromMethod(payMethod) {
  if (payMethod === 'Pending') return 'Pending';
  if (payMethod === 'Charged to Room' || payMethod === 'Room Charge') return 'Charged to Room';
  return 'Paid';
}
function rentIsPaidMethod(payMethod) {
  return payMethod && payMethod !== 'Pending';
}
function rentRentalIsPayable(r) {
  return r && rowDataVisible(r) && r.status !== 'Completed' && r.status !== 'Cancelled' && !r.transactionId;
}
function rentCanChargeRoom(r) {
  return rentRentalIsPayable(r) && String(r.roomNumber || '').trim() !== '' && String(r.bookingId || '').trim() !== '';
}
function rentOpenCashPayModal(grandTotal, title, onValid) {
  if (typeof openCashPaymentModal !== 'function') {
    if (typeof onValid === 'function') onValid(grandTotal, 0);
    return;
  }
  openCashPaymentModal({
    grandTotal: grandTotal,
    title: title,
    onValid: onValid
  });
}
function rentFormatPaymentDisplay(r) {
  if (!r) return '—';
  if (r.paymentMethod && r.paymentMethod !== 'Pending') return r.paymentMethod;
  if (r.paymentStatus === 'Charged to Room') return 'Room Charge';
  if (r.paymentStatus === 'Pending') return (typeof t === 'function' ? t('rental.payPending') : 'Pending');
  if (r.paymentStatus === 'Paid') return 'Cash';
  return r.paymentStatus || '—';
}
function rentPostRentalSale(rental, payMethod, items, orderSuffix) {
  if (!items || !items.length || payMethod === 'Pending') return null;
  return processSale({
    source: 'Vehicle Rental',
    orderId: rental.rentalNumber + (orderSuffix || ''),
    guestName: rental.guestName,
    roomNumber: rental.roomNumber,
    bookingId: rental.bookingId,
    paymentMethod: rentMapPayMethod(payMethod),
    items: items,
    taxRate: rentGetTaxRate()
  });
}
function rentBuildPayBarHtml(total, opts) {
  opts = opts || {};
  var amt = parseFloat(total) || 0;
  if (!(amt > 0) && !opts.allowZero) return '';
  var roomLbl = (typeof t === 'function' ? t('rental.payRoom') : 'Charge to room');
  var pendingLbl = (typeof t === 'function' ? t('rental.payPending') : 'Pending');
  var extraBtns = '';
  if (opts.roomOnclick) extraBtns += '<button type="button" class="btn btn-sm btn-primary" style="width:100%;" onclick="' + opts.roomOnclick + '">' + roomLbl + '</button>';
  if (opts.pendingOnclick) extraBtns += '<button type="button" class="btn btn-sm btn-outline" style="width:100%;" onclick="' + opts.pendingOnclick + '">' + pendingLbl + '</button>';
  if (typeof guestQrBuildOpenBillPayBarHtml === 'function' && opts.cashOnclick && opts.cardOnclick) {
    var core = guestQrBuildOpenBillPayBarHtml(amt, opts.cashOnclick, opts.cardOnclick, opts.seeInvoiceOnclick || '');
    if (!extraBtns) return core;
    return core.replace('</div></div>', extraBtns + '</div></div>');
  }
  var totalLbl = (typeof t === 'function' && t('minimart.totalActiveOrder') !== 'minimart.totalActiveOrder') ? t('minimart.totalActiveOrder') : 'Total';
  var cashLbl = (typeof t === 'function' && t('minimart.payTotalCash') !== 'minimart.payTotalCash') ? t('minimart.payTotalCash') : 'Pay total — Cash';
  var cardLbl = (typeof t === 'function' && t('minimart.payTotalCard') !== 'minimart.payTotalCard') ? t('minimart.payTotalCard') : 'Pay total — Credit card';
  var btns = '';
  if (opts.cashOnclick) btns += '<button type="button" class="btn btn-sm btn-success" style="width:100%;" onclick="' + opts.cashOnclick + '">' + cashLbl + '</button>';
  if (opts.cardOnclick) btns += '<button type="button" class="btn btn-sm btn-outline" style="width:100%;" onclick="' + opts.cardOnclick + '">' + cardLbl + '</button>';
  if (opts.roomOnclick) btns += '<button type="button" class="btn btn-sm btn-primary" style="width:100%;" onclick="' + opts.roomOnclick + '">' + roomLbl + '</button>';
  if (opts.pendingOnclick) btns += '<button type="button" class="btn btn-sm btn-outline" style="width:100%;" onclick="' + opts.pendingOnclick + '">' + pendingLbl + '</button>';
  return '<div class="rest-bill-table-actions rent-pay-bar" style="position:sticky;bottom:0;z-index:1;border:1px solid var(--border);border-radius:10px;padding:0.75rem 0.85rem;margin:0.65rem 0 0.25rem;background:linear-gradient(180deg, rgba(26,115,232,0.07) 0%, var(--card-bg) 55%);box-shadow:0 -4px 12px rgba(0,0,0,0.05);">' +
    '<div style="display:flex;flex-wrap:wrap;align-items:center;gap:0.5rem 0.75rem;margin-bottom:0.5rem;">' +
    '<span style="font-size:0.85rem;color:var(--text-light);">' + totalLbl + '</span>' +
    '<strong style="font-size:1.05rem;">' + fmt$(amt) + '</strong></div>' +
    '<div style="display:flex;flex-direction:column;gap:0.45rem;">' + btns + '</div></div>';
}
function rentBuildPayBarOpts(prefix, id, extra) {
  extra = extra || {};
  var opts = {
    cashOnclick: prefix + "('" + id + "','Cash')",
    cardOnclick: prefix + "('" + id + "','Credit Card')",
    roomOnclick: prefix + "('" + id + "','Charged to Room')",
    pendingOnclick: prefix + "('" + id + "','Pending')"
  };
  if (extra.hideRoom) delete opts.roomOnclick;
  if (extra.hidePending) delete opts.pendingOnclick;
  return opts;
}
function rentRenderBillSummaryHtml(bill) {
  var subLbl = (typeof t === 'function' && t('minimart.subtotal') !== 'minimart.subtotal') ? t('minimart.subtotal') : 'Subtotal';
  var taxLbl = (typeof t === 'function' && t('minimart.tax') !== 'minimart.tax') ? t('minimart.tax', { rate: bill.taxRate }) : ('Tax (' + bill.taxRate + '%)');
  var grandLbl = (typeof t === 'function' && t('minimart.grandTotal') !== 'minimart.grandTotal') ? t('minimart.grandTotal') : 'Grand total';
  return '<div class="rent-bill-summary" style="background:var(--card-bg,#f8fafc);border:1px solid var(--border);border-radius:10px;padding:0.65rem 0.75rem;margin:0.65rem 0;font-size:0.85rem;">' +
    '<div style="display:flex;justify-content:space-between;"><span>' + subLbl + '</span><strong>' + fmt$(bill.subtotal) + '</strong></div>' +
    '<div style="display:flex;justify-content:space-between;color:var(--text-light);"><span>' + taxLbl + '</span><span>' + fmt$(bill.taxAmount) + '</span></div>' +
    '<div style="display:flex;justify-content:space-between;margin-top:0.35rem;padding-top:0.35rem;border-top:1px dashed var(--border);font-size:1rem;"><span>' + grandLbl + '</span><strong>' + fmt$(bill.grandTotal) + '</strong></div></div>';
}
function rentReadCheckoutBill(vehicle) {
  var s = document.getElementById('rCkStart');
  var e = document.getElementById('rCkEnd');
  var del = rentDeliveryFeeForCheckout();
  var base = rentCalcTotalPrice(vehicle, s && s.value, e && e.value, 0);
  var subEl = document.getElementById('rCkSubtotal');
  var subtotal = subEl ? parseFloat(subEl.value) : rentRoundMoney(base + del);
  if (isNaN(subtotal) || subtotal < 0) subtotal = rentRoundMoney(base + del);
  var items = [];
  var rentalBase = rentRoundMoney(subtotal - del);
  if (del > 0) {
    items.push({ name: vehicle.plateNumber + ' rental', qty: 1, unitPrice: Math.max(0, rentalBase) });
    items.push({ name: 'Delivery fee', qty: 1, unitPrice: del });
  } else {
    items.push({ name: vehicle.plateNumber + ' rental', qty: 1, unitPrice: subtotal });
  }
  return computeLineTotalsFromRawLineItems(items, rentGetTaxRate());
}
function rentUpdateCheckoutBillSummary(vehicleId) {
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return;
  var bill = rentReadCheckoutBill(v);
  var box = document.getElementById('rCkBillSummary');
  if (box) box.innerHTML = rentRenderBillSummaryHtml(bill);
  var payBar = document.getElementById('rCkPayBar');
  if (payBar) payBar.innerHTML = rentBuildPayBarHtml(bill.grandTotal, rentBuildPayBarOpts('rentSaveCheckoutWithPay', vehicleId));
  var sub = document.getElementById('rCkSubtotal');
  if (sub && document.activeElement !== sub) sub.value = bill.subtotal;
}
function rentLocationOptions(selectedId) {
  return (rentLocations || []).filter(rowDataVisible).map(function(loc) {
    return '<option value="' + escAttr(loc.id) + '"' + (selectedId === loc.id ? ' selected' : '') + '>' +
      escAttr(loc.name) + (loc.deliveryFee ? ' (+' + fmt$(loc.deliveryFee) + ')' : '') + '</option>';
  }).join('');
}
function rentGetLocationById(id) {
  return (rentLocations || []).find(function(l) { return l.id === id; }) || rentLocations[0];
}
function rentDeliveryFeeForCheckout() {
  var pu = document.getElementById('rCkPickup');
  var dr = document.getElementById('rCkDropoff');
  if (!pu || !dr) return 0;
  var a = rentGetLocationById(pu.value);
  var b = rentGetLocationById(dr.value);
  return (parseFloat(a && a.deliveryFee) || 0) + (parseFloat(b && b.deliveryFee) || 0);
}
function rentRecalcCheckoutTotal(vehicleId) {
  rentUpdateCheckoutBillSummary(vehicleId);
  rentUpdateConflictWarn(vehicleId);
}
function rentUpdateConflictWarn(vehicleId) {
  var box = document.getElementById('rCkConflict');
  if (!box) return;
  var s = document.getElementById('rCkStart');
  var e = document.getElementById('rCkEnd');
  if (rentHasConflict(vehicleId, s && s.value, e && e.value, null)) {
    box.style.display = '';
    box.textContent = (typeof t === 'function' ? t('rental.conflict') : 'Schedule conflict — this vehicle is already booked or in maintenance for these dates.');
  } else box.style.display = 'none';
}
function rentNextRentalNumber() {
  var nums = (vehicleRentals || []).map(function(r) {
    var m = String(r.rentalNumber || '').match(/(\d+)/);
    return m ? parseInt(m[1], 10) : 0;
  });
  var n = nums.length ? Math.max.apply(null, nums) + 1 : 1001;
  return 'RNT-' + n;
}
function rentNormalizePhone(phone) {
  return String(phone || '').replace(/\D/g, '');
}
function rentGetContactForRental(r) {
  var phone = String(r.guestPhone || '');
  var email = String(r.guestEmail || '');
  if (r.guestId) {
    var g = (guests || []).find(function(x) { return x.id === r.guestId; });
    if (g) {
      if (!phone) phone = String(g.phone || g.mobile || '');
      if (!email) email = String(g.email || '');
    }
  }
  return { phone: phone, email: email };
}
function rentBuildMessage(r, kind) {
  var hotel = (settings && settings.hotelName) ? settings.hotelName : 'Hotel';
  var pu = r.pickupLocationName || 'Hotel';
  var dr = r.dropoffLocationName || 'Hotel';
  var maps = r.pickupMapsUrl || r.dropoffMapsUrl || '';
  if (kind === 'confirm') {
    var gt = rentGetDisplayGrandTotal(r);
    return hotel + ': Rental ' + r.rentalNumber + ' confirmed. ' + r.vehicleLabel + '. Pickup: ' + pu + '. Return: ' + dr + '. Due: ' + (r.endDate || '') + '. Total: ' + fmt$(gt) + (maps ? ' Map: ' + maps : '');
  }
  if (kind === 'reminder') {
    return hotel + ': Reminder — return ' + r.vehicleLabel + ' (' + r.rentalNumber + ') by ' + (r.endDate || '') + '. Drop-off: ' + dr + '.';
  }
  if (kind === 'location') {
    return hotel + ': Pickup location for ' + r.rentalNumber + ': ' + pu + (maps ? ' ' + maps : '');
  }
  return hotel + ': Rental ' + r.rentalNumber + ' — ' + r.guestName;
}
window.rentOpenWhatsApp = function(rentalId, kind) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var c = rentGetContactForRental(r);
  var ph = rentNormalizePhone(c.phone);
  if (!ph) { toast(typeof t === 'function' ? t('rental.needPhone') : 'Add guest phone number'); return; }
  var msg = rentBuildMessage(r, kind || 'confirm');
  window.open('https://wa.me/' + ph + '?text=' + encodeURIComponent(msg), '_blank', 'noopener,noreferrer');
};
window.rentOpenSms = function(rentalId, kind) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var c = rentGetContactForRental(r);
  var ph = rentNormalizePhone(c.phone);
  if (!ph) { toast(typeof t === 'function' ? t('rental.needPhone') : 'Add guest phone number'); return; }
  window.open('sms:' + ph + '?body=' + encodeURIComponent(rentBuildMessage(r, kind || 'confirm')), '_self');
};
window.rentOpenEmail = function(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var c = rentGetContactForRental(r);
  if (!c.email) { toast(typeof t === 'function' ? t('rental.needEmail') : 'Add guest email'); return; }
  var sub = 'Rental agreement ' + r.rentalNumber;
  var body = rentBuildMessage(r, 'confirm') + '\n\nVehicle: ' + r.vehicleLabel + '\nSigned: ' + (r.contractSignedName || '—');
  window.open('mailto:' + encodeURIComponent(c.email) + '?subject=' + encodeURIComponent(sub) + '&body=' + encodeURIComponent(body), '_self');
};
window.rentInitSigPad = function() {
  var c = document.getElementById('rCkSig');
  if (!c || c._rentSigReady) return;
  c._rentSigReady = true;
  var ctx = c.getContext('2d');
  ctx.strokeStyle = '#1a73e8';
  ctx.lineWidth = 2;
  var drawing = false;
  function pos(ev) {
    var r = c.getBoundingClientRect();
    var cx = ev.touches ? ev.touches[0].clientX : ev.clientX;
    var cy = ev.touches ? ev.touches[0].clientY : ev.clientY;
    return { x: (cx - r.left) * (c.width / r.width), y: (cy - r.top) * (c.height / r.height) };
  }
  function start(ev) { drawing = true; var p = pos(ev); ctx.beginPath(); ctx.moveTo(p.x, p.y); ev.preventDefault(); }
  function move(ev) { if (!drawing) return; var p = pos(ev); ctx.lineTo(p.x, p.y); ctx.stroke(); ev.preventDefault(); }
  function end() { drawing = false; }
  c.addEventListener('mousedown', start); c.addEventListener('mousemove', move); c.addEventListener('mouseup', end); c.addEventListener('mouseleave', end);
  c.addEventListener('touchstart', start, { passive: false }); c.addEventListener('touchmove', move, { passive: false }); c.addEventListener('touchend', end);
};
window.rentClearSig = function() {
  var c = document.getElementById('rCkSig');
  if (!c) return;
  var ctx = c.getContext('2d');
  ctx.clearRect(0, 0, c.width, c.height);
};
window.rentGetSigData = function() {
  var c = document.getElementById('rCkSig');
  return c ? c.toDataURL('image/png') : '';
};
window.rentPrintContract = function(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var hotel = (settings && settings.hotelName) ? settings.hotelName : 'Hotel';
  var sigHtml = r.contractSignature ? '<p><img src="' + r.contractSignature + '" alt="Signature" style="max-width:240px;border-bottom:1px solid #333;"></p>' : '';
  var html = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Rental ' + escapeHtml(r.rentalNumber) + '</title><style>body{font-family:system-ui,sans-serif;padding:16mm;line-height:1.5;}h1{font-size:1.2rem;border-bottom:2px solid #1a73e8;padding-bottom:8px;}table{width:100%;border-collapse:collapse;margin:12px 0;}td{padding:4px 8px;border-bottom:1px solid #ddd;}td:first-child{font-weight:600;width:38%;}</style></head><body>' +
    '<h1>' + escapeHtml(hotel) + ' — Vehicle rental agreement</h1>' +
    '<table><tr><td>Rental #</td><td>' + escapeHtml(r.rentalNumber) + '</td></tr>' +
    '<tr><td>Guest</td><td>' + escapeHtml(r.guestName) + '</td></tr>' +
    '<tr><td>Vehicle</td><td>' + escapeHtml(r.vehicleLabel) + '</td></tr>' +
    '<tr><td>Period</td><td>' + escapeHtml(r.startDate) + ' → ' + escapeHtml(r.endDate) + '</td></tr>' +
    '<tr><td>Pickup</td><td>' + escapeHtml(r.pickupLocationName || '—') + '</td></tr>' +
    '<tr><td>Drop-off</td><td>' + escapeHtml(r.dropoffLocationName || '—') + '</td></tr>' +
    '<tr><td>Subtotal</td><td>' + escapeHtml(fmt$(r.subtotal || r.totalPrice || 0)) + '</td></tr>' +
    '<tr><td>Tax</td><td>' + escapeHtml(fmt$(r.taxAmount || 0)) + '</td></tr>' +
    '<tr><td>Grand total</td><td>' + escapeHtml(fmt$(rentGetDisplayGrandTotal(r))) + '</td></tr>' +
    '<tr><td>Deposit</td><td>' + escapeHtml(fmt$(r.deposit || 0)) + '</td></tr>' +
    '<tr><td>Signed by</td><td>' + escapeHtml(r.contractSignedName || '—') + '</td></tr></table>' +
    sigHtml + '<p style="font-size:0.85rem;color:#555;">Generated ' + new Date().toLocaleString() + '</p></body></html>';
  var frame = document.getElementById('hrmmInvoicePrintFrame');
  if (!frame) {
    frame = document.createElement('iframe');
    frame.id = 'hrmmInvoicePrintFrame';
    frame.style.cssText = 'position:fixed;width:0;height:0;border:0;opacity:0;left:-9999px;';
    document.body.appendChild(frame);
  }
  var win = frame.contentWindow;
  win.document.open();
  win.document.write(html);
  win.document.close();
  setTimeout(function() { try { win.focus(); win.print(); } catch (e) {} }, 200);
};
window.rentFloorClick = function(vehicleId) {
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return;
  if (v.status === 'Maintenance') { toast(t('rental.inMaintenance')); return; }
  var active = rentGetActiveRentalForVehicle(vehicleId);
  if (active) rentOpenRentalDetail(active.id);
  else {
    if (!rentEnsureShiftOpen()) return;
    rentOpenCheckoutModal(vehicleId);
  }
};
window.rentOpenCheckoutModal = function(vehicleId) {
  if (!rentEnsureShiftOpen()) return;
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return;
  var ctx = rentFillContextFromSelection();
  var now = new Date();
  var end = new Date(now.getTime() + 86400000);
  var startVal = now.toISOString().slice(0, 16);
  var endVal = end.toISOString().slice(0, 16);
  var del = 0;
  var baseSub = rentCalcTotalPrice(v, startVal, endVal, 0);
  var initBill = computeLineTotalsFromRawLineItems([
    { name: v.plateNumber + ' rental', qty: 1, unitPrice: baseSub }
  ], rentGetTaxRate());
  openModal('<div class="modal-header"><h2>' + t('rental.checkoutTitle') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body">' +
    '<p style="font-size:0.85rem;margin:0 0 0.75rem;"><strong>' + rentVehicleIcon(v.type) + ' ' + escAttr(v.brand + ' ' + v.model) + '</strong> · ' + escAttr(v.plateNumber) + ' · ' + fmt$(v.dailyRate) + '/' + t('rental.perDay') + '</p>' +
    '<div id="rCkConflict" class="rent-conflict-warn" style="display:none;"></div>' +
    '<div class="form-group"><label>' + t('g.guest') + '</label><input type="text" class="form-control" id="rCkGuest" value="' + escAttr(ctx.guestName) + '" placeholder="' + t('rental.phGuest') + '"></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.guestPhone') + '</label><input type="tel" class="form-control" id="rCkPhone" value="' + escAttr(ctx.guestPhone) + '"></div>' +
    '<div class="form-group"><label>' + t('rental.guestEmail') + '</label><input type="email" class="form-control" id="rCkEmail" value="' + escAttr(ctx.guestEmail) + '"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.roomNumber') + '</label><input type="text" class="form-control" id="rCkRoom" value="' + escAttr(ctx.roomNumber) + '"></div>' +
    '<div class="form-group"><label>' + t('rental.bookingRef') + '</label><input type="text" class="form-control" id="rCkBk" value="' + escAttr(ctx.bookingId) + '"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.pickupLoc') + '</label><select class="form-control" id="rCkPickup" onchange="rentRecalcCheckoutTotal(\'' + v.id + '\')">' + rentLocationOptions('hotel') + '</select></div>' +
    '<div class="form-group"><label>' + t('rental.dropoffLoc') + '</label><select class="form-control" id="rCkDropoff" onchange="rentRecalcCheckoutTotal(\'' + v.id + '\')">' + rentLocationOptions('hotel') + '</select></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.startDate') + '</label><input type="datetime-local" class="form-control" id="rCkStart" value="' + startVal + '" onchange="rentRecalcCheckoutTotal(\'' + v.id + '\')"></div>' +
    '<div class="form-group"><label>' + t('rental.endDate') + '</label><input type="datetime-local" class="form-control" id="rCkEnd" value="' + endVal + '" onchange="rentRecalcCheckoutTotal(\'' + v.id + '\')"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.fuelOut') + '</label><select class="form-control" id="rCkFuel"><option>Full</option><option>3/4</option><option>1/2</option><option>1/4</option></select></div>' +
    '<div class="form-group"><label>' + t('rental.mileageOut') + '</label><input type="number" class="form-control" id="rCkMile" value="0" min="0"></div></div>' +
    '<div class="form-group"><label>' + ((typeof t === 'function' && t('minimart.subtotal') !== 'minimart.subtotal') ? t('minimart.subtotal') : 'Subtotal') + '</label><input type="number" class="form-control" id="rCkSubtotal" step="0.01" value="' + initBill.subtotal + '" oninput="rentUpdateCheckoutBillSummary(\'' + v.id + '\')"></div>' +
    '<div id="rCkBillSummary">' + rentRenderBillSummaryHtml(initBill) + '</div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.deposit') + '</label><input type="number" class="form-control" id="rCkDeposit" step="0.01" value="0"></div></div>' +
    '<div class="form-group"><label>' + t('rental.notes') + '</label><textarea class="form-control" id="rCkNotes" rows="2"></textarea></div>' +
    '<div id="rCkPayBar">' + rentBuildPayBarHtml(initBill.grandTotal, rentBuildPayBarOpts('rentSaveCheckoutWithPay', v.id)) + '</div>' +
    '<div class="rent-sig-wrap"><label>' + t('rental.contractSign') + '</label><canvas id="rCkSig" width="320" height="80"></canvas>' +
    '<div style="display:flex;gap:0.35rem;margin-top:0.35rem;"><input type="text" class="form-control" id="rCkSignName" placeholder="' + t('rental.signHere') + '" style="flex:1;">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentClearSig()">' + t('rental.clearSig') + '</button></div></div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button></div>');
  setTimeout(function() { rentInitSigPad(); rentRecalcCheckoutTotal(v.id); }, 50);
};
function rentBuildCheckoutRental(vehicleId) {
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (!v) return null;
  var start = document.getElementById('rCkStart').value;
  var end = document.getElementById('rCkEnd').value;
  if (rentHasConflict(vehicleId, start, end, null)) {
    toast(typeof t === 'function' ? t('rental.conflictBlocked') : 'Cannot book — schedule conflict');
    return null;
  }
  var guestName = (document.getElementById('rCkGuest') && document.getElementById('rCkGuest').value.trim()) || '';
  if (!guestName) { toast(t('rental.needGuest')); return null; }
  var puLoc = rentGetLocationById(document.getElementById('rCkPickup').value);
  var drLoc = rentGetLocationById(document.getElementById('rCkDropoff').value);
  var delFee = rentDeliveryFeeForCheckout();
  var bill = rentReadCheckoutBill(v);
  var ctx = rentFillContextFromSelection();
  return {
    v: v,
    rental: {
      id: genId(), rentalNumber: rentNextRentalNumber(), vehicleId: v.id,
      vehicleLabel: v.plateNumber + ' ' + v.brand + ' ' + v.model, vehicleType: v.type,
      guestId: rentCrmGuestId || ctx.guestId || '',
      guestName: guestName,
      guestPhone: document.getElementById('rCkPhone').value.trim(),
      guestEmail: document.getElementById('rCkEmail').value.trim(),
      roomNumber: document.getElementById('rCkRoom').value.trim(),
      bookingId: document.getElementById('rCkBk').value.trim(),
      pickupLocationId: puLoc.id, pickupLocationName: puLoc.name, pickupMapsUrl: puLoc.mapsUrl || '',
      dropoffLocationId: drLoc.id, dropoffLocationName: drLoc.name, dropoffMapsUrl: drLoc.mapsUrl || '',
      deliveryFee: delFee,
      baseSubtotal: rentRoundMoney(bill.subtotal - delFee),
      startDate: start, endDate: end,
      actualReturnDate: null, initialFuelLevel: document.getElementById('rCkFuel').value,
      returnFuelLevel: null, initialMileage: parseInt(document.getElementById('rCkMile').value, 10) || 0,
      returnMileage: null, deposit: parseFloat(document.getElementById('rCkDeposit').value) || 0,
      extraCharges: 0, notes: document.getElementById('rCkNotes').value.trim(),
      subtotal: bill.subtotal, taxAmount: bill.taxAmount, grandTotal: bill.grandTotal, taxRate: bill.taxRate,
      totalPrice: bill.subtotal, paymentStatus: 'Pending', paymentMethod: 'Pending', status: 'Out',
      contractSignature: rentGetSigData(), contractSignedName: document.getElementById('rCkSignName').value.trim(),
      timestamp: new Date().toISOString(), staffName: currentUser ? currentUser.name : currentRole, visible: true
    }
  };
}
window.rentSaveCheckoutWithPay = function(vehicleId, payMethod, skipCashModal) {
  if (!rentEnsureShiftOpen()) return;
  var built = rentBuildCheckoutRental(vehicleId);
  if (!built) return;
  var rental = built.rental;
  var v = built.v;
  if (payMethod === 'Cash' && !skipCashModal) {
    rentOpenCashPayModal(rental.grandTotal, t('rental.checkoutTitle') + ' — ' + rental.vehicleLabel, function(tenderAmt, changeDue) {
      toast(typeof t === 'function' ? t('msg.changeDue', { amount: fmt$(changeDue) }) : ('Change: ' + fmt$(changeDue)));
      rentSaveCheckoutWithPay(vehicleId, 'Cash', true);
    });
    return;
  }
  rental.paymentMethod = rentMapPayMethod(payMethod);
  rental.paymentStatus = rentPaymentStatusFromMethod(payMethod);
  if (rentIsPaidMethod(payMethod)) {
    var txn = rentPostRentalSale(rental, payMethod, rentBuildSaleItems(rental), '');
    if (!txn) return;
    rental.transactionId = txn.transactionId;
  }
  vehicleRentals.push(rental);
  v.status = 'Rented';
  save('vehicleRentals', vehicleRentals); save('vehicles', vehicles);
  logAudit('Checkout', 'Vehicle Rental', rental.rentalNumber, 'Checked out ' + v.plateNumber + ' to ' + rental.guestName + ' · ' + fmt$(rental.grandTotal) + ' · ' + rental.paymentMethod);
  closeModal(); rentRefreshRelatedViews(); toast(t('rental.checkedOut', { num: rental.rentalNumber }));
};
window.rentSaveCheckout = function(vehicleId) { rentSaveCheckoutWithPay(vehicleId, 'Pending'); };
window.rentPayRental = function(rentalId, payMethod, skipCashModal) {
  if (!rentEnsureShiftOpen()) return;
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  if (r.transactionId) { toast(typeof t === 'function' ? t('msg.alreadyCharged') : 'Already paid'); return; }
  if (!rentRentalIsPayable(r)) return;
  rentApplyBillToRental(r);
  if (payMethod === 'Charged to Room' && !rentCanChargeRoom(r)) {
    toast(typeof t === 'function' ? t('msg.filterOneRoomToCharge') : 'Select an in-house booking with room');
    return;
  }
  if (payMethod === 'Cash' && !skipCashModal) {
    rentOpenCashPayModal(r.grandTotal, t('rental.detailTitle') + ' — ' + r.rentalNumber, function(tenderAmt, changeDue) {
      toast(typeof t === 'function' ? t('msg.changeDue', { amount: fmt$(changeDue) }) : ('Change: ' + fmt$(changeDue)));
      rentPayRental(rentalId, 'Cash', true);
    });
    return;
  }
  var txn = rentPostRentalSale(r, payMethod, rentBuildSaleItems(r), '');
  if (!txn) return;
  r.transactionId = txn.transactionId;
  r.paymentMethod = rentMapPayMethod(payMethod);
  r.paymentStatus = rentPaymentStatusFromMethod(payMethod);
  save('vehicleRentals', vehicleRentals);
  logAudit('Payment', 'Vehicle Rental', r.rentalNumber, 'Paid ' + fmt$(r.grandTotal) + ' · ' + r.paymentMethod);
  closeModal(); rentRefreshRelatedViews();
  toast(typeof t === 'function' ? t('rental.paid', { num: r.rentalNumber }) : ('Rental paid: ' + r.rentalNumber));
};
window.rentOpenRentalDetail = function(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var mapsBtn = (r.pickupMapsUrl || r.dropoffMapsUrl) ?
    '<button type="button" class="btn btn-sm btn-outline" onclick="window.open(\'' + escAttr(r.pickupMapsUrl || r.dropoffMapsUrl) + '\',\'_blank\')">' + t('rental.openMaps') + '</button>' : '';
  var bill = rentApplyBillToRental(Object.assign({}, r));
  var payOpts = rentBuildPayBarOpts('rentPayRental', r.id, { hidePending: true });
  if (!rentCanChargeRoom(r)) payOpts.hideRoom = true;
  var payBarHtml = rentRentalIsPayable(r) ? rentBuildPayBarHtml(bill.grandTotal, payOpts) : '';
  openModal('<div class="modal-header"><h2>' + t('rental.detailTitle') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body">' +
    '<p><strong>' + escAttr(r.rentalNumber) + '</strong> · ' + escAttr(r.guestName) + ' · ' + escAttr(r.vehicleLabel) + '</p>' +
    '<p style="font-size:0.85rem;">' + escAttr(r.startDate) + ' → ' + escAttr(r.endDate) + '<br>' +
    t('rental.pickupLoc') + ': ' + escAttr(r.pickupLocationName || '—') + '<br>' +
    t('rental.dropoffLoc') + ': ' + escAttr(r.dropoffLocationName || '—') + '<br>' +
    escAttr(rentFormatPaymentDisplay(r)) + (r.transactionId ? ' · Txn ' + escAttr(r.transactionId) : '') + '</p>' +
    rentRenderBillSummaryHtml(bill) + payBarHtml +
    '<div class="rent-comm-btns">' +
    '<button type="button" class="btn btn-sm btn-primary" onclick="rentOpenWhatsApp(\'' + r.id + '\',\'confirm\')">' + t('rental.sendWhatsApp') + '</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentOpenSms(\'' + r.id + '\',\'reminder\')">' + t('rental.sendSms') + '</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentOpenEmail(\'' + r.id + '\')">' + t('rental.sendEmail') + '</button>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentOpenWhatsApp(\'' + r.id + '\',\'location\')">' + t('rental.msgLocation') + '</button>' +
    mapsBtn +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentPrintContract(\'' + r.id + '\')">' + t('rental.printContract') + '</button>' +
    '</div></div>' +
    '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button>' +
    (r.status !== 'Completed' ? '<button class="btn btn-primary" onclick="closeModal();rentOpenReturnModal(\'' + r.id + '\')">' + t('rental.returnBtn') + '</button>' : '') +
    '</div>');
};
window.rentUpdateReturnBillSummary = function(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var extra = parseFloat(document.getElementById('rRtExtra') && document.getElementById('rRtExtra').value) || 0;
  var draft = Object.assign({}, r, { extraCharges: extra });
  rentApplyBillToRental(draft);
  var box = document.getElementById('rRtBillSummary');
  if (box) box.innerHTML = rentRenderBillSummaryHtml(draft);
  var payBar = document.getElementById('rRtPayBar');
  if (payBar) payBar.innerHTML = rentBuildPayBarHtml(draft.grandTotal, rentBuildPayBarOpts('rentCompleteReturnWithPay', rentalId));
};
function rentReadReturnDraft(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return null;
  var extra = parseFloat(document.getElementById('rRtExtra') && document.getElementById('rRtExtra').value) || 0;
  var draft = Object.assign({}, r, { extraCharges: rentRoundMoney(extra) });
  rentApplyBillToRental(draft);
  return draft;
}
window.rentOpenReturnModal = function(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return;
  var now = new Date().toISOString().slice(0, 16);
  var draft = Object.assign({}, r, { extraCharges: 0 });
  rentApplyBillToRental(draft);
  openModal('<div class="modal-header"><h2>' + t('rental.returnTitle') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body">' +
    '<p style="font-size:0.85rem;">' + escAttr(r.rentalNumber) + ' · ' + escAttr(r.guestName) + ' · ' + escAttr(r.vehicleLabel) + '</p>' +
    '<div class="form-group"><label>' + t('rental.returnDate') + '</label><input type="datetime-local" class="form-control" id="rRtDate" value="' + now + '"></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.fuelIn') + '</label><select class="form-control" id="rRtFuel"><option>Full</option><option>3/4</option><option>1/2</option><option>1/4</option></select></div>' +
    '<div class="form-group"><label>' + t('rental.mileageIn') + '</label><input type="number" class="form-control" id="rRtMile" value="' + (r.initialMileage || 0) + '" min="0"></div></div>' +
    '<div class="form-group"><label>' + t('rental.extraCharges') + '</label><input type="number" class="form-control" id="rRtExtra" step="0.01" value="0" oninput="rentUpdateReturnBillSummary(\'' + r.id + '\')"></div>' +
    '<div id="rRtBillSummary">' + rentRenderBillSummaryHtml(draft) + '</div>' +
    '<div id="rRtPayBar">' + rentBuildPayBarHtml(draft.grandTotal, rentBuildPayBarOpts('rentCompleteReturnWithPay', r.id)) + '</div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button></div>');
};
function rentApplyReturnFields(rentalId) {
  var r = vehicleRentals.find(function(x) { return x.id === rentalId; });
  if (!r) return null;
  r.actualReturnDate = document.getElementById('rRtDate').value;
  r.returnFuelLevel = document.getElementById('rRtFuel').value;
  r.returnMileage = parseInt(document.getElementById('rRtMile').value, 10) || 0;
  r.extraCharges = rentRoundMoney(parseFloat(document.getElementById('rRtExtra').value) || 0);
  rentApplyBillToRental(r);
  return r;
}
window.rentCompleteReturnWithPay = function(rentalId, payMethod, skipCashModal) {
  if (!rentEnsureShiftOpen()) return;
  var draft = rentReadReturnDraft(rentalId);
  if (!draft) return;
  var pay = payMethod || 'Pending';
  if (pay === 'Cash' && !skipCashModal) {
    rentOpenCashPayModal(draft.grandTotal, t('rental.returnTitle') + ' — ' + draft.rentalNumber, function(tenderAmt, changeDue) {
      toast(typeof t === 'function' ? t('msg.changeDue', { amount: fmt$(changeDue) }) : ('Change: ' + fmt$(changeDue)));
      rentCompleteReturnWithPay(rentalId, 'Cash', true);
    });
    return;
  }
  var r = rentApplyReturnFields(rentalId);
  if (!r) return;
  r.status = 'Completed';
  var v = vehicles.find(function(x) { return x.id === r.vehicleId; });
  if (v) { v.status = 'Available'; save('vehicles', vehicles); }
  if (rentIsPaidMethod(pay)) {
    if (!r.transactionId) {
      var txn = rentPostRentalSale(r, pay, rentBuildSaleItems(r), '');
      if (!txn) {
        r.status = 'Out';
        if (v) { v.status = 'Rented'; save('vehicles', vehicles); }
        return;
      }
      r.transactionId = txn.transactionId;
      r.paymentMethod = rentMapPayMethod(pay);
      r.paymentStatus = rentPaymentStatusFromMethod(pay);
    } else if (r.extraCharges > 0 && !r.extraTransactionId) {
      var extraPay = pay;
      if (r.paymentMethod && r.paymentMethod !== 'Pending') extraPay = r.paymentMethod;
      var extraTxn = rentPostRentalSale(r, extraPay, [{ name: r.vehicleLabel + ' extra charges', qty: 1, unitPrice: r.extraCharges }], '-X');
      if (!extraTxn) {
        r.status = 'Out';
        if (v) { v.status = 'Rented'; save('vehicles', vehicles); }
        return;
      }
      r.extraTransactionId = extraTxn.transactionId;
    }
  } else {
    r.paymentMethod = 'Pending';
    r.paymentStatus = 'Pending';
  }
  save('vehicleRentals', vehicleRentals);
  logAudit('Return', 'Vehicle Rental', r.rentalNumber, 'Returned ' + r.vehicleLabel + ' · ' + fmt$(r.grandTotal) + ' · ' + rentFormatPaymentDisplay(r));
  closeModal(); rentRefreshRelatedViews(); toast(t('rental.returned', { num: r.rentalNumber }));
};
window.rentCompleteReturn = function(rentalId) { rentCompleteReturnWithPay(rentalId, 'Pending'); };
window.rentSelectBooking = function(id) { rentSelectedBooking = id || null; rentCrmGuestId = null; renderVehicleRental(); };
window.rentSelectGuestDir = function(id) { rentCrmGuestId = id || null; rentSelectedBooking = null; renderVehicleRental(); };
window.rentSetView = function(mode) { window.rentViewMode = mode; renderVehicleRental(); };
window.rentCalNav = function(delta) {
  var d = rentCalStart ? new Date(rentCalStart) : new Date();
  d.setDate(d.getDate() + delta);
  d.setHours(0, 0, 0, 0);
  window.rentCalStart = d.toISOString();
  renderVehicleRental();
};
window.filterRentGuestCards = function(val) {
  window.rentGuestSearch = val || '';
  var term = String(val || '').toLowerCase();
  document.querySelectorAll('#rentGuestCards .rest-guest-card').forEach(function(el) {
    var hay = (el.getAttribute('data-search') || '').toLowerCase();
    el.style.display = !term || hay.indexOf(term) >= 0 ? '' : 'none';
  });
};
function rentRenderGuestPickerHtml() {
  var cards = '';
  getBookingsForGuestPicker().forEach(function(b) {
    var sel = rentSelectedBooking === b.id ? ' rest-guest-card--balance-zero' : '';
    cards += '<button type="button" class="rest-guest-card' + sel + '" data-search="' + escAttr(b.roomNumber + ' ' + b.guestName + ' ' + b.bookingId) + '" onclick="rentSelectBooking(\'' + b.id + '\')">' +
      '<span class="rgc-top-row"><span class="rgc-room">' + escAttr(b.roomNumber) + '</span><span class="rgc-main"><span class="rgc-name">' + escAttr(b.guestName) + '</span></span></span></button>';
  });
  getGuestDirectoryOnlyForPicker().forEach(function(g) {
    var sel2 = rentCrmGuestId === g.id ? ' rest-guest-card--balance-zero' : '';
    cards += '<button type="button" class="rest-guest-card' + sel2 + '" data-search="' + escAttr(guestDisplayNameFromProfile(g) + ' ' + (g.phone || '') + ' ' + (g.email || '')) + '" onclick="rentSelectGuestDir(\'' + g.id + '\')">' +
      '<span class="rgc-top-row"><span class="rgc-room">CRM</span><span class="rgc-main"><span class="rgc-name">' + escAttr(guestDisplayNameFromProfile(g)) + '</span></span></span></button>';
  });
  return '<input type="search" class="form-control rent-guest-search" placeholder="' + t('rental.searchGuest') + '" value="' + escAttr(rentGuestSearch || '') + '" oninput="filterRentGuestCards(this.value)">' +
    '<div class="rest-guest-cards" id="rentGuestCards">' + (cards || '<p style="font-size:0.85rem;">—</p>') + '</div>';
}
function rentRenderCalendarHtml() {
  var days = 7;
  var start = rentCalStart ? new Date(rentCalStart) : new Date();
  start.setHours(0, 0, 0, 0);
  var cols = '';
  for (var i = 0; i < days; i++) {
    var d = new Date(start.getTime() + i * 86400000);
    cols += '<th>' + d.toLocaleDateString(undefined, { weekday: 'short', month: 'short', day: 'numeric' }) + '</th>';
  }
  var rows = '';
  rentSortedVehicles().forEach(function(v) {
    rows += '<tr><td>' + rentVehicleIcon(v.type) + ' ' + escAttr(v.plateNumber) + '</td>';
    for (var j = 0; j < days; j++) {
      var dayStart = new Date(start.getTime() + j * 86400000);
      var dayEnd = new Date(dayStart.getTime() + 86400000);
      var state = 'free';
      var label = '';
      (vehicleMaintBlocks || []).forEach(function(b) {
        if (!rowDataVisible(b) || b.vehicleId !== v.id) return;
        if (rentRangesOverlap(dayStart, dayEnd, rentParseDt(b.startDate), rentParseDt(b.endDate))) { state = 'maint'; label = 'M'; }
      });
      (vehicleRentals || []).forEach(function(r) {
        if (!rowDataVisible(r) || r.vehicleId !== v.id || r.status === 'Cancelled') return;
        var re = rentParseDt(r.actualReturnDate) || rentParseDt(r.endDate);
        if (rentRangesOverlap(dayStart, dayEnd, rentParseDt(r.startDate), re)) {
          state = r.status === 'Completed' ? 'done' : 'booked';
          label = (r.guestName || '').split(' ')[0].slice(0, 6) || '•';
        }
      });
      rows += '<td class="rent-cal-' + state + '" title="' + escAttr(label) + '">' + (label || '·') + '</td>';
    }
    rows += '</tr>';
  });
  return '<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.5rem;">' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentCalNav(-7)">←</button>' +
    '<strong>' + t('rental.calendarTitle') + '</strong>' +
    '<button type="button" class="btn btn-sm btn-outline" onclick="rentCalNav(7)">→</button></div>' +
    '<div class="rent-cal-wrap"><table class="rent-cal-grid"><thead><tr><th>' + t('rental.vehicle') + '</th>' + cols + '</tr></thead><tbody>' + rows + '</tbody></table></div>';
}
function rentVehicleRevenueSum(vehicleId) {
  var sum = 0;
  (vehicleRentals || []).forEach(function(r) {
    if (!rowDataVisible(r) || r.vehicleId !== vehicleId || r.status !== 'Completed') return;
    var posted = rentGetPostedGrandTotal(r);
    sum += posted > 0 ? posted : rentGetDisplayGrandTotal(r);
  });
  return rentRoundMoney(sum);
}
function rentVehicleExpenseSum(vehicleId) {
  var sum = 0;
  (vehicleExpenses || []).forEach(function(e) {
    if (rowDataVisible(e) && e.vehicleId === vehicleId) sum += parseFloat(e.amount) || 0;
  });
  return sum;
}
function rentRenderPnlHtml() {
  var cards = '';
  rentSortedVehicles().forEach(function(v) {
    var rev = rentVehicleRevenueSum(v.id);
    var exp = rentVehicleExpenseSum(v.id);
    var net = Math.round((rev - exp) * 100) / 100;
    cards += '<div class="rent-pnl-card"><h4>' + rentVehicleIcon(v.type) + ' ' + escAttr(v.plateNumber) + '</h4>' +
      '<div class="rent-pnl-row"><span>' + t('rental.revenue') + '</span><span>' + fmt$(rev) + '</span></div>' +
      '<div class="rent-pnl-row"><span>' + t('rental.expenses') + '</span><span>' + fmt$(exp) + '</span></div>' +
      '<div class="rent-pnl-row rent-pnl-net"><span>' + t('rental.netProfit') + '</span><span>' + fmt$(net) + '</span></div>' +
      '<div style="margin-top:0.45rem;display:flex;gap:0.3rem;flex-wrap:wrap;">' +
      '<button type="button" class="btn btn-sm btn-outline" onclick="rentShowAddExpense(\'' + v.id + '\')">+ ' + t('rental.addExpense') + '</button>' +
      '<button type="button" class="btn btn-sm btn-outline" onclick="rentShowScheduleMaint(\'' + v.id + '\')">' + t('rental.scheduleMaint') + '</button>' +
      (v.status !== 'Maintenance' ? '' : '<button type="button" class="btn btn-sm btn-primary" onclick="rentClearMaint(\'' + v.id + '\')">' + t('rental.clearMaint') + '</button>') +
      '</div></div>';
  });
  return '<div class="rent-pnl-grid">' + cards + '</div>';
}
window.rentShowAddExpense = function(vehicleId) {
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  openModal('<div class="modal-header"><h2>' + t('rental.addExpense') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' +
    '<p style="font-size:0.85rem;">' + escAttr(v ? v.plateNumber : '') + '</p>' +
    '<div class="form-group"><label>' + t('rental.expCategory') + '</label><select class="form-control" id="rExCat"><option>Insurance</option><option>Registration</option><option>Repair</option><option>Fuel</option><option>Other</option></select></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.amount') + '</label><input type="number" class="form-control" id="rExAmt" step="0.01" value="0"></div>' +
    '<div class="form-group"><label>' + t('g.date') + '</label><input type="date" class="form-control" id="rExDate" value="' + new Date().toISOString().slice(0, 10) + '"></div></div>' +
    '<div class="form-group"><label>' + t('rental.notes') + '</label><input type="text" class="form-control" id="rExNote"></div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button><button class="btn btn-primary" onclick="rentSaveExpense(\'' + vehicleId + '\')">' + t('common.save') + '</button></div>');
};
window.rentSaveExpense = function(vehicleId) {
  vehicleExpenses.push({
    id: genId(), vehicleId: vehicleId, category: document.getElementById('rExCat').value,
    amount: parseFloat(document.getElementById('rExAmt').value) || 0,
    date: document.getElementById('rExDate').value, notes: document.getElementById('rExNote').value.trim(),
    visible: true, timestamp: new Date().toISOString()
  });
  save('vehicleExpenses', vehicleExpenses);
  closeModal(); rentRefreshRelatedViews(); toast(t('rental.expenseSaved'));
};
window.rentShowScheduleMaint = function(vehicleId) {
  var now = new Date();
  var end = new Date(now.getTime() + 86400000);
  openModal('<div class="modal-header"><h2>' + t('rental.scheduleMaint') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div><div class="modal-body">' +
    '<div class="form-row"><div class="form-group"><label>' + t('rental.startDate') + '</label><input type="datetime-local" class="form-control" id="rMbStart" value="' + now.toISOString().slice(0, 16) + '"></div>' +
    '<div class="form-group"><label>' + t('rental.endDate') + '</label><input type="datetime-local" class="form-control" id="rMbEnd" value="' + end.toISOString().slice(0, 16) + '"></div></div>' +
    '<div class="form-group"><label>' + t('rental.notes') + '</label><input type="text" class="form-control" id="rMbNote" placeholder="' + t('rental.maintWindow') + '"></div>' +
  '</div><div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">' + t('common.cancel') + '</button><button class="btn btn-primary" onclick="rentSaveMaintBlock(\'' + vehicleId + '\')">' + t('common.save') + '</button></div>');
};
window.rentSaveMaintBlock = function(vehicleId) {
  vehicleMaintBlocks.push({
    id: genId(), vehicleId: vehicleId,
    startDate: document.getElementById('rMbStart').value,
    endDate: document.getElementById('rMbEnd').value,
    notes: document.getElementById('rMbNote').value.trim(), visible: true
  });
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (v) { v.status = 'Maintenance'; save('vehicles', vehicles); }
  save('vehicleMaintBlocks', vehicleMaintBlocks);
  closeModal(); rentRefreshRelatedViews(); toast(t('rental.maintScheduled'));
};
window.rentClearMaint = function(vehicleId) {
  var v = vehicles.find(function(x) { return x.id === vehicleId; });
  if (v) { v.status = 'Available'; save('vehicles', vehicles); }
  rentRefreshRelatedViews();
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
  var plate = document.getElementById('mVPlate').value.trim();
  if (!plate) { toast(t('rental.needPlate')); return; }
  var maxSort = rentSortedVehicles().reduce(function(m, v) { return Math.max(m, parseInt(v.sortOrder, 10) || 0); }, 0);
  vehicles.push({
    id: genId(), type: document.getElementById('mVType').value, brand: document.getElementById('mVBrand').value.trim(),
    model: document.getElementById('mVModel').value.trim(), plateNumber: plate,
    dailyRate: parseFloat(document.getElementById('mVDaily').value) || 0,
    hourlyRate: parseFloat(document.getElementById('mVHourly').value) || null,
    status: 'Available', sortOrder: maxSort + 1, visible: true
  });
  save('vehicles', vehicles); closeModal(); rentRefreshRelatedViews(); toast(t('rental.vehicleAdded'));
};
function renderVehicleRental() {
  rentSyncOverdueRentals();
  var pg = document.getElementById('page-vehiclerental');
  if (!pg) return;
  var list = rentSortedVehicles();
  var active = (vehicleRentals || []).filter(function(r) { return rowDataVisible(r) && r.status !== 'Completed' && r.status !== 'Cancelled'; });
  var avail = list.filter(function(v) { return rentGetVehicleFloorState(v) === 'available'; }).length;
  var out = active.length;
  var due = active.filter(function(r) { return r.status === 'Due' || r.paymentStatus === 'Pending'; }).length;
  var mode = window.rentViewMode || 'floor';
  var tabs = '<div class="rent-tabs">' +
    '<button type="button" class="rent-tab' + (mode === 'floor' ? ' active' : '') + '" onclick="rentSetView(\'floor\')">' + t('rental.tabFloor') + '</button>' +
    '<button type="button" class="rent-tab' + (mode === 'calendar' ? ' active' : '') + '" onclick="rentSetView(\'calendar\')">' + t('rental.tabCalendar') + '</button>' +
    '<button type="button" class="rent-tab' + (mode === 'pnl' ? ' active' : '') + '" onclick="rentSetView(\'pnl\')">' + t('rental.tabFleet') + '</button></div>';
  var mainBody = '';
  if (mode === 'calendar') {
    mainBody = rentRenderCalendarHtml();
  } else if (mode === 'pnl') {
    mainBody = rentRenderPnlHtml();
  } else {
    var tiles = '';
    list.forEach(function(v) {
      var st = rentGetVehicleFloorState(v);
      var ar = rentGetActiveRentalForVehicle(v.id);
      var tag = st === 'available' ? t('rental.stAvailable') : st === 'occupied' ? t('rental.stOut') : st === 'pending' ? t('rental.stDue') : t('rental.stMaint');
      var sub = ar ? (ar.guestName || '') : fmt$(v.dailyRate) + '/' + t('rental.perDay');
      tiles += '<button type="button" class="rent-vehicle-tile ' + st + '" onclick="rentFloorClick(\'' + v.id + '\')">' +
        '<span class="rvt-icon">' + rentVehicleIcon(v.type) + '</span>' +
        '<span class="rvt-plate">' + escAttr(v.plateNumber) + '</span>' +
        '<span class="rvt-tag">' + tag + '</span>' +
        '<span class="rvt-sub">' + escAttr(sub) + '</span></button>';
    });
    mainBody = '<div class="rent-floor-summary">' +
      '<span><span class="rent-legend-dot" style="background:#43a047;"></span> ' + avail + ' ' + t('rental.stAvailable') + '</span>' +
      '<span><span class="rent-legend-dot" style="background:#c62828;"></span> ' + out + ' ' + t('rental.stOut') + '</span>' +
      '<span><span class="rent-legend-dot" style="background:#f57c00;"></span> ' + due + ' ' + t('rental.stDue') + '</span></div>' +
      '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.5rem;">' + t('rental.floorHint') + '</p>' +
      '<div class="rent-vehicle-floor">' + (tiles || '<p>' + t('rental.noVehicles') + '</p>') + '</div>';
  }
  pg.innerHTML = rentRenderShiftNoticeHtml() +
    '<div class="card"><div class="card-header" style="flex-wrap:wrap;gap:0.5rem;"><h2>' + t('pageTitle.vehiclerental') + '</h2>' +
    '<div style="display:flex;gap:0.35rem;flex-wrap:wrap;"><button type="button" class="btn btn-sm btn-primary" onclick="showAddVehicle()">+ ' + t('rental.addVehicle') + '</button></div></div>' +
    '<div class="card-body">' + tabs +
    '<div class="stats-grid" style="margin-bottom:0.75rem;">' +
    '<div class="stat-card"><div class="stat-info"><h3>' + avail + '</h3><p>' + t('rental.stAvailable') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + out + '</h3><p>' + t('rental.stOut') + '</p></div></div>' +
    '<div class="stat-card"><div class="stat-info"><h3>' + due + '</h3><p>' + t('rental.stDue') + '</p></div></div></div>' +
    '<div style="margin-bottom:0.75rem;"><label style="font-size:0.82rem;font-weight:600;">' + t('rental.linkGuest') + ' / ' + t('rental.linkBooking') + '</label>' +
    rentRenderGuestPickerHtml() + '</div>' + mainBody + '</div></div>' +
    '<div class="card"><div class="card-header"><h2>' + t('rental.activeRentals') + '</h2></div><div class="card-body"><div id="rentActiveGrid"></div></div></div>' +
    '<div class="card"><div class="card-header"><h2>' + t('rental.reportTitle') + '</h2></div><div class="card-body"><div id="rentReportGrid"></div></div></div>';
  new XGrid('rentActiveGrid', {
    columns: [
      {field:'rentalNumber',label:t('rental.rentalNum'),filterable:true,width:'95px'},
      {field:'vehicleLabel',label:t('rental.vehicle'),filterable:true},
      {field:'guestName',label:t('g.guest'),filterable:true},
      {field:'pickupLocationName',label:t('rental.pickupLoc'),filterable:true,width:'100px'},
      {field:'startDate',label:t('rental.startDate'),width:'130px'},
      {field:'endDate',label:t('rental.endDate'),width:'130px'},
      {field:'grandTotal',label:(typeof t === 'function' && t('minimart.grandTotal') !== 'minimart.grandTotal') ? t('minimart.grandTotal') : 'Grand total',format:function(v){return fmt$(v);},width:'95px'},
      {field:'paymentMethod',label:t('g.payment'),filterable:true,width:'110px',format:function(v,row){return rentFormatPaymentDisplay(row);}}
    ],
    data: active,
    showSearch: true,
    emptyMessage: t('rental.noActive'),
    actions: [
      {name:'detail',label:t('common.view'),cls:'btn-outline',handler:function(id){ rentOpenRentalDetail(id); }},
      {name:'payRoom',label:t('rental.payRoom'),cls:'btn-primary',condition:function(r){ return rentCanChargeRoom(r); },handler:function(id){ rentPayRental(id,'Charged to Room'); }},
      {name:'payCash',label:t('minimart.cash'),cls:'btn-success',condition:function(r){ return rentRentalIsPayable(r); },handler:function(id){ rentPayRental(id,'Cash'); }},
      {name:'payCard',label:t('minimart.creditCard'),cls:'btn-warning',condition:function(r){ return rentRentalIsPayable(r); },handler:function(id){ rentPayRental(id,'Credit Card'); }},
      {name:'return',label:t('rental.returnBtn'),cls:'btn-primary',handler:function(id){ rentOpenReturnModal(id); }},
      {name:'wa',label:'WA',cls:'btn-outline',handler:function(id){ rentOpenWhatsApp(id,'confirm'); }}
    ]
  });
  active.forEach(function(r) { rentApplyBillToRental(r); });
  var completed = (vehicleRentals || []).filter(rowDataVisible).slice().reverse();
  completed.forEach(function(r) { rentApplyBillToRental(r); });
  new XGrid('rentReportGrid', {
    columns: [
      {field:'rentalNumber',label:t('rental.rentalNum'),filterable:true},
      {field:'vehicleType',label:t('rental.type'),filterable:true,width:'90px'},
      {field:'guestName',label:t('g.guest'),filterable:true},
      {field:'grandTotal',label:(typeof t === 'function' && t('minimart.grandTotal') !== 'minimart.grandTotal') ? t('minimart.grandTotal') : 'Grand total',format:function(v){return fmt$(v);}},
      {field:'paymentMethod',label:t('g.payment'),filterable:true,format:function(v,row){return rentFormatPaymentDisplay(row);}},
      {field:'status',label:t('g.status'),filterable:true},
      {field:'timestamp',label:t('g.date'),format:function(v){try{return new Date(v).toLocaleString();}catch(e){return v;}},width:'140px'}
    ],
    data: completed,
    showSearch: true,
    summaryRow: {rentalNumber:'label', grandTotal:'sum'},
    emptyMessage: t('rental.noHistory')
  });
  if (rentGuestSearch) filterRentGuestCards(rentGuestSearch);
}
