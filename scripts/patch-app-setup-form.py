#!/usr/bin/env python3
"""Add business/admin initialization form fields to setup overlay (21 locales)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-SETUP-FORM-v1"
INDEX = Path("public/index.html")

CSS_ANCHOR = "    .setup-card .setup-welcome strong { color: #1a73e8; }"
CSS_NEW = """    .setup-card .setup-welcome strong { color: #1a73e8; }
    .setup-section-title {
      font-size: 0.92rem;
      font-weight: 600;
      color: #4b5563;
      margin: 1.1rem 0 0.65rem;
      padding-bottom: 0.35rem;
      border-bottom: 1px solid #e5e7eb;
      text-align: start;
    }
    .setup-form-section .form-group { margin-bottom: 0.75rem; text-align: start; }
    .setup-form-section .form-group label { display: block; margin-bottom: 0.35rem; font-weight: 500; font-size: 0.85rem; color: #1a73e8; }
    .setup-form-section .form-control { width: 100%; font-size: 0.95rem; padding: 0.65rem; }
    .setup-form-section input[readonly] { background-color: #f9fafb; color: #6b7280; }
    body.dark-mode .setup-section-title { color: #b0b8c4; border-bottom-color: #2a3a50; }
    body.dark-mode .setup-form-section input[readonly] { background-color: #0f1a2e; color: #9aa5b5; }"""

EMAIL_SECTION_OLD = """      <div class="setup-email-section" style="margin-top:1.25rem;padding-top:1rem;border-top:1px solid #e0e0e0;">
        <h3 data-i18n="setup.createAccount">Create Your Account</h3>
        <p data-i18n="setup.createAccountP">This is your personal login. All devices that sign in with the same email and password will synchronize data automatically.</p>
        <div class="form-group">
          <label style="color:#1a73e8;font-weight:600;" data-i18n="setup.email">Email</label>
          <input type="email" class="form-control" id="setupEmail" data-i18n-placeholder="setup.emailPh" placeholder="your.email@company.com" style="font-size:1rem;padding:0.7rem;">
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label style="color:#1a73e8;font-weight:600;" data-i18n="setup.password">Password</label>
          <input type="password" class="form-control" id="setupPassword" data-i18n-placeholder="setup.passwordPh" placeholder="Create a password" style="font-size:1rem;padding:0.7rem;">
        </div>
      </div>"""

EMAIL_SECTION_NEW = """      <div class="setup-form-section" style="margin-top:1rem;padding-top:0.5rem;border-top:1px solid #e0e0e0;text-align:start;">
        <div class="setup-section-title" data-i18n="setup.secBusiness">Business Information</div>
        <div class="form-group">
          <label data-i18n="setup.bizName">Business Name</label>
          <input type="text" class="form-control" id="setupBizName" data-i18n-placeholder="setup.placeholderBizName" placeholder="Enter your business name" required>
        </div>
        <div class="form-group">
          <label data-i18n="setup.sysHeaderLabel">System Header</label>
          <input type="text" class="form-control" id="setupSysHeader" readonly data-i18n-value="setup.sysHeaderTitle" value="Hotel restaurant Minimart management">
        </div>
        <div class="setup-section-title" data-i18n="setup.secAdmin">Admin Account Setup</div>
        <div class="form-group">
          <label data-i18n="setup.adminUsername">Admin Username</label>
          <input type="text" class="form-control" id="setupAdminUser" data-i18n-placeholder="setup.placeholderAdminUser" placeholder="Choose admin username" value="admin" required>
        </div>
        <div class="form-group">
          <label data-i18n="setup.email">Admin Email</label>
          <input type="email" class="form-control" id="setupEmail" data-i18n-placeholder="setup.placeholderAdminEmail" placeholder="Enter admin email address" value="zz@zz.com" required style="direction:ltr;text-align:left;">
        </div>
        <div class="form-group" style="margin-bottom:0;">
          <label data-i18n="setup.password">Password</label>
          <input type="password" class="form-control" id="setupPassword" data-i18n-placeholder="setup.placeholderAdminPass" placeholder="Create strong password" value="1234" required style="direction:ltr;text-align:left;">
        </div>
      </div>"""

BTN_OLD = '<span data-i18n="setup.createBtn">Create Account &amp; Get Started</span>'
BTN_NEW = '<span data-i18n="setup.submitInitialize">Save &amp; Initialize System</span>'

HIDE_WELCOME_CSS = """    .setup-card .setup-welcome,
    .setup-card .setup-step { display: none; }"""

COMPLETE_SETUP_SAVE_OLD = """  const email = (emailEl.value || '').trim();
  const password = passEl.value || '';
  if (!email || !email.includes('@')) {"""

COMPLETE_SETUP_SAVE_NEW = """  const email = (emailEl.value || '').trim();
  const password = passEl.value || '';
  const bizNameEl = document.getElementById('setupBizName');
  const adminUserEl = document.getElementById('setupAdminUser');
  const bizName = bizNameEl ? (bizNameEl.value || '').trim() : '';
  const adminUser = adminUserEl ? (adminUserEl.value || '').trim() : '';
  if (!email || !email.includes('@')) {"""

COMPLETE_SETUP_ACCOUNT_OLD = """  const existing = Array.isArray(accounts) && accounts.length ? accounts.find(a => a && a.email && String(a.email).toLowerCase() === String(email).toLowerCase()) : null;
  if (!existing) {
    const name = email.split('@')[0].replace(/[._-]/g,' ').replace(/\\b\\w/g,c=>c.toUpperCase());
    accounts.push({id:genId(), name:name, email:email, role:'Admin', status:'active'});"""

COMPLETE_SETUP_ACCOUNT_NEW = """  if (bizName && typeof settings === 'object' && settings) {
    settings.hotelName = bizName;
    try { save('settings', settings); } catch (e) {}
  }
  const existing = Array.isArray(accounts) && accounts.length ? accounts.find(a => a && a.email && String(a.email).toLowerCase() === String(email).toLowerCase()) : null;
  if (!existing) {
    const name = adminUser || email.split('@')[0].replace(/[._-]/g,' ').replace(/\\b\\w/g,c=>c.toUpperCase());
    accounts.push({id:genId(), name:name, email:email, role:'Admin', status:'active'});"""

EARLY_SAVE_OLD = """      var email0 = (e0.value || '').trim();
      var pass0 = p0.value || '';
      if (!email0 || email0.indexOf('@') < 0) { if (err0) err0.textContent = (typeof t === 'function' ? t('setup.invalidEmail') : 'Please enter a valid email address'); return; }"""

EARLY_SAVE_NEW = """      var bizEl0 = document.getElementById('setupBizName');
      var adminEl0 = document.getElementById('setupAdminUser');
      var bizName0 = bizEl0 ? (bizEl0.value || '').trim() : '';
      var adminUser0 = adminEl0 ? (adminEl0.value || '').trim() : '';
      var email0 = (e0.value || '').trim();
      var pass0 = p0.value || '';
      if (!email0 || email0.indexOf('@') < 0) { if (err0) err0.textContent = (typeof t === 'function' ? t('setup.invalidEmail') : 'Please enter a valid email address'); return; }"""

EARLY_ACC_OLD = """        acc0 = [
          { id: hotelGenIdEarly(), name: 'Admin User', email: 'admin@hotel.com', role: 'Admin', status: 'active' },"""

EARLY_ACC_NEW = """        var adminName0 = adminUser0 || 'Admin User';
        var adminEmail0 = email0 || 'admin@hotel.com';
        acc0 = [
          { id: hotelGenIdEarly(), name: adminName0, email: adminEmail0, role: 'Admin', status: 'active' },"""

EARLY_SETTINGS_OLD = """      if (!Array.isArray(acc0) || acc0.length === 0) {
        acc0 = [
          { id: hotelGenIdEarly(), name: adminName0, email: adminEmail0, role: 'Admin', status: 'active' },
          { id: hotelGenIdEarly(), name: 'Jane Smith', email: 'jane@hotel.com', role: 'Receptionist', status: 'active' },"""

# Need to find where settings are saved in early setup - after acc0 creation, before reload
EARLY_RELOAD_ANCHOR = """      try { localStorage.setItem(K + 'accounts', JSON.stringify(acc0)); } catch (e) { if (err0) err0.textContent = (typeof t === 'function' ? t('setup.saveFailedSetup') : 'Could not save. Try again, or go Back to sign in and use a demo user.'); return; }"""


def patch(content: str) -> str:
    if MARKER in content and 'id="setupBizName"' in content:
        content = re.sub(r"HRMM-SETUP-FORM-v\d+", MARKER, content)
        return content

    if CSS_ANCHOR in content and ".setup-section-title" not in content:
        content = content.replace(CSS_ANCHOR, CSS_NEW + "\n" + HIDE_WELCOME_CSS, 1)

    if EMAIL_SECTION_OLD in content:
        content = content.replace(EMAIL_SECTION_OLD, EMAIL_SECTION_NEW, 1)

    if BTN_OLD in content:
        content = content.replace(BTN_OLD, BTN_NEW, 1)

    if COMPLETE_SETUP_SAVE_OLD in content and "setupBizName" not in content.split("window.completeSetup = function()")[1][:800]:
        content = content.replace(COMPLETE_SETUP_SAVE_OLD, COMPLETE_SETUP_SAVE_NEW, 1)

    if COMPLETE_SETUP_ACCOUNT_OLD in content:
        content = content.replace(COMPLETE_SETUP_ACCOUNT_OLD, COMPLETE_SETUP_ACCOUNT_NEW, 1)

    if EARLY_SAVE_OLD in content and "setupBizName" not in content.split("hotelCompleteSetupEarly")[1][:1200]:
        content = content.replace(EARLY_SAVE_OLD, EARLY_SAVE_NEW, 1)

    if EARLY_ACC_OLD in content:
        content = content.replace(EARLY_ACC_OLD, EARLY_ACC_NEW, 1)

    if EARLY_RELOAD_ANCHOR in content and "setupBizNameEarly" not in content:
        biz_save = """
      if (bizName0) {
        var settings0 = null;
        try { settings0 = JSON.parse(localStorage.getItem(K + 'settings') || 'null'); } catch (e) { settings0 = null; }
        if (!settings0 || typeof settings0 !== 'object') settings0 = {};
        settings0.hotelName = bizName0;
        try { localStorage.setItem(K + 'settings', JSON.stringify(settings0)); } catch (e) {}
        if (isAn0) { try { HotelDB.saveSetting('settings', JSON.stringify(settings0)); } catch (e1) {} }
      }"""
        content = content.replace(EARLY_RELOAD_ANCHOR, biz_save + "\n" + EARLY_RELOAD_ANCHOR, 1)

    if MARKER not in content:
        content = content.replace("</head>", f"  <!-- {MARKER} -->\n</head>", 1)

    return content


def main() -> int:
    if not INDEX.is_file():
        print(f"Missing {INDEX}", file=sys.stderr)
        return 1
    text = INDEX.read_text(encoding="utf-8")
    patched = patch(text)
    if patched == text:
        print("No setup form changes applied (already patched or anchors missing).")
        return 0
    INDEX.write_text(patched, encoding="utf-8")
    print(f"Patched {INDEX} ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
