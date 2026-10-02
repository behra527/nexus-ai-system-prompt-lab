import streamlit as st

from src.llm_client import generate_response
from src.prompt_builder import build_messages
from src.validator import validate_llm_response


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Nexus AI ",
    page_icon="⚡",
    layout="wide",
)


# ---------------------------------------------------------
# Custom Styling (Production-Ready & Polished UI)
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* Global Theme & Sleek Light Background */
    .stApp {
        background-color: #F8FAFC;
        color: #0F172A;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 6rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Main Header Styling */
    .console-header-container {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 0.4rem;
    }

    .console-logo-box {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 20px;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.3);
    }

    .console-title {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.7px;
        color: #0F172A;
    }

    .console-subtitle {
        color: #64748B;
        font-size: 1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Sidebar Professional Dark Contrast Styling */
    section[data-testid="stSidebar"] {
        background-color: #0B0F19;
        border-right: 1px solid #1E293B;
        padding: 1.5rem 1rem;
    }

    /* Sidebar Brand Header with High Contrast Logo */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding-bottom: 1.2rem;
        margin-bottom: 1.2rem;
        border-bottom: 1px solid #1E293B;
    }

    .sidebar-logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #FFFFFF;
        font-size: 18px;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
    }

    .sidebar-brand-text {
        font-size: 0.98rem;
        font-weight: 700;
        color: #F8FAFC;
        letter-spacing: -0.01em;
    }

    section[data-testid="stSidebar"] h2 {
        color: #94A3B8 !important;
        font-size: 0.75rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        margin-top: 1.2rem !important;
        margin-bottom: 0.75rem !important;
    }

    section[data-testid="stSidebar"] label {
        color: #CBD5E1 !important;
        font-size: 0.78rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.04em !important;
        margin-bottom: 0.25rem !important;
    }

    /* Sleek Sidebar Input Fields & Text Fix */
    section[data-testid="stSidebar"] .stTextInput input, 
    section[data-testid="stSidebar"] div[data-baseweb="input"],
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        color: #FFFFFF !important;
        min-height: 40px !important;
    }

    section[data-testid="stSidebar"] .stTextInput input {
        color: #FFFFFF !important;
        background-color: #111827 !important;
        -webkit-text-fill-color: #FFFFFF !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: #FFFFFF !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
    }

    section[data-testid="stSidebar"] .stTextInput input:focus, 
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
        background-color: #1E293B !important;
    }

    /* Sidebar Action Buttons */
    section[data-testid="stSidebar"] div.stButton > button {
        background-color: #1E293B;
        color: #E2E8F0;
        border: 1px solid #334155;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.85rem;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] div.stButton > button:hover {
        background-color: #334155;
        border-color: #475569;
        color: #FFFFFF;
    }

    /* Chat Messages Container */
    div[data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: none !important;
        padding: 1.2rem 0 !important;
        margin: 0 !important;
        border-bottom: 1px solid #E2E8F0 !important;
    }

    div[data-testid="stChatMessage"] p {
        font-size: 0.98rem !important;
        line-height: 1.65 !important;
        color: #1E293B !important;
    }

    /* Expanders & Code blocks */
    div[data-testid="stExpander"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
    }

    pre {
        background-color: #F1F5F9 !important;
        border-radius: 8px !important;
        border: 1px solid #E2E8F0 !important;
    }
    
    pre code {
        color: #0F172A !important;
    }

    hr {
        border-color: #E2E8F0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Header with Professional Logo & Brand Name
# ---------------------------------------------------------

st.markdown(
    """
    <div class="console-header-container">
        <div class="console-logo-box">⚡</div>
        <div class="console-title">Nexus AI </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="console-subtitle">'
    "Enterprise-grade system prompt engineering workspace with multi-turn context and real-time validation."
    "</div>",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# Sidebar — Branding & Configuration
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="sidebar-logo-icon">⚡</div>
            <div class="sidebar-brand-text">Nexus Workspace</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.header("Prompt Parameters")

    role = st.text_input(
        "Role",
        value="a professional AI engineering assistant",
    )

    tone = st.selectbox(
        "Tone",
        options=[
            "Professional",
            "Technical",
            "Friendly",
            "Concise",
            "Formal",
        ],
    )

    response_style = st.selectbox(
        "Response Style",
        options=[
            "clear and concise",
            "detailed and structured",
            "short and direct",
            "step-by-step",
        ],
    )

    output_format = st.selectbox(
        "Output Format",
        options=[
            "Plain Text",
            "Markdown",
            "Strict JSON",
        ],
    )

    safety_level = st.selectbox(
        "Safety Level",
        options=[
            "Standard",
            "Strict",
        ],
    )

    accuracy_level = st.selectbox(
        "Accuracy Level",
        options=[
            "high",
            "very high",
            "maximum",
        ],
    )

    st.divider()
    st.header("Model Settings")

    model = st.selectbox(
        "Model",
        options=[
            "x-ai/grok-4.3",
        ],
    )

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    if st.button("Clear Conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# ---------------------------------------------------------
# Initialize Session State for Chat History
# ---------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------------------------------------------------
# Display Existing Chat History with Professional Avatars
# ---------------------------------------------------------

for message in st.session_state.messages:
    if message["role"] == "user":
        with st.chat_message("user", avatar="💻"):
            st.markdown(message["content"])
    else:
        with st.chat_message("assistant", avatar="⚡"):
            st.markdown(message["content"])


# ---------------------------------------------------------
# Chat Input
# ---------------------------------------------------------

user_prompt = st.chat_input("Message Nexus AI Console...")

if user_prompt:

    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user", avatar="💻"):
        st.markdown(user_prompt)

    try:
        with st.spinner("Generating response..."):
            
            system_messages = build_messages(
                user_prompt=user_prompt,
                role=role,
                tone=tone,
                response_style=response_style,
                output_format=output_format,
                safety_level=safety_level,
                accuracy_level=accuracy_level,
            )
            
            system_prompt_content = system_messages[0]["content"]

            full_payload = [{"role": "system", "content": system_prompt_content}]
            for msg in st.session_state.messages:
                full_payload.append({"role": msg["role"], "content": msg["content"]})

            response = generate_response(
                messages=full_payload,
                model=model,
            )

        st.session_state.messages.append({"role": "assistant", "content": response})

        with st.chat_message("assistant", avatar="⚡"):
            if output_format == "Strict JSON":
                valid, parsed_response, error = validate_llm_response(response)
                if valid:
                    st.success("JSON validation passed.")
                    st.json(parsed_response.model_dump())
                else:
                    st.error("JSON validation failed.")
                    st.code(response, language="json")
            elif output_format == "Markdown":
                st.markdown(response)
            else:
                st.write(response)

    except RuntimeError as error:
        st.error(f"API request failed: {error}")
    except ValueError as error:
        st.error(f"Configuration error: {error}")
    except Exception as error:
        st.error(f"Unexpected error: {error}")