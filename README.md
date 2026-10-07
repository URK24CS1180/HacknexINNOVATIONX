# 🔎 Proof-Carrying Data Analyst

### Agentic GenAI for Reliable and Reproducible Data Analysis

Proof-Carrying Data Analyst is an **Agentic GenAI-powered data analysis system** that answers natural-language questions over messy, multi-table datasets while providing **executable Python proof for numerical results**.

Unlike traditional AI data-analysis systems that directly generate answers, this project separates:

- Question understanding
- Data validation
- Computation
- Verification
- Evidence generation

The AI understands the user's question, while **Python performs the actual numerical calculation**. The generated code is executed and independently re-run to verify reproducibility.

If the data is incomplete, duplicated, ambiguous, or inconsistent, the system can **refuse to answer instead of producing a potentially incorrect result**.

---
Problem Statement

Generative AI can answer questions about data, but numerical answers generated directly by an LLM may not always be reliable.

Real-world datasets often contain:

- Duplicate records
- Missing values
- Multiple currencies
- Inconsistent information
- Ambiguous questions
- Empty results
- Invalid queries

A conventional AI system may still produce a confident answer.

**Proof-Carrying Data Analyst solves this problem by making the AI-generated answer carry executable proof.**

### Core Principle

> **The AI understands the question. Python calculates the answer. The verifier checks the result.**

---

## ✨ Key Features

- 🧠 Natural-language data analysis
- 🤖 Agentic GenAI question understanding
- 🗃️ Multi-table data processing
- 🔗 Automatic table joining
- 🛡️ Data-quality validation
- 🔍 Duplicate transaction detection
- ❌ Missing-value detection
- 💱 Currency consistency checking
- 🐍 Executable Python code generation
- ▶️ Automatic code execution
- 🔁 Reproducibility verification
- 📊 Evidence generation
- 🚫 Intelligent refusal for unreliable questions
- 🌐 Interactive Streamlit interface

---

## 🏗️ System Architecture

```text
                         ┌──────────────────────┐
                         │     User Question    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Gemini GenAI     │
                         │ Question Understanding│
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Structured Query   │
                         │        Plan          │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Decision Engine   │
                         │   Data Safety Check  │
                         └──────────┬───────────┘
                                    │
                         ┌──────────┴──────────┐
                         │                     │
                         ▼                     ▼
                     ❌ Unsafe              ✅ Safe
                         │                     │
                         ▼                     ▼
                  Refuse Answer        Python Generator
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Python Executor │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │    Verifier     │
                                      │    Run Twice    │
                                      └────────┬────────┘
                                               │
                                               ▼
                                      ┌─────────────────┐
                                      │ Answer + Proof  │
                                      │   + Evidence    │
                                      └─────────────────┘
