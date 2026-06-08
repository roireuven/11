#!/usr/bin/env python3
"""Generate doc/i18n/guest-order-app-keys.json for all 21 app locales."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "doc" / "i18n" / "guest-order-app-keys.json"

# English source strings
EN = {
    "bnav": {
        "guestOrder": "Order QR",
        "guestOrderRest": "Restaurant QR",
        "guestOrderMart": "Mini-Mart QR",
    },
    "guestOrder": {
        "restaurantQr": "Restaurant QR",
        "minimartQr": "Mini-Mart QR",
        "modalTitleRest": "Restaurant order QR",
        "modalTitleMart": "Mini-Mart order QR",
        "leadRest": "Scan this QR so the customer can self-order from the restaurant. Pick an order number (1–60) below.",
        "leadMart": "Scan this QR so the customer can self-order from the mini-mart. Pick an order number (1–60) below.",
        "orderNumber": "Order number",
        "selectOrderNum": "— Select order number —",
        "orderNumOption": "Order number {n}",
        "scanToOrder": "Scan to order",
        "selectOrderNumHint": "Select order number",
        "orderLink": "Order link",
        "openOrderScreen": "Open order screen",
        "copyLink": "Copy link",
        "linkCopied": "Link copied",
        "orderSent": "Order sent!",
        "orderSubmitted": "Order submitted!",
        "searchMenu": "Search menu…",
        "searchItems": "Search items…",
        "browseMenu": "Browse the menu and send your order to the kitchen",
        "browseItems": "Browse items and submit your mini-mart order",
        "noMenuItems": "No menu items available right now.",
        "noStoreItems": "No items available right now.",
        "orderMore": "Order more",
        "restaurantOrder": "Restaurant order",
        "minimartOrder": "Mini-mart order",
        "qrReportBtn": "QR Orders Report",
        "orderNumLabel": "Order number {n}",
        "selectOrderNumFirst": "Select order number first",
        "sendToKitchen": "Send to kitchen",
        "sendOrder": "Send order",
        "orderSentKitchen": "Your order was submitted to the kitchen. Staff will prepare it shortly.",
        "orderSentMart": "Your mini-mart order was sent. Staff will prepare it for pickup or delivery.",
        "qrAlt": "Order QR code",
    },
    "guestQrReport": {
        "titleRest": "Restaurant QR orders report",
        "titleMart": "Mini-Mart QR orders report",
        "qrOrders": "QR orders",
        "slotsUsed": "Slots used",
        "open": "Open",
        "revenue": "Revenue",
        "charts": "Charts & graphs",
        "statusBreakdown": "Status breakdown",
        "paid": "Paid",
        "other": "Other",
        "revenueBySlot": "Revenue by order # (top slots)",
        "noSlotRevenue": "No slot revenue yet",
        "ordersByHour": "Orders by hour of day",
        "noTimeData": "No time data yet",
        "orderNums": "Order numbers 1–60",
        "exportCsv": "Export Excel (CSV)",
        "refresh": "Refresh",
        "spreadsheet": "All QR scan orders (spreadsheet)",
        "noOrders": "No QR scan orders yet",
        "free": "Free",
        "csvDownloaded": "CSV downloaded",
        "colOrderNum": "Order #",
        "colTicket": "Ticket",
        "colTime": "Time",
        "colStatus": "Status",
        "colItems": "Items",
        "colTotal": "Total",
        "colPayment": "Payment",
        "colGuest": "Guest",
    },
}

# Per-locale overrides (merge onto EN structure)
LOCALES: dict[str, dict] = {
    "es": {
        "bnav": {"guestOrder": "QR pedido", "guestOrderRest": "QR restaurante", "guestOrderMart": "QR mini-mart"},
        "guestOrder": {
            "modalTitleRest": "QR pedido restaurante",
            "modalTitleMart": "QR pedido mini-mart",
            "leadRest": "Escanee este QR para que el cliente pida en el restaurante. Elija un número de pedido (1–60).",
            "leadMart": "Escanee este QR para que el cliente pida en el mini-mart. Elija un número de pedido (1–60).",
            "orderNumber": "Número de pedido",
            "selectOrderNum": "— Seleccionar número —",
            "scanToOrder": "Escanear para pedir",
            "orderLink": "Enlace del pedido",
            "openOrderScreen": "Abrir pantalla de pedido",
            "copyLink": "Copiar enlace",
            "linkCopied": "Enlace copiado",
            "qrReportBtn": "Informe QR pedidos",
        },
        "guestQrReport": {
            "titleRest": "Informe pedidos QR restaurante",
            "titleMart": "Informe pedidos QR mini-mart",
            "exportCsv": "Exportar Excel (CSV)",
            "spreadsheet": "Todos los pedidos QR (hoja)",
        },
    },
    "fr": {
        "bnav": {"guestOrder": "QR commande", "guestOrderRest": "QR restaurant", "guestOrderMart": "QR mini-mart"},
        "guestOrder": {
            "modalTitleRest": "QR commande restaurant",
            "modalTitleMart": "QR commande mini-mart",
            "leadRest": "Scannez ce QR pour que le client commande au restaurant. Choisissez un numéro de commande (1–60).",
            "leadMart": "Scannez ce QR pour que le client commande au mini-mart. Choisissez un numéro de commande (1–60).",
            "orderNumber": "Numéro de commande",
            "qrReportBtn": "Rapport commandes QR",
        },
        "guestQrReport": {"titleRest": "Rapport commandes QR restaurant", "titleMart": "Rapport commandes QR mini-mart"},
    },
    "de": {
        "bnav": {"guestOrder": "QR Bestellung", "guestOrderRest": "Restaurant-QR", "guestOrderMart": "Mini-Mart-QR"},
        "guestOrder": {"qrReportBtn": "QR-Bestellbericht", "orderNumber": "Bestellnummer"},
        "guestQrReport": {"titleRest": "Restaurant QR-Bestellbericht", "titleMart": "Mini-Mart QR-Bestellbericht"},
    },
    "ja": {
        "bnav": {"guestOrder": "QR注文", "guestOrderRest": "レストランQR", "guestOrderMart": "ミニマートQR"},
        "guestOrder": {"qrReportBtn": "QR注文レポート", "orderNumber": "注文番号"},
        "guestQrReport": {"titleRest": "レストランQR注文レポート", "titleMart": "ミニマートQR注文レポート"},
    },
    "ko": {
        "bnav": {"guestOrder": "QR 주문", "guestOrderRest": "레스토랑 QR", "guestOrderMart": "미니마트 QR"},
        "guestOrder": {"qrReportBtn": "QR 주문 보고서", "orderNumber": "주문 번호"},
        "guestQrReport": {"titleRest": "레스토랑 QR 주문 보고서", "titleMart": "미니마트 QR 주문 보고서"},
    },
    "ar": {
        "bnav": {"guestOrder": "طلب QR", "guestOrderRest": "مطعم QR", "guestOrderMart": "متجر QR"},
        "guestOrder": {"qrReportBtn": "تقرير طلبات QR", "orderNumber": "رقم الطلب"},
        "guestQrReport": {"titleRest": "تقرير طلبات QR للمطعم", "titleMart": "تقرير طلبات QR للمتجر"},
    },
    "hi": {
        "bnav": {"guestOrder": "QR ऑर्डर", "guestOrderRest": "रेस्तरां QR", "guestOrderMart": "मिनी-मार्ट QR"},
        "guestOrder": {"qrReportBtn": "QR ऑर्डर रिपोर्ट", "orderNumber": "ऑर्डर नंबर"},
    },
    "th": {
        "bnav": {"guestOrder": "สั่ง QR", "guestOrderRest": "ร้านอาหาร QR", "guestOrderMart": "มินิมาร์ท QR"},
        "guestOrder": {"qrReportBtn": "รายงานออเดอร์ QR", "orderNumber": "หมายเลขออเดอร์"},
    },
    "vi": {
        "bnav": {"guestOrder": "Đặt QR", "guestOrderRest": "Nhà hàng QR", "guestOrderMart": "Siêu thị QR"},
        "guestOrder": {"qrReportBtn": "Báo cáo đơn QR", "orderNumber": "Số đơn"},
    },
    "id": {
        "bnav": {"guestOrder": "Pesan QR", "guestOrderRest": "Restoran QR", "guestOrderMart": "Mini-mart QR"},
        "guestOrder": {"qrReportBtn": "Laporan pesanan QR", "orderNumber": "Nomor pesanan"},
    },
    "tr": {
        "bnav": {"guestOrder": "QR sipariş", "guestOrderRest": "Restoran QR", "guestOrderMart": "Mini-market QR"},
        "guestOrder": {"qrReportBtn": "QR sipariş raporu", "orderNumber": "Sipariş no"},
    },
    "ru": {
        "bnav": {"guestOrder": "QR заказ", "guestOrderRest": "Ресторан QR", "guestOrderMart": "Мини-маркет QR"},
        "guestOrder": {"qrReportBtn": "Отчёт QR заказов", "orderNumber": "Номер заказа"},
    },
    "it": {
        "bnav": {"guestOrder": "Ordine QR", "guestOrderRest": "Ristorante QR", "guestOrderMart": "Mini-market QR"},
        "guestOrder": {"qrReportBtn": "Report ordini QR", "orderNumber": "Numero ordine"},
    },
    "nl": {
        "bnav": {"guestOrder": "QR bestelling", "guestOrderRest": "Restaurant QR", "guestOrderMart": "Mini-mart QR"},
        "guestOrder": {"qrReportBtn": "QR-bestelrapport", "orderNumber": "Bestelnummer"},
    },
    "pl": {
        "bnav": {"guestOrder": "Zamówienie QR", "guestOrderRest": "Restauracja QR", "guestOrderMart": "Mini-mart QR"},
        "guestOrder": {"qrReportBtn": "Raport zamówień QR", "orderNumber": "Numer zamówienia"},
    },
    "he": {
        "bnav": {"guestOrder": "הזמנת QR", "guestOrderRest": "מסעדה QR", "guestOrderMart": "מיני-מרט QR"},
        "guestOrder": {"qrReportBtn": "דוח הזמנות QR", "orderNumber": "מספר הזמנה"},
    },
    "lo": {
        "bnav": {"guestOrder": "ສັ່ງ QR", "guestOrderRest": "ຮ້ານອາຫານ QR", "guestOrderMart": "ມິນິມາດ QR"},
        "guestOrder": {"qrReportBtn": "ລາຍງານສັ່ງ QR", "orderNumber": "ເລກສັ່ງ"},
    },
    "pt-BR": {
        "bnav": {"guestOrder": "Pedido QR", "guestOrderRest": "Restaurante QR", "guestOrderMart": "Mini-mercado QR"},
        "guestOrder": {"qrReportBtn": "Relatório pedidos QR", "orderNumber": "Número do pedido"},
    },
    "zh-Hans": {
        "bnav": {"guestOrder": "QR点餐", "guestOrderRest": "餐厅QR", "guestOrderMart": "便利店QR"},
        "guestOrder": {"qrReportBtn": "QR订单报表", "orderNumber": "订单号"},
        "guestQrReport": {"titleRest": "餐厅QR订单报表", "titleMart": "便利店QR订单报表"},
    },
    "zh-Hant": {
        "bnav": {"guestOrder": "QR點餐", "guestOrderRest": "餐廳QR", "guestOrderMart": "便利店QR"},
        "guestOrder": {"qrReportBtn": "QR訂單報表", "orderNumber": "訂單號"},
        "guestQrReport": {"titleRest": "餐廳QR訂單報表", "titleMart": "便利店QR訂單報表"},
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    out = dict(base)
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def main() -> int:
    all_locales = ["en"] + sorted(LOCALES.keys())
    payload = {"en": EN}
    for code in sorted(LOCALES.keys()):
        payload[code] = _deep_merge(EN, LOCALES[code])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} ({len(all_locales)} locales)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
