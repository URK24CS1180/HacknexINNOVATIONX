import pandas as pd

from data_engine import build_complete_data


def generate_evidence(plan):

    data = build_complete_data()

    product = plan.get("product")
    city = plan.get("city")
    currency = plan.get("currency")
    customer = plan.get("customer")

    # ==========================================
    # NORMALIZE VALUES
    # ==========================================

    if product:
        product = str(product).strip().lower()

    if city:
        city = str(city).strip().lower()

    if currency:
        currency = str(currency).strip().upper()

    if customer:
        customer = str(customer).strip().lower()

    # ==========================================
    # FILTER DATA
    # ==========================================

    matching = data.copy()

    if product:
        matching = matching[
            matching["product_name"]
            .astype(str)
            .str.lower()
            .isin([
                product,
                "mouse" if product == "mice" else product
            ])
        ]

    if city:
        matching = matching[
            matching["city"]
            .astype(str)
            .str.lower()
            == city
        ]

    if currency:
        matching = matching[
            matching["currency"]
            .astype(str)
            .str.upper()
            == currency
        ]

    if customer:
        matching = matching[
            matching["customer_name"]
            .astype(str)
            .str.lower()
            == customer
        ]

    # ==========================================
    # DUPLICATES
    # ==========================================

    duplicate_mask = matching[
        "transaction_id"
    ].duplicated(
        keep=False
    )

    duplicate_ids = (
        matching.loc[
            duplicate_mask,
            "transaction_id"
        ]
        .dropna()
        .unique()
        .tolist()
    )

    # ==========================================
    # MISSING VALUES
    # ==========================================

    missing_price = int(
        matching["price"].isna().sum()
    )

    missing_quantity = int(
        matching["quantity"].isna().sum()
    )

    # ==========================================
    # CURRENCIES
    # ==========================================

    currencies = (
        matching["currency"]
        .dropna()
        .unique()
        .tolist()
    )

    # ==========================================
    # RETURN EVIDENCE
    # ==========================================

    return {
        "matching_rows": len(matching),
        "duplicate_transaction_ids": duplicate_ids,
        "duplicate_count": len(duplicate_ids),
        "missing_price_count": missing_price,
        "missing_quantity_count": missing_quantity,
        "currencies": currencies
    }