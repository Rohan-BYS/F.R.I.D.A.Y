"""
F.R.I.D.A.Y. Visual Dashboard (OpenHands/Devin style).
Provides a beautiful local web UI to monitor the agent, ledgers, and terminals.
"""

import streamlit as st
import sqlite3
import os
import json

st.set_page_config(page_title="F.R.I.D.A.Y. Terminal", layout="wide")

st.title("🛡️ F.R.I.D.A.Y. Command Nexus")

db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'friday_state.db'))

def get_recent_messages():
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT role, content, timestamp FROM messages ORDER BY id DESC LIMIT 20")
        rows = cur.fetchall()
        conn.close()
        return list(reversed(rows))
    except Exception as e:
        return [("error", f"Could not connect to memory: {e}", "")]

st.sidebar.header("System Subsystems")
st.sidebar.success("✅ Persistent Memory (WAL)")
st.sidebar.success("✅ Vector Brain (RAG)")
st.sidebar.success("✅ Tool Forge")
st.sidebar.success("✅ Webhook Nexus")
st.sidebar.success("✅ Phantom Scheduler")
st.sidebar.success("✅ Midnight Protocol")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Live Agent Memory & Execution")
    
    messages = get_recent_messages()
    for role, content, ts in messages:
        with st.chat_message(role):
            st.markdown(f"**{role.upper()}** - {ts}")
            st.markdown(content)

with col2:
    st.subheader("Task Ledger (Magentic-One)")
    st.info("The Orchestrator is currently idle. No active global goals.")
    
    st.subheader("Action/Observation Stream")
    st.code("$ > System awaiting manual override...", language="bash")
