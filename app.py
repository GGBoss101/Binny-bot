import streamlit as st
import threading
import os
import sys

# 1. Force Streamlit to wait for the packages to finish installing
try:
    import discord
except ImportError:
    st.warning("Installing dependencies... Please wait a moment.")
    st.stop()  # Stops the script temporarily until the installer finishes

# 2. Display the web page interface
st.title("🤖 Discord Bot Status")
st.success("The bot is online and running in the background!")

# 3. Define the background thread function
def run_bot():
    # Force python to use the exact same environment where dependencies are installed
    os.system(f"{sys.executable} main.py") 

# 4. Safely start the background thread
if "bot_started" not in st.session_state:
    st.session_state.bot_started = True
    threading.Thread(target=run_bot, daemon=True).start()
