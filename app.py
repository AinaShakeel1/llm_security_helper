
import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("LLM Security Helper")

# Create two tabs
tabs = st.tabs(["Code Analysis", "Specs Analysis"])

with tabs[0]:
    st.header("Analyze Code for Security Vulnerabilities")
    
    # Text input area for code
    code_input = st.text_area("Paste your code here:")

    # Button to trigger analysis
    if st.button("Analyze Code"):
        if code_input.strip():  # Make sure input is not empty
            prompt = f"""
            Identify security vulnerabilities in this code and suggest fixes.
            Focus only on security issues, not general refactoring.

            Code:
            {code_input}
            """
            
            # Call LLM API
            response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
            
            # Display results
            st.subheader("Security Analysis Results")
            # st.text(response['choices'][0]['message']['content'])
            security_analysis = response.choices[0].message.content
            st.text(security_analysis)  
        else:
            st.warning("Please enter some code to analyze.")

with tabs[1]:
    st.header("Analyze App Specs for Potential Vulnerabilities")
    
    # Text input area for app specs
    specs_input = st.text_area("Enter app specifications here:")

    # Button to trigger analysis
    if st.button("Analyze Specs"):
        if specs_input.strip():  # Make sure input is not empty
            prompt = f"""
            Given the following GenAI/Agentic app specification, identify potential security vulnerabilities.
            Map the issues to:
              1) OWASP Top 10 for LLM applications
              2) ATLAS (AI Threat Landscape) threats
            Provide clear, actionable, and specific recommendations.

            App Specs:
            {specs_input}
            """
            
            # Call LLM API
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500
            )
            
            # Display results
            st.subheader("Vulnerability Analysis Results")
            st.text(response['choices'][0]['message']['content'])
        else:
            st.warning("Please enter app specifications to analyze.")
