import streamlit as st
import time
from ollama import Client

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Local LLM Chat", page_icon="💬", layout="centered")
st.title("💬 Local LLM Chat (Ollama)")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    model = st.selectbox(
        "Choose your model",
        ["llama3", "mistral"],
        help="Select which local model to use (make sure it's installed with ollama pull <model>)"
    )
    st.caption("💡 Tip: you can install more models using 'ollama pull <model>' in your terminal.")

# --- OLLAMA CLIENT ---
client = Client(host="http://127.0.0.1:11434")

# --- INITIALIZE SESSION STATE ---
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "You are a concise and helpful AI assistant."}
    ]

# --- DISPLAY PAST MESSAGES ---
for m in st.session_state["messages"]:
    if m["role"] == "user":
        st.chat_message("user").write(m["content"])
    elif m["role"] == "assistant":
        st.chat_message("assistant").write(m["content"])

# --- USER INPUT ---
prompt = st.chat_input("Type your message...")
if prompt:
    st.session_state["messages"].append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # --- MEASURE START TIME ---
    start_time = time.time()

    # --- ASSISTANT RESPONSE (STREAMING) ---
    with st.chat_message("assistant"):
        holder = st.empty()
        txt = ""
        for chunk in client.chat(model=model, messages=st.session_state["messages"], stream=True):
            delta = chunk.get("message", {}).get("content", "")
            if delta:
                txt += delta
                holder.write(txt)

        # --- MEASURE END TIME ---
        end_time = time.time()
        elapsed = round(end_time - start_time, 2)

        # --- SAVE ASSISTANT MESSAGE ---
        st.session_state["messages"].append({"role": "assistant", "content": txt})

        # --- SHOW PERFORMANCE METRIC ---
        st.markdown(f"⏱️ **Response time:** {elapsed} seconds")