"""Streamlit UI: session state, sidebar upload and chat."""
from PIL import Image
import streamlit as st

from eye_disease_classifier.analysis import process_image_and_query

def init_session_state():
    # Initialize session states
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_image" not in st.session_state:
        st.session_state.uploaded_image = None

def main(client):
    st.title("🤖 Eye Disease Analysis Assistant")
    st.markdown("""
    ### Specialized in analyzing:
    - 👁️ Cataracts
    - 🔴 Conjunctivitis (Pink Eye)
    - 🌐 Pterygium
    
    *Note: This tool provides educational information only, not medical diagnosis. Always consult healthcare professionals for proper medical advice.*
    """)
    
    # Sidebar for image upload and information
    with st.sidebar:
        st.header("Upload Eye Image")
        uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
        
        st.markdown("---")
        st.markdown("""
        ### About These Conditions:
        
        **Cataracts:**
        - Clouding of eye lens
        - Blurry vision
        - Common in older adults
        
        **Conjunctivitis:**
        - Eye inflammation
        - Redness and irritation
        - Various causes
        
        **Pterygium:**
        - Tissue growth on cornea
        - UV exposure related
        - May affect vision
        """)
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.session_state.uploaded_image = image

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "image" in message:
                st.image(message["image"], caption="Analyzed Image", use_column_width=True)
            st.write(message["content"])

    # Suggested questions
    if not st.session_state.messages:
        st.markdown("""
        ### Suggested Questions:
        - What signs of eye conditions can you see in this image?
        - Are there any visible symptoms of cataracts?
        - Does this image show signs of conjunctivitis?
        - Can you identify any pterygium formation?
        - What are the key characteristics you notice in this eye image?
        """)

    # Chat input
    if prompt := st.chat_input("Ask about the eye condition..."):
        if st.session_state.uploaded_image is None:
            st.error("Please upload an eye image first!")
            return

        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "image": st.session_state.uploaded_image
        })

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing image..."):
                response = process_image_and_query(
                    client,
                    st.session_state.uploaded_image,
                    prompt
                )
                st.write(response)

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })

    # Clear chat button
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.uploaded_image = None
        st.rerun()
