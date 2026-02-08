import streamlit as st
import os
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()
# -----------------------------
# Set your Groq API key as an environment variable
# -----------------------------
# Example: export GROQ_API_KEY="your_api_key_here" on Linux/macOS
# Or set in Windows environment variables
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Please set your GROQ_API_KEY environment variable.")
    st.stop()

# -----------------------------
# Helper function to call Groq LLM API
# -----------------------------

def call_groq_model(prompt: str, model: str = "llama-3.1-8b-instant") -> str:
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_completion_tokens": 500
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        return f"Error: {response.status_code} − {response.text}"
    return response.json()["choices"][0]["message"]["content"]

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("LLM Security Helper (Groq API)")

# Create two tabs
tabs = st.tabs(["Code Analysis", "Specs Analysis"])

# -----------------------------
# Tab 1: Code Analysis
# -----------------------------
with tabs[0]:
    st.header("Analyze Code for Security Vulnerabilities")
    code_input = st.text_area("Paste your code here:")

    if st.button("Analyze Code", key="code_button"):
        if code_input.strip():
            prompt = f"""
            Identify security vulnerabilities in this code and suggest fixes.
            Focus only on security issues, not general refactoring.

            Code:
            {code_input}
            """
            with st.spinner("Analyzing code..."):
                security_analysis = call_groq_model(prompt)
            st.subheader("Security Analysis Results")
            st.text(security_analysis)
        else:
            st.warning("Please enter some code to analyze.")

# -----------------------------
# Tab 2: Specs Analysis
# -----------------------------
with tabs[1]:
    st.header("Analyze App Specs for Potential Vulnerabilities")
    specs_input = st.text_area("Enter app specifications here:")

    if st.button("Analyze Specs", key="specs_button"):
        if specs_input.strip():
            prompt = f"""
            Given the following GenAI/Agentic app specification, identify potential security vulnerabilities.
            Map the issues to:
              1) OWASP Top 10 for LLM applications
              2) ATLAS (AI Threat Landscape) threats
            Provide clear, actionable, and specific recommendations.

            App Specs:
            {specs_input}
            """
            with st.spinner("Analyzing specifications..."):
                vulnerability_analysis = call_groq_model(prompt)
            st.subheader("Vulnerability Analysis Results")
            st.text(vulnerability_analysis)
        else:
            st.warning("Please enter app specifications to analyze.")
