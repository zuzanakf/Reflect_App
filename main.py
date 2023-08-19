import streamlit as st
from streamlit_extras.switch_page_button import switch_page

#Page configurations
st.set_page_config(page_title="Reflect - Emotional Exploration", page_icon=":brain:", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none;
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(#5a8c8c,#224040);
    }
</style>
""",
    unsafe_allow_html=True,
)

#App introduction and description
st.title(":sunrise_over_mountains: Welcome to Reflect")

st.markdown("""
    Reflect is an interactive tool designed to help you explore your emotions. 
    You will answer a few questions and then talk to ReflectBot.
    Let's get started!
    *Please note: Reflect is not a substitute for professional mental health services.*
    """)

#Personal information inputs
st.header("Tell us about yourself")

col1, col2 = st.columns(2)
with col1:
   user_name = st.text_input("Your name", value="", help="Enter your name here.")
with col2:
    user_emotion = st.selectbox(
        "Your main emotion right now", 
        ('Happy', 'Sad', 'Angry', 'Anxious', 'Excited', 'Confused', 'Neutral', 'Jealous'),
        help="Select the emotion that best describes how you're feeling at this moment.")
    
# Save data to session state
st.session_state.data = {
    'User Name': user_name,
    'Main Emotion': user_emotion
}

# Create three columns
col1, col2, col3 = st.columns([1,1,1])

# Empty space in the first and third columns
with col2:
    st.write("")  
with col3:
    st.write("")  

# Place the button in the middle column
with col1:
    if st.button('NEXT'):
        switch_page('emotions')
