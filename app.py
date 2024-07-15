import streamlit_antd_components as sac
from langflow.load import run_flow_from_json
import streamlit as st
import streamlit.components.v1 as components
import base64
import time
import pyaudio
import wave
import requests
import pandas as pd
from openai import OpenAI as OP
import os
from PIL import Image
from io import BytesIO
import json
import os
from dotenv import load_dotenv

# Load .env file
#load_dotenv()

# Access api_key
#api_key = os.getenv("api_key")
api_key = st.secrets["openai"]["api_key"]
# ------------------------------------------- Record Voice Notes ----------------------------------------------------------

def record_audio(seconds=5, rate=44100, channels=1):
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT, channels=channels,
                        rate=rate, input=True,
                        frames_per_buffer=CHUNK)

    frames = []
    for i in range(int(rate / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Convert frames to binary data
    wave_output = wave.open("output.wav", 'wb')
    wave_output.setnchannels(channels)
    wave_output.setsampwidth(audio.get_sample_size(FORMAT))
    wave_output.setframerate(rate)
    wave_output.writeframes(b''.join(frames))
    wave_output.close()

# ----------------------------------------------- autoplay audio -----------------------------------------------------------

def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true" style="display: none;">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
            
        )


# ---------------------------------------------------------------------------------------------------------------------------

def generate_speech(input_text):
    url = 'https://api.aimlapi.com/tts'  # Replace with the actual API endpoint
    headers = {
        "Content-Type": "application/json",
        'Authorization': 'Bearer 0f6cfe3d82254c6f83395b4a6bdc32fd'
    }
    body = {
        "model": "#g1_aura-asteria-en",
        "text": input_text
    }

    response = requests.post(url, headers=headers, json=body)

    if response.status_code in [200, 201]:
        with open('audio.wav', 'wb') as f:
            f.write(response.content)
        print("Audio saved as audio.wav")
    else:
        print(f"Request failed with status code {response.status_code}")


# ---------------------------------------------------------------------------------------------------------------------------


vopenai = OP(
    api_key= api_key
)


def generateTextFromVoice(path):
    audio_file= open(path, "rb")
    transcription = vopenai.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file
    )
    return transcription.text


def home_page():
    
    with open('style.css') as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    # Display HTML content
    st.markdown("""
    <div class="area" >
        <ul class="circles">
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
        </ul>
       
    </div >
    """, unsafe_allow_html=True)
    
    st.session_state['b64_image'] =""
    with open("./Back.png", "rb") as img_file:
        img_back = base64.b64encode(img_file.read()).decode("utf-8")
        # st.image(f'data:image/png;base64,{img_back}', use_column_width=False)
        st.markdown(f"""<img class="back_img"  src="data:image/png;base64,{img_back}" alt="Frozen Image">""",unsafe_allow_html=True)
    st.markdown("""<h1 class="Title">Welcome To Health Path</h1>""",unsafe_allow_html=True)
    
    
    
def chatBottt(prompt):
    TWEAKS = {
    "Prompt-2RAUm": {},
    "ChatInput-zfFG2": {},
    "ChatOutput-GhWIQ": {},
    "GroqModel-PEURW": {}
    }

    result = run_flow_from_json(flow="Memory_Chatbot.json",
                                input_value=prompt,
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)
    
    output = result[0].outputs[0].results['message'].text
    return output

    
    
    
    
    
def Assistant() :
    st.title("Health Path Assistant")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
            
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    # Accept user input
    if prompt := st.chat_input("What is up?"):
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = "".join(chatBottt(prompt))
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

        generate_speech(response)
        autoplay_audio("audio.wav")   

    if st.button("Record"):
        record_audio()
        VoiceMessage = generateTextFromVoice("./output.wav")
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": VoiceMessage})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(VoiceMessage)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = "".join(chatBottt(VoiceMessage))
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})


        generate_speech(response)
        autoplay_audio("audio.wav")
            

def response_generator(agent, prompt):
    response_dict = agent(prompt)
    response = response_dict["output"]
    print(response)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def RAG_ChatBot(prompt):
    TWEAKS = {
    "ParseData-XhkUG": {},
    "Prompt-bd0HK": {},
    "ChatOutput-A46us": {},
    "AIMLAPIModel-tsWmW": {},
    "Pinecone-zqmTC": {},
    "ChatInput-a8STv": {},
    "AIMLAPIEmbeddings-iAzCX": {}
    }

    result = run_flow_from_json(flow="AIML_API_RAG_LANGFLOW.json",
                                input_value="message",
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)


    message_text = result[0].outputs[0].results['message'].text
    print(message_text)
    for word in message_text.split():
        yield word + " "
        time.sleep(0.05)


