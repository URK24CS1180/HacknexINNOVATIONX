import ast
import os
import subprocess
import sys


# ==========================================
# CONFIGURATION
# ==========================================

TIMEOUT_SECONDS = 10


# ==========================================
# CHECK GENERATED CODE SAFETY
# ==========================================

def validate_code(code):

    try:
        tree = ast.parse(code)

    except SyntaxError as error:

        return {
            "safe": False,
            "reason": f"Invalid Python syntax: {error}"
        }

    # ======================================
    # Allowed imports
    # ======================================

    allowed_imports = {
        "pandas"
    }

    # ======================================
    # Dangerous functions
    # ======================================

    dangerous_functions = {
        "eval",
        "exec",
        "open",
        "input",
        "compile",
        "__import__",
        "globals",
        "locals",
        "getattr",
        "setattr",
        "delattr"
    }

    for node in ast.walk(tree):

        # ----------------------------------
        # Check imports
        # ----------------------------------

        if isinstance(
            node,
            ast.Import
        ):

            for alias in node.names:

                if alias.name not in allowed_imports:

                    return {
                        "safe": False,
                        "reason": (
                            f"Import not allowed: "
                            f"{alias.name}"
                        )
                    }

        # ----------------------------------
        # Check from-import
        # ----------------------------------

        if isinstance(
            node,
            ast.ImportFrom
        ):

            if node.module not in allowed_imports:

                return {
                    "safe": False,
                    "reason": (
                        f"Import not allowed: "
                        f"{node.module}"
                    )
                }

        # ----------------------------------
        # Check dangerous functions
        # ----------------------------------

        if isinstance(
            node,
            ast.Call
        ):

            if isinstance(
                node.func,
                ast.Name
            ):

                if node.func.id in dangerous_functions:

                    return {
                        "safe": False,
                        "reason": (
                            f"Dangerous function "
                            f"not allowed: "
                            f"{node.func.id}"
                        )
                    }

    return {
        "safe": True,
        "reason": "Code passed safety validation."
    }


# ==========================================
# EXECUTE CODE ONCE
# ==========================================

def execute_code(code):

    project_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    try:

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                code
            ],

            cwd=project_dir,

            capture_output=True,

            text=True,

            timeout=TIMEOUT_SECONDS,

            env={
                "PATH": os.environ.get(
                    "PATH",
                    ""
                ),

                "PYTHONNOUSERSITE": "1"
            }
        )

        if result.returncode != 0:

            return {
                "success": False,
                "output": "",
                "error": result.stderr
            }

        return {
            "success": True,
            "output": result.stdout.strip(),
            "error": ""
        }

    except subprocess.TimeoutExpired:

        return {
            "success": False,
            "output": "",
            "error": (
                "Execution timed out after "
                f"{TIMEOUT_SECONDS} seconds."
            )
        }

    except Exception as error:

        return {
            "success": False,
            "output": "",
            "error": str(error)
        }


# ==========================================
# NORMALIZE OUTPUT
# ==========================================

def normalize_output(output):

    return "\n".join(
        line.strip()
        for line in output.strip().splitlines()
        if line.strip()
    )


# ==========================================
# RUN AND VERIFY
# ==========================================

def run_code(code):

    # ======================================
    # STEP 1 — SAFETY VALIDATION
    # ======================================

    validation = validate_code(code)

    if not validation["safe"]:

        return {
            "success": False,
            "output": "",
            "error": validation["reason"],
            "verified": False,
            "verification_message": (
                "Code was rejected by the safety validator."
            )
        }

    # ======================================
    # STEP 2 — FIRST EXECUTION
    # ======================================

    first_run = execute_code(code)

    if not first_run["success"]:

        return {
            "success": False,
            "output": "",
            "error": first_run["error"],
            "verified": False,
            "verification_message": (
                "The generated code failed during execution."
            )
        }

    # ======================================
    # STEP 3 — SECOND EXECUTION
    # ======================================

    second_run = execute_code(code)

    if not second_run["success"]:

        return {
            "success": False,
            "output": "",
            "error": second_run["error"],
            "verified": False,
            "verification_message": (
                "The generated code failed during "
                "the reproducibility check."
            )
        }

    # ======================================
    # STEP 4 — COMPARE RESULTS
    # ======================================

    result_1 = normalize_output(
        first_run["output"]
    )

    result_2 = normalize_output(
        second_run["output"]
    )

    # ======================================
    # STEP 5 — VERIFICATION
    # ======================================

    if result_1 != result_2:

        return {
            "success": False,
            "output": result_1,
            "error": (
                "The two executions produced "
                "different results."
            ),
            "verified": False,
            "first_result": result_1,
            "second_result": result_2,
            "verification_message": (
                "❌ Reproducibility verification failed."
            )
        }

    # ======================================
    # STEP 6 — VERIFIED
    # ======================================

    return {
        "success": True,
        "output": result_1,
        "error": "",
        "verified": True,
        "first_result": result_1,
        "second_result": result_2,
        "verification_message": (
            "✅ VERIFIED — Both executions "
            "produced the same result."
        )
    }