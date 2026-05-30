import os
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# --- PAGE CONFIG ---
st.set_page_config(page_title="Persona Chatbot", page_icon="🤖", layout="centered")

# Load environment variables
load_dotenv()
api_key = os.getenv("MISTRAL_API_KEY")

# Initialize Model
model = ChatMistralAI(
    model="mistral-large-latest",
    api_key=api_key
)

# --- STYLED UI ---
st.title("🎭 Persona Chatbot")
st.markdown("---")

# Sidebar for Mode Selection
with st.sidebar:
    st.header("Settings")
    choice = st.radio(
        "Select the AI's Mood:",
        ["Angry", "Sad", "Funny", "Sarcastic"],
        index=2
    )
    
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Define System Prompt based on choice
mode_map = {
    "Angry": "You are an angry person. You always respond in an angry tone.",
    "Sad": "You are a sad person. You always respond in a sad tone.",
    "Funny": "You are a funny person. You always respond in a funny tone.",
    "Sarcastic": "You are a sarcastic person. You always respond in a sarcastic tone."
}
system_prompt = mode_map[choice]

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").write(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").write(msg.content)

# Chat Input
if prompt := st.chat_input("Say something..."):
    # Display user message
    st.chat_message("user").write(prompt)
    
    # Prepare LangChain message list
    langchain_messages = [SystemMessage(content=system_prompt)] + st.session_state.messages + [HumanMessage(content=prompt)]
    
    # Get AI Response
    with st.spinner("Thinking..."):
        response = model.invoke(langchain_messages)
    
    # Update state and display
    st.session_state.messages.append(HumanMessage(content=prompt))
    st.session_state.messages.append(AIMessage(content=response.content))
    st.chat_message("assistant").write(response.content)
