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
st.set_page_config(page_title="Shinchan Fun World", layout="wide")

# -----------------------------
# CSS: background, chat bubbles, input
# -----------------------------
st.markdown("""
<style>
body {background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1, #fffa65, #4bcffa);
      background-size: 400% 400%;
      animation: gradientBG 15s ease infinite;}
@keyframes gradientBG {0% {background-position:0% 50%;} 50% {background-position:100% 50%;} 100% {background-position:0% 50%;}}
.title {text-align:center; font-size:52px; font-weight:bold; color:#ff3c78; text-shadow:2px 2px #fff;}
div[data-testid="stChatMessage"][data-user="true"] > div {background-color:#ffd966!important; color:#000!important; border-radius:20px!important; padding:10px!important;}
div[data-testid="stChatMessage"][data-user="false"] > div {background-color:#ff6f91!important; color:#fff!important; border-radius:20px!important; padding:10px!important;}
.css-18e3th9 input {background-color:#fff3b0!important; color:#000!important; font-weight:bold; font-size:18px; border-radius:15px!important; padding:10px!important;}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Floating Emojis
# -----------------------------
emojis = ["😂","🎉","🍭","🍕","🧸","🌈","⭐","🤪"]
for i in range(5):
    left = random.randint(5,85)
    st.markdown(f'<div style="position:fixed;font-size:30px;left:{left}vw;">{random.choice(emojis)}</div>', unsafe_allow_html=True)

# -----------------------------
# Shinchan Image
# -----------------------------
try:
    url = "https://upload.wikimedia.org/wikipedia/en/7/70/Shinnosuke_Nohara.png"
    response = requests.get(url)
    shinchan_img = Image.open(BytesIO(response.content))
    st.image(shinchan_img, width=200, caption="Shinchan 😎")
except:
    st.write("🖼 Shinchan image could not load")

# -----------------------------
# Title
# -----------------------------
st.markdown('<div class="title">🎭 Shinchan Fun World</div>', unsafe_allow_html=True)
st.write("💬 Chat • 😂 Meme • 🎨 Draw • 🌈 XP & Fun")

# -----------------------------
# Sidebar / Settings
# -----------------------------
st.sidebar.title("⚙️ Settings")
temperature = st.sidebar.slider("🔥 Mischief Level", 0.0,1.5,0.9,0.1)
if st.sidebar.button("🧹 Clear Chat & XP"):
    st.session_state.messages = []
    st.session_state.xp = 0
    st.rerun()

# -----------------------------
# XP system
# -----------------------------
if "xp" not in st.session_state:
    st.session_state.xp = 0
st.sidebar.progress(st.session_state.xp%100)
st.sidebar.write(f"⭐ XP: {st.session_state.xp}")
st.sidebar.write(f"🎖 Level: {st.session_state.xp//100}")

# -----------------------------
# Session messages
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

SYSTEM_PROMPT = """
You are Shinchan.
Stay 100% in character.
Be playful, cheeky, mischievous, dramatic.
Reply in user's language.
Never say you are AI.
Include funny reactions like *gasp*, hehe~, hmmmm~.
"""

def enforce_personality(messages):
    return [{"role":"system","content":SYSTEM_PROMPT}]+messages

# -----------------------------
# Multi-feature navigation
# -----------------------------
tab = st.sidebar.radio("Select Feature", ["Funny Chat","Meme Generator","Draw Board"])

# -----------------------------
# Funny Chat Mode
# -----------------------------
if tab=="Funny Chat":
    st.subheader("😂 Chat with Shinchan")
    user_input = st.chat_input("Type your message...")
    if user_input:
        st.session_state.xp+=10
        st.session_state.messages.append({"role":"user","content":user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            placeholder = st.empty()
            placeholder.markdown("💭 Shinchan thinking...")
            time.sleep(1)
            response = ollama.chat(model="gemma3:latest", messages=enforce_personality(st.session_state.messages), options={"temperature":temperature})
            reply = response["message"]["content"]
            placeholder.markdown(reply)
        st.session_state.messages.append({"role":"assistant","content":reply})
        if any(w in reply.lower() for w in ["haha","hehe","lol","funny"]):
            st.balloons()

# -----------------------------
# Meme Generator
# -----------------------------
elif tab=="Meme Generator":
    st.subheader("🖼 Meme Generator")
    meme_text = st.text_input("Enter meme text:","When homework attacks 😭")
    if st.button("Generate Meme"):
        img = Image.new("RGB",(600,400),color=(255,220,0))
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()
        draw.text((50,180), meme_text, fill="black", font=font)
        st.image(img)

# -----------------------------
# Drawing Board
# -----------------------------
elif tab=="Draw Board":
    st.subheader("🎨 Draw with Shinchan")
    width,height=700,400
    if "drawing_img" not in st.session_state:
        st.session_state.drawing_img = Image.new("RGB",(width,height),"white")
    img_draw = ImageDraw.Draw(st.session_state.drawing_img)
    st.image(st.session_state.drawing_img)
    draw_text = st.text_input("Add text to canvas:")
    if draw_text:
        img_draw.text((50,50), draw_text, fill="black")
    if st.button("Clear Canvas"):
        st.session_state.drawing_img = Image.new("RGB",(width,height),"white")
        st.experimental_rerun()
