import re
import requests
import datetime
import streamlit as st
from functionality.conversation_functionality import evaluate_lead_with_groq

API_URL = "http://localhost:8000/conversations/lead"

st.set_page_config(page_title="Lead Representative Chat", layout="centered")
st.title("💬 Chat with AI - Representative")

# Chat bubble styles
st.markdown("""
<style>
.chat-message {
    padding: 0.5rem 1rem;
    margin: 0.5rem 0;
    border-radius: 1rem;
    max-width: 80%;
    word-wrap: break-word;
    clear: both;
    color: black;
    font-size: 1rem;
    line-height: 1.5;
}
.user {
    background-color: #DCF8C6;
    float: right;
    text-align: right;
}
.assistant {
    background-color: #F1F0F0;
    float: left;
    text-align: left;
}
</style>
""", unsafe_allow_html=True)

if st.button("🔄 Start Fresh Chat"):
    st.session_state.chat_history = []
    st.session_state.step = "email"
    st.session_state.email = ""
    st.session_state.company_name = ""
    st.session_state.chat_input = ""
    st.rerun()

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "step" not in st.session_state:
    st.session_state.step = "email"  # email -> company -> question

if "email" not in st.session_state:
    st.session_state.email = ""

if "company_name" not in st.session_state:
    st.session_state.company_name = ""

# Initial assistant prompt
if len(st.session_state.chat_history) == 0 and st.session_state.step == "email":
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": "👋 Hi! Let's qualify your lead. First, can you provide your email address?"
    })

# Display chat
for msg in st.session_state.chat_history:
    role_class = "user" if msg["role"] == "user" else "assistant"
    st.markdown(
        f"<div class='chat-message {role_class}'>{msg['content']}</div><div style='clear: both'></div>",
        unsafe_allow_html=True
    )

# Input form (clears after submit)
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Your response", key="chat_input")
    submitted = st.form_submit_button("Send")

# Process input after submission
if submitted and user_input.strip():
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    if st.session_state.step == "email":
        email = user_input.strip()
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$"
        if re.match(email_pattern, email):
            st.session_state.email = email
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Great! What's your company name?"
            })
            st.session_state.step = "company"
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "❗ That doesn't look like a valid email address. Please enter a valid email."
            })

    elif st.session_state.step == "company":
        company_name = user_input.strip()
        if re.match(r'^[A-Za-z0-9\s&\-\.]+$', company_name):
            st.session_state.company_name = company_name
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "Thanks! Now tell me a bit about your project or what you're looking for."
            })
            st.session_state.step = "question"
        else:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": "❗ Company name should not contain special characters. Please enter a valid company name (only letters, numbers, spaces, &, -, . allowed)."
            })

    elif st.session_state.step == "question":
        # Collect user messages only
        conversation_parts = [msg["content"] for msg in st.session_state.chat_history if msg["role"] == "user"]
        conversation = "\n".join(conversation_parts).strip()

        payload = {
            "email": st.session_state.email,
            "company_name": st.session_state.company_name,
            "conversation": conversation
        }

        # try:
        #     res = requests.post(API_URL, json=payload)
        #     if res.status_code == 200:
        #         data = res.json()
        #         relevance = data.get("lead_relevance", "unknown").capitalize()
        #         message = data.get("message", "")
        #         timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        #         response_msg = f"🕓 {timestamp}\n\n**Lead Relevance:** {relevance}"
        #         if message:
        #             response_msg += f"\n\n{message}"

        #         st.session_state.chat_history.append({"role": "assistant", "content": response_msg})
        #     else:
        #         st.session_state.chat_history.append({
        #             "role": "assistant",
        #             "content": "❌ Server error occurred while classifying the lead."
        #         })

        # except Exception as e:
        #     st.session_state.chat_history.append({
        #         "role": "assistant",
        #         "content": f"⚠️ Request failed: {str(e)}"
        #     })

        try:
            relevance, message = evaluate_lead_with_groq(conversation)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

            response_msg = f"🕓 {timestamp}\n\n**Lead Relevance:** {relevance.capitalize()}"
            if message:
                response_msg += f"\n\n{message}"

            st.session_state.chat_history.append({"role": "assistant", "content": response_msg})
        except Exception as e:
            st.session_state.chat_history.append({
                "role": "assistant",
                "content": f"⚠️ Failed to evaluate lead locally: {str(e)}"
            })


        # Reset flow after classification
        st.session_state.step = "email"
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": "Would you like to analyze another lead? Please enter a new email address."
        })

    st.rerun()
