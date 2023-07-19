import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import openai
import pandas as pd

#Page configurations
st.set_page_config(page_title="Reflect - Emotional Exploration", page_icon=":brain:", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

#App introduction and description
#App introduction and description
st.title("Welcome to Reflect :brain:")

# Create two columns for description and image
col1, col2 = st.columns([3,1])  # adjust the numbers to change the width ratio of the columns

with col1:
    st.markdown("""
    Sometimes it can be difficult to understand our emotional reactions.
    Reflect is here as a guide on your journey of emotional self-discovery. 
    Through a series of interactive questions, Reflect helps you delve deeper into your feelings, 
    identify your emotional triggers, and gain a better understanding of your reactions. 
    Let's get started! :rocket:
                
    Please note, Reflect is not a substitute for professional mental health services.
    This is a project!
    """)

with col2:
    st.image('image.png')  # replace 'image.png' with the path to your image file


#Personal information inputs
st.header("Let's Reflect :thought_balloon:")
col1, col2 = st.columns(2)

with col1:
    user_name = st.text_input("What is your name? :bust_in_silhouette:")
    user_emotion = st.selectbox(
        "What is your main emotion right now? :face_with_monocle:", 
        ('Happy', 'Sad', 'Angry', 'Anxious', 'Excited', 'Confused', 'Neutral'))
    
with col2:
    emotion_intensity = st.select_slider(
        "On a scale of 1-5, how intense is this emotion? :thermometer:",
        options=[1, 2, 3, 4, 5])
    emotion_duration = st.selectbox(
        "How long have you been feeling this way? :hourglass_flowing_sand:",
        ('Just now', 'A few hours', 'A day', 'A few days', 'A week or more'))
    emotion_context = st.text_input("Can you briefly describe the context or situation? :memo:")

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
