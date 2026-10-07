import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()


# ==========================================
# GEMINI CLIENT
# ==========================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set."
    )

client = genai.Client(
    api_key=api_key
)


# ==========================================
# AI QUESTION ANALYZER
# ==========================================

def analyze_with_ai(question):

    prompt = f"""
You are the question-understanding component
of a Proof-Carrying Data Analyst.

Your job is ONLY to understand the user's
data-analysis question.

DO NOT calculate the answer.

Convert the question into JSON.

Allowed values:

metric:
- revenue
- quantity
- sales
- null

operation:
- sum
- average
- maximum
- minimum
- count
- null

product:
- product name
- null

city:
- city name
- null

currency:
- INR
- USD
- null

customer:
- customer name
- null

If something is not mentioned, use null.

If the question is ambiguous, use null
for the ambiguous field.

Return ONLY valid JSON.

Example:

{{
    "metric": "revenue",
    "operation": "sum",
    "product": "Laptop",
    "city": "Coimbatore",
    "currency": null,
    "customer": null
}}

User question:

{question}
"""

    # ======================================
    # CALL GEMINI
    # ======================================

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    text = response.text.strip()

    # ======================================
    # CLEAN JSON RESPONSE
    # ======================================

    if text.startswith("```json"):
        text = text[7:]

    elif text.startswith("```"):
        text = text[3:]

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    # ======================================
    # CONVERT JSON STRING TO PYTHON DICT
    # ======================================

    try:

        result = json.loads(text)

        return result

    except json.JSONDecodeError:

        return {
            "error": "AI returned invalid JSON",
            "raw_response": text
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    print("======================================")
    print("       AI QUESTION ANALYZER")
    print("======================================")

    question = input(
        "\nEnter your question: "
    )

    result = analyze_with_ai(question)

    print("\n===== AI ANALYSIS =====")

    print(
        json.dumps(
            result,
            indent=4
        )
    )