import streamlit as st
import os
from dotenv import load_dotenv
load_dotenv()

from multiagent import app as langgraph_app

st.set_page_config(page_title="AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("AI Chatbot")
st.caption("Ask any question. The agent system will research and answer.")


user_input = st.chat_input("Type your question...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    result = langgraph_app.invoke({
        "user_input": user_input,
        "plan": [],
        "research": [],
        "final_answer": ""
    })

    st.session_state.messages.append({
        "role": "assistant",
        "content": result["final_answer"]
    })


for msg in st.session_state.messages:
    
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        