import smtplib
from email.mime.text import MIMEText

import streamlit as st
from google import genai
from google.genai import types

from prompts import (
    SYSTEM_PROMPT,
    WELCOME_MESSAGE_TEMPLATE,
    SUMMARY_REQUEST_PROMPT,
)

# ---------------- CONFIG ---------------- #

MODEL_NAME = "gemini-3.5-flash-lites" 

st.set_page_config(
    page_title="CareerLens AI",
    page_icon="🎯",
)

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GMAIL_EMAIL = st.secrets["GMAIL_EMAIL"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]


# ---------------- CLIENTS ---------------- #

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=GEMINI_API_KEY)


gemini_client = get_gemini_client()


# ---------------- EMAIL ---------------- #

def send_email(to_email, subject, body):
    try:
        msg = MIMEText(body)

        msg["Subject"] = subject
        msg["From"] = GMAIL_EMAIL
        msg["To"] = to_email

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                GMAIL_EMAIL,
                GMAIL_APP_PASSWORD,
            )
            server.send_message(msg)

        return True, "Email Sent"

    except Exception as error:
        return False, str(error)


# ---------------- CHAT HELPERS ---------------- #

def render_message(message):
    with st.chat_message(message["role"]):

        if message["kind"] == "text":
            st.write(message["content"])

        elif message["kind"] == "image":
            st.image(message["content"])


def add_message(role, kind, content):

    st.session_state.messages.append(
        {
            "role": role,
            "kind": kind,
            "content": content,
        }
    )

    render_message(st.session_state.messages[-1])


def ask_gemini(parts):

    try:

        response = st.session_state.chat.send_message(
            parts
        )

        return response.text

    except Exception as error:

        return f"❌ Error: {error}"


# ---------------- ONBOARDING ---------------- #

if "onboarded" not in st.session_state:

    st.title("🎯 CareerLens AI")

    st.caption(
        "Upload. Analyze. Prepare. Get Hired."
    )

    with st.form("onboarding_form"):

        name = st.text_input(
            "👤 Your Name"
        )

        email = st.text_input(
            "📧 Email Address",
            placeholder="yourname@gmail.com",
        )

        submitted = st.form_submit_button(
            "Let's Go 🚀"
        )

    if submitted:

        if not name.strip() or not email.strip():

            st.warning(
                "Please enter name and email."
            )

        else:

            st.session_state.name = name.strip()
            st.session_state.email = email.strip()

            st.session_state.chat = (
                gemini_client.chats.create(
                    model=MODEL_NAME,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_PROMPT
                    ),
                )
            )

            st.session_state.messages = []
            st.session_state.onboarded = True

            st.rerun()

    st.stop()


# ---------------- HEADER ---------------- #

header_col, button_col = st.columns(
    [5, 2]
)

with header_col:

    st.title("🎯 CareerLens AI")

with button_col:

    send_disabled = (
        len(st.session_state.messages) <= 1
    )

    if st.button(
        "📧 Send Report",
        disabled=send_disabled,
        use_container_width=True,
    ):

        with st.spinner(
            "Preparing report..."
        ):

            summary = ask_gemini(
                [SUMMARY_REQUEST_PROMPT]
            )

        success, info = send_email(
            st.session_state.email,
            "🎯 CareerLens AI Report",
            summary,
        )

        if success:

            st.success(
                "📧 Report sent successfully!"
            )

        else:

            st.error(
                f"Failed to send email: {info}"
            )


st.caption(
    f"👤 {st.session_state.name} | 📧 {st.session_state.email}"
)


# ---------------- WELCOME ---------------- #

if not st.session_state.messages:

    add_message(
        "assistant",
        "text",
        WELCOME_MESSAGE_TEMPLATE.format(
            name=st.session_state.name
        ),
    )

else:

    for message in st.session_state.messages:

        render_message(message)


# ---------------- INPUT ---------------- #

user_input = st.chat_input(
    "📄 Upload Resume, Job Description, Internship Posting or Placement Notice",
    accept_file=True,
    file_type=["jpg", "jpeg", "png"],
)


# ---------------- ANALYSIS ---------------- #

if user_input:

    parts = []

    uploaded_file = (
        user_input.files[0]
        if user_input.files
        else None
    )

    text = user_input.text

    if uploaded_file:

        image_bytes = uploaded_file.getvalue()

        add_message(
            "user",
            "image",
            image_bytes,
        )

        parts.append(
            types.Part.from_bytes(
                data=image_bytes,
                mime_type=uploaded_file.type,
            )
        )

    if text:

        add_message(
            "user",
            "text",
            text,
        )

        parts.append(text)

    elif uploaded_file:

        parts.append(
            """
Analyze this document.

Provide:

📌 Document Type

🎯 Role Name

🛠 Required Skills

📈 Missing Skills

✅ Eligibility Criteria

❓ Interview Questions

📅 30-Day Preparation Plan

💡 Career Advice
"""
        )

    with st.spinner(
        "🔍 Analyzing document..."
    ):

        answer = ask_gemini(parts)

    add_message(
        "assistant",
        "text",
        answer,
    )