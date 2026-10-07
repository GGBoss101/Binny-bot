import streamlit as subprocess_streamlit
import threading
import os

# 1. Display a simple message on the web page so Streamlit knows it's working
subprocess_streamlit.title("🤖 Discord Bot Status")
subprocess_streamlit.write("The bot is currently running in the background!")

# 2. Define a function to start your actual Discord bot script
def run_bot():
    # This executes your main bot file in a background thread
    os.system("python main.py") # Change 'main.py' to whatever your main file is named

# 3. Start the background thread so your Discord bot runs forever
if "bot_started" not in subprocess_streamlit.session_state:
    subprocess_streamlit.session_state.bot_started = True
    threading.Thread(target=run_bot, daemon=True).start()
