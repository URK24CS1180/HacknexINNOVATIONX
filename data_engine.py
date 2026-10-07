import pandas as pd


def load_tables():
    sales = pd.read_csv("data/sales.csv")
    customers = pd.read_csv("data/customers.csv")
    products = pd.read_csv("data/products.csv")

    sales["date"] = pd.to_datetime(sales["date"])

    return sales, customers, products


def build_complete_data():
    sales, customers, products = load_tables()

    data = sales.merge(
        customers,
        on="customer_id",
        how="left"
    )

    data = data.merge(
        products,
        on="product_id",
        how="left"
    )

    return data


def detect_issues(data):
    issues = []

    # Check duplicate transactions
    duplicate_count = data["transaction_id"].duplicated().sum()

    if duplicate_count > 0:
        issues.append(
            f"Duplicate transactions detected: {duplicate_count}"
        )

    # Check missing values
    missing = data.isnull().sum()

    for column, count in missing.items():
        if count > 0:
            issues.append(
                f"Missing values in {column}: {count}"
            )

    # Check currencies
    currencies = data["currency"].dropna().unique()

    if len(currencies) > 1:
        issues.append(
            f"Multiple currencies detected: {list(currencies)}"
        )

    return issues


def calculate_revenue(data):
    data = data.dropna(subset=["price"]).copy()

    data["revenue"] = (
        data["quantity"] *
        data["price"]
    )

    return data


if __name__ == "__main__":

    print("===== LOADING DATA =====")

    data = build_complete_data()

    print(data)

    print("\n===== DATA ISSUES =====")

    issues = detect_issues(data)

    if issues:
        for issue in issues:
            print("WARNING:", issue)
    else:
        print("No issues detected.")

    print("\n===== REVENUE =====")

    revenue_data = calculate_revenue(data)

    print(
        revenue_data[
            [
                "transaction_id",
                "customer_name",
                "product_name",
                "quantity",
                "price",
                "currency",
                "revenue"
            ]
        ]
    )