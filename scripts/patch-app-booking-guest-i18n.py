#!/usr/bin/env python3
"""Wire booking quick-add guest modal and nationality picker to i18n."""
from __future__ import annotations

import sys
from pathlib import Path

MARKER = "HRMM-BOOKING-GUEST-I18N-v1"
INDEX = Path("public/index.html")

HELPER = r"""function newGuestFromBookingModalMarkup() {
  return '<div class="modal-header"><h2>' + t('msg.newGuest') + '</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>' +
    '<div class="modal-body">' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.firstName') + '</label><input type="text" class="form-control" id="mNgFirst" placeholder="' + t('g.firstName') + '"></div><div class="form-group"><label>' + t('g.lastName') + '</label><input type="text" class="form-control" id="mNgLast" placeholder="' + t('g.lastName') + '"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.passportId') + '</label><input type="text" class="form-control" id="mNgPassport" placeholder="' + t('guest.phPassport') + '"></div><div class="form-group"><label>' + t('g.nationality') + '</label><input type="text" class="form-control" id="mNgNat" placeholder="' + t('guest.phNat') + '" readonly onclick="openNationalityPicker(\'mNgNat\')" style="cursor:pointer;"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('guest.dobLabel') + '</label><input type="date" class="form-control" id="mNgDob"></div><div class="form-group"><label>' + t('g.payment') + adminEditBtn('paymentMethods') + '</label><select class="form-control" id="mNgPay">' + getPaymentMethods().map(function(s) { return '<option>' + s + '</option>'; }).join('') + '</select></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.email') + '</label><input type="email" class="form-control" id="mNgEmail" placeholder="' + t('guest.phEmail') + '"></div><div class="form-group"><label>' + t('g.phone') + '</label><input type="tel" class="form-control" id="mNgPhone" placeholder="' + t('guest.phPhone') + '"></div></div>' +
    '<div class="form-group"><label>' + t('guest.notesLabel') + '</label><textarea class="form-control" id="mNgNotes" rows="2" placeholder="' + t('guest.phNotes') + '"></textarea></div></div>' +
    '<div class="modal-footer"><button class="btn btn-outline" onclick="cancelNewGuestFromBooking()">' + t('common.cancel') + '</button><button class="btn btn-primary" onclick="saveNewGuestFromBooking()">' + t('msg.addGuestReturn') + '</button></div>';
}
"""

