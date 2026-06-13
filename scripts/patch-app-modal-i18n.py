#!/usr/bin/env python3
"""Wire add/edit modal forms to i18n (maintenance, invoice, inventory, menu, store, user)."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-MODAL-I18N-v2"
INDEX = Path("public/index.html")

REPLACEMENTS: list[tuple[str, str]] = [
    # Maintenance ticket
    (
        'openModal(`<div class="modal-header"><h2>New Maintenance Ticket</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-row"><div class="form-group"><label>Room Number</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.newTicketTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-row"><div class="form-group"><label>${t(\'g.roomNumber\')}</label>',
    ),
    (
        '"><select class="form-control" id="mTkRoom">${(rooms || []).filter(rowDataVisible).map(r=>`<option value="${r.roomNumber}">${r.roomNumber} - ${r.roomType}</option>`).join(\'\')}</select></div><div class="form-group"><label>Priority${adminEditBtn(\'ticketPriorities\')}</label>',
        '"><select class="form-control" id="mTkRoom">${(rooms || []).filter(rowDataVisible).map(r=>`<option value="${r.roomNumber}">${r.roomNumber} - ${r.roomType}</option>`).join(\'\')}</select></div><div class="form-group"><label>${t(\'g.priority\')}${adminEditBtn(\'ticketPriorities\')}</label>',
    ),
    (
        '<div class="form-group"><label>Issue Description</label><textarea class="form-control" id="mTkIssue" rows="3" placeholder="Describe the issue..."></textarea></div>\n    <div class="form-group"><label>Notes</label><textarea class="form-control" id="mTkNotes" rows="2" placeholder="Additional notes..."></textarea></div></div>\n    <div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="addTicket()">Create Ticket</button></div>`);',
        '<div class="form-group"><label>${t(\'g.issue\')}</label><textarea class="form-control" id="mTkIssue" rows="3" placeholder="${String(t(\'modal.phDescribeIssue\')).replace(/"/g, \'&quot;\')}"></textarea></div>\n    <div class="form-group"><label>${t(\'g.notes\')}</label><textarea class="form-control" id="mTkNotes" rows="2" placeholder="${String(t(\'modal.phAdditionalNotes\')).replace(/"/g, \'&quot;\')}"></textarea></div></div>\n    <div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="addTicket()">${t(\'modal.createTicket\')}</button></div>`);',
    ),
    # Add invoice
    (
        'openModal(`<div class="modal-header"><h2>Add Invoice (${invNum})</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-row"><div class="form-group"><label>Guest Name</label><input type="text" class="form-control" id="mInvGuest" placeholder="Enter guest name"></div><div class="form-group"><label>Room Number</label><input type="text" class="form-control" id="mInvRoom" placeholder="e.g. 201"></div></div>\n    <div class="form-row"><div class="form-group"><label>Date</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.addInvoiceTitle\', { num: String(invNum) })}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-row"><div class="form-group"><label>${t(\'g.guest\')}</label><input type="text" class="form-control" id="mInvGuest" placeholder="${String(t(\'modal.phGuestNameInv\')).replace(/"/g, \'&quot;\')}"></div><div class="form-group"><label>${t(\'g.roomNumber\')}</label><input type="text" class="form-control" id="mInvRoom" placeholder="${String(t(\'modal.phRoomEg\')).replace(/"/g, \'&quot;\')}"></div></div>\n    <div class="form-row"><div class="form-group"><label>${t(\'g.date\')}</label>',
    ),
    (
        '"><input type="date" class="form-control" id="mInvDate" value="${today()}"></div><div class="form-group"><label>Currency${adminEditBtn(\'currencies\')}</label>',
        '"><input type="date" class="form-control" id="mInvDate" value="${today()}"></div><div class="form-group"><label>${t(\'g.currency\')}${adminEditBtn(\'currencies\')}</label>',
    ),
    (
        '<div class="form-row"><div class="form-group"><label>Subtotal</label><input type="number" class="form-control" id="mInvSub" step="0.01" placeholder="0.00"></div><div class="form-group"><label>Discount</label>',
        '<div class="form-row"><div class="form-group"><label>${t(\'g.subtotal\')}</label><input type="number" class="form-control" id="mInvSub" step="0.01" placeholder="0.00"></div><div class="form-group"><label>${t(\'g.discount\')}</label>',
    ),
    (
        '<div class="form-row"><div class="form-group"><label>Tax Total</label><input type="number" class="form-control" id="mInvTax" step="0.01" value="0"></div><div class="form-group"><label>Payment Status${adminEditBtn(\'invoiceStatuses\')}</label>',
        '<div class="form-row"><div class="form-group"><label>${t(\'modal.taxTotal\')}</label><input type="number" class="form-control" id="mInvTax" step="0.01" value="0"></div><div class="form-group"><label>${t(\'g.paymentStatus\')}${adminEditBtn(\'invoiceStatuses\')}</label>',
    ),
    (
        '<div class="form-group"><label>Transaction ID</label><input type="text" class="form-control" id="mInvTxn" placeholder="Optional"></div>\n    <div class="form-group"><label>Billing Address</label><input type="text" class="form-control" id="mInvAddr" placeholder="Optional"></div></div>\n    <div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="addInvoice()">Add Invoice</button></div>`);',
        '<div class="form-group"><label>${t(\'modal.transactionId\')}</label><input type="text" class="form-control" id="mInvTxn" placeholder="${String(t(\'modal.phOptional\')).replace(/"/g, \'&quot;\')}"></div>\n    <div class="form-group"><label>${t(\'modal.billingAddress\')}</label><input type="text" class="form-control" id="mInvAddr" placeholder="${String(t(\'modal.phBillingAddr\')).replace(/"/g, \'&quot;\')}"></div></div>\n    <div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="addInvoice()">${t(\'modal.addInvoiceBtn\')}</button></div>`);',
    ),
    # Edit invoice header/labels (partial - key fields)
    (
        'openModal(`<div class="modal-header"><h2>Edit ${inv.invoiceNumber}</h2>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.editInvoiceTitle\', { num: String(inv.invoiceNumber) })}</h2>',
    ),
    (
        '    <div class="form-row"><div class="form-group"><label>Guest Name</label><input type="text" class="form-control" id="eInvGuest" value="${inv.guestName}"></div><div class="form-group"><label>Room Number</label><input type="text" class="form-control" id="eInvRoom" value="${inv.roomNumber}"></div></div>\n    <div class="form-row"><div class="form-group"><label>Date</label><input type="date" class="form-control" id="eInvDate" value="${inv.date}"></div><div class="form-group"><label>Currency${adminEditBtn(\'currencies\')}</label>',
        '    <div class="form-row"><div class="form-group"><label>${t(\'g.guest\')}</label><input type="text" class="form-control" id="eInvGuest" value="${inv.guestName}"></div><div class="form-group"><label>${t(\'g.roomNumber\')}</label><input type="text" class="form-control" id="eInvRoom" value="${inv.roomNumber}"></div></div>\n    <div class="form-row"><div class="form-group"><label>${t(\'g.date\')}</label><input type="date" class="form-control" id="eInvDate" value="${inv.date}"></div><div class="form-group"><label>${t(\'g.currency\')}${adminEditBtn(\'currencies\')}</label>',
    ),
    (
        '    <div class="form-row"><div class="form-group"><label>Subtotal</label><input type="number" class="form-control" id="eInvSub" step="0.01" value="${inv.subtotal}"></div><div class="form-group"><label>Discount</label><input type="number" class="form-control" id="eInvDisc" step="0.01" value="${inv.discountAmount}"></div></div>\n    <div class="form-row"><div class="form-group"><label>Tax Total</label><input type="number" class="form-control" id="eInvTax" step="0.01" value="${inv.taxTotal}"></div><div class="form-group"><label>Payment Status${adminEditBtn(\'invoiceStatuses\')}</label>',
        '    <div class="form-row"><div class="form-group"><label>${t(\'g.subtotal\')}</label><input type="number" class="form-control" id="eInvSub" step="0.01" value="${inv.subtotal}"></div><div class="form-group"><label>${t(\'g.discount\')}</label><input type="number" class="form-control" id="eInvDisc" step="0.01" value="${inv.discountAmount}"></div></div>\n    <div class="form-row"><div class="form-group"><label>${t(\'modal.taxTotal\')}</label><input type="number" class="form-control" id="eInvTax" step="0.01" value="${inv.taxTotal}"></div><div class="form-group"><label>${t(\'g.paymentStatus\')}${adminEditBtn(\'invoiceStatuses\')}</label>',
    ),
    (
        '    <div class="form-group"><label>Transaction ID</label><input type="text" class="form-control" id="eInvTxn" value="${inv.paymentTransactionId||\'\'}"></div>\n    <div class="form-group"><label>Billing Address</label><input type="text" class="form-control" id="eInvAddr" value="${inv.billingAddress||\'\'}"></div></div>',
        '    <div class="form-group"><label>${t(\'modal.transactionId\')}</label><input type="text" class="form-control" id="eInvTxn" value="${inv.paymentTransactionId||\'\'}"></div>\n    <div class="form-group"><label>${t(\'modal.billingAddress\')}</label><input type="text" class="form-control" id="eInvAddr" value="${inv.billingAddress||\'\'}"></div></div>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="updateInvoice(\'${inv.id}\')">Save</button></div>`);\n};\nwindow.updateInvoice = function(id) {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="updateInvoice(\'${inv.id}\')">${t(\'common.save\')}</button></div>`);\n};\nwindow.updateInvoice = function(id) {',
    ),
    # Add inventory
    (
        'openModal(`<div class="modal-header"><h2>Add Inventory Item</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>Name</label><input type="text" class="form-control" id="mInvName" placeholder="e.g. Bath Towels"></div>\n    <div class="form-group"><label>Barcode (UPC / SKU)</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.addInventoryTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>${t(\'g.name\')}</label><input type="text" class="form-control" id="mInvName" placeholder="${String(t(\'modal.phTowels\')).replace(/"/g, \'&quot;\')}"></div>\n    <div class="form-group"><label>${t(\'g.barcode\')}</label>',
    ),
    (
        'placeholder="e.g. 5901234123457" autocomplete="off" autocapitalize="off" spellcheck="false" inputmode="numeric"></div>\n    <div class="form-row"><div class="form-group"><label>Category${adminEditBtn(\'inventoryCategories\')}</label>',
        'placeholder="${String(t(\'modal.phBarcodeEg\')).replace(/"/g, \'&quot;\')}" autocomplete="off" autocapitalize="off" spellcheck="false" inputmode="numeric"></div>\n    <div class="form-row"><div class="form-group"><label>${t(\'g.category\')}${adminEditBtn(\'inventoryCategories\')}</label>',
    ),
    (
        '"><select class="form-control" id="mInvCat">${getInventoryCategories().map(s=>\'<option>\'+s+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>Quantity on hand</label>',
        '"><select class="form-control" id="mInvCat">${getInventoryCategories().map(s=>\'<option>\'+s+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>${t(\'modal.quantityOnHand\')}</label>',
    ),
    (
        '<div class="form-group"><label>Available on POS</label><select class="form-control" id="mInvPosAvail"><option value="true">Yes</option><option value="false">No</option></select></div>\n    <div class="form-group"><label>Description</label><textarea class="form-control" id="mInvDesc" rows="2" placeholder="Internal notes, SKU, or shelf location…"></textarea></div>',
        '<div class="form-group"><label>${t(\'modal.availableOnPos\')}</label><select class="form-control" id="mInvPosAvail"><option value="true">${t(\'common.yes\')}</option><option value="false">${t(\'common.no\')}</option></select></div>\n    <div class="form-group"><label>${t(\'g.description\')}</label><textarea class="form-control" id="mInvDesc" rows="2" placeholder="${String(t(\'modal.phInternalNotes\')).replace(/"/g, \'&quot;\')}"></textarea></div>',
    ),
    (
        '<div class="form-row"><div class="form-group"><label>Reorder level</label><input type="number" class="form-control" id="mInvReorder" value="10" min="0"></div><div class="form-group"><label>Last ordered</label>',
        '<div class="form-row"><div class="form-group"><label>${t(\'modal.reorderLevel\')}</label><input type="number" class="form-control" id="mInvReorder" value="10" min="0"></div><div class="form-group"><label>${t(\'modal.lastOrdered\')}</label>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="addInventoryItem()">Add Item</button></div>`);\n};\nwindow.addInventoryItem = function() {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="addInventoryItem()">${t(\'modal.addItemBtn\')}</button></div>`);\n};\nwindow.addInventoryItem = function() {',
    ),
    # Add menu item
    (
        'openModal(`<div class="modal-header"><h2>Add Menu Item</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>Name</label><input type="text" class="form-control" id="mMiName" placeholder="e.g. Pad Thai"></div>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.addMenuTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>${t(\'g.name\')}</label><input type="text" class="form-control" id="mMiName" placeholder="${String(t(\'modal.phPadThai\')).replace(/"/g, \'&quot;\')}"></div>',
    ),
    (
        '<div class="form-row"><div class="form-group"><label>Category${adminEditBtn(\'menuCategories\')}</label><select class="form-control" id="mMiCat">${getMenuCategories().map(s=>\'<option>\'+s+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>Price ($)</label>',
        '<div class="form-row"><div class="form-group"><label>${t(\'g.category\')}${adminEditBtn(\'menuCategories\')}</label><select class="form-control" id="mMiCat">${getMenuCategories().map(s=>\'<option>\'+s+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>${t(\'modal.priceUsd\')}</label>',
    ),
    (
        '<div class="form-group"><label>Available</label><select class="form-control" id="mMiAvail"><option value="true">Yes</option><option value="false">No</option></select></div>\n    <div class="form-group"><label>${t(\'g.imageFromFile\')}</label>',
        '<div class="form-group"><label>${t(\'g.available\')}</label><select class="form-control" id="mMiAvail"><option value="true">${t(\'common.yes\')}</option><option value="false">${t(\'common.no\')}</option></select></div>\n    <div class="form-group"><label>${t(\'g.imageFromFile\')}</label>',
    ),
    (
        '<div class="form-group"><label>Description</label><textarea class="form-control" id="mMiDesc" rows="2" placeholder="Item description..."></textarea></div>\n    <div class="form-group"><label>Barcode (UPC / SKU)</label>',
        '<div class="form-group"><label>${t(\'g.description\')}</label><textarea class="form-control" id="mMiDesc" rows="2" placeholder="${String(t(\'modal.phItemDesc\')).replace(/"/g, \'&quot;\')}"></textarea></div>\n    <div class="form-group"><label>${t(\'g.barcode\')}</label>',
    ),
    (
        '<div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>Uses inventory (F&amp;B stock)</label><select class="form-control" id="mMiInv">${inventoryOptionsForMenuHtml(\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">When a guest order is <strong>paid</strong>, this stock line decreases by (units per serving × quantity sold). Optional: if unset, the app may still match by exact dish name to an inventory item.</small></div>\n    <div class="form-group"><label>Units per serving</label>',
        '<div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>${t(\'modal.usesInventory\')}</label><select class="form-control" id="mMiInv">${inventoryOptionsForMenuHtml(\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">${t(\'modal.menuStockHint\')}</small></div>\n    <div class="form-group"><label>${t(\'g.unitsPerServing\')}</label>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="addMenuItem()">Add Item</button></div>`);\n};\nwindow.addMenuItem = function() {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="addMenuItem()">${t(\'modal.addItemBtn\')}</button></div>`);\n};\nwindow.addMenuItem = function() {',
    ),
    # Add store item
    (
        'openModal(`<div class="modal-header"><h2>Add Store Item</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>Name</label><input type="text" class="form-control" id="mSiName" placeholder="e.g. Water Bottle"></div>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.addStoreTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>${t(\'g.name\')}</label><input type="text" class="form-control" id="mSiName" placeholder="${String(t(\'modal.phWaterBottle\')).replace(/"/g, \'&quot;\')}"></div>',
    ),
    (
        '<div class="form-row"><div class="form-group"><label>Category${adminEditBtn(\'storeCategories\')}</label><select class="form-control" id="mSiCat">${getStoreCategories().map(s=>\'<option>\'+s+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>Price ($)</label>',
        '<div class="form-row"><div class="form-group"><label>${t(\'g.category\')}${adminEditBtn(\'storeCategories\')}</label><select class="form-control" id="mSiCat">${getStoreCategories().map(s=>\'<option>\'+s+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>${t(\'modal.priceUsd\')}</label>',
    ),
    (
        '<div class="form-group"><label>Shelf icon (emoji, optional if no photo)</label><input type="text" class="form-control" id="mSiEmoji" maxlength="12" placeholder="e.g. 💧"></div>\n    <div class="form-group"><label>Description</label><textarea class="form-control" id="mSiDesc" rows="2" placeholder="Item description..."></textarea></div>\n    <div class="form-group"><label>Barcode (UPC / SKU)</label><input type="text" class="form-control" id="mSiBarcode" placeholder="Scan or type barcode (e.g. 5901234123457)"',
        '<div class="form-group"><label>${t(\'modal.shelfIconLabel\')}</label><input type="text" class="form-control" id="mSiEmoji" maxlength="12" placeholder="${String(t(\'modal.phShelfIcon\')).replace(/"/g, \'&quot;\')}"></div>\n    <div class="form-group"><label>${t(\'g.description\')}</label><textarea class="form-control" id="mSiDesc" rows="2" placeholder="${String(t(\'modal.phItemDesc\')).replace(/"/g, \'&quot;\')}"></textarea></div>\n    <div class="form-group"><label>${t(\'g.barcode\')}</label><input type="text" class="form-control" id="mSiBarcode" placeholder="${String(t(\'modal.phScanBarcode\')).replace(/"/g, \'&quot;\')}"',
    ),
    (
        '<div class="form-group"><label>Stock</label><input type="number" class="form-control" id="mSiStock" value="0" min="0"></div>\n    <div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>Uses inventory (F&amp;B stock)</label><select class="form-control" id="mSiInv">${inventoryOptionsForMenuHtml(\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">When a Mini-Mart sale completes, this stock line decreases by (units per serving × quantity sold), in addition to the shelf <strong>Stock</strong> count above. Leave unset to match by product name only.</small></div>\n    <div class="form-group"><label>Units per serving</label>',
        '<div class="form-group"><label>${t(\'g.stock\')}</label><input type="number" class="form-control" id="mSiStock" value="0" min="0"></div>\n    <div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>${t(\'modal.usesInventory\')}</label><select class="form-control" id="mSiInv">${inventoryOptionsForMenuHtml(\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">${t(\'modal.storeStockHint\')}</small></div>\n    <div class="form-group"><label>${t(\'g.unitsPerServing\')}</label>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="addStoreItem()">Add Item</button></div>`);\n};\nwindow.addStoreItem = function() {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="addStoreItem()">${t(\'modal.addItemBtn\')}</button></div>`);\n};\nwindow.addStoreItem = function() {',
    ),
    # Add user account
    (
        'openModal(`<div class="modal-header"><h2>Add User</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body"><div class="form-group"><label>Full Name</label><input type="text" class="form-control" id="mAName"></div>\n    <div class="form-group"><label>Email</label><input type="email" class="form-control" id="mAEmail"></div>\n    <div class="form-group"><label>Password</label><input type="password" class="form-control" id="mAPass" placeholder="Set password"></div>\n    <div class="form-group"><label>Role${adminEditBtn(\'userRoles\')}</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.addUserTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body"><div class="form-group"><label>${t(\'modal.fullName\')}</label><input type="text" class="form-control" id="mAName"></div>\n    <div class="form-group"><label>${t(\'g.email\')}</label><input type="email" class="form-control" id="mAEmail"></div>\n    <div class="form-group"><label>${t(\'modal.password\')}</label><input type="password" class="form-control" id="mAPass" placeholder="${String(t(\'modal.phSetPassword\')).replace(/"/g, \'&quot;\')}"></div>\n    <div class="form-group"><label>${t(\'g.role\')}${adminEditBtn(\'userRoles\')}</label>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="addAccount()">Add User</button></div>`);\n};\nwindow.addAccount = function() {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="addAccount()">${t(\'modal.addUserBtn\')}</button></div>`);\n};\nwindow.addAccount = function() {',
    ),
    (
        'openModal(`<div class="modal-header"><h2>Edit User</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body"><div class="form-group"><label>Full Name</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.editUserTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body"><div class="form-group"><label>${t(\'modal.fullName\')}</label>',
    ),
    (
        'placeholder="Change password"></div>\n    <div class="form-group"><label>Role${adminEditBtn(\'userRoles\')}</label><select class="form-control" id="eARole">${getUserRoles().map(r=>`<option ${r===a.role?\'selected\':\'\'}>${r}</option>`).join(\'\')}</select></div></div>\n    <div class="modal-footer"><button class="btn btn-danger" onclick="deleteAccount(\'${a.id}\')">Delete</button><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="updateAccount(\'${a.id}\')">Save</button></div>`);',
        'placeholder="${String(t(\'modal.phChangePassword\')).replace(/"/g, \'&quot;\')}"></div>\n    <div class="form-group"><label>${t(\'g.role\')}${adminEditBtn(\'userRoles\')}</label><select class="form-control" id="eARole">${getUserRoles().map(r=>`<option ${r===a.role?\'selected\':\'\'}>${r}</option>`).join(\'\')}</select></div></div>\n    <div class="modal-footer"><button class="btn btn-danger" onclick="deleteAccount(\'${a.id}\')">${t(\'common.delete\')}</button><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="updateAccount(\'${a.id}\')">${t(\'common.save\')}</button></div>`);',
    ),
    (
        '    <div class="form-group"><label>Email</label><input type="email" class="form-control" id="eAEmail" value="${a.email}"></div>\n    <div class="form-group"><label>Password</label><input type="password" class="form-control" id="eAPass" value="${a.password||\'\'}" placeholder="${String(t(\'modal.phChangePassword\')).replace(/"/g, \'&quot;\')}"></div>',
        '    <div class="form-group"><label>${t(\'g.email\')}</label><input type="email" class="form-control" id="eAEmail" value="${a.email}"></div>\n    <div class="form-group"><label>${t(\'modal.password\')}</label><input type="password" class="form-control" id="eAPass" value="${a.password||\'\'}" placeholder="${String(t(\'modal.phChangePassword\')).replace(/"/g, \'&quot;\')}"></div>',
    ),
    (
        '<div class="form-group"><label>Available</label><select class="form-control" id="mSiAvail"><option value="true">Yes</option><option value="false">No</option></select></div>\n    <div class="form-group"><label>${t(\'g.imageFromFile\')}</label><input type="file" id="mSiImgFile"',
        '<div class="form-group"><label>${t(\'g.available\')}</label><select class="form-control" id="mSiAvail"><option value="true">${t(\'common.yes\')}</option><option value="false">${t(\'common.no\')}</option></select></div>\n    <div class="form-group"><label>${t(\'g.imageFromFile\')}</label><input type="file" id="mSiImgFile"',
    ),
    # Edit inventory
    (
        'openModal(`<div class="modal-header"><h2>Edit Inventory Item</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>Name</label><input type="text" class="form-control" id="eInvName" value="${escAttr(it.itemName)}"></div>\n    <div class="form-group"><label>Barcode (UPC / SKU)</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.editInventoryTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>${t(\'g.name\')}</label><input type="text" class="form-control" id="eInvName" value="${escAttr(it.itemName)}"></div>\n    <div class="form-group"><label>${t(\'g.barcode\')}</label>',
    ),
    (
        'value="${escAttr(it.barcode||\'\')}" placeholder="e.g. 5901234123457" autocomplete="off" autocapitalize="off" spellcheck="false" inputmode="numeric"></div>\n    <div class="form-row"><div class="form-group"><label>Category${adminEditBtn(\'inventoryCategories\')}</label>',
        'value="${escAttr(it.barcode||\'\')}" placeholder="${String(t(\'modal.phBarcodeEg\')).replace(/"/g, \'&quot;\')}" autocomplete="off" autocapitalize="off" spellcheck="false" inputmode="numeric"></div>\n    <div class="form-row"><div class="form-group"><label>${t(\'g.category\')}${adminEditBtn(\'inventoryCategories\')}</label>',
    ),
    (
        '"><select class="form-control" id="eInvCat">${getInventoryCategories().map(c=>`<option ${c===it.category?\'selected\':\'\'}>${c}</option>`).join(\'\')}</select></div><div class="form-group"><label>Quantity on hand</label>',
        '"><select class="form-control" id="eInvCat">${getInventoryCategories().map(c=>`<option ${c===it.category?\'selected\':\'\'}>${c}</option>`).join(\'\')}</select></div><div class="form-group"><label>${t(\'modal.quantityOnHand\')}</label>',
    ),
    (
        '<div class="form-group"><label>Available on POS</label><select class="form-control" id="eInvPosAvail"><option value="true" ${it.posAvailable!==false?\'selected\':\'\'}>Yes</option><option value="false" ${it.posAvailable===false?\'selected\':\'\'}>No</option></select></div>\n    <div class="form-group"><label>Description</label>',
        '<div class="form-group"><label>${t(\'modal.availableOnPos\')}</label><select class="form-control" id="eInvPosAvail"><option value="true" ${it.posAvailable!==false?\'selected\':\'\'}>${t(\'common.yes\')}</option><option value="false" ${it.posAvailable===false?\'selected\':\'\'}>${t(\'common.no\')}</option></select></div>\n    <div class="form-group"><label>${t(\'g.description\')}</label>',
    ),
    (
        '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.25rem;${(it.imageUrl && String(it.imageUrl).indexOf(\'data:image/\')===0)?\'\':\'display:none;\'}">Photo file stored on this device — choose a new file to replace.</p>',
        '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.25rem;${(it.imageUrl && String(it.imageUrl).indexOf(\'data:image/\')===0)?\'\':\'display:none;\'}">${t(\'modal.photoStoredHint\')}</p>',
    ),
    (
        '    <div class="form-row"><div class="form-group"><label>Reorder level</label><input type="number" class="form-control" id="eInvReorder" value="${it.reorderLevel}" min="0"></div><div class="form-group"><label>Last ordered</label><input type="date" class="form-control" id="eInvDate" value="${it.lastOrdered||\'\'}"></div></div></div>\n    <div class="modal-footer"><button class="btn btn-danger" onclick="deleteInventoryItem(\'${it.id}\')">Delete</button><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="updateInventoryItem(\'${it.id}\')">Save</button></div>`);',
        '    <div class="form-row"><div class="form-group"><label>${t(\'modal.reorderLevel\')}</label><input type="number" class="form-control" id="eInvReorder" value="${it.reorderLevel}" min="0"></div><div class="form-group"><label>${t(\'modal.lastOrdered\')}</label><input type="date" class="form-control" id="eInvDate" value="${it.lastOrdered||\'\'}"></div></div></div>\n    <div class="modal-footer"><button class="btn btn-danger" onclick="deleteInventoryItem(\'${it.id}\')">${t(\'common.delete\')}</button><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="updateInventoryItem(\'${it.id}\')">${t(\'common.save\')}</button></div>`);',
    ),
    # Edit menu item
    (
        'openModal(`<div class="modal-header"><h2>Edit Menu Item</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>Name</label><input type="text" class="form-control" id="eMiName" value="${m.name.replace(/"/g, \'&quot;\')}"></div>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.editMenuTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>${t(\'g.name\')}</label><input type="text" class="form-control" id="eMiName" value="${m.name.replace(/"/g, \'&quot;\')}"></div>',
    ),
    (
        '    <div class="form-row"><div class="form-group"><label>Category${adminEditBtn(\'menuCategories\')}</label><select class="form-control" id="eMiCat">${getMenuCategories().map(c=>\'<option\'+(c===m.category?\' selected\':\'\')+\'>\'+c+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>Price ($)</label>',
        '    <div class="form-row"><div class="form-group"><label>${t(\'g.category\')}${adminEditBtn(\'menuCategories\')}</label><select class="form-control" id="eMiCat">${getMenuCategories().map(c=>\'<option\'+(c===m.category?\' selected\':\'\')+\'>\'+c+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>${t(\'modal.priceUsd\')}</label>',
    ),
    (
        '    <div class="form-group"><label>Available</label><select class="form-control" id="eMiAvail"><option value="true" ${m.available?\'selected\':\'\'}>Yes</option><option value="false" ${!m.available?\'selected\':\'\'}>No</option></select></div>',
        '    <div class="form-group"><label>${t(\'g.available\')}</label><select class="form-control" id="eMiAvail"><option value="true" ${m.available?\'selected\':\'\'}>${t(\'common.yes\')}</option><option value="false" ${!m.available?\'selected\':\'\'}>${t(\'common.no\')}</option></select></div>',
    ),
    (
        '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.25rem;${dataImg ? \'\' : \'display:none;\'}">Photo file stored on this device — choose a new file to replace.</p>',
        '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.25rem;${dataImg ? \'\' : \'display:none;\'}">${t(\'modal.photoStoredHint\')}</p>',
    ),
    (
        '    <div class="form-group"><label>Description</label><textarea class="form-control" id="eMiDesc" rows="2">${(m.description||\'\').replace(/</g,\'&lt;\')}</textarea></div>\n    <div class="form-group"><label>Barcode (UPC / SKU)</label><input type="text" class="form-control" id="eMiBarcode" value="${escAttr(m.barcode || \'\')}" placeholder="e.g. 5901234123457"',
        '    <div class="form-group"><label>${t(\'g.description\')}</label><textarea class="form-control" id="eMiDesc" rows="2">${(m.description||\'\').replace(/</g,\'&lt;\')}</textarea></div>\n    <div class="form-group"><label>${t(\'g.barcode\')}</label><input type="text" class="form-control" id="eMiBarcode" value="${escAttr(m.barcode || \'\')}" placeholder="${String(t(\'modal.phBarcodeEg\')).replace(/"/g, \'&quot;\')}"',
    ),
    (
        '    <div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>Uses inventory (F&amp;B stock)</label><select class="form-control" id="eMiInv">${inventoryOptionsForMenuHtml(m.inventoryItemId||\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">Stock is reduced when the order is <strong>paid</strong> (checkout or settle bill).</small></div>\n    <div class="form-group"><label>Units per serving</label>',
        '    <div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>${t(\'modal.usesInventory\')}</label><select class="form-control" id="eMiInv">${inventoryOptionsForMenuHtml(m.inventoryItemId||\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">${t(\'modal.menuStockHintEdit\')}</small></div>\n    <div class="form-group"><label>${t(\'g.unitsPerServing\')}</label>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="updateMenuItem(\'${m.id}\')">Save</button></div>`);\n};\nwindow.updateMenuItem = function(id) {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="updateMenuItem(\'${m.id}\')">${t(\'common.save\')}</button></div>`);\n};\nwindow.updateMenuItem = function(id) {',
    ),
    # Edit store item
    (
        'openModal(`<div class="modal-header"><h2>Edit Store Item</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>Name</label><input type="text" class="form-control" id="eSiName" value="${escAttr(s.name)}"></div>\n    <div class="form-row"><div class="form-group"><label>Category${adminEditBtn(\'storeCategories\')}</label>',
        'openModal(`<div class="modal-header"><h2>${t(\'modal.editStoreTitle\')}</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>\n    <div class="modal-body">\n    <div class="form-group"><label>${t(\'g.name\')}</label><input type="text" class="form-control" id="eSiName" value="${escAttr(s.name)}"></div>\n    <div class="form-row"><div class="form-group"><label>${t(\'g.category\')}${adminEditBtn(\'storeCategories\')}</label>',
    ),
    (
        '"><select class="form-control" id="eSiCat">${getStoreCategories().map(c=>\'<option\'+(c===s.category?\' selected\':\'\')+\'>\'+c+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>Price ($)</label>',
        '"><select class="form-control" id="eSiCat">${getStoreCategories().map(c=>\'<option\'+(c===s.category?\' selected\':\'\')+\'>\'+c+\'</option>\').join(\'\')}</select></div><div class="form-group"><label>${t(\'modal.priceUsd\')}</label>',
    ),
    (
        '    <div class="form-group"><label>Available</label><select class="form-control" id="eSiAvail"><option value="true" ${s.available!==false?\'selected\':\'\'}>Yes</option><option value="false" ${s.available===false?\'selected\':\'\'}>No</option></select></div>',
        '    <div class="form-group"><label>${t(\'g.available\')}</label><select class="form-control" id="eSiAvail"><option value="true" ${s.available!==false?\'selected\':\'\'}>${t(\'common.yes\')}</option><option value="false" ${s.available===false?\'selected\':\'\'}>${t(\'common.no\')}</option></select></div>',
    ),
    (
        '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.25rem;${dataImgS ? \'\' : \'display:none;\'}">Photo file stored on this device — choose a new file to replace.</p>',
        '<p style="font-size:0.78rem;color:var(--text-light);margin:0 0 0.25rem;${dataImgS ? \'\' : \'display:none;\'}">${t(\'modal.photoStoredHint\')}</p>',
    ),
    (
        '    <div class="form-group"><label>Shelf icon (emoji)</label><input type="text" class="form-control" id="eSiEmoji" maxlength="12" value="${escAttr(imgPh)}" placeholder="e.g. 💧"></div>\n    <div class="form-group"><label>Description</label>',
        '    <div class="form-group"><label>${t(\'modal.shelfIconLabel\')}</label><input type="text" class="form-control" id="eSiEmoji" maxlength="12" value="${escAttr(imgPh)}" placeholder="${String(t(\'modal.phShelfIcon\')).replace(/"/g, \'&quot;\')}"></div>\n    <div class="form-group"><label>${t(\'g.description\')}</label>',
    ),
    (
        '    <div class="form-group"><label>Barcode (UPC / SKU)</label><input type="text" class="form-control" id="eSiBarcode" value="${escAttr(s.barcode||\'\')}" placeholder="Scan or type barcode"',
        '    <div class="form-group"><label>${t(\'g.barcode\')}</label><input type="text" class="form-control" id="eSiBarcode" value="${escAttr(s.barcode||\'\')}" placeholder="${String(t(\'modal.phScanBarcode\')).replace(/"/g, \'&quot;\')}"',
    ),
    (
        '    <div class="form-group"><label>Stock</label><input type="number" class="form-control" id="eSiStock" value="${s.stock}" min="0"></div>\n    <div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>Uses inventory (F&amp;B stock)</label><select class="form-control" id="eSiInv">${inventoryOptionsForMenuHtml(s.inventoryItemId||\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">Linked stock is reduced when the Mini-Mart sale completes.</small></div>\n    <div class="form-group"><label>Units per serving</label>',
        '    <div class="form-group"><label>${t(\'g.stock\')}</label><input type="number" class="form-control" id="eSiStock" value="${s.stock}" min="0"></div>\n    <div class="form-row"><div class="form-group" style="flex:2;min-width:200px;"><label>${t(\'modal.usesInventory\')}</label><select class="form-control" id="eSiInv">${inventoryOptionsForMenuHtml(s.inventoryItemId||\'\')}</select>\n    <small style="font-size:0.72rem;color:var(--text-light);display:block;margin-top:0.3rem;line-height:1.35;">${t(\'modal.storeStockHintEdit\')}</small></div>\n    <div class="form-group"><label>${t(\'g.unitsPerServing\')}</label>',
    ),
    (
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">Cancel</button><button class="btn btn-primary" onclick="updateStoreItem(\'${s.id}\')">Save</button></div>`);\n};\nwindow.updateStoreItem = function(id) {',
        '<div class="modal-footer"><button class="btn btn-outline" onclick="closeModal()">${t(\'common.cancel\')}</button><button class="btn btn-primary" onclick="updateStoreItem(\'${s.id}\')">${t(\'common.save\')}</button></div>`);\n};\nwindow.updateStoreItem = function(id) {',
    ),
]


def patch(content: str) -> str:
    if MARKER in content and "modal.editInventoryTitle" in content:
        return content
    changed = 0
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new, 1)
            changed += 1
    if changed == 0:
        print("No modal i18n replacements matched.", file=sys.stderr)
        return content
    if MARKER not in content:
        content = content.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)
    print(f"Applied {changed} modal i18n replacements")
    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    patched = patch(text)
    if patched != text:
        INDEX.write_text(patched, encoding="utf-8")
        print(f"Patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
