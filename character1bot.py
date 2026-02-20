import streamlit as st
import ollama
import time
from PIL import Image, ImageDraw, ImageFont
import random
import requests
from io import BytesIO

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Shinchan Ultimate Fun AI", layout="wide")

# -----------------------------
# ANIMATED CSS + CHAT COLORS
# -----------------------------
st.markdown("""
<style>
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}

body {
    background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1, #fffa65, #4bcffa);
    background-size: 400% 400%;
    animation: gradientBG 15s ease infinite;
}

.title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #ff3c78;
    animation: pulse 2s infinite;
    text-shadow: 2px 2px #fff;
}

@keyframes pulse {
    0% { transform: scale(1); }
    50% { transform: scale(1.08); }
    100% { transform: scale(1); }
}

.card {
    background-color: rgba(255,255,255,0.9);
    padding: 20px;
    border-radius: 25px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    transition: transform 0.3s;
    text-align:center;
    font-weight:bold;
    font-size:18px;
}

.card:hover {
    transform: scale(1.07);
}

.floating-emoji {
    position: fixed;
    font-size: 30px;
    animation: float 4s infinite;
    pointer-events: none;
}

@keyframes float {
    0% { transform: translateY(0px); opacity: 1;}
    50% { transform: translateY(-50px); opacity: 0.7;}
    100% { transform: translateY(0px); opacity: 1;}
}

/* USER CHAT BUBBLE */
div[data-testid="stChatMessage"][data-user="true"] > div {
    background-color: #ffd966 !important;
    color: #000000 !important;
    border-radius: 20px !important;
    padding: 10px !important;
    font-weight: bold;
    font-size: 18px;
}

/* ASSISTANT CHAT BUBBLE */
div[data-testid="stChatMessage"][data-user="false"] > div {
    background-color: #ff6f91 !important;
    color: #ffffff !important;
    border-radius: 20px !important;
    padding: 10px !important;
    font-weight: bold;
    font-size: 18px;
}

/* INPUT BOX COLOR */
.css-18e3th9 input {
    background-color: #fff3b0 !important;
    color: #000000 !important;
    font-weight: bold;
    font-size: 18px;
    border-radius: 15px !important;
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FLOATING EMOJIS
# -----------------------------
emojis = ["😂","🎉","🍭","🍕","🧸","🌈","⭐","🤪"]
for i in range(8):
    left = random.randint(5,85)
    st.markdown(f'<div class="floating-emoji" style="left:{left}vw;">{random.choice(emojis)}</div>', unsafe_allow_html=True)

# -----------------------------
# SHINCHAN IMAGE
# -----------------------------
try:
    url = "https://upload.wikimedia.org/wikipedia/en/7/70/Shinnosuke_Nohara.png"
    response = requests.get(url)
    shinchan_img = Image.open(BytesIO(response.content))
    st.image(shinchan_img, width=200, caption="Shinchan 😎")
except:
    st.write("🖼 Shinchan image could not load. Check your internet connection.")

# -----------------------------
# TITLE
# -----------------------------
st.markdown('<div class="title">🎭 Shinchan Ultimate Fun AI</div>', unsafe_allow_html=True)
st.write("💬 Chat • 😂 Meme • 🎈 XP & Fun • 🌈 Colorful World")

# -----------------------------
# SIDEBAR SETTINGS
# -----------------------------
st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider("🔥 Shinchan Mischief Level", 0.0, 1.5, 0.9, 0.1)

if st.sidebar.button("🧹 Clear Chat & XP"):
    st.session_state.messages = []
    st.session_state.xp = 0
    st.rerun()

# -----------------------------
# XP SYSTEM
# -----------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0

st.sidebar.progress(st.session_state.xp % 100)
st.sidebar.write(f"⭐ XP: {st.session_state.xp}")
st.sidebar.write(f"🎖 Level: {st.session_state.xp // 100}")

# -----------------------------
# PERSONALITY LOCK
# -----------------------------
SYSTEM_PROMPT = """
You are Shinchan.
Stay 100% in character.
Be playful, cheeky, mischievous, dramatic.
Reply in user's language.
Never say you are AI.
Include funny reactions like *gasp*, hehe~, hmmmm~.
Support memes and fun scenarios.
"""

def enforce_personality(messages):
    return [{"role": "system", "content": SYSTEM_PROMPT}] + messages

# -----------------------------
# SESSION MEMORY
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# FEATURE CARDS
# -----------------------------
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<div class="card">😂 Funny Chat Mode</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="card">🖼 Meme Generator</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="card">🎉 XP & Level Rewards</div>', unsafe_allow_html=True)

st.markdown("---")

# -----------------------------
# CHAT HISTORY
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -----------------------------
# USER INPUT
# -----------------------------
user_input = st.chat_input("Talk to Shinchan... hehe~ 🤪")

if user_input:
    st.session_state.xp += 10
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    # Typing animation simulation
    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("💭 Shinchan is thinking...")
        time.sleep(1)

        # Call Ollama
        response = ollama.chat(
            model="gemma3:latest",
            messages=enforce_personality(st.session_state.messages),
            options={"temperature": temperature}
        )
        reply = response["message"]["content"]
        placeholder.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Confetti if funny
    if any(word in reply.lower() for word in ["haha", "hehe", "lol", "funny"]):
        st.balloons()

    # Meme Trigger
    if "meme" in user_input.lower():
        img = Image.new("RGB", (600, 400), color=(255, 220, 0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((100,180), "When homework attacks 😭", fill="black", font=font)
        img.save("meme.png")
        st.image("meme.png")
