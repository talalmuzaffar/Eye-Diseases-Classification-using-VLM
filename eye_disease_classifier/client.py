"""Groq client configured from Streamlit secrets."""
from groq import Groq
import streamlit as st

def create_client():
    # Get API key from Streamlit secrets
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except KeyError:
        st.error("Please set GROQ_API_KEY in your Streamlit secrets")
        st.stop()

    # Initialize Groq client
    return Groq(api_key=api_key)
