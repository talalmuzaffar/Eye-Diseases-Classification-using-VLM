from groq import Groq
from PIL import Image
import streamlit as st
import base64
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(page_title="Eye Disease Analysis Assistant", layout="wide")

# Get API key from Streamlit secrets
try:
    api_key = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("Please set GROQ_API_KEY in your Streamlit secrets")
    st.stop()

# Initialize Groq client
client = Groq(api_key=api_key)

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None

def encode_image_to_base64(image):
    """Convert PIL Image to base64 string."""
    try:
        # Ensure image size is within limits (4MB for base64)
        max_size = (800, 800)  # Resize if needed to stay under limits
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        buffered = BytesIO()
        image.save(buffered, format="JPEG", quality=85)  # Compress to reduce size
        file_size = len(buffered.getvalue()) / (1024 * 1024)  # Size in MB
        
        if file_size > 4:
            raise ValueError("Image size exceeds 4MB limit after compression")
            
        return base64.b64encode(buffered.getvalue()).decode('utf-8')
    except Exception as e:
        raise Exception(f"Error encoding image: {str(e)}")

def process_image_and_query(
    image,
    query: str
) -> str:
    """Process an image with a query using the multimodal model."""
    try:
        # Convert image to base64
        base64_image = encode_image_to_base64(image)
        
        # Create messages for the API call - no system prompt as per docs
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""As an expert ophthalmologist, analyze this eye image for:
1. Cataracts (clouding, blurry vision)
2. Conjunctivitis (inflammation, redness)
3. Pterygium (tissue growth)

{query}

Note: This is for educational purposes only, not medical diagnosis."""
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        # Make the API call using llama-3.2-90b-vision-preview as recommended
        chat_completion = client.chat.completions.create(
            messages=messages,
            model="llama-3.2-90b-vision-preview",  # Using the more capable 90B model
            temperature=0.7,
            max_tokens=1024,
            stream=False  # Explicit non-streaming for better reliability
        )
        
        return chat_completion.choices[0].message.content
        
    except Exception as e:
        return f"Error processing image and query: {str(e)}"

def main():
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
            st.image(image, caption="Uploaded Image", use_container_width=True)
            st.session_state.uploaded_image = image

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if "image" in message:
                st.image(message["image"], caption="Analyzed Image", use_container_width=True)
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

if __name__ == "__main__":
    main()
