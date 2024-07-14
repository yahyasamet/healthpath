import streamlit as st
import base64
from PIL import Image
from io import BytesIO
import requests
st.title("Image Upload and Serve")

# Function to decode base64 image
def decode_image(base64_string):
    image_data = base64.b64decode(base64_string)
    image = Image.open(BytesIO(image_data))
    return image

# Function to save the image and return the path
def save_image(image, path):
    image.save(path)
    return path

# Image upload section
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Read image file
    bytes_data = uploaded_image.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    # Decode and save the image
    image = decode_image(base64_image)
    image_path = "food.jpg"
    save_image(image, image_path)

    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Display the URL to access the image
    image_url = f"http://localhost:8501/{image_path}"
    st.write("Image URL:", image_url)

    # Run the API call using the generated URL
    url = "https://api.aimlapi.com/chat/completions"
    headers = {
      "Content-Type": "application/json",
      "Authorization": "Bearer a409119d7e844a8ba1c017970008b218"
    }
    payload = {
      "model": "gpt-4o",
      "messages": [
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "What’s in this image?"},
            {"type": "image_url", "image_url": {"url": image_url}}
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post(url, headers=headers, json=payload)
    st.write(response.json())
