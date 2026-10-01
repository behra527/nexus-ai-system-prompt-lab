import pandas as pd
import streamlit as st

from src.grok_client import OpenRouterClient
from src.prompt_builder import build_system_prompt
from src.validator import validate_response
from src.evaluator import evaluate_compliance
from src.security import (
    SECURITY_TESTS,
    evaluate_security_response,
)


# ==================================================
# Page Configuration
# ==================================================

st.set_page_config(
    page_title="System Prompt Engineering Lab",
    page_icon="AI",
    layout="wide",
)


# ==================================================
# Session State
# ==================================================

if "experiment_history" not in st.session_state:
    st.session_state.experiment_history = []


# ==================================================
# Header
# ==================================================

st.title("System Prompt Engineering Lab")

st.caption(
    "Explore how system-level instructions control role, "
    "tone, constraints, output format, safety, and model behavior."
)


# ==================================================
# Sidebar: Prompt Configuration
# ==================================================

with st.sidebar:

    st.header("Prompt Configuration")

    role = st.selectbox(
        "Role",
        [
            "Senior AI Engineer",
            "Python Developer",
            "Data Scientist",
            "Technical Research Assistant",
        ],
    )

    tone = st.selectbox(
        "Tone",
        [
            "Professional",
            "Technical",
            "Concise",
            "Formal",
        ],
    )

    response_style = st.selectbox(
        "Response Style",
        [
            "Concise and structured",
            "Detailed and explanatory",
            "Step-by-step",
        ],
    )

    output_format = st.selectbox(
        "Output Format",
        [
            "Markdown",
            "Plain Text",
            "Strict JSON",
        ],
    )

    safety_level = st.selectbox(
        "Safety Level",
        [
            "Standard",
            "Strict",
        ],
    )

    accuracy_level = st.selectbox(
        "Accuracy Level",
        [
            "High",
            "Very High",
        ],
    )

    st.divider()

    st.header("Model Configuration")

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
    )

    max_tokens = st.slider(
        "Maximum Tokens",
        min_value=100,
        max_value=2000,
        value=700,
        step=100,
    )

    st.divider()

    st.header("Security Testing")

    security_test = st.selectbox(
        "Injection Test",
        [
            "None",
            *SECURITY_TESTS.keys(),
        ],
    )


# ==================================================
# User Prompt
# ==================================================

if security_test == "None":

    user_prompt = st.text_area(
        "User Prompt",
        placeholder=(
            "Example: Design a production architecture "
            "for a RAG application."
        ),
        height=180,
    )

else:

    user_prompt = st.text_area(
        "Security Test Prompt",
        value=SECURITY_TESTS[security_test],
        height=180,
    )


# ==================================================
# Dynamic System Prompt
# ==================================================

system_prompt = build_system_prompt(
    role=role,
    tone=tone,
    response_style=response_style,
    output_format=output_format,
    safety_level=safety_level,
    accuracy_level=accuracy_level,
)


# ==================================================
# Run Experiment
# ==================================================

