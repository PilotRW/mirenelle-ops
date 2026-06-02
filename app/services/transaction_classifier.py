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