REPLACEMENTS: list[tuple[str, str]] = [
    (
        "window.addNewGuestFromBooking = function() {",
        HELPER + "\nwindow.addNewGuestFromBooking = function() {",
    ),
    (
        """  openModal(`<div class="modal-header"><h2>New Guest</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>
    <div class="modal-body">
    <div class="form-row"><div class="form-group"><label>First Name</label><input type="text" class="form-control" id="mNgFirst" placeholder="First name"></div><div class="form-group"><label>Last Name</label><input type="text" class="form-control" id="mNgLast" placeholder="Last name"></div></div>
    <div class="form-row"><div class="form-group"><label>Passport / ID</label><input type="text" class="form-control" id="mNgPassport" placeholder="e.g. US-12345678"></div><div class="form-group"><label>Nationality</label><input type="text" class="form-control" id="mNgNat" placeholder="Tap to select" readonly onclick="openNationalityPicker('mNgNat')" style="cursor:pointer;"></div></div>
    <div class="form-row"><div class="form-group"><label>Date of Birth</label><input type="date" class="form-control" id="mNgDob"></div><div class="form-group"><label>Payment Method${adminEditBtn('paymentMethods')}</label><select class="form-control" id="mNgPay">${getPaymentMethods().map(s=>'<option>'+s+'</option>').join('')}</select></div></div>
    <div class="form-row"><div class="form-group"><label>Email</label><input type="email" class="form-control" id="mNgEmail" placeholder="email@example.com"></div><div class="form-group"><label>Phone</label><input type="tel" class="form-control" id="mNgPhone" placeholder="+1 555-0000"></div></div>
    <div class="form-group"><label>Guest Notes</label><textarea class="form-control" id="mNgNotes" rows="2" placeholder="Allergies, preferences..."></textarea></div></div>
    <div class="modal-footer"><button class="btn btn-outline" onclick="cancelNewGuestFromBooking()">Cancel</button><button class="btn btn-primary" onclick="saveNewGuestFromBooking()">Add Guest & Return</button></div>`);""",
        "  openModal(newGuestFromBookingModalMarkup());",
    ),
    (
        """function reopenNewGuestForm(backup) {
  _natReturnHandler = 'booking';
  openModal(`<div class="modal-header"><h2>New Guest</h2><button class="modal-close" onclick="closeModal()">&times;</button></div>
    <div class="modal-body">
    <div class="form-row"><div class="form-group"><label>First Name</label><input type="text" class="form-control" id="mNgFirst" placeholder="First name"></div><div class="form-group"><label>Last Name</label><input type="text" class="form-control" id="mNgLast" placeholder="Last name"></div></div>
    <div class="form-row"><div class="form-group"><label>Passport / ID</label><input type="text" class="form-control" id="mNgPassport" placeholder="e.g. US-12345678"></div><div class="form-group"><label>Nationality</label><input type="text" class="form-control" id="mNgNat" placeholder="Tap to select" readonly onclick="openNationalityPicker('mNgNat')" style="cursor:pointer;"></div></div>
    <div class="form-row"><div class="form-group"><label>Date of Birth</label><input type="date" class="form-control" id="mNgDob"></div><div class="form-group"><label>Payment Method${adminEditBtn('paymentMethods')}</label><select class="form-control" id="mNgPay">${getPaymentMethods().map(s=>'<option>'+s+'</option>').join('')}</select></div></div>
    <div class="form-row"><div class="form-group"><label>Email</label><input type="email" class="form-control" id="mNgEmail" placeholder="email@example.com"></div><div class="form-group"><label>Phone</label><input type="tel" class="form-control" id="mNgPhone" placeholder="+1 555-0000"></div></div>
    <div class="form-group"><label>Guest Notes</label><textarea class="form-control" id="mNgNotes" rows="2" placeholder="Allergies, preferences..."></textarea></div></div>
    <div class="modal-footer"><button class="btn btn-outline" onclick="cancelNewGuestFromBooking()">Cancel</button><button class="btn btn-primary" onclick="saveNewGuestFromBooking()">Add Guest & Return</button></div>`);""",
        """function reopenNewGuestForm(backup) {
  _natReturnHandler = 'booking';
  openModal(newGuestFromBookingModalMarkup());""",
    ),
    (
        """    '<div class="form-row"><div class="form-group"><label>First Name</label><input type="text" class="form-control" id="mMartQaFirst" placeholder="First name"></div><div class="form-group"><label>Last Name</label><input type="text" class="form-control" id="mMartQaLast" placeholder="Last name"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>Passport / ID</label><input type="text" class="form-control" id="mMartQaPassport" placeholder="e.g. US-12345678"></div><div class="form-group"><label>Nationality</label><input type="text" class="form-control" id="mMartQaNat" placeholder="Tap to select" readonly onclick="openNationalityPicker(\\'mMartQaNat\\')" style="cursor:pointer;"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>Date of Birth</label><input type="date" class="form-control" id="mMartQaDob"></div><div class="form-group"><label>Payment Method' + adminEditBtn('paymentMethods') + '</label><select class="form-control" id="mMartQaPay">' + getPaymentMethods().map(s=>'<option>'+s+'</option>').join('') + '</select></div></div>' +
    '<div class="form-row"><div class="form-group"><label>Email</label><input type="email" class="form-control" id="mMartQaEmail" placeholder="email@example.com"></div><div class="form-group"><label>Phone</label><input type="tel" class="form-control" id="mMartQaPhone" placeholder="+1 555-0000"></div></div>' +
    '<div class="form-group"><label>Guest Notes</label><textarea class="form-control" id="mMartQaNotes" rows="2" placeholder="Allergies, preferences..."></textarea></div></div>' +""",
        """    '<div class="form-row"><div class="form-group"><label>' + t('g.firstName') + '</label><input type="text" class="form-control" id="mMartQaFirst" placeholder="' + t('g.firstName') + '"></div><div class="form-group"><label>' + t('g.lastName') + '</label><input type="text" class="form-control" id="mMartQaLast" placeholder="' + t('g.lastName') + '"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.passportId') + '</label><input type="text" class="form-control" id="mMartQaPassport" placeholder="' + t('guest.phPassport') + '"></div><div class="form-group"><label>' + t('g.nationality') + '</label><input type="text" class="form-control" id="mMartQaNat" placeholder="' + t('guest.phNat') + '" readonly onclick="openNationalityPicker(\\'mMartQaNat\\')" style="cursor:pointer;"></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('guest.dobLabel') + '</label><input type="date" class="form-control" id="mMartQaDob"></div><div class="form-group"><label>' + t('g.payment') + adminEditBtn('paymentMethods') + '</label><select class="form-control" id="mMartQaPay">' + getPaymentMethods().map(s=>'<option>'+s+'</option>').join('') + '</select></div></div>' +
    '<div class="form-row"><div class="form-group"><label>' + t('g.email') + '</label><input type="email" class="form-control" id="mMartQaEmail" placeholder="' + t('guest.phEmail') + '"></div><div class="form-group"><label>' + t('g.phone') + '</label><input type="tel" class="form-control" id="mMartQaPhone" placeholder="' + t('guest.phPhone') + '"></div></div>' +
    '<div class="form-group"><label>' + t('guest.notesLabel') + '</label><textarea class="form-control" id="mMartQaNotes" rows="2" placeholder="' + t('guest.phNotes') + '"></textarea></div></div>' +""",
    ),
    (
        """    openModal(`<div class="modal-header"><h2>Select Nationality</h2><button class="modal-close" onclick="cancelNatPicker()">&times;</button></div>
      <div class="modal-body" style="padding:0.75rem;">
      <div style="padding:0.5rem 0;"><input type="text" class="form-control" id="natPickerSearch" placeholder="Search nationality..." value="${filterVal}" oninput="window._natFilter(this.value)" style="font-size:1rem;"></div>
      <div id="natList" style="max-height:calc(100vh - 200px);overflow-y:auto;">
      ${filtered.map(n => '<div class="nat-item" data-nat="'+n+'" style="padding:0.85rem 1rem;border-bottom:1px solid var(--border);cursor:pointer;font-size:1rem;">'+n+'</div>').join('')}
      ${filtered.length===0?'<div style="padding:2rem;text-align:center;color:#999;">No match found</div>':''}""",
        """    openModal(`<div class="modal-header"><h2>${t('msg.nationalityTitle')}</h2><button class="modal-close" onclick="cancelNatPicker()">&times;</button></div>
      <div class="modal-body" style="padding:0.75rem;">
      <div style="padding:0.5rem 0;"><input type="text" class="form-control" id="natPickerSearch" placeholder="${String(t('msg.searchNat')).replace(/"/g, '&quot;')}" value="${filterVal}" oninput="window._natFilter(this.value)" style="font-size:1rem;"></div>
      <div id="natList" style="max-height:calc(100vh - 200px);overflow-y:auto;">
      ${filtered.map(n => '<div class="nat-item" data-nat="'+n+'" style="padding:0.85rem 1rem;border-bottom:1px solid var(--border);cursor:pointer;font-size:1rem;">'+n+'</div>').join('')}
      ${filtered.length===0?'<div style="padding:2rem;text-align:center;color:#999;">'+t('msg.noNatMatch')+'</div>':''}""",
    ),
    (
        """    openModal(`<div class="modal-header"><h2>Select Nationality</h2><button class="modal-close" onclick="cancelNatStandalone()">&times;</button></div>
      <div class="modal-body" style="padding:0.75rem;">
      <div style="padding:0.5rem 0;"><input type="text" class="form-control" id="natSSearch" placeholder="Search nationality..." value="${filterVal}" oninput="window._nsFilter(this.value)" style="font-size:1rem;"></div>
      <div id="natSList" style="max-height:calc(100vh - 200px);overflow-y:auto;">
      ${filtered.map(n => '<div class="nat-item" data-nat="'+n+'" style="padding:0.85rem 1rem;border-bottom:1px solid var(--border);cursor:pointer;font-size:1rem;">'+n+'</div>').join('')}
      ${filtered.length===0?'<div style="padding:2rem;text-align:center;color:#999;">No match</div>':''}""",
        """    openModal(`<div class="modal-header"><h2>${t('msg.nationalityTitle')}</h2><button class="modal-close" onclick="cancelNatStandalone()">&times;</button></div>
      <div class="modal-body" style="padding:0.75rem;">
      <div style="padding:0.5rem 0;"><input type="text" class="form-control" id="natSSearch" placeholder="${String(t('msg.searchNat')).replace(/"/g, '&quot;')}" value="${filterVal}" oninput="window._nsFilter(this.value)" style="font-size:1rem;"></div>
      <div id="natSList" style="max-height:calc(100vh - 200px);overflow-y:auto;">
      ${filtered.map(n => '<div class="nat-item" data-nat="'+n+'" style="padding:0.85rem 1rem;border-bottom:1px solid var(--border);cursor:pointer;font-size:1rem;">'+n+'</div>').join('')}
      ${filtered.length===0?'<div style="padding:2rem;text-align:center;color:#999;">'+t('msg.noNatMatch')+'</div>':''}""",
    ),
]


def patch(content: str) -> str:
    if MARKER in content and "newGuestFromBookingModalMarkup" in content:
        return content
    changed = 0
    for old, new in REPLACEMENTS:
        if old in content:
            content = content.replace(old, new, 1)
            changed += 1
    if changed == 0:
        print("No booking guest i18n replacements matched.", file=sys.stderr)
        return content
    if MARKER not in content:
        content = content.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)
    print(f"Applied {changed} booking guest i18n replacements")
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