def Food_Helper():
    
    prompt = """
        You are an expert meal prep AI assistant for diabetics. You need to see the pizza ("a pepperoni pizza. It has a golden-brown crust, melted cheese, and is topped with evenly spaced pepperoni slices. One slice is being pulled away, highlighting the gooey cheese and the crispy edges of the pizza") and calculate the total glycemic index in mg/dl, also provide the details of every food item in it with glycemic index intake in the following format:

        Item 1 - glycemic index in mg/dl
        Item 2 - glycemic index in mg/dl
        Finally, you must mention whether the food is healthy, balanced, or not healthy, and what additional food items can be added to the diet which are healthy. Calculate the insulin dosage using the following formula:

        CHO insulin dose = (Total grams of CHO in the meal) / (Grams of CHO disposed by 1 unit of insulin)
    """
    
    
    st.session_state.messages = []
    
    with open('style.css') as f:
        st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)
    # Display HTML content
    st.markdown("""
    <div class="area" >
        <ul class="circles">
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
            <li></li>
        </ul>
                
    </div >
    """, unsafe_allow_html=True)
    
    def analyseimage(image_url):
        url = "https://api.aimlapi.com/chat/completions"
        prompt = """
        You are an expert meal prep AI assistant for diabetics. You need to see the food items from the image and calculate the total glycemic index in mg/dl, also provide the details of every food item with glycemic index intake in the following format:

        Item 1 - glycemic index in mg/dl
        Item 2 - glycemic index in mg/dl
        Finally, you must mention whether the food is healthy, balanced, or not healthy, and what additional food items can be added to the diet which are healthy. Calculate the insulin dosage using the following formula:

        CHO insulin dose = (Total grams of CHO in the meal) / (Grams of CHO disposed by 1 unit of insulin)
        """
        payload = json.dumps({
        "model": "gpt-4o",
        "messages": [
            {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": image_url}} if image_url else {"type": "text", "text": ""}
            ]
            }
        ]
        })

        headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer 0f6cfe3d82254c6f83395b4a6bdc32fd'
        }

        response = requests.post(url, headers=headers, data=payload)
        output = response.json()["choices"][0]["message"]["content"]
        return output
        
    ##initialize our streamlit app


    st.header("Food Helper")
        # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        
            
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    
    # Accept user input
    if image_url := st.chat_input("Type down below the URL for the dish picture 😊 "):
        if is_valid_image_url(image_url):
            
            # Display user message in chat message container
            with st.chat_message("user"):
                st.image(image_url, use_column_width=True)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                response = "".join(chatBottt(prompt))
                st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Generate speech and play audio
            generate_speech(response)
            autoplay_audio("audio.wav")
        else:
            st.error("Invalid image URL. Please try again.")



def is_valid_image_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return True
    except Exception:
        return False



def Statistics():
    
    # Existing sample data
    data = """FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 07:12 PM,0,457,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 07:27 PM,0,459,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 07:42 PM,0,455,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 07:57 PM,0,437,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 08:13 PM,0,414,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 08:28 PM,0,426,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 08:43 PM,0,433,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 08:58 PM,0,411,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 09:13 PM,0,383,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 09:28 PM,0,357,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 09:43 PM,0,322,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 09:58 PM,0,280,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 10:13 PM,0,231,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 10:28 PM,0,182,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 10:43 PM,0,146,,,,,,,,,,,,,,"""

    # Additional data to be added
    additional_data = """FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 10:58 PM,0,100,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 11:13 PM,0,90,,,,,,,,,,,,,,
    FreeStyle LibreLink,10D06121-1654-4FE8-8850-08C1E630EF7C,07-29-2022 11:28 PM,0,85,,,,,,,,,,,,,,"""

    # Concatenate additional data to the existing data
    data += additional_data

    # Function to process data
    def process_data(data):
        lines = data.splitlines()
        data_list = [line.split(",") for line in lines]
        dates = [row[2].strip() for row in data_list]
        glucose_values = [int(row[4]) for row in data_list]
        max_glucose = max(glucose_values)
        min_glucose = min(glucose_values)
        df = pd.DataFrame({"Date": dates, "Glucose Value": glucose_values})
        # Optional: Convert "Date" to datetime format
        df["Date"] = pd.to_datetime(df["Date"], format='%m-%d-%Y %I:%M %p')
        return df,max_glucose,min_glucose

    # Process the data
    df, max_glucose, min_glucose= process_data(data)
    last_glucose_value = df.iloc[-1]["Glucose Value"]
    percentage1=(100-last_glucose_value)/100
    col1, col2, col3 = st.columns(3)
    col1.metric("highest glucose level", str(max_glucose) +" mg/dL", "max%")
    col2.metric("lower glucose level", str(min_glucose) +" mg/dL", "-min%")
    col3.metric("Current glucose level", str(last_glucose_value)+" mg/dL", str(percentage1)+"%")
    # Title and header
    st.title("Blood Glucose Monitoring Chart")
    st.header("FreeStyle LibreLink Data")



    # Display the line chart
    st.line_chart(df, x="Date", y="Glucose Value")

if 'current_tab' not in st.session_state:
    st.session_state.current_tab = 'Home'

with st.sidebar:
    selected_tab = sac.menu([
        sac.MenuItem('Home', icon='house-fill'),
        sac.MenuItem('Assistant', icon='chat-text-fill'),
        sac.MenuItem('Food-Helper', icon='bi bi-award-fill'),
        sac.MenuItem('Statistics', icon='bi bi-bar-chart-fill')
    ], color='cyan', size='lg', open_all=True)

if selected_tab != st.session_state.current_tab:
    st.session_state.current_tab = selected_tab

if st.session_state.current_tab == 'Home':
    home_page()
elif st.session_state.current_tab == 'Assistant':
    Assistant()  
elif st.session_state.current_tab == 'Food-Helper':
    Food_Helper()
elif st.session_state.current_tab == 'Statistics':
    Statistics()
    
