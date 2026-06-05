from dataclasses import dataclass


REQUIRED_PAYMENT_TRANSACTION_FIELDS = {
    "transaction_date",
    "transaction_type",
    "external_transaction_id",
    "product_details",
    "product_charges",
    "amazon_fees",
    "total_amount",
}


PAYMENT_TRANSACTION_HEADER_ALIASES: dict[str, set[str]] = {
    "transaction_date": {
        "Date",
        "Date/time",
        "Date/Time",
        "Datum",
        "Datum/Uhrzeit",
        "Data",
        "Data/ora",
        "Fecha",
        "Fecha/hora",
        "Fecha y hora",
        "Date/heure",
        "Datum/tijd",
        "Data/godzina",
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
        "Type",
        "Transaction type",
        "Typ",
        "Transaktionstyp",
        "Type de transaction",
        "Tipo",
        "Tipo di transazione",
        "Tipo de transacción",
        "Tipo de transaccion",
        "Transactietype",
        "Typ transakcji",
    },
    "external_transaction_id": {
        "Order ID",
        "Bestellnummer",
        "Transaktionsnummer",
        "Numéro de commande",
        "Numero de commande",
        "Numéro de la commande",
        "Numero de la commande",
        "N° de commande",
        "ID ordine",
        "Id. de pedido",
        "Id de pedido",
        "ID de pedido",
        "Número de pedido",
        "Numero de pedido",
        "Bestelnummer",
        "Numer zamówienia",
        "Numer zamowienia",
        "Ordernummer",
    },
    "product_details": {
        "Product Details",
        "Description",
        "Beschreibung",
        "Produktdetails",
        "Détails du produit",
        "Details du produit",
        "Description du produit",
        "Opis",
        "Dettagli prodotto",
        "Descrizione",
        "Detalles del producto",
        "Descripción",
        "Descripcion",
        "Productgegevens",
        "Beschrijving",
        "Szczegóły produktu",
        "Szczegoly produktu",
        "Produktinformation",
    },
    "product_charges": {
        "Total product charges",
        "Product sales",
        "Product Sales",
        "Umsätze",
        "Umsatze",
        "Produktumsätze",
        "Produktumsatze",
        "Artikelpreise gesamt",
        "Ventes de produits",
        "Total des frais produit",
        "Vendite prodotti",
        "Totale addebiti prodotto",
        "Ventas de productos",
        "Total de cargos del producto",
        "Productverkoop",
        "Verkoop van producten",
        "Totale productkosten",
        "Sprzedaż produktów",
        "Sprzedaz produktow",
        "Łączne opłaty za produkt",
        "Laczne oplaty za produkt",
        "Produktförsäljning",
        "Produktforsaljning",
        "Totala produktavgifter",
    },
    "promotional_rebates": {
        "Total promotional rebates",
        "Promotional rebates",
        "Rabatte aus Werbeaktionen",
        "Gesamtsumme der Aktionsrabatte",
        "Remises promotionnelles",
        "Total des remises promotionnelles",
        "Total des réductions",
        "Total des reductions",
        "Sconti promozionali",
        "Totale sconti promozionali",
        "Descuentos promocionales",
        "Devoluciones promocionales",
        "Total de descuentos promocionales",
        "Promotiekortingen",
        "Totale promotiekortingen",
        "Rabaty promocyjne",
        "Łączne rabaty promocyjne",
        "Laczne rabaty promocyjne",
        "Kampanjrabatter",
        "Totala kampanjrabatter",
    },
    "amazon_fees": {
        "Amazon fees",
        "Selling fees",
        "Verkaufsgebühren",
        "Verkaufsgebuhren",
        "Verkaufsgebuehren",
        "Amazon-Gebühren",
        "Amazon-Gebuhren",
        "Frais de vente",
        "Frais Amazon",
        "Commissioni di vendita",
        "Commissioni Amazon",
        "Tarifas de venta",
        "Tarifas de Amazon",
        "Verkoopkosten",
        "Amazon-kosten",
        "Opłaty za sprzedaż",
        "Oplaty za sprzedaz",
        "Opłaty Amazon",
        "Oplaty Amazon",
        "Försäljningsavgifter",
        "Forsaljningsavgifter",
        "Amazon-avgifter",
    },
    "other_amount": {
        "Other",
        "Andere",
        "Autre",
        "Autres",
        "Altro",
        "Otro",
        "Otros",
        "Overig",
        "Overige",
        "Inne",
        "Övrigt",
        "Ovrigt",
    },
    "total_amount": {
        "Total",
        "Gesamt",
        "Summe",
        "Somme",
        "Totale",
        "Totaal",
        "Total (EUR)",
        "Total (SEK)",
        "Summe (EUR)",
        "Summe (SEK)",
    },
    "sku": {
        "SKU",
        "Seller SKU",
        "MSKU",
    },
    "quantity": {
        "Quantity",
        "Qty",
        "Menge",
        "Anzahl",
        "Quantité",
        "Quantite",
        "Quantità",
        "Quantita",
        "Cantidad",
        "Aantal",
        "Ilość",
        "Ilosc",
        "Antal",
    },
    "fba_fees": {
        "Gebühren zu Versand durch Amazon",
        "Gebuhren zu Versand durch Amazon",
        "Gebuehren zu Versand durch Amazon",
        "FBA fees",
        "Fulfillment by Amazon fees",
        "Frais Expédié par Amazon",
        "Frais Expedie par Amazon",
        "Frais d'expédition par Amazon",
        "Frais pour le service Expédié par Amazon",
        "Frais pour le service Expedie par Amazon",
        "Costi Logistica di Amazon",
        "Tarifas de Logística de Amazon",
        "Tarifas de Logistica de Amazon",
        "FBA-kosten",
        "FBA-vergoedingen",
        "Opłaty za realizację przez Amazon",
        "Oplaty za realizacje przez Amazon",
        "Avgifter för Fraktas av Amazon",
        "Avgifter for Fraktas av Amazon",
    },
    "other_transaction_fees": {
        "Andere Transaktionsgebühren",
        "Andere Transaktionsgebuhren",
        "Andere Transaktionsgebuehren",
        "Other transaction fees",
        "Autres frais de transaction",
        "Altri costi transazione",
        "Otros gastos de transacción",
        "Otros gastos de transaccion",
        "Tarifas de otras transacciones",
        "Overige transactiekosten",
        "Inne opłaty transakcyjne",
        "Inne oplaty transakcyjne",
        "Övriga transaktionsavgifter",
        "Ovriga transaktionsavgifter",
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
