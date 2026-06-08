#!/usr/bin/env python3
"""Full-screen modals for QR screens and all app pop-ups."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-FULLSCREEN-MODAL-v2"
INDEX = Path("public/index.html")

OPEN_MODAL_PLAIN = (
    "function openModal(html) { document.getElementById('modalContent').innerHTML = html; "
    "document.getElementById('modalOverlay').classList.add('active'); }"
)

OPEN_MODAL_SHELL = """function openModal(html) { document.getElementById('modalContent').innerHTML = html; document.getElementById('modalOverlay').classList.add('active'); }
window.openShellModal = function(html, opts) {
  opts = opts || {};
  var overlay = document.getElementById('modalOverlay');
  var content = document.getElementById('modalContent');
  if (!overlay || !content) return;
  if (typeof showBottomNav === 'function') showBottomNav(true);
  content.innerHTML = html;
  content.classList.add('modal--shell');
  if (opts.wide) content.classList.add('modal--shell-wide');
  overlay.classList.add('modal-overlay--shell', 'active');
};"""

OPEN_MODAL_FULLSCREEN = """function openModal(html) {
  var overlay = document.getElementById('modalOverlay');
  var content = document.getElementById('modalContent');
  if (!overlay || !content) return;
  content.innerHTML = html;
  content.classList.remove('modal--shell', 'modal--shell-wide');
  content.classList.add('modal--fullscreen');
  overlay.classList.remove('modal-overlay--shell');
  overlay.classList.add('modal-overlay--fullscreen', 'active');
}
window.openShellModal = function(html, opts) { openModal(html); };"""

CLOSE_MODAL_PLAIN = """function closeModal() {
  window._cashPaymentCtx = null;
  try { window._wpClosingDept = null; } catch (e) {}
  document.getElementById('modalOverlay').classList.remove('active');
}"""

CLOSE_MODAL_EXTENDED = """function closeModal() {
  window._cashPaymentCtx = null;
  try { window._wpClosingDept = null; } catch (e) {}
  var overlay = document.getElementById('modalOverlay');
  var content = document.getElementById('modalContent');
  if (overlay) overlay.classList.remove('active', 'modal-overlay--shell', 'modal-overlay--fullscreen');
  if (content) content.classList.remove('modal--shell', 'modal--shell-wide', 'modal--fullscreen');
}"""

FULLSCREEN_MODAL_CSS = """
    /* HRMM full-screen modals */
    .modal-overlay.modal-overlay--fullscreen,
    .modal-overlay.active {
      display: flex;
      position: fixed;
      inset: 0;
      z-index: 10050;
      align-items: stretch;
      justify-content: stretch;
      padding: 0;
      overflow: hidden;
      background: linear-gradient(135deg, rgba(10,30,60,0.97) 0%, rgba(26,115,232,0.92) 100%);
    }
    .modal.modal--fullscreen,
    .modal-overlay.active .modal {
      width: 100%;
      max-width: 100%;
      min-height: 100vh;
      height: 100%;
      border-radius: 0;
      box-shadow: none;
      margin: 0;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .modal.modal--fullscreen .modal-body,
    .modal-overlay.active .modal .modal-body {
      flex: 1 1 auto;
      min-height: 0;
      overflow-y: auto;
      -webkit-overflow-scrolling: touch;
    }
    .modal-hd {
      padding: 0.85rem 1rem;
      border-bottom: 2px solid var(--primary);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 0.5rem;
      background: linear-gradient(135deg, #1a3a5c 0%, #1a73e8 100%);
      color: #fff;
      flex-shrink: 0;
      position: sticky;
      top: 0;
      z-index: 2;
    }
    .modal-hd h2 { font-size: 1.05rem; color: #fff; margin: 0; line-height: 1.3; }
    body.dark-mode .modal-hd { background: linear-gradient(135deg, #0a1628 0%, #16213e 100%); }
    .modal--fullscreen .guest-order-qr-modal,
    .modal-overlay.active .guest-order-qr-modal {
      max-width: min(560px, 100%);
      width: 100%;
      margin: 0 auto;
    }
    .modal--fullscreen .guest-order-qr-preview,
    .modal-overlay.active .guest-order-qr-preview {
      max-width: min(320px, 90vw);
      margin-left: auto;
      margin-right: auto;
    }
    .modal--fullscreen .guest-qr-report-modal,
    .modal-overlay.active .guest-qr-report-modal {
      max-width: min(1100px, 100%);
      width: 100%;
      margin: 0 auto;
    }
    #modalContent.modal:has(.modal-cash-panel) {
      max-width: 100%;
      min-height: 100vh;
      margin: 0;
      border-radius: 0;
    }
    /* __HRMM_FULLSCREEN_MODAL_MARKER__ */
"""


def _css_block() -> str:
    return FULLSCREEN_MODAL_CSS.replace("__HRMM_FULLSCREEN_MODAL_MARKER__", MARKER)


def _strip_old_modal_css(content: str) -> str:
    content = re.sub(
        r"\n\s*/\* HRMM shell modal[\s\S]*?/\* HRMM-SHELL-MODAL-v\d+ \*/\n",
        "\n",
        content,
    )
    content = re.sub(
        r"\n\s*/\* HRMM full-screen modals \*/[\s\S]*?/\* HRMM-FULLSCREEN-MODAL-v\d+ \*/\n",
        "\n",
        content,
    )
    return content


def _upgrade_open_close(content: str) -> str:
    if OPEN_MODAL_FULLSCREEN.split("window.openShellModal")[0].strip() in content:
        return content
    if OPEN_MODAL_SHELL in content:
        content = content.replace(OPEN_MODAL_SHELL, OPEN_MODAL_FULLSCREEN, 1)
    elif OPEN_MODAL_PLAIN in content:
        content = content.replace(OPEN_MODAL_PLAIN, OPEN_MODAL_FULLSCREEN, 1)
    new_close = """  if (overlay) overlay.classList.remove('active', 'modal-overlay--shell', 'modal-overlay--fullscreen');
  if (content) content.classList.remove('modal--shell', 'modal--shell-wide', 'modal--fullscreen');"""
    if new_close not in content:
        old_close = """  if (overlay) overlay.classList.remove('active', 'modal-overlay--shell');
  if (content) content.classList.remove('modal--shell', 'modal--shell-wide');"""
        if old_close in content:
            content = content.replace(old_close, new_close, 1)
        elif CLOSE_MODAL_PLAIN in content:
            content = content.replace(CLOSE_MODAL_PLAIN, CLOSE_MODAL_EXTENDED, 1)
    return content


def patch(content: str) -> str:
    content = _strip_old_modal_css(content)
    content = _upgrade_open_close(content)

    close_ok = "overlay.classList.remove('active', 'modal-overlay--shell', 'modal-overlay--fullscreen')" in content
    if MARKER in content and "modal-overlay--fullscreen" in content and "modal--fullscreen" in content and close_ok:
        print(f"Already patched {MARKER} — skipping")
        return content

    if f"/* {MARKER} */" not in content:
        content = content.replace(
            "  </style>\n</head>",
            _css_block() + "  </style>\n</head>",
            1,
        )

    content = re.sub(r"HRMM-(?:SHELL|FULLSCREEN)-MODAL-v\d+", MARKER, content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — all modals open full screen")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
