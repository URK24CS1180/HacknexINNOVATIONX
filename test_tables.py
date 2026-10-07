import pandas as pd

# Load the three tables
sales = pd.read_csv("data/sales.csv")
customers = pd.read_csv("data/customers.csv")
products = pd.read_csv("data/products.csv")

# Convert date column
sales["date"] = pd.to_datetime(sales["date"])

# Connect sales with customers
sales_customers = sales.merge(
    customers,
    on="customer_id",
    how="left"
)

# Connect with products
complete_data = sales_customers.merge(
    products,
    on="product_id",
    how="left"
)

print("\n===== CONNECTED DATA =====")
print(complete_data)

# Calculate revenue
complete_data["revenue"] = (
    complete_data["quantity"] *
    complete_data["price"]
)

print("\n===== REVENUE DATA =====")
print(
    complete_data[
        [
            "transaction_id",
            "customer_name",
            "city",
            "product_name",
            "quantity",
            "price",
            "currency",
            "revenue"
        ]
    ]
)