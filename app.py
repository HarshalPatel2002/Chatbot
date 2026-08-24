import uuid
import streamlit as st
from langchain_core.messages import HumanMessage
from langgraph_chatboat import chatbot


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Chatbot",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM FUTURISTIC CSS & STYLING SYSTEM
# ============================================================


def inject_custom_css():
    css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* COLOR SYSTEM & DESIGN VARIABLES */
        :root {
            --bg-base: #030509;
            --bg-surface: rgba(10, 15, 26, 0.75);
            --bg-card-user: linear-gradient(135deg, rgba(30, 41, 67, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%);
            --bg-card-ai: rgba(13, 19, 33, 0.7);
            
            --accent-cyan: #38BDF8;
            --accent-blue: #6366F1;
            --accent-violet: #8B5CF6;
            --accent-purple: #D946EF;
            --accent-saffron: #FF9933;
            --accent-gold: #F4C46B;
            
            --border-glow: rgba(56, 189, 248, 0.25);
            --border-subtle: rgba(255, 255, 255, 0.08);
            --border-highlight: rgba(139, 92, 246, 0.35);
            
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --text-muted: #64748B;
            
            --glow-primary: rgba(56, 189, 248, 0.15);
            --glow-secondary: rgba(139, 92, 246, 0.15);
        }

        /* GLOBAL STYLES & BACKGROUND EFFECT */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: var(--bg-base) !important;
            color: var(--text-primary);
            font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
            background-image: 
                radial-gradient(circle at 50% -10%, rgba(56, 189, 248, 0.12) 0%, transparent 60%),
                radial-gradient(circle at 85% 40%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
                radial-gradient(circle at 15% 75%, rgba(217, 70, 239, 0.05) 0%, transparent 45%),
                linear-gradient(rgba(255, 255, 255, 0.015) 1px, transparent 1px),
                linear-gradient(90deg, rgba(255, 255, 255, 0.015) 1px, transparent 1px);
            background-size: 100% 100%, 100% 100%, 100% 100%, 40px 40px, 40px 40px;
            background-attachment: fixed;
        }

        /* HIDE DEFAULT STREAMLIT HEADERS & FOOTERS */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        footer {
            visibility: hidden;
        }

        /* MAIN CONTENT CONTAINER */
        .block-container {
            max-width: 880px !important;
            padding-top: 1.8rem !important;
            padding-bottom: 7rem !important;
        }

        /* SIDEBAR FUTURISTIC STYLING */
        section[data-testid="stSidebar"] {
            background-color: var(--bg-surface) !important;
            border-right: 1px solid var(--border-subtle) !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 10px 0 40px rgba(0, 0, 0, 0.6);
        }

        /* SIDEBAR BRAND HEADER */
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 10px 4px 20px 4px;
            border-bottom: 1px solid var(--border-subtle);
            margin-bottom: 22px;
        }
        .brand-core {
            position: relative;
            width: 42px;
            height: 42px;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet));
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 0 20px rgba(56, 189, 248, 0.4);
        }
        .brand-core::after {
            content: "💬";
            font-size: 20px;
        }
        .brand-text-title {
            font-size: 1.25rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            background: linear-gradient(90deg, #FFFFFF 0%, #38BDF8 50%, #C084FC 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .brand-text-sub {
            font-size: 0.72rem;
            color: var(--text-muted);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            font-weight: 500;
        }

        /* SIDEBAR BUTTONS */
        div[data-testid="stSidebar"] .stButton > button {
            background-color: rgba(255, 255, 255, 0.02) !important;
            color: var(--text-secondary) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 12px !important;
            padding: 10px 14px !important;
            font-size: 0.88rem !important;
            font-weight: 500 !important;
            text-align: left !important;
            transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        div[data-testid="stSidebar"] .stButton > button:hover {
            color: var(--text-primary) !important;
            background-color: rgba(56, 189, 248, 0.08) !important;
            border-color: rgba(56, 189, 248, 0.35) !important;
            transform: translateX(3px);
            box-shadow: 0 4px 15px rgba(56, 189, 248, 0.1);
        }

        /* NEW CHAT BUTTON ACCENT */
        div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type > button {
            background: linear-gradient(135deg, rgba(56, 189, 248, 0.2) 0%, rgba(139, 92, 246, 0.25) 100%) !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(56, 189, 248, 0.45) !important;
            box-shadow: 0 4px 20px rgba(56, 189, 248, 0.2) !important;
            font-weight: 600 !important;
        }
        div[data-testid="stSidebar"] div[data-testid="stButton"]:first-of-type > button:hover {
            border-color: var(--accent-cyan) !important;
            box-shadow: 0 4px 25px rgba(56, 189, 248, 0.4) !important;
            transform: translateY(-1px);
        }

        /* WELCOME / EMPTY STATE SCREEN */
        .empty-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 60px 20px 40px 20px;
            animation: fadeIn 0.8s ease-out;
        }
        .orb-wrapper {
            position: relative;
            width: 100px;
            height: 100px;
            margin-bottom: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .orb-core {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: radial-gradient(circle at 35% 35%, #38BDF8 0%, #8B5CF6 55%, #FF9933 95%);
            box-shadow: 0 0 50px rgba(56, 189, 248, 0.45), 0 0 20px rgba(255, 153, 51, 0.25), inset 0 0 20px rgba(255, 255, 255, 0.8);
            animation: float 4s ease-in-out infinite;
        }
        .orb-ring {
            position: absolute;
            width: 96px;
            height: 96px;
            border-radius: 50%;
            border: 1.5px solid rgba(56, 189, 248, 0.35);
            border-top-color: rgba(244, 196, 107, 0.5);
            border-bottom-color: rgba(217, 70, 239, 0.35);
            animation: spin 12s linear infinite;
        }
        .welcome-heading {
            font-size: 2.3rem;
            font-weight: 700;
            margin-bottom: 12px;
            color: #F8FAFC;
            letter-spacing: -0.02em;
        }
        .welcome-brand {
            background: linear-gradient(110deg, #FFFFFF 0%, #38BDF8 40%, #C084FC 75%, #F4C46B 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .welcome-divider {
            width: 48px;
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, rgba(244, 196, 107, 0.6) 50%, transparent 100%);
            margin: 4px 0 18px 0;
            border-radius: 2px;
        }
        .empty-subtitle {
            font-size: 0.98rem;
            color: var(--text-secondary);
            max-width: 520px;
            line-height: 1.65;
            font-weight: 400;
        }

        /* CHAT MESSAGE BUBBLES */
        .stChatMessage {
            background-color: transparent !important;
            padding: 14px 0px !important;
            animation: fadeIn 0.4s ease-out;
        }

        div[data-testid="stChatMessageContent"] {
            padding: 20px 24px !important;
            border-radius: 18px !important;
            font-size: 0.98rem !important;
            line-height: 1.7 !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25) !important;
        }

        /* USER BUBBLE */
        div[data-testid="stChatMessage"]:nth-child(even) div[data-testid="stChatMessageContent"] {
            background: var(--bg-card-user) !important;
            border: 1px solid rgba(139, 92, 246, 0.25) !important;
            color: #F8FAFC !important;
            border-top-right-radius: 4px !important;
        }

        /* ASSISTANT BUBBLE */
        div[data-testid="stChatMessage"]:nth-child(odd) div[data-testid="stChatMessageContent"] {
            background: var(--bg-card-ai) !important;
            border: 1px solid var(--border-glow) !important;
            backdrop-filter: blur(16px) !important;
            color: var(--text-primary) !important;
            border-top-left-radius: 4px !important;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4), inset 0 0 15px rgba(56, 189, 248, 0.05) !important;
        }

        /* AI IDENTITY TAG */
        .ai-identity-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--accent-cyan);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .status-dot {
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background-color: var(--accent-cyan);
            box-shadow: 0 0 10px var(--accent-cyan);
        }

        /* CHAT INPUT BAR */
        div[data-testid="stBottom"] {
            background: transparent !important;
            padding-bottom: 20px !important;
            bottom: 0 !important;
        }

        div[data-testid="stBottom"] > div {
            padding-bottom: 0 !important;
        }

        div[data-testid="stChatInput"] {
            max-width: 680px !important;
            margin: 0 auto !important;
            background: rgba(13, 19, 33, 0.95) !important;
            border: 1px solid rgba(56, 189, 248, 0.35) !important;
            border-radius: 28px !important;
            backdrop-filter: blur(24px) !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.6), 0 0 15px rgba(56, 189, 248, 0.15) !important;
            outline: none !important;
            padding: 4px 10px !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }

        div[data-testid="stChatInput"] > div {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }

        div[data-testid="stChatInput"]:focus-within {
            border: 1px solid var(--accent-cyan) !important;
            box-shadow: 0 8px 35px rgba(56, 189, 248, 0.35), 0 0 20px rgba(56, 189, 248, 0.2) !important;
            outline: none !important;
        }

        div[data-testid="stChatInput"] textarea {
            color: var(--text-primary) !important;
            font-size: 0.95rem !important;
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            padding-left: 12px !important;
        }

        div[data-testid="stChatInput"] button {
            border-radius: 50% !important;
            background: linear-gradient(135deg, var(--accent-cyan), var(--accent-violet)) !important;
            color: #FFFFFF !important;
            border: none !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.3) !important;
        }

        /* CODE BLOCKS */
        code {
            font-family: 'JetBrains Mono', monospace !important;
            background: rgba(0, 0, 0, 0.45) !important;
            border: 1px solid var(--border-subtle) !important;
            border-radius: 6px !important;
            padding: 2px 6px !important;
            color: var(--accent-cyan) !important;
        }
        pre code {
            padding: 14px !important;
            display: block !important;
            color: #E2E8F0 !important;
            border-radius: 12px !important;
        }

        /* ANIMATIONS */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(8px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }
        @keyframes spin {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================
# BACKEND FUNCTIONS & STATE MANAGEMENT
# ============================================================


def generate_thread_id():
    return uuid.uuid4()


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    st.session_state["message_history"] = []


def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)


def load_conversation(thread_id):
    return chatbot.get_state(
        config={"configurable": {"thread_id": thread_id}}
    ).values.get("messages", [])


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = []

if "chat_titles" not in st.session_state:
    st.session_state["chat_titles"] = {}

# Apply UI CSS Injection
inject_custom_css()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-brand">
        <div class="brand-core"></div>
        <div>
            <div class="brand-text-title">Chatbot</div>
            <div class="brand-text-sub">AI Assistant</div>
        </div>
    </div>
""",
    unsafe_allow_html=True,
)

if st.sidebar.button("+ New Conversation", use_container_width=True):
    reset_chat()
    st.rerun()

st.sidebar.markdown(
    "<div style='margin-top: 24px; margin-bottom: 10px; font-size: 0.7rem; font-weight: 700; color: #475569; letter-spacing: 0.1em; text-transform: uppercase;'>Conversation History</div>",
    unsafe_allow_html=True,
)

switch_thread_to = None

for thread_id in st.session_state["chat_threads"][::-1]:
    title = st.session_state["chat_titles"].get(thread_id, "New Chat")
    is_active = thread_id == st.session_state["thread_id"]
    prefix = "• " if is_active else "◦ "
    button_label = f"{prefix} {title}"

    if st.sidebar.button(
        button_label, key=str(thread_id), use_container_width=True
    ):
        switch_thread_to = thread_id

if switch_thread_to:
    st.session_state["thread_id"] = switch_thread_to
    messages = load_conversation(switch_thread_to)

    temp_messages = []
    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        else:
            role = "assistant"

        temp_messages.append({"role": role, "content": msg.content})

    st.session_state["message_history"] = temp_messages
    st.rerun()


# ============================================================
# CONFIGURATION
# ============================================================

CONFIG = {"configurable": {"thread_id": st.session_state["thread_id"]}}


# ============================================================
# MAIN CHAT & STREAMING INTERFACE
# ============================================================

# RENDER WELCOME SCREEN ONLY IF NO MESSAGES IN CURRENT SESSION
if len(st.session_state["message_history"]) == 0:
    st.markdown(
        """
        <div class="empty-container">
            <div class="orb-wrapper">
                <div class="orb-ring"></div>
                <div class="orb-core"></div>
            </div>
            <div class="welcome-heading">
                Welcome to <span class="welcome-brand">Chatbot</span>
            </div>
            <div class="welcome-divider"></div>
            <div class="empty-subtitle">
                Your AI assistant is ready. Ask anything, explore ideas, solve problems, or build something amazing.
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )
else:
    # RENDER CHAT HISTORY WHEN MESSAGES EXIST
    for message in st.session_state["message_history"]:
        if message["role"] == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(
                    '<div class="ai-identity-tag"><span class="status-dot"></span> Chatbot</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(message["content"])

# USER CHAT INPUT COMPONENT
user_input = st.chat_input("Ask anything...")

if user_input:
    thread_id = st.session_state["thread_id"]
    is_first_message = thread_id not in st.session_state["chat_threads"]

    # Register thread if new session
    if is_first_message:
        add_thread(thread_id)

    # Set smart conversation title from first question
    if thread_id not in st.session_state["chat_titles"]:
        title = user_input.strip().replace("\n", " ")
        if len(title) > 20:
            title = title[:20] + "..."
        st.session_state["chat_titles"][thread_id] = title

    # Record User Message
    st.session_state["message_history"].append(
        {"role": "user", "content": user_input}
    )

    # RERUN TO HIDE WELCOME SCREEN IMMEDIATELY UPON FIRST QUESTION
    st.rerun()

# AFTER RERUN: STREAM ASSISTANT RESPONSE IF LAST MESSAGE IS USER
if (
    len(st.session_state["message_history"]) > 0
    and st.session_state["message_history"][-1]["role"] == "user"
):

    latest_user_input = st.session_state["message_history"][-1]["content"]

    # Stream & Display Assistant Message from LangGraph
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(
            '<div class="ai-identity-tag"><span class="status-dot"></span> Chatbot</div>',
            unsafe_allow_html=True,
        )

        ai_message = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=latest_user_input)]},
                config=CONFIG,
                stream_mode="messages",
            )
        )

    # Record Assistant Message
    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
    st.rerun()
