# pages/ai_chat.py
import streamlit as st
import time
from utils.llama_api import ask_llama
from utils.theme_injector import apply_global_styles

st.set_page_config(layout="wide", page_title="AI Career Assistant")

# Apply the global app-wide luxury alabaster light theme styles
apply_global_styles()

# Premium styling to replicate the exact soft ivory lighting & reflections from your image
st.markdown("""
<style>
    /* Exact replication of your uploaded luxury cream/ivory background and natural light caustic play */
    
    /* Elegant floating white cards with clean borders and subtle soft-shadows */
    .chat-card {
        background: #ffffff !important;
        border-radius: 12px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        border: 1px solid rgba(230, 223, 217, 0.8) !important;
        box-shadow: 0 4px 20px rgba(44, 37, 35, 0.02) !important;
    }
    
    .user-tag { 
        color: #8c7a6b !important; 
        font-weight: 700; 
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .ai-tag { 
        color: #2c2523 !important; 
        font-weight: 700; 
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Luxury Typing Indicator Container matching the ivory palette */
    .typing-container {
        display: flex;
        align-items: center;
        gap: 5px;
        padding: 10px 14px;
        background: #f4efeb;
        border-radius: 8px;
        width: fit-content;
        margin-top: 8px;
    }
    
    .typing-dot {
        width: 6px;
        height: 6px;
        background: #8c7a6b; /* Luxury Warm Taupe accent */
        border-radius: 50%;
        animation: pulse 1.4s infinite ease-in-out both;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }

    @keyframes pulse {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1.0); }
    }
</style>
""", unsafe_allow_html=True)

st.title("🤖 AI Career Assistant")
st.caption("Gain professional advice, resume critique, and job-market preparation assistance instantly.")

# Interactive Suggested Prompts chips
col_p1, col_p2, col_p3 = st.columns(3)
with col_p1:
    if st.button("💡 Core Resume Tips", use_container_width=True):
        st.session_state.temp_prompt = "Provide 3 high-impact strategies to make my resume stand out."
        st.rerun()
with col_p2:
    if st.button("📈 System Design Guide", use_container_width=True):
        st.session_state.temp_prompt = "What are the key points to cover in a Senior System Design interview?"
        st.rerun()
with col_p3:
    if st.button("🤝 Negotiating Salaries", use_container_width=True):
        st.session_state.temp_prompt = "Give me a negotiation script for an engineering offer."
        st.rerun()

if "messages" not in st.session_state:
    st.session_state.messages = []

# 1. Display historical messages inside structured warm-white HTML cards
for msg in st.session_state.messages:
    role_class = "user-tag" if msg["role"] == "user" else "ai-tag"
    role_name = "👤 You" if msg["role"] == "user" else "🤖 Career AI"
    
    st.markdown(f"""
    <div class="chat-card">
        <span class="{role_class}">{role_name}</span>
        <div style="margin-top: 8px; line-height: 1.6; color:#2c2523; font-size:0.95rem;">
            {msg["content"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

# 2. Handle new inputs (either typed or chosen from suggestions)
initial_prompt = st.session_state.pop("temp_prompt", "")
user_input = st.chat_input("Ask about jobs, skills, resumes...")

active_input = user_input or initial_prompt

if active_input:
    # Print the user's message inside a custom card instantly
    st.session_state.messages.append({"role": "user", "content": active_input})
    st.markdown(f"""
    <div class="chat-card">
        <span class="user-tag">👤 You</span>
        <div style="margin-top: 8px; line-height: 1.6; color:#2c2523; font-size:0.95rem;">
            {active_input}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Establish placeholder container for real-time streaming inside a custom card
    assistant_placeholder = st.empty()
    
    # Display the luxury animated typing loader inside the card first
    assistant_placeholder.markdown(f"""
    <div class="chat-card">
        <span class="ai-tag">🤖 Career AI</span>
        <div class="typing-container">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Fetch response from API / Router
    response = ask_llama(active_input)

    # Fluidly stream words inside the elegant custom HTML card wrapper
    accrued_text = ""
    for word in response.split(" "):
        accrued_text += word + " "
        assistant_placeholder.markdown(f"""
        <div class="chat-card">
            <span class="ai-tag">🤖 Career AI</span>
            <div style="margin-top: 8px; line-height: 1.6; color:#2c2523; font-size:0.95rem;">
                {accrued_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.04) # Perfect, natural human typing cadence

    # Commit message to state and refresh to align with the main render loop cleanly
    st.session_state.messages.append({"role": "assistant", "content": accrued_text})
    st.rerun()