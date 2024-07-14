import streamlit as st
import streamlit.components.v1 as components
# fix_size_css = """
# <style>
# /* Fixer la taille de la page */
# body {
#     width: 1000vw;
#     height: 1000vh;
#     overflow: hidden;  /* Désactiver le défilement */
# }

# /* Fixer la taille de la section principale */
# .main {
#     width: 100%;
#     height: 100%;
#     overflow: hidden;  /* Désactiver le défilement */
# }
# </style>
# """

# st.markdown(fix_size_css, unsafe_allow_html=True)
st.title("Langflow Chat Integration")
st.write("This is an integration of the Langflow chat widget in a Streamlit app.")
# HTML code to embed
html_code = """
<script src="https://cdn.jsdelivr.net/gh/logspace-ai/langflow-embedded-chat@v1.0.3/dist/build/static/js/bundle.min.js"></script>
<langflow-chat
  window_title="Chatbot"
  flow_id="51674562-3448-451f-abe5-2df0748175b8"
  host_url="http://localhost:7860"
></langflow-chat>
"""

# Embed the HTML code in Streamlit
components.html(html_code, height=1000)