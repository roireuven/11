#!/usr/bin/env python3
"""Small-phone UI: scrollable pages, visible buttons, safe areas (5–8 inch screens)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-SMALL-PHONE-v2"
INDEX = Path("public/index.html")

SMALL_PHONE_CSS = """
    /* HRMM small-phone layout v2 — scroll pages, wrap buttons, 5–8 inch + narrow phones */
    html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }
    @media (max-width: 768px) {
      .content { padding-left: 0.65rem; padding-right: 0.65rem; }
      .xgrid-search-bar { width: 100% !important; max-width: 100%; box-sizing: border-box; }
      .topbar-right { flex-wrap: wrap; justify-content: flex-end; gap: 0.25rem; max-width: 52%; }
      .topbar .topbar-locale-pick { max-width: 100%; }
      .topbar .topbar-locale-sel { max-width: 100%; min-width: 0; }
      .rest-menu-grid, .mart-grid, .pos-item-grid { grid-template-columns: repeat(2, 1fr) !important; }
      .rest-table-floor { grid-template-columns: repeat(4, 1fr) !important; }
      .rest-order-num-floor { grid-template-columns: repeat(8, 1fr) !important; }
    }
    @media (max-width: 600px) {
      .main {
        display: flex;
        flex-direction: column;
        min-height: 0;
        height: 100dvh;
        height: 100vh;
        overflow: hidden;
      }
      .content {
        flex: 1 1 auto;
        min-height: 0 !important;
        height: auto !important;
        max-height: none !important;
        overflow-y: auto !important;
        overflow-x: hidden;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
        padding-bottom: calc(58px + env(safe-area-inset-bottom, 0px)) !important;
      }
      .page { min-height: 0; }
      .card { margin-bottom: 0.85rem; }
      .card-header {
        flex-direction: column !important;
        align-items: stretch !important;
        gap: 0.5rem !important;
      }
      .card-header h2 { width: 100%; margin: 0; }
      .card-header > div,
      .card-header > .btn,
      .card-header > button {
        width: 100%;
        max-width: 100%;
        box-sizing: border-box;
      }
      .card-header > div {
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
        align-items: stretch !important;
      }
      .card-header .btn,
      .card-header button.btn {
        min-height: 44px;
        flex: 1 1 calc(50% - 0.25rem);
        justify-content: center;
        text-align: center;
      }
      .card-body .btn[style*="width:100%"],
      .card-body > div > .btn[style*="width:100%"] {
        min-height: 44px;
      }
      .form-row,
      .modal-body .form-row,
      .card-body .form-row {
        grid-template-columns: 1fr !important;
        gap: 0.65rem !important;
      }
      .stats-grid { grid-template-columns: 1fr 1fr !important; gap: 0.65rem; }
      .dash-grid { grid-template-columns: 1fr !important; }
      .xgrid-toolbar {
        flex-wrap: wrap !important;
        gap: 0.4rem !important;
      }
      .xgrid-toolbar .btn { min-height: 44px; }
      .xgrid-toolbar .xg-info {
        width: 100%;
        margin-left: 0 !important;
        order: 10;
      }
      .table-wrap {
        max-width: 100%;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
      }
      .modal-overlay.active,
      .modal-overlay.modal-overlay--fullscreen {
        align-items: stretch;
        justify-content: stretch;
        padding: 0;
      }
      .modal,
      .modal.modal--fullscreen,
      .modal-overlay.active .modal {
        display: flex !important;
        flex-direction: column !important;
        min-height: 100dvh !important;
        max-height: 100dvh !important;
        height: 100dvh !important;
        width: 100% !important;
        overflow: hidden !important;
      }
      .modal-header,
      .modal-hd {
        flex-shrink: 0;
        position: sticky;
        top: 0;
        z-index: 3;
      }
      .modal-body {
        flex: 1 1 auto !important;
        min-height: 0 !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch;
        overscroll-behavior: contain;
      }
      .modal-footer {
        flex-shrink: 0;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 0.45rem !important;
        padding: 0.75rem 0.65rem calc(0.75rem + env(safe-area-inset-bottom, 0px)) !important;
        position: sticky;
        bottom: 0;
        z-index: 3;
      }
      .modal-footer .btn {
        flex: 1 1 calc(50% - 0.3rem);
        min-height: 44px !important;
        min-width: 0 !important;
        max-width: 100%;
        justify-content: center;
      }
      .modal-close {
        min-width: 44px !important;
        min-height: 44px !important;
        width: 44px !important;
        height: 44px !important;
      }
      .modal-cash-key,
      .modal-cash-key-c {
        min-width: 0 !important;
        flex: 1 1 22%;
        min-height: 44px !important;
        font-size: 1rem !important;
      }
      .guest-order-qr-actions .btn {
        flex: 1 1 100% !important;
        min-height: 44px !important;
      }
      .guest-qr-report-btn {
        white-space: normal !important;
        line-height: 1.2;
        text-align: center;
      }
      .guest-qr-report-stats { grid-template-columns: repeat(2, 1fr) !important; }
      .guest-qr-charts { grid-template-columns: 1fr !important; }
      .guest-qr-slots-grid {
        max-height: none !important;
        grid-template-columns: repeat(5, 1fr) !important;
      }
      .rest-order-type .btn { flex: 1 1 100%; min-width: 0 !important; }
      .pos-actions { grid-template-columns: 1fr !important; }
      .pos-actions .btn { min-height: 48px; width: 100%; }
      .rest-floor-title-actions { width: 100%; }
      .rest-floor-title-actions .btn { min-height: 44px; }
      .doc-embed-wrap {
        height: auto !important;
        min-height: calc(100dvh - 7rem) !important;
        margin-bottom: 0.5rem;
      }
      .doc-embed-wrap iframe { min-height: 55dvh; }
      #setupOverlay {
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch;
        align-items: flex-start !important;
        padding: max(0.75rem, env(safe-area-inset-top, 0px)) 0.65rem max(1rem, env(safe-area-inset-bottom, 0px)) !important;
      }
      .setup-card { width: 100%; max-width: 100%; margin: 0 auto; }
      #natList, #natSList, #lmList {
        max-height: none !important;
        overflow-y: visible !important;
      }
      .post-payment-invoice-overlay { padding: 0.5rem; align-items: flex-start; overflow-y: auto; }
      .post-payment-invoice-card { max-height: none; margin: auto 0; }
      .btn { min-height: 40px; }
      .btn-sm { min-height: 40px; min-width: 44px; }
      .xgrid-wrap { max-width: 100%; -webkit-overflow-scrolling: touch; }
      .xgrid td .cell-actions {
        flex-wrap: wrap !important;
        justify-content: flex-start !important;
        gap: 0.35rem !important;
        padding: 0.35rem 0.25rem !important;
        max-width: 100%;
      }
      .xgrid td .cell-actions .btn {
        flex: 1 1 calc(50% - 0.25rem);
        min-height: 40px !important;
        min-width: 0 !important;
        white-space: normal;
        line-height: 1.15;
        padding-left: 0.35rem;
        padding-right: 0.35rem;
      }
      .xgrid th:last-child, .xgrid td:last-child { min-width: 9.5rem; width: auto !important; }
      .xgrid-footer { justify-content: center; }
      .xgrid-footer .xg-page-btns button { min-height: 40px; min-width: 40px; }
      .post-payment-invoice-ft {
        flex-wrap: wrap !important;
        gap: 0.45rem !important;
        justify-content: center !important;
      }
      .post-payment-invoice-ft .btn { flex: 1 1 calc(50% - 0.25rem); min-height: 44px; }
      .login-card { width: 100%; max-width: 100%; margin: 0 auto; }
      .rest-menu-tabs { gap: 0.35rem; }
      .rest-menu-tabs .btn { flex: 1 1 calc(50% - 0.2rem); min-height: 40px; }
      .rest-floor-head { flex-direction: column; align-items: stretch; }
      .rest-floor-summary { width: 100%; }
      .hk-grid { grid-template-columns: repeat(2, 1fr) !important; }
      .pos-top .btn { width: 100%; justify-content: center; }
    }
    @media (max-width: 480px) {
      .topbar-right { max-width: 58%; }
      .rest-menu-grid, .mart-grid, .pos-item-grid { grid-template-columns: repeat(2, 1fr) !important; }
      .xgrid td .cell-actions .btn { flex: 1 1 100%; }
    }
    @media (max-width: 400px) {
      .stats-grid { grid-template-columns: 1fr !important; }
      .rest-order-num-floor { grid-template-columns: repeat(4, 1fr) !important; }
      .rest-table-floor { grid-template-columns: repeat(3, 1fr) !important; }
      .room-grid { grid-template-columns: repeat(2, 1fr) !important; }
      .card-header .btn,
      .card-header button.btn {
        flex: 1 1 100%;
      }
      .modal-footer .btn { flex: 1 1 100%; }
      .guest-qr-slots-grid { grid-template-columns: repeat(4, 1fr) !important; }
      .content { padding-left: 0.5rem; padding-right: 0.5rem; }
    }
    @media (max-width: 360px) {
      .rest-order-num-floor { grid-template-columns: repeat(3, 1fr) !important; }
      .bottom-nav-item { min-width: 46px; font-size: 0.48rem; }
      .topbar h1 { font-size: 0.95rem; }
    }
    @media (max-width: 320px) {
      .content { padding-left: 0.35rem; padding-right: 0.35rem; }
      .card-body { padding: 0.65rem; }
      .card-header { padding: 0.65rem 0.75rem; }
      .bottom-nav-item { min-width: 42px; max-width: 64px; }
      .rest-order-num-floor { grid-template-columns: repeat(3, 1fr) !important; gap: 0.3rem; }
      .guest-qr-slots-grid { grid-template-columns: repeat(3, 1fr) !important; }
    }
    @media (max-height: 520px) and (orientation: landscape) {
      .content { padding-bottom: calc(48px + env(safe-area-inset-bottom, 0px)) !important; }
      .bottom-nav { height: calc(44px + env(safe-area-inset-bottom, 0px)); }
      .modal-body { max-height: calc(100dvh - 7rem); }
      .setup-card, .login-card { max-height: none; }
    }
    /* __HRMM_SMALL_PHONE_MARKER__ */
"""


def _css_block() -> str:
    return SMALL_PHONE_CSS.replace("__HRMM_SMALL_PHONE_MARKER__", MARKER)


def _strip_old_css(content: str) -> str:
    return re.sub(
        r"\n\s*/\* HRMM small-phone layout[^\n]*\*/[\s\S]*?/\* HRMM-SMALL-PHONE-v\d+ \*/\n",
        "\n",
        content,
    )


def patch(content: str) -> str:
    if MARKER in content and ".xgrid td .cell-actions" in content:
        print(f"Already patched {MARKER} — skipping")
        return content

    content = _strip_old_css(content)
    content = content.replace(
        "  </style>\n</head>",
        _css_block() + "  </style>\n</head>",
        1,
    )
    return content


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    index = root / INDEX
    if not index.is_file():
        print(f"Missing {index}", file=sys.stderr)
        return 1
    text = index.read_text(encoding="utf-8")
    out = patch(text)
    if MARKER not in out:
        print("Small-phone patch failed — missing marker", file=sys.stderr)
        return 1
    index.write_text(out, encoding="utf-8")
    print(f"Patched {index} — small-phone scroll and button layout ({MARKER})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
