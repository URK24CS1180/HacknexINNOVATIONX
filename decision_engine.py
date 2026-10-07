from data_engine import build_complete_data


# ==========================================
# PRODUCT NORMALIZATION
# ==========================================

def normalize_product(product):

    if product is None:
        return None

    product = str(product).strip().lower()

    product_map = {
        "mouse": "Mouse",
        "mice": "Mouse",
        "mouses": "Mouse",

        "laptop": "Laptop",
        "laptops": "Laptop",

        "keyboard": "Keyboard",
        "keyboards": "Keyboard",

        "monitor": "Monitor",
        "monitors": "Monitor"
    }

    return product_map.get(
        product,
        product.title()
    )


# ==========================================
# CITY NORMALIZATION
# ==========================================

def normalize_city(city):

    if city is None:
        return None

    city = str(city).strip().lower()

    city_map = {
        "coimbatore": "Coimbatore",
        "chennai": "Chennai",
        "madurai": "Madurai",
        "salem": "Salem",
        "bangalore": "Bangalore",
        "bengaluru": "Bangalore"
    }

    return city_map.get(
        city,
        city.title()
    )


# ==========================================
# CURRENCY NORMALIZATION
# ==========================================

def normalize_currency(currency):

    if currency is None:
        return None

    currency = str(currency).strip().upper()

    currency_map = {
        "RUPEE": "INR",
        "RUPEES": "INR",
        "₹": "INR",
        "DOLLAR": "USD",
        "DOLLARS": "USD",
        "$": "USD"
    }

    return currency_map.get(
        currency,
        currency
    )


# ==========================================
# CHECK QUESTION
# ==========================================

def check_question(question, plan):

    # ======================================
    # CHECK AI PLAN
    # ======================================

    if plan is None:

        return {
            "allowed": False,
            "reason": "No question plan was provided."
        }

    if plan.get("error"):

        return {
            "allowed": False,
            "reason": (
                "The AI returned an invalid question plan."
            )
        }

    # ======================================
    # GET PLAN VALUES
    # ======================================

    metric = plan.get("metric")

    operation = plan.get("operation")

    product = normalize_product(
        plan.get("product")
    )

    city = normalize_city(
        plan.get("city")
    )

    currency = normalize_currency(
        plan.get("currency")
    )

    customer = plan.get("customer")

    # ======================================
    # VALIDATE METRIC
    # ======================================

    allowed_metrics = [
        "revenue",
        "quantity",
        "sales"
    ]

    if metric is None:

        return {
            "allowed": False,
            "reason": "The metric is not clear."
        }

    if metric not in allowed_metrics:

        return {
            "allowed": False,
            "reason": (
                f"Unsupported metric: {metric}"
            )
        }

    # ======================================
    # VALIDATE OPERATION
    # ======================================

    allowed_operations = [
        "sum",
        "average",
        "maximum",
        "minimum",
        "count"
    ]

    if operation is None:

        return {
            "allowed": False,
            "reason": (
                "The requested operation is not clear."
            )
        }

    if operation not in allowed_operations:

        return {
            "allowed": False,
            "reason": (
                f"Unsupported operation: {operation}"
            )
        }

    # ======================================
    # LOAD COMPLETE DATA
    # ======================================

    try:

        data = build_complete_data()

    except Exception as error:

        return {
            "allowed": False,
            "reason": (
                f"Could not load the dataset: {error}"
            )
        }

    # ======================================
    # FILTER RELEVANT DATA
    # ======================================

    matching = data.copy()

    # --------------------------------------
    # Product filter
    # --------------------------------------

    if product is not None:

        matching = matching[
            matching["product_name"]
            .astype(str)
            .str.lower()
            == product.lower()
        ]

    # --------------------------------------
    # City filter
    # --------------------------------------

    if city is not None:

        matching = matching[
            matching["city"]
            .astype(str)
            .str.lower()
            == city.lower()
        ]

    # --------------------------------------
    # Currency filter
    # --------------------------------------

    if currency is not None:

        matching = matching[
            matching["currency"]
            .astype(str)
            .str.upper()
            == currency.upper()
        ]

    # --------------------------------------
    # Customer filter
    # --------------------------------------

    if customer is not None:

        matching = matching[
            matching["customer_name"]
            .astype(str)
            .str.lower()
            == str(customer).lower()
        ]

    # ======================================
    # CHECK WHETHER DATA EXISTS
    # ======================================

    if len(matching) == 0:

        return {
            "allowed": False,
            "reason": (
                "No matching records were found."
            )
        }

    # ======================================
    # REVENUE SAFETY CHECK
    # ======================================

    if metric == "revenue":

        # ----------------------------------
        # Check currencies
        # ----------------------------------

        currencies = (
            matching["currency"]
            .dropna()
            .astype(str)
            .str.upper()
            .unique()
        )

        if len(currencies) > 1:

            return {
                "allowed": False,
                "reason": (
                    "Revenue cannot be calculated safely "
                    "because multiple currencies are present "
                    f"in the matching data: {list(currencies)}."
                )
            }

        # ----------------------------------
        # Check missing prices
        # ----------------------------------

        if matching["price"].isna().any():

            missing_count = int(
                matching["price"].isna().sum()
            )

            return {
                "allowed": False,
                "reason": (
                    "Revenue cannot be calculated reliably "
                    f"because {missing_count} matching "
                    "record(s) have a missing price."
                )
            }

    # ======================================
    # DUPLICATE TRANSACTION CHECK
    # ======================================

    duplicate_mask = matching[
        "transaction_id"
    ].duplicated(
        keep=False
    )

    if duplicate_mask.any():

        duplicate_ids = (
            matching.loc[
                duplicate_mask,
                "transaction_id"
            ]
            .dropna()
            .unique()
            .tolist()
        )

        return {
            "allowed": False,
            "reason": (
                "The requested result may be affected "
                "by duplicate transaction IDs: "
                f"{duplicate_ids}."
            )
        }

    # ======================================
    # CHECK MISSING QUANTITY
    # ======================================

    if metric in ["quantity", "sales"]:

        if matching["quantity"].isna().any():

            missing_count = int(
                matching["quantity"].isna().sum()
            )

            return {
                "allowed": False,
                "reason": (
                    "The answer cannot be calculated "
                    "reliably because "
                    f"{missing_count} matching record(s) "
                    "have missing quantity values."
                )
            }

    # ======================================
    # FINAL SAFETY DECISION
    # ======================================

    return {
        "allowed": True,
        "reason": (
            "Question passed all data safety checks."
        ),

        # Useful information for our future
        # evidence/proof report
        "matching_rows": len(matching),

        "normalized_plan": {
            "metric": metric,
            "operation": operation,
            "product": product,
            "city": city,
            "currency": currency,
            "customer": customer
        }
    }


# ==========================================
# TESTING
# ==========================================

if __name__ == "__main__":

    print("========================================")
    print("          DECISION ENGINE")
    print("========================================")

    print("\nThis file is normally called by app.py.")

    print(
        "\nUse the Streamlit application to test "
        "natural-language questions."
    )