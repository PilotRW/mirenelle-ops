ORDER_PAYMENT_TYPES = {
    "order",
    "order payment",
    "bestelling",
    "bestellung",
    "bezahlung der bestellung",
    "commande",
    "ordine",
    "pedido",
    "zamówienie",
    "zamowienie",
}

REFUND_TYPES = {
    "refund",
    "refunds",
    "erstattung",
    "remboursement",
    "rimborso",
    "reembolso",
    "retour",
    "zwrot",
}

SERVICE_FEE_TYPES = {
    "service fee",
    "service fees",
    "servicegebühr",
    "service-gebühren",
    "service-gebuhren",
    "frais de service",
    "tariffa di servizio",
    "tarifas de servicio",
    "opłata za usługę",
    "oplata za usluge",
}


def normalize_type(value: str | None) -> str:
    return (value or "").strip().casefold()


def is_order_payment(value: str | None) -> bool:
    return normalize_type(value) in ORDER_PAYMENT_TYPES


def is_refund(value: str | None) -> bool:
    return normalize_type(value) in REFUND_TYPES


def is_service_fee(value: str | None) -> bool:
    return normalize_type(value) in SERVICE_FEE_TYPES


def classify_payment_type(value: str | None) -> str:
    normalized = normalize_type(value)
    if normalized in ORDER_PAYMENT_TYPES:
        return "order"
    if normalized in REFUND_TYPES:
        return "refund"
    if normalized in SERVICE_FEE_TYPES:
        return "service_fee"
    if "rücksend" in normalized or "rucksend" in normalized or "customer return" in normalized:
        return "return_fee"
    if "versand durch amazon" in normalized or "fba" in normalized:
        return "fba_fee"
    if "lagergebühr" in normalized or "lagergebuhr" in normalized or "storage fee" in normalized:
        return "fba_fee"
    if "übertrag" in normalized or "ubertrag" in normalized or "transfer" in normalized:
        return "transfer"
    if "fee" in normalized or "gebühr" in normalized or "gebuhr" in normalized:
        return "service_fee"
    if not normalized:
        return "unknown"
    return "other"