if st.button("Run Experiment", type="primary"):

    if not user_prompt.strip():

        st.warning("Please enter a user prompt.")

        st.stop()


    # --------------------------------------------------
    # Generate Response
    # --------------------------------------------------

    with st.spinner("Generating response..."):

        try:

            client = OpenRouterClient()

            result = client.generate(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

        except Exception as exc:

            st.error(f"API error: {exc}")

            st.stop()


    response = result["content"]
    usage = result["usage"]


    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    valid = False
    validation_result = "Not required."

    if output_format == "Strict JSON":

        valid, validation_result = validate_response(
            response
        )


    validation_status = "N/A"

    if output_format == "Strict JSON":

        validation_status = (
            "PASS"
            if valid
            else "FAIL"
        )


    # --------------------------------------------------
    # Compliance Evaluation
    # --------------------------------------------------

    compliance_results = evaluate_compliance(
        response=response,
        output_format=output_format,
        role=role,
        safety_level=safety_level,
    )


    # --------------------------------------------------
    # Security Evaluation
    # --------------------------------------------------

    security_result = None
    security_status = "N/A"

    if security_test != "None":

        security_result = evaluate_security_response(
            response
        )

        security_passed = (
            security_result["system_prompt_protection"]
            and security_result["secret_protection"]
        )

        security_status = (
            "PASS"
            if security_passed
            else "FAIL"
        )


    # --------------------------------------------------
    # Save Experiment
    # --------------------------------------------------

    experiment = {
        "Role": role,
        "Tone": tone,
        "Style": response_style,
        "Format": output_format,
        "Safety": safety_level,
        "Accuracy": accuracy_level,
        "Temperature": temperature,
        "Total Tokens": usage["total_tokens"],
        "Validation": validation_status,
        "Security": security_status,
    }

    st.session_state.experiment_history.append(
        experiment
    )


    # ==================================================
    # Model Response
    # ==================================================

    st.subheader("Model Response")

    if output_format == "Strict JSON":

        st.code(
            response,
            language="json",
        )

        st.subheader("Schema Validation")

        if valid:

            st.success(
                "Valid structured output."
            )

        else:

            st.error(
                "Output validation failed."
            )

            with st.expander(
                "Validation Details"
            ):

                st.code(
                    validation_result,
                    language="text",
                )

    else:

        st.write(response)


    # ==================================================
    # Prompt Compliance
    # ==================================================

    st.subheader("Prompt Compliance")

    for check_name, check_result in compliance_results.items():

        status = check_result["status"]
        message = check_result["message"]

        if status == "PASS":

            st.success(
                f"{check_name}: PASS — {message}"
            )

        elif status == "FAIL":

            st.error(
                f"{check_name}: FAIL — {message}"
            )

        else:

            st.warning(
                f"{check_name}: REVIEW — {message}"
            )


    # ==================================================
    # Security Test Results
    # ==================================================

    if security_result is not None:

        st.subheader("Security Test Results")

        col1, col2 = st.columns(2)

        if security_result[
            "system_prompt_protection"
        ]:

            col1.success(
                "System Prompt Protection: PASS"
            )

        else:

            col1.error(
                "System Prompt Protection: FAIL"
            )

        if security_result[
            "secret_protection"
        ]:

            col2.success(
                "Secret Protection: PASS"
            )

        else:

            col2.error(
                "Secret Protection: FAIL"
            )

        if (
            security_result[
                "detected_indicators"
            ]
            or security_result[
                "detected_sensitive_patterns"
            ]
        ):

            with st.expander(
                "Security Details"
            ):

                if security_result[
                    "detected_indicators"
                ]:

                    st.write(
                        "Detected indicators:",
                        security_result[
                            "detected_indicators"
                        ],
                    )

                if security_result[
                    "detected_sensitive_patterns"
                ]:

                    st.write(
                        "Detected sensitive patterns:",
                        security_result[
                            "detected_sensitive_patterns"
                        ],
                    )


    # ==================================================
    # Token Usage
    # ==================================================

    st.subheader("Token Usage")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Prompt Tokens",
        usage["prompt_tokens"],
    )

    col2.metric(
        "Completion Tokens",
        usage["completion_tokens"],
    )

    col3.metric(
        "Total Tokens",
        usage["total_tokens"],
    )


    # ==================================================
    # System Prompt Inspector
    # ==================================================

    with st.expander(
        "View Generated System Prompt"
    ):

        st.code(
            system_prompt,
            language="text",
        )


# ==================================================
# Experiment History
# ==================================================

st.divider()

st.subheader("Experiment History")

history = st.session_state.experiment_history


if history:

    # --------------------------------------------------
    # Summary Metrics
    # --------------------------------------------------

    total_experiments = len(history)

    total_tokens = sum(
        item["Total Tokens"]
        for item in history
    )

    validation_passed = sum(
        item["Validation"] == "PASS"
        for item in history
    )

    security_passed = sum(
        item["Security"] == "PASS"
        for item in history
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Experiments",
        total_experiments,
    )

    col2.metric(
        "Total Tokens",
        total_tokens,
    )

    col3.metric(
        "Valid Outputs",
        validation_passed,
    )

    col4.metric(
        "Security Tests Passed",
        security_passed,
    )


    # --------------------------------------------------
    # History Table
    # --------------------------------------------------

    history_df = pd.DataFrame(history)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True,
    )

else:

    st.info(
        "Run an experiment to populate the history."
    )