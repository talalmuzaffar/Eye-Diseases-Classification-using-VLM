"""Eye image analysis with the Llama 3.2 vision model via Groq."""
from eye_disease_classifier.image_utils import encode_image_to_base64

def process_image_and_query(
    client,
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
