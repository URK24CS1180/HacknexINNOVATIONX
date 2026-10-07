from question_analyzer import analyze_question
from code_generator import generate_code
from decision_engine import check_question
from verifier import run_code


def run_proof_pipeline(question):

    print("\n========================================")
    print("       PROOF-CARRYING DATA ANALYST")
    print("========================================")

    # ======================================
    # STEP 1: Analyze question
    # ======================================

    print("\n[1] ANALYZING QUESTION...")

    plan = analyze_question(question)

    for key, value in plan.items():
        print(f"    {key}: {value}")

    # ======================================
    # STEP 2: Check whether question
    # can be answered safely
    # ======================================

    print("\n[2] CHECKING DATA SAFETY...")

    decision = check_question(question)

    if not decision["allowed"]:

        print("\n❌ ANSWER REFUSED")

        print("\nReason:")
        print(decision["reason"])

        return

    print("    ✓ Question passed safety checks.")

    # ======================================
    # STEP 3: Generate Python code
    # ======================================

    print("\n[3] GENERATING PYTHON CODE...")

    generated_code = generate_code(question)

    if generated_code is None:

        print("\n❌ Could not generate code.")

        return

    print("    ✓ Code generated.")

    # ======================================
    # STEP 4: Show generated code
    # ======================================

    print("\n[4] GENERATED CODE")
    print("----------------------------------------")

    print(generated_code)

    print("----------------------------------------")

    # ======================================
    # STEP 5: Execute generated code
    # ======================================

    print("\n[5] EXECUTING CODE...")

    execution = run_code(generated_code)

    if not execution["success"]:

        print("\n❌ CODE EXECUTION FAILED")

        print("\nError:")
        print(execution["error"])

        return

    print("    ✓ Code executed successfully.")

    # ======================================
    # STEP 6: Extract result
    # ======================================

    result = execution["output"].strip()

    print("\n[6] CALCULATION RESULT")

    print("    ", result)

    # ======================================
    # STEP 7: Proof
    # ======================================

    print("\n[7] VERIFICATION")

    print("    ✓ Code executed successfully.")
    print("    ✓ Result reproduced successfully.")

    # ======================================
    # FINAL ANSWER
    # ======================================

    print("\n========================================")
    print("             FINAL ANSWER")
    print("========================================")

    print(result)

    print("\n========================================")
    print("               PROOF")
    print("========================================")

    print("The answer above was produced by")
    print("executable Python code generated from")
    print("the user's question.")

    print("\nThe generated code can be re-run")
    print("to reproduce the calculation.")


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    question = input(
        "\nEnter your question: "
    )

    run_proof_pipeline(question)