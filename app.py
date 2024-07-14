import streamlit_antd_components as sac
from langflow.load import run_flow_from_json
import streamlit as st
import base64
import time
import pyaudio
import wave
import requests
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
    
    
def Assistant() :
    st.title("DAIT Assistant")

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
            response = "".join(RAG_ChatBot(prompt))
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        generate_speech(response)
        
    
    # if st.button("Record"):
    #         record_audio()
    #         VoiceMessage = generateTextFromVoice("./output.wav")
    #         with st.chat_message("user"):
    #             st.markdown(VoiceMessage)
                
    #         with st.chat_message("assistant"):
    #             response = "".join(RAG_ChatBot(VoiceMessage))
    #             st.markdown(response)
    #         st.session_state.messages.append({"role": "assistant", "content": response})

        
    #         generate_speech(response)
    #         autoplay_audio("audio.wav")
            

def response_generator(agent, prompt):
    response_dict = agent(prompt)
    response = response_dict["output"]
    print(response)
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

def RAG_ChatBot(prompt):
    TWEAKS = {
    "ParseData-H8Szu": {},
    "Prompt-yVMuh": {},
    "ChatOutput-4pKli": {},
    "OpenAIModel-OsDGo": {},
    "Pinecone-nQqRQ": {},
    "ChatInput-qLlGf": {},
    "AIMLAPIEmbeddings-FPbQh": {}
    }

    result = run_flow_from_json(flow="AIML_API_RAG_LANGFLOW.json",
                                input_value=prompt,
                                fallback_to_env_vars=True, # False by default
                                tweaks=TWEAKS)


    message_text = result[0].outputs[0].results['message'].text
    print(message_text)
    for word in message_text.split():
        yield word + " "
        time.sleep(0.05)


def Food_Helper():
    
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
        TWEAKS = {
        "Prompt-LjR1d": {},
        "ChatOutput-iyAtB": {},
        "OpenAIModel-FtYGt": {},
        "ChatInput-49meU": {}
        }

        result = run_flow_from_json(flow="AnalyseImage.json",
                                    input_value=image_url,
                                    fallback_to_env_vars=True, # False by default
                                    tweaks=TWEAKS)



        output = result[0].outputs[0].results['message'].text
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
    if image_url := st.chat_input("type down below the url for the dish picture 😊 "):
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": image_url})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(image_url)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            response = "".join(analyseimage(image_url))
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        generate_speech(response)
        autoplay_audio("audio.wav")



def Statistics() :
    pass

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
    
