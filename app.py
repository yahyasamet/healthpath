import streamlit as st
import base64


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
    
    
home_page()