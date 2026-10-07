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
# CODE GENERATOR
# ==========================================

def generate_code(question, plan):

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

    # ======================================
    # VALIDATE PLAN
    # ======================================

    if metric is None:
        return None

    if operation is None:
        return None

    # ======================================
    # START CODE
    # ======================================

    code = """import pandas as pd

# ==========================================
# LOAD SOURCE DATA
# ==========================================

sales = pd.read_csv("data/sales.csv")

customers = pd.read_csv(
    "data/customers.csv"
)

products = pd.read_csv(
    "data/products.csv"
)


# ==========================================
# CONVERT DATE
# ==========================================

sales["date"] = pd.to_datetime(
    sales["date"]
)


# ==========================================
# JOIN SALES + CUSTOMERS
# ==========================================

data = sales.merge(
    customers,
    on="customer_id",
    how="left"
)


# ==========================================
# JOIN WITH PRODUCTS
# ==========================================

data = data.merge(
    products,
    on="product_id",
    how="left"
)

"""

    # ======================================
    # PRODUCT FILTER
    # ======================================

    if product is not None:

        safe_product = (
            str(product)
            .replace('"', '\\"')
        )

        code += f'''# Filter product
data = data[
    data["product_name"] == "{safe_product}"
]

'''

    # ======================================
    # CITY FILTER
    # ======================================

    if city is not None:

        safe_city = (
            str(city)
            .replace('"', '\\"')
        )

        code += f'''# Filter city
data = data[
    data["city"] == "{safe_city}"
]

'''

    # ======================================
    # CURRENCY FILTER
    # ======================================

    if currency is not None:

        safe_currency = (
            str(currency)
            .replace('"', '\\"')
        )

        code += f'''# Filter currency
data = data[
    data["currency"] == "{safe_currency}"
]

'''

    # ======================================
    # CHECK WHETHER DATA EXISTS
    # ======================================

    code += """# Check matching records
if len(data) == 0:
    raise ValueError(
        "No matching records found."
    )

"""

    # ======================================
    # METRIC
    # ======================================

    if metric == "revenue":

        code += """# ==========================================
# CALCULATE REVENUE
# ==========================================

data = data.dropna(
    subset=["price"]
)

data["revenue"] = (
    data["quantity"] *
    data["price"]
)

"""

        column = "revenue"

    elif metric == "quantity":

        column = "quantity"

    elif metric == "sales":

        column = "quantity"

    else:

        return None

    # ======================================
    # OPERATION
    # ======================================

    if operation == "sum":

        code += f"""# Calculate total
answer = data["{column}"].sum()

"""

    elif operation == "average":

        code += f"""# Calculate average
answer = data["{column}"].mean()

"""

    elif operation == "maximum":

        code += f"""# Calculate maximum
answer = data["{column}"].max()

"""

    elif operation == "minimum":

        code += f"""# Calculate minimum
answer = data["{column}"].min()

"""

    elif operation == "count":

        code += f"""# Calculate count
answer = data["{column}"].count()

"""

    else:

        return None

    # ======================================
    # FINAL OUTPUT
    # ======================================

    code += """# Print only the final answer
print(answer)
"""

    return code