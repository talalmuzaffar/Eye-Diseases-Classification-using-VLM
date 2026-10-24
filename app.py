import streamlit as st

from eye_disease_classifier.client import create_client
from eye_disease_classifier.ui import init_session_state, main

# Set page configuration
st.set_page_config(page_title="Eye Disease Analysis Assistant", layout="wide")

client = create_client()

init_session_state()

if __name__ == "__main__":
    main(client)
