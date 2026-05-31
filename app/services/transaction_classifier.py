ORDER_PAYMENT_TYPES = {
    "order payment",
    "bezahlung der bestellung",
}

REFUND_TYPES = {
    "refund",
    "erstattung",
}

SERVICE_FEE_TYPES = {
    "service fees",
    "service-gebühren",
    "service-gebuhren",
}


def normalize_type(value: str | None) -> str:
    return (value or "").strip().casefold()


def is_order_payment(value: str | None) -> bool:
    return normalize_type(value) in ORDER_PAYMENT_TYPES


def is_refund(value: str | None) -> bool:
    return normalize_type(value) in REFUND_TYPES


def is_service_fee(value: str | None) -> bool:
    return normalize_type(value) in SERVICE_FEE_TYPES

