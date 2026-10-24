"""Image preprocessing for the vision model."""
from PIL import Image
import base64
from io import BytesIO

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
