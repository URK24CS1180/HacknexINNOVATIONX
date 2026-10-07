import pandas as pd

from question_analyzer import analyze_question
from data_engine import build_complete_data, detect_issues


def calculate_answer(question):

    # -----------------------------
    # Step 1: Analyze question
    # -----------------------------

    plan = analyze_question(question)

    print("\n===== QUESTION PLAN =====")

    for key, value in plan.items():
        print(f"{key}: {value}")

    # -----------------------------
    # Step 2: Check whether we
    # understand the question
    # -----------------------------

    if plan["metric"] is None:
        return "Cannot determine: metric is not clear."

    if plan["operation"] is None:
        return "Cannot determine: operation is not clear."

    # -----------------------------
    # Step 3: Load complete data
    # -----------------------------

    data = build_complete_data()

    # -----------------------------
    # Step 4: Check data problems
    # -----------------------------

    issues = detect_issues(data)

    print("\n===== DATA CHECK =====")

    for issue in issues:
        print("WARNING:", issue)

    # -----------------------------
    # Step 5: Filter data
    # -----------------------------

    filtered = data.copy()

    if plan["product"] is not None:
        filtered = filtered[
            filtered["product_name"] == plan["product"]
        ]

    if plan["city"] is not None:
        filtered = filtered[
            filtered["city"] == plan["city"]
        ]

    if plan["currency"] is not None:
        filtered = filtered[
            filtered["currency"] == plan["currency"]
        ]

    # -----------------------------
    # Step 6: Calculate metric
    # -----------------------------

    if plan["metric"] == "revenue":

        filtered = filtered.dropna(
            subset=["price"]
        )

        filtered["revenue"] = (
            filtered["quantity"] *
            filtered["price"]
        )

        column = "revenue"

    elif plan["metric"] == "quantity":

        column = "quantity"

    else:

        return "Cannot determine: unsupported metric."

    if len(filtered) == 0:
        return "Cannot determine: no matching data found."

    # -----------------------------
    # Step 7: Perform operation
    # -----------------------------

    if plan["operation"] == "sum":

        answer = filtered[column].sum()

    elif plan["operation"] == "average":

        answer = filtered[column].mean()

    elif plan["operation"] == "max":

        answer = filtered[column].max()

    elif plan["operation"] == "min":

        answer = filtered[column].min()

    elif plan["operation"] == "count":

        answer = filtered[column].count()

    else:

        return "Cannot determine: unsupported operation."

    # -----------------------------
    # Step 8: Return result
    # -----------------------------

    return answer


# =====================================
# MAIN PROGRAM
# =====================================

if __name__ == "__main__":

    print("====================================")
    print("   PROOF-CARRYING DATA ANALYST")
    print("====================================")

    question = input(
        "\nEnter your question: "
    )

    answer = calculate_answer(question)

    print("\n===== FINAL ANSWER =====")
    print(answer)