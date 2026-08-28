import streamlit as st
import re
from datetime import datetime


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Rule-Based AI Chatbot",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #777777;
        margin-bottom: 25px;
    }

    .chat-user {
        background-color: #e8f0fe;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
    }

    .chat-bot {
        background-color: #f1f3f4;
        padding: 12px 16px;
        border-radius: 15px;
        margin: 8px 0;
    }

    .status-box {
        padding: 12px;
        border-radius: 10px;
        background-color: #eef7ee;
        border: 1px solid #c8e6c9;
    }

    .info-card {
        padding: 18px;
        border-radius: 12px;
        border: 1px solid #dddddd;
        margin-bottom: 12px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# CHATBOT RESPONSE RULES
# ============================================================

RULES = {

    "greeting": {
        "patterns": [
            r"\bhello\b",
            r"\bhi\b",
            r"\bhey\b",
            r"\bhiya\b",
            r"\bgreetings\b"
        ],
        "responses": [
            "Hello! 👋 How can I help you today?",
            "Hi there! 🤖 What would you like to know?",
            "Hey! Welcome to the Rule-Based AI Chatbot."
        ]
    },

    "how_are_you": {
        "patterns": [
            r"how are you",
            r"how do you feel",
            r"are you fine",
            r"are you doing well"
        ],
        "responses": [
            "I'm doing great! Thanks for asking. 😊",
            "I'm ready to help you!",
            "I'm functioning perfectly and ready for your questions."
        ]
    },

    "name": {
        "patterns": [
            r"what is your name",
            r"who are you",
            r"your name",
            r"tell me about yourself"
        ],
        "responses": [
            "I am a Rule-Based AI Chatbot.",
            "I'm a chatbot built using Python and predefined rules.",
            "I'm a simple conversational AI application."
        ]
    },

    "purpose": {
        "patterns": [
            r"what can you do",
            r"what do you do",
            r"your purpose",
            r"what are your features"
        ],
        "responses": [
            "I can respond to predefined questions and conversational patterns.",
            "I can handle greetings, basic questions, help requests and simple conversations.",
            "I identify user inputs using pattern matching and select an appropriate response."
        ]
    },

    "python": {
        "patterns": [
            r"what is python",
            r"tell me about python",
            r"python language",
            r"python"
        ],
        "responses": [
            "Python is a high-level programming language known for its simple syntax and wide use in AI, data science and web development."
        ]
    },

    "ai": {
        "patterns": [
            r"what is ai",
            r"what is artificial intelligence",
            r"tell me about ai",
            r"artificial intelligence"
        ],
        "responses": [
            "Artificial Intelligence is the field of creating systems that can perform tasks that normally require human-like intelligence."
        ]
    },

    "rule_based": {
        "patterns": [
            r"what is rule based",
            r"what is a rule based chatbot",
            r"how does this chatbot work",
            r"how do you work"
        ],
        "responses": [
            "I work using predefined rules and pattern matching. Your input is compared with known patterns and the matching response is selected."
        ]
    },

    "help": {
        "patterns": [
            r"\bhelp\b",
            r"help me",
            r"what can i ask",
            r"commands"
        ],
        "responses": [
            "You can ask me about my name, purpose, Python, AI, rule-based chatbots, or simply say hello!"
        ]
    },

    "thanks": {
        "patterns": [
            r"thank you",
            r"thanks",
            r"thank u",
            r"thx"
        ],
        "responses": [
            "You're welcome! 😊",
            "Happy to help!",
            "You're welcome. Feel free to ask another question."
        ]
    },

    "goodbye": {
        "patterns": [
            r"\bbye\b",
            r"goodbye",
            r"see you",
            r"exit",
            r"quit"
        ],
        "responses": [
            "Goodbye! 👋 Have a great day!",
            "See you later!",
            "Thanks for chatting with me!"
        ]
    }
}


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "matched_questions" not in st.session_state:
    st.session_state.matched_questions = 0

if "start_time" not in st.session_state:
    st.session_state.start_time = datetime.now()


# ============================================================
# CHATBOT ENGINE
# ============================================================

def clean_text(text):
    """
    Cleans and normalizes user input.
    """
    text = text.lower().strip()
    text = re.sub(r"\s+", " ", text)
    return text


def find_intent(user_input):
    """
    Searches all predefined patterns and returns
    the matching intent.
    """

    cleaned_input = clean_text(user_input)

    for intent, data in RULES.items():

        for pattern in data["patterns"]:

            if re.search(pattern, cleaned_input):
                return intent

    return None


def generate_response(user_input):
    """
    Generates a response using the rule-based system.
    """

    intent = find_intent(user_input)

    if intent is None:
        return (
            "I'm sorry, I don't understand that yet. 🤔 "
            "Try asking about Python, AI, my purpose, or type 'help'."
        )

    responses = RULES[intent]["responses"]

    # Select response based on current message count
    index = st.session_state.total_questions % len(responses)

    return responses[index]


def process_message(user_input):
    """
    Processes a complete user message.
    """

    if not user_input.strip():
        return

    st.session_state.total_questions += 1

    intent = find_intent(user_input)

    if intent is not None:
        st.session_state.matched_questions += 1

    response = generate_response(user_input)

    current_time = datetime.now().strftime("%H:%M")

    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "time": current_time
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "time": current_time
    })


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("🤖 Chatbot Controls")

    st.markdown("""
    ### About

    This is a **rule-based chatbot** built using Python.

    It does not use an external AI API. Instead, it uses:

    - Predefined rules
    - Pattern matching
    - Conditional logic
    - Regular expressions
    """)

    st.divider()

    st.subheader("📊 Statistics")

    st.metric(
        "Questions Asked",
        st.session_state.total_questions
    )

    st.metric(
        "Recognized Inputs",
        st.session_state.matched_questions
    )

    if st.session_state.total_questions > 0:

        accuracy = (
            st.session_state.matched_questions
            / st.session_state.total_questions
        ) * 100

        st.metric(
            "Rule Match Rate",
            f"{accuracy:.0f}%"
        )

    st.divider()

    st.subheader("⚡ Quick Questions")

    quick_questions = [
        "Hello",
        "What is your name?",
        "What can you do?",
        "What is Python?",
        "What is AI?",
        "How does this chatbot work?",
        "Help"
    ]

    for question in quick_questions:

        if st.button(
            question,
            use_container_width=True
        ):
            process_message(question)
            st.rerun()

    st.divider()

    if st.button(
        "🗑️ Clear Conversation",
        use_container_width=True
    ):

        st.session_state.messages = []
        st.session_state.total_questions = 0
        st.session_state.matched_questions = 0

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🤖 Rule-Based AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'A Python chatbot that understands user inputs using predefined rules and pattern matching.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# STATUS
# ============================================================

