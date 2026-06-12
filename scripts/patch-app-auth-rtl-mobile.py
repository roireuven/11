#!/usr/bin/env python3
"""Login/setup screens: RTL layout + small-phone tuning (5–8 inch, Hebrew/Arabic)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

MARKER = "HRMM-AUTH-RTL-MOBILE-v1"
INDEX = Path("public/index.html")

CSS_ANCHOR = "    body.dark-mode .setup-email-section p { color: #b0b0b0; }"
CSS_BLOCK = """
    /* Auth login/setup — RTL + small phones */
    #loginOverlay,
    #setupOverlay {
      display: flex;
      flex-direction: column;
      align-items: stretch;
      justify-content: flex-start;
    }
    .auth-language-header {
      max-width: min(460px, calc(100vw - 1.5rem));
      margin-inline: auto;
      padding-inline: max(0.15rem, env(safe-area-inset-left, 0px)) max(0.15rem, env(safe-area-inset-right, 0px));
    }
    [dir="rtl"] .auth-language-header { justify-content: flex-start; }
    [dir="ltr"] .auth-language-header { justify-content: flex-end; }
    .login-card,
    .setup-card {
      margin-inline: auto;
      max-width: min(460px, calc(100vw - 1.5rem));
      box-sizing: border-box;
    }
    .login-card .form-group,
    .login-creds,
    .login-creds th,
    .setup-card .setup-welcome,
    .setup-step,
    .setup-email-section,
    .setup-email-section p {
      text-align: start;
    }
    .setup-step .step-num {
      margin-right: 0;
      margin-inline-end: 0.5rem;
      vertical-align: top;
      flex-shrink: 0;
    }
    [dir="rtl"] .setup-step .step-title,
    [dir="rtl"] .setup-step p {
      text-align: start;
    }
    [dir="rtl"] .login-creds tr[data-tip]:hover::after,
    [dir="rtl"] .login-creds tr[data-tip]:active::after {
      left: auto;
      right: 0;
    }
    [dir="rtl"] .login-creds th,
    [dir="rtl"] .login-creds td {
      text-align: start;
    }
    /* Email/password stay LTR inside RTL UI */
    [dir="rtl"] #loginOverlay input[type="email"],
    [dir="rtl"] #loginOverlay input[type="text"],
    [dir="rtl"] #loginOverlay input[type="password"],
    [dir="rtl"] #setupOverlay input[type="email"],
    [dir="rtl"] #setupOverlay input[type="password"] {
      direction: ltr;
      text-align: left;
    }
    .login-creds {
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      max-width: 100%;
      min-width: 0;
    }
    .login-tap-hint .btn,
    #btnFirstTimeSetup,
    #linkBackToSignIn {
      touch-action: manipulation;
      -webkit-tap-highlight-color: transparent;
    }
    @media (max-width: 600px) {
      #loginOverlay,
      #setupOverlay {
        padding-inline: max(0.45rem, env(safe-area-inset-left, 0px)) max(0.45rem, env(safe-area-inset-right, 0px)) !important;
      }
      .auth-language-header {
        max-width: 100% !important;
        width: 100%;
        position: sticky;
        top: 0;
        z-index: 5;
        background: linear-gradient(180deg, rgba(44,62,80,0.92) 0%, rgba(44,62,80,0) 100%);
        padding-top: 0.15rem;
        padding-bottom: 0.35rem;
      }
      #setupOverlay .auth-language-header {
        background: linear-gradient(180deg, rgba(26,26,46,0.92) 0%, rgba(26,26,46,0) 100%);
      }
      .auth-language-header select.auth-locale-sel {
        width: 100%;
        max-width: 100%;
        font-size: 0.82rem;
        min-height: 44px;
      }
      .login-card,
      .setup-card {
        width: 100% !important;
        max-width: 100% !important;
        padding: 0.85rem 0.75rem 0.9rem !important;
        border-radius: 12px;
        margin-bottom: 1rem;
      }
      .login-card h1,
      .setup-card h1 {
        font-size: 1.05rem !important;
        line-height: 1.35;
        word-break: break-word;
        hyphens: auto;
      }
      .login-card .login-sub,
      .setup-card .setup-welcome {
        font-size: 0.78rem;
        line-height: 1.45;
      }
      .setup-card .setup-logo,
      .login-card .login-logo {
        width: 48px !important;
        height: 48px !important;
        font-size: 1.75rem !important;
      }
      .setup-step {
        padding: 0.7rem 0.65rem;
        margin-bottom: 0.55rem;
      }
      .setup-step .step-title { font-size: 0.84rem; }
      .setup-step p { font-size: 0.74rem; line-height: 1.45; }
      .setup-email-section {
        padding: 0.85rem 0.75rem !important;
        margin-top: 0.85rem !important;
      }
      .login-card .form-control,
      .setup-card .form-control {
        min-height: 44px;
        font-size: 16px;
      }
      .btn-login,
      .btn-setup,
      #btnFirstTimeSetup {
        min-height: 48px !important;
        font-size: 0.92rem !important;
        width: 100%;
      }
      #linkBackToSignIn {
        min-height: 44px;
        margin-top: 0.25rem;
      }
      .login-creds table { font-size: 0.64rem; width: 100%; }
      .login-creds th,
      .login-creds td {
        padding: 0.22rem 0.28rem;
        word-break: break-word;
        vertical-align: top;
      }
      .login-creds .cred-email {
        font-size: 0.62rem;
        word-break: break-all;
      }
      .login-creds .cred-role { white-space: normal; }
      .login-lang-hint,
      .login-tap-hint {
        font-size: 0.66rem !important;
        line-height: 1.4 !important;
      }
    }
    @media (max-width: 400px) {
      .login-card h1,
      .setup-card h1 { font-size: 0.96rem !important; }
      .setup-card .setup-ver { font-size: 0.68rem; }
      .login-creds th:nth-child(2),
      .login-creds td:nth-child(2) { max-width: 9.5rem; }
    }
    @media (max-width: 360px) {
      .login-card,
      .setup-card { padding: 0.75rem 0.6rem !important; }
      .setup-step .step-num {
        width: 20px;
        height: 20px;
        line-height: 20px;
        font-size: 0.68rem;
      }
    }
    @media (max-width: 320px) {
      .auth-language-header select.auth-locale-sel { font-size: 0.76rem; padding: 0.45rem 0.55rem; }
      .login-creds table { font-size: 0.58rem; }
    }
    @media (max-height: 520px) and (orientation: landscape) {
      #loginOverlay,
      #setupOverlay {
        align-items: stretch !important;
        justify-content: flex-start !important;
      }
      .setup-card .setup-logo,
      .login-card .login-logo { width: 40px !important; height: 40px !important; font-size: 1.4rem !important; }
      .setup-step { padding: 0.5rem; margin-bottom: 0.4rem; }
      .setup-card h1 { font-size: 0.95rem !important; }
    }"""

def patch(content: str) -> str:
    if MARKER in content and "Auth login/setup — RTL + small phones" in content:
        content = re.sub(r"HRMM-AUTH-RTL-MOBILE-v\d+", MARKER, content)
        return content

    if CSS_ANCHOR in content and "Auth login/setup — RTL + small phones" not in content:
        content = content.replace(CSS_ANCHOR, CSS_ANCHOR + CSS_BLOCK, 1)

    if f"<!-- {MARKER} -->" not in content:
        content = content.replace(
            "<title>HotelRestaurantMini-MartManagement</title>",
            f"<title>HotelRestaurantMini-MartManagement</title>\n  <!-- {MARKER} -->",
            1,
        )
    else:
        content = re.sub(r"HRMM-AUTH-RTL-MOBILE-v\d+", MARKER, content)

    return content


def main() -> int:
    path = INDEX
    if not path.is_file():
        print(f"Missing {path}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    path.write_text(patch(text), encoding="utf-8")
    print(f"Patched {path} — {MARKER} (auth RTL + small-phone layout)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
