import streamlit as st
from streamlit_extras.switch_page_button import switch_page

#Page configurations
st.set_page_config(page_title="Reflect - Emotional Exploration", page_icon=":brain:", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(0.25turn, #3f87a6, #ebf8e1, #f69d3c)
    }
</style>
""",
    unsafe_allow_html=True,
)

#App introduction and description
st.title("Welcome to Reflect")

# Create two columns for description and image
col1, col2 = st.columns([3,1])  

with col1:
    st.markdown("""
    Reflect is an interactive tool designed to help you explore and understand your emotions. 
    You will be guided through a series of questions and based on your responses, Reflect will provide you with insights into your emotional state.
    Let's get started!
    *Please note: Reflect is not a substitute for professional mental health services.*
    """)

with col2:
    st.image('image.png')  # replace 'image.png' with the path to your image file

#Personal information inputs
st.header("Tell us about yourself")

user_name = st.text_input("Your name", value="", help="Enter your name here.")

st.header("Your current emotional state")

col1, col2 = st.columns(2)

with col1:
    user_emotion = st.selectbox(
        "Your main emotion right now", 
        ('Happy', 'Sad', 'Angry', 'Anxious', 'Excited', 'Confused', 'Neutral'),
        help="Select the emotion that best describes how you're feeling at this moment.")
    
with col2:
    emotion_intensity = st.select_slider(
        "Intensity of this emotion",
        options=[1, 2, 3, 4, 5],
        help="On a scale of 1-5, how intense is this emotion? 1 being mild and 5 being very strong.")

emotion_duration = st.selectbox(
    "Duration of this emotion",
    ('Just now', 'A few hours', 'A day', 'A few days', 'A week or more'),
    help="Approximately how long have you been feeling this way?")

emotion_context = st.text_area("Context", value="", height=100, help="Can you briefly describe the situation or event that led to this emotion?")

if st.button('NEXT :arrow_right:'):
    # storing page data so can be accessed in export function on next page
    st.session_state.data = {
    'User Name': user_name,
    'Main Emotion': user_emotion,
    'Emotion Intensity': emotion_intensity,
    'Emotion Duration': emotion_duration,
    'Emotion Context': emotion_context
    }
    switch_page('first')