st.markdown(
    """
    <div class="status-box">
    🟢 <b>Chatbot Status:</b> Online &nbsp; | &nbsp;
    ⚙️ <b>Mode:</b> Rule-Based &nbsp; | &nbsp;
    🧠 <b>External API:</b> Not Required
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# CHAT DISPLAY
# ============================================================

if not st.session_state.messages:

    st.info(
        "👋 Welcome! Start a conversation below. "
        "Try saying **hello** or asking **what can you do?**"
    )

else:

    for message in st.session_state.messages:

        if message["role"] == "user":

            st.markdown(
                f"""
                <div class="chat-user">
                    👤 <b>You</b> &nbsp;
                    <small>{message["time"]}</small>
                    <br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="chat-bot">
                    🤖 <b>Bot</b> &nbsp;
                    <small>{message["time"]}</small>
                    <br>
                    {message["content"]}
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Type your message here..."
)

if user_input:

    process_message(user_input)

    st.rerun()


# ============================================================
# PROJECT INFORMATION
# ============================================================

with st.expander("📚 How this chatbot works"):

    st.markdown("""
    ### Processing Flow

    **1. User Input**

    The user enters a natural-language message.

    **2. Text Cleaning**

    The application converts the input to lowercase
    and removes unnecessary spaces.

    **3. Pattern Matching**

    The input is compared against predefined patterns
    using regular expressions.

    **4. Intent Detection**

    A matching intent is identified.

    **5. Response Selection**

    The chatbot selects an appropriate predefined response.

    **6. Response Display**

    The response is displayed in the conversation window.

    ### Example

    ```text
    User:
    What is Python?

            ↓

    Text Cleaning

            ↓

    Pattern Matching

            ↓

    Python Intent Detected

            ↓

    Predefined Response

            ↓

    Bot:
    Python is a high-level programming language...
    ```
    """)


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "Task 1 — Chatbot with Rule-Based Responses | "
    "Built with Python & Streamlit"
)
