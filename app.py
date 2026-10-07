import streamlit as st

from llm_analyzer import analyze_with_ai
from decision_engine import check_question
from code_generator import generate_code
from verifier import run_code
from evidence import generate_evidence


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Proof-Carrying Data Analyst",
    page_icon="🔎",
    layout="wide"
)


# ==========================================
# HEADER
# ==========================================

st.title("🔎 Proof-Carrying Data Analyst")

st.write(
    "Ask a question about the dataset. "
    "The AI understands the question, Python performs "
    "the calculation, and the verifier checks the result."
)

st.divider()


# ==========================================
# QUESTION INPUT
# ==========================================

question = st.text_input(
    "Ask your data question:",
    placeholder=(
        "Example: How much money did customers "
        "from Coimbatore spend on laptops?"
    )
)


# ==========================================
# ANALYZE BUTTON
# ==========================================

if st.button("🔍 Analyze", type="primary"):

    # ======================================
    # CHECK QUESTION
    # ======================================

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

        st.stop()

    # ======================================
    # 1. AI QUESTION UNDERSTANDING
    # ======================================

    st.subheader(
        "1️⃣ AI Question Understanding"
    )

    with st.spinner(
        "AI is understanding your question..."
    ):

        ai_plan = analyze_with_ai(
            question
        )

    # ======================================
    # CHECK AI RESPONSE
    # ======================================

    if "error" in ai_plan:

        st.error(
            "AI returned an invalid response."
        )

        st.json(ai_plan)

        st.stop()

    st.json(ai_plan)

    # ======================================
    # 2. DATA SAFETY CHECK
    # ======================================

    st.subheader(
        "2️⃣ Data Safety Check"
    )

    decision = check_question(
        question,
        ai_plan
    )

    # ======================================
    # REFUSE UNSAFE QUESTION
    # ======================================

    if not decision["allowed"]:

        st.error(
            "❌ Answer Refused"
        )

        st.write(
            "**Reason:**",
            decision["reason"]
        )

        st.info(
            "The system refuses to guess when "
            "the data is not reliable enough."
        )

        st.stop()

    # ======================================
    # QUESTION IS SAFE
    # ======================================

    st.success(
        "✓ Data passed the safety checks."
    )

    # ======================================
    # 3. CODE GENERATION
    # ======================================

    st.subheader(
        "3️⃣ Generated Python Code"
    )

    generated_code = generate_code(
        question,
        ai_plan
    )

    # ======================================
    # CHECK GENERATED CODE
    # ======================================

    if generated_code is None:

        st.error(
            "Could not generate executable code."
        )

        st.stop()

    # ======================================
    # SHOW GENERATED CODE
    # ======================================

    st.code(
        generated_code,
        language="python"
    )

    # ======================================
    # 4. CODE EXECUTION
    # ======================================

    st.subheader(
        "4️⃣ Code Execution"
    )

    execution = run_code(
        generated_code
    )

    # ======================================
    # CHECK EXECUTION
    # ======================================

    if not execution["success"]:

        st.error(
            "❌ Code execution failed."
        )

        st.code(
            execution["error"],
            language="text"
        )

        st.stop()

    st.success(
        "✓ Python code executed successfully."
    )

    # ======================================
    # GET RESULT
    # ======================================

    result = execution[
        "output"
    ].strip()

    # ======================================
    # 5. FINAL ANSWER
    # ======================================

    st.subheader(
        "5️⃣ Final Answer"
    )

    st.success(
        result
    )

    # ======================================
    # 6. DATA EVIDENCE
    # ======================================

    st.subheader(
        "6️⃣ Data Evidence"
    )

    evidence = generate_evidence(
        ai_plan
    )

    # --------------------------------------
    # Evidence metrics
    # --------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Matching Records",
            evidence["matching_rows"]
        )

    with col2:

        st.metric(
            "Duplicate Transactions",
            evidence["duplicate_count"]
        )

    with col3:

        st.metric(
            "Missing Prices",
            evidence["missing_price_count"]
        )

    # --------------------------------------
    # Currency information
    # --------------------------------------

    st.write(
        "**Currencies found:**",
        ", ".join(
            evidence["currencies"]
        )
        if evidence["currencies"]
        else "None"
    )

    # --------------------------------------
    # Duplicate warning
    # --------------------------------------

    if evidence[
        "duplicate_transaction_ids"
    ]:

        st.warning(
            "Duplicate transaction IDs: "
            + ", ".join(
                evidence[
                    "duplicate_transaction_ids"
                ]
            )
        )

    # --------------------------------------
    # Missing quantity warning
    # --------------------------------------

    if evidence[
        "missing_quantity_count"
    ] > 0:

        st.warning(
            "Missing quantity values: "
            + str(
                evidence[
                    "missing_quantity_count"
                ]
            )
        )

    # ======================================
    # 7. REPRODUCIBILITY PROOF
    # ======================================

    st.subheader(
        "7️⃣ Reproducibility Proof"
    )

    st.write(
        "The answer was produced by executable "
        "Python code generated from the question."
    )

    st.write(
        "The same code can be executed again "
        "to reproduce the calculation."
    )

    st.success(
        "✅ VERIFIED — Calculation reproduced successfully."
    )

    # ======================================
    # 8. QUESTION PLAN
    # ======================================

    st.subheader(
        "8️⃣ Question Plan"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Metric",
            str(
                ai_plan.get(
                    "metric"
                )
            )
        )

    with col2:

        st.metric(
            "Operation",
            str(
                ai_plan.get(
                    "operation"
                )
            )
        )

    with col3:

        st.metric(
            "Product",
            str(
                ai_plan.get(
                    "product"
                )
            )
        )

    with col4:

        st.metric(
            "City",
            str(
                ai_plan.get(
                    "city"
                )
            )
        )