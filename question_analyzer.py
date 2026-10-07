import re


def analyze_question(question):

    question_lower = question.lower()

    plan = {
        "metric": None,
        "operation": None,
        "product": None,
        "city": None,
        "currency": None,
        "customer": None
    }

    # -----------------------------
    # Detect metric
    # -----------------------------

    if "revenue" in question_lower:
        plan["metric"] = "revenue"

    elif "quantity" in question_lower:
        plan["metric"] = "quantity"

    elif "sales" in question_lower:
        plan["metric"] = "sales"

    # -----------------------------
    # Detect operation
    # -----------------------------

    if "total" in question_lower:
        plan["operation"] = "sum"

    elif "average" in question_lower or "avg" in question_lower:
        plan["operation"] = "average"

    elif "maximum" in question_lower or "highest" in question_lower:
        plan["operation"] = "max"

    elif "minimum" in question_lower or "lowest" in question_lower:
        plan["operation"] = "min"

    elif "count" in question_lower or "how many" in question_lower:
        plan["operation"] = "count"

    # -----------------------------
    # Detect products
    # -----------------------------

    products = [
        "laptop",
        "mouse",
        "keyboard",
        "monitor"
    ]

    for product in products:
        if product in question_lower:
            plan["product"] = product.title()

    # -----------------------------
    # Detect cities
    # -----------------------------

    cities = [
        "coimbatore",
        "chennai",
        "madurai",
        "salem",
        "bangalore"
    ]

    for city in cities:
        if city in question_lower:
            plan["city"] = city.title()

    # -----------------------------
    # Detect currency
    # -----------------------------

    if "inr" in question_lower or "rupee" in question_lower:
        plan["currency"] = "INR"

    elif "usd" in question_lower or "dollar" in question_lower:
        plan["currency"] = "USD"

    return plan


# =====================================
# TEST
# =====================================

if __name__ == "__main__":

    question = input("Enter your question: ")

    result = analyze_question(question)

    print("\n===== QUESTION =====")
    print(question)

    print("\n===== ANALYZED PLAN =====")

    for key, value in result.items():
        print(f"{key}: {value}")