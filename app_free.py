import streamlit as st
from ollama import Client

st.set_page_config(page_title="Local LLM Chat", page_icon="💬")
st.title("💬 Local LLM Chat (Ollama)")

client = Client(host="http://127.0.0.1:11434")
MODEL = "llama3"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"system","content":"Você é um assistente conciso."}]

for m in st.session_state["messages"]:
    if m["role"] == "user":
        st.chat_message("user").write(m["content"])
    elif m["role"] == "assistant":
        st.chat_message("assistant").write(m["content"])

prompt = st.chat_input("Digite sua mensagem…")
if prompt:
    st.session_state["messages"].append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        holder = st.empty()
        txt = ""
        for chunk in client.chat(model=MODEL, messages=st.session_state["messages"], stream=True):
            delta = chunk.get("message", {}).get("content", "")
            if delta:
                txt += delta
                holder.write(txt)
        st.session_state["messages"].append({"role":"assistant","content":txt})