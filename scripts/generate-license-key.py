#!/usr/bin/env python3
"""Generate an annual license key for a customer email (matches in-app CRC32)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BILLING = Path(__file__).resolve().parents[1] / "config" / "hrmm-billing.json"


def crc32(s: str) -> int:
    crc = 0xFFFFFFFF
    for ch in s:
        crc ^= ord(ch)
        for _ in range(8):
            crc = (crc >> 1) ^ 0xEDB88320 if crc & 1 else crc >> 1
    return crc ^ 0xFFFFFFFF


def license_key(email: str, price: int = 100) -> str:
    em = email.strip().lower()
    if not em:
        raise ValueError("email is required")
    seed = f"{em}|hrmm|annual|{price}"
    n = crc32(seed) & 0xFFFFFFFF
    key = "HRMM-" + _base36(n).upper()
    return "".join(ch for ch in key if ch.isalnum() or ch == "-")


def _base36(n: int) -> str:
  # Match JS Number.toString(36) for unsigned 32-bit values
    if n < 0:
        n += 1 << 32
    if n == 0:
        return "0"
    digits = "0123456789abcdefghijklmnopqrstuvwxyz"
    out = []
    while n:
        n, r = divmod(n, 36)
        out.append(digits[r])
    return "".join(reversed(out))


def load_price() -> int:
    try:
        data = json.loads(BILLING.read_text(encoding="utf-8"))
        return int(data.get("licensePriceUsd") or 100)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return 100


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate HRMM annual license key for an email")
    parser.add_argument("email", help="Customer email used at sign-in")
    parser.add_argument("--price", type=int, default=None, help="License price (default from config)")
    args = parser.parse_args()
    price = args.price if args.price is not None else load_price()
    key = license_key(args.email, price)
    print(key)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
