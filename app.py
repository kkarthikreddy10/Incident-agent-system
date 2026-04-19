import streamlit as st
import os
from dotenv import load_dotenv

# Load env variables BEFORE importing graph so ChatGoogleGenerativeAI gets the API Key
load_dotenv()

from graph import app, MODEL_NAME  # Mana AI Graph ni import chesthunnam
from langchain_core.messages import HumanMessage

# Page Configuration
st.set_page_config(page_title="AI Incident Agent", page_icon="🤖", layout="wide")

st.title("🤖 AI Autonomous Incident Response Agent")
st.markdown("### CascadeFlow + Hindsight AI Powered")

# Sidebar for Status
with st.sidebar:
    st.header("Agent Status")
    if os.getenv("GOOGLE_API_KEY"):
        st.success("API Key: Connected")
    else:
        st.error("API Key: Missing")
    st.info("Mode: Autonomous Investigation")
    st.write(f"Active Model: `{MODEL_NAME}`")

# User Input
alert_input = st.text_input("Enter Incident Alert:", placeholder="e.g., Billing service is down with 500 errors")

if st.button("Start Investigation"):
    if alert_input:
        st.write("---")
        # Chat-like container for logs
        with st.status("🚀 Agent Working...", expanded=True) as status:
            inputs = {"messages": [HumanMessage(content=alert_input)]}
            
            # Streaming results to the UI
            try:
                for output in app.stream(inputs):
                    for key, value in output.items():
                        st.write(f"*Step: {key.upper()}*")
                        last_msg = value["messages"][-1]
                        
                        # Show tool calls
                        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                            for tc in last_msg.tool_calls:
                                st.code(f"🛠️ Calling Tool: {tc['name']}", language="text")
                        
                        # Show AI thoughts
                        if hasattr(last_msg, 'content') and last_msg.content:
                            st.info(last_msg.content)
                
                status.update(label="✅ Investigation Complete!", state="complete", expanded=False)
                st.success("Investigation Finished. Check the findings above.")
                
            except Exception as e:
                st.error(f"Execution Error: {e}")
    else:
        st.warning("Please enter an alert first!")

# Visual appeal for Hackathon
st.markdown("---")
st.caption("Powered by LangGraph & Gemini 1.5 Flash")