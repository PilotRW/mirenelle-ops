from dataclasses import dataclass


REQUIRED_PAYMENT_TRANSACTION_FIELDS = {
    "transaction_date",
    "transaction_status",
    "transaction_type",
    "external_transaction_id",
    "product_details",
    "product_charges",
    "promotional_rebates",
    "amazon_fees",
    "other_amount",
    "total_amount",
}


PAYMENT_TRANSACTION_HEADER_ALIASES: dict[str, set[str]] = {
    "transaction_date": {
        "Date",
        "Datum",
        "Data",
        "Fecha",
    },
    "transaction_status": {
        "Transaction status",
        "Transaktionsstatus",
        "Statut de la transaction",
        "Stato transazione",
        "Estado de la transacción",
        "Estado de la transaccion",
        "Transactiestatus",
        "Status transakcji",
    },
    "transaction_type": {
        "Transaction type",
        "Transaktionstyp",
        "Type de transaction",
        "Tipo di transazione",
        "Tipo de transacción",
        "Tipo de transaccion",
        "Transactietype",
        "Typ transakcji",
    },
    "external_transaction_id": {
        "Order ID",
        "Transaktionsnummer",
        "Numéro de commande",
        "Numero de commande",
        "ID ordine",
        "Id. de pedido",
        "ID de pedido",
        "Bestelnummer",
        "Numer zamówienia",
        "Numer zamowienia",
        "Ordernummer",
    },
    "product_details": {
        "Product Details",
        "Produktdetails",
        "Détails du produit",
        "Details du produit",
        "Dettagli prodotto",
        "Detalles del producto",
        "Productgegevens",
        "Szczegóły produktu",
        "Szczegoly produktu",
        "Produktinformation",
    },
    "product_charges": {
        "Total product charges",
        "Artikelpreise gesamt",
        "Total des frais produit",
        "Totale addebiti prodotto",
        "Total de cargos del producto",
        "Totale productkosten",
        "Łączne opłaty za produkt",
        "Laczne oplaty za produkt",
        "Totala produktavgifter",
    },
    "promotional_rebates": {
        "Total promotional rebates",
        "Gesamtsumme der Aktionsrabatte",
        "Total des remises promotionnelles",
        "Totale sconti promozionali",
        "Total de descuentos promocionales",
        "Totale promotiekortingen",
        "Łączne rabaty promocyjne",
        "Laczne rabaty promocyjne",
        "Totala kampanjrabatter",
    },
    "amazon_fees": {
        "Amazon fees",
        "Amazon-Gebühren",
        "Amazon-Gebuhren",
        "Frais Amazon",
        "Commissioni Amazon",
        "Tarifas de Amazon",
        "Amazon-kosten",
        "Opłaty Amazon",
        "Oplaty Amazon",
        "Amazon-avgifter",
    },
    "other_amount": {
        "Other",
        "Andere",
        "Autre",
        "Altro",
        "Otros",
        "Overig",
        "Inne",
        "Övrigt",
        "Ovrigt",
    },
    "total_amount": {
        "Total",
        "Summe",
        "Somme",
        "Totale",
        "Total (EUR)",
        "Total (SEK)",
        "Summe (EUR)",
        "Summe (SEK)",
    },
}


@dataclass(frozen=True)
class HeaderMappingResult:
    mapping: dict[str, str]
    missing_fields: list[str]
    ambiguous_headers: dict[str, list[str]]
    unknown_headers: list[str]


def normalize_header(header: str) -> str:
    return " ".join(header.strip().replace("\ufeff", "").split()).casefold()


def strip_currency_suffix(header: str) -> str:
    clean = header.strip()
    if clean.endswith(")") and "(" in clean:
        return clean[: clean.rfind("(")].strip()
    return clean


def detect_payment_transaction_mapping(headers: list[str]) -> HeaderMappingResult:
    normalized_aliases: dict[str, set[str]] = {}
    for canonical, aliases in PAYMENT_TRANSACTION_HEADER_ALIASES.items():
        expanded = set(aliases)
        expanded.update(strip_currency_suffix(alias) for alias in aliases)
        normalized_aliases[canonical] = {normalize_header(alias) for alias in expanded}

    mapping: dict[str, str] = {}
    ambiguous_headers: dict[str, list[str]] = {}
    matched_headers: set[str] = set()

    for header in headers:
        normalized = normalize_header(header)
        normalized_without_currency = normalize_header(strip_currency_suffix(header))
        matches = [
            canonical
            for canonical, aliases in normalized_aliases.items()
            if normalized in aliases or normalized_without_currency in aliases
        ]
        if len(matches) == 1:
            canonical = matches[0]
            if canonical in mapping:
                ambiguous_headers.setdefault(header, []).append(canonical)
            else:
                mapping[canonical] = header
                matched_headers.add(header)
        elif len(matches) > 1:
            ambiguous_headers[header] = matches

    missing_fields = sorted(REQUIRED_PAYMENT_TRANSACTION_FIELDS - set(mapping))
    unknown_headers = [header for header in headers if header not in matched_headers]

    return HeaderMappingResult(
        mapping=mapping,
        missing_fields=missing_fields,
        ambiguous_headers=ambiguous_headers,
        unknown_headers=unknown_headers,
    )

