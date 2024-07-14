import streamlit as st
import requests
import base64
from io import BytesIO

# Display a title
st.title('Speech to Text Conversion')

# Your API key
api_key = '17fb61bf44e84f4085b988909705e2df'

# Function to call the STT API
def call_stt_api(audio_url):
    request_body = {
        "model": "#g1_whisper-large",
        "url": audio_url,
        "detect_language": True,
        "punctuate": True,
        "intents": True,
        "languages": "en",
        "profanity_filter": True,
        "topics": True
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    response = requests.post('https://api.aimlapi.com/stt', headers=headers, json=request_body)

    if response.ok:
        data = response.json()
        try:
            # Extract the transcript
            transcript = data['results']['channels'][0]['alternatives'][0]['transcript']
            return transcript
        except KeyError as e:
            return f"KeyError: {e} - Please check the response structure."
    else:
        error_text = response.text
        return f'Error: {response.status_code} {error_text}'

# Streamlit UI
audio_url = st.text_input('Enter the audio file URL', 'https://www.dropbox.com/scl/fi/85m6vbcg3y7zz5owk18hg/test.wav?rlkey=nyjcomejkypi2pnqsi3ss12ss&e=1&st=bblboxfa&dl=1')

if st.button('Convert to Text'):
    transcript = call_stt_api(audio_url)
    st.text_area('Transcript', value=transcript, height=300)