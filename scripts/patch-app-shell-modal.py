#!/usr/bin/env python3
"""Centered in-app modals that keep top bar and bottom navigation visible."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-SHELL-MODAL-v1"
INDEX = Path("public/index.html")

OPEN_MODAL_OLD = (
    "function openModal(html) { document.getElementById('modalContent').innerHTML = html; "
    "document.getElementById('modalOverlay').classList.add('active'); }"
)

OPEN_MODAL_NEW = """function openModal(html) { document.getElementById('modalContent').innerHTML = html; document.getElementById('modalOverlay').classList.add('active'); }
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

CLOSE_MODAL_OLD = """function closeModal() {
  window._cashPaymentCtx = null;
  try { window._wpClosingDept = null; } catch (e) {}
  document.getElementById('modalOverlay').classList.remove('active');
}"""

CLOSE_MODAL_NEW = """function closeModal() {
  window._cashPaymentCtx = null;
  try { window._wpClosingDept = null; } catch (e) {}
  var overlay = document.getElementById('modalOverlay');
  var content = document.getElementById('modalContent');
  if (overlay) overlay.classList.remove('active', 'modal-overlay--shell');
  if (content) content.classList.remove('modal--shell', 'modal--shell-wide');
}"""

SHELL_MODAL_CSS = """
    /* HRMM shell modal — centered between top bar and bottom nav */
    :root { --hrmm-topbar-h: 56px; --hrmm-bnav-h: 56px; }
    @media (max-width: 600px) { :root { --hrmm-bnav-h: 52px; } }
    .modal-overlay.modal-overlay--shell {
      top: var(--hrmm-topbar-h);
      bottom: var(--hrmm-bnav-h);
      left: 0;
      right: 0;
      inset: auto;
      background: rgba(15, 23, 42, 0.42);
      backdrop-filter: blur(3px);
      z-index: 180;
      align-items: center;
      justify-content: center;
      padding: 0.65rem;
      overflow-y: auto;
    }
    .modal-overlay.modal-overlay--shell .modal.modal--shell {
      width: 100%;
      max-width: min(480px, 94vw);
      min-height: 0;
      max-height: calc(100vh - var(--hrmm-topbar-h) - var(--hrmm-bnav-h) - 1.25rem);
      border-radius: 14px;
      box-shadow: 0 18px 48px rgba(0, 0, 0, 0.28);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      margin: auto;
    }
    .modal-overlay.modal-overlay--shell .modal.modal--shell.modal--shell-wide {
      max-width: min(1024px, 96vw);
    }
    .modal-overlay.modal-overlay--shell .modal.modal--shell .modal-body {
      min-height: 0;
      max-height: none;
      overflow-y: auto;
      flex: 1 1 auto;
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
    }
    .modal-hd h2 { font-size: 1.05rem; color: #fff; margin: 0; line-height: 1.3; }
    body.dark-mode .modal-hd { background: linear-gradient(135deg, #0a1628 0%, #16213e 100%); }
    .modal-overlay.modal-overlay--shell .guest-order-qr-modal {
      max-width: none;
      margin: 0 auto;
    }
    .modal-overlay.modal-overlay--shell .guest-order-qr-preview {
      max-width: 280px;
      margin-left: auto;
      margin-right: auto;
    }
    .modal-overlay.modal-overlay--shell .guest-qr-report-modal {
      max-width: none;
    }
    /* __HRMM_SHELL_MODAL_MARKER__ */
"""


def _css_block() -> str:
    return SHELL_MODAL_CSS.replace("__HRMM_SHELL_MODAL_MARKER__", MARKER)


def _route_qr_modals_to_shell(content: str) -> str:
    content = content.replace(
        "  openModal(html);\n  guestOrderQrRefreshPreview();",
        "  openShellModal(html);\n  guestOrderQrRefreshPreview();",
    )
    content = re.sub(
        r"(window\.openGuestQrOrdersReport = function\(dept\) \{[\s\S]*?)  openModal\(html\);",
        r"\1  openShellModal(html, { wide: true });",
        content,
        count=1,
    )
    return content


def patch(content: str) -> str:
    if MARKER in content and "openShellModal" in content and "modal-overlay--shell" in content:
        content = _route_qr_modals_to_shell(content)
        print(f"Already patched {MARKER} — QR shell routing checked")
        return content

    if f"/* {MARKER} */" not in content:
        content = content.replace(
            "  </style>\n</head>",
            _css_block() + "  </style>\n</head>",
            1,
        )

    if OPEN_MODAL_OLD in content:
        content = content.replace(OPEN_MODAL_OLD, OPEN_MODAL_NEW, 1)
    elif "window.openShellModal" not in content and "function openModal(html)" in content:
        content = content.replace(
            "function openModal(html) { document.getElementById('modalContent').innerHTML = html; document.getElementById('modalOverlay').classList.add('active'); }",
            OPEN_MODAL_NEW.split("window.openShellModal")[0].rstrip() + "\n" + "window.openShellModal" + OPEN_MODAL_NEW.split("window.openShellModal", 1)[1],
            1,
        )

    if CLOSE_MODAL_OLD in content:
        content = content.replace(CLOSE_MODAL_OLD, CLOSE_MODAL_NEW, 1)

    content = _route_qr_modals_to_shell(content)
    content = re.sub(r"HRMM-SHELL-MODAL-v\d+", MARKER, content)
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    index.write_text(patch(text), encoding="utf-8")
    print(f"Patched {index} — shell-centered modals keep top and bottom menus visible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
