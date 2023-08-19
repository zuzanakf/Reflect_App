import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import openai
import pandas as pd

# Page configurations
st.set_page_config(page_title="Reflect - Emotional Exploration", page_icon=":brain:", initial_sidebar_state="collapsed")

# Custom CSS for styling
st.markdown(
    """
    <style>
        .custom-list-item {
            background-color: #698686;
            padding: 10px;
            border-radius: 10px;
            margin-bottom: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App introduction and description
st.title("Reflect :brain:")
st.markdown("""
Welcome back to Reflect! Let's review your emotional exploration. 
Here, you'll see a summary of the emotions you've explored and the key topics related to each emotion. 
""")

# Load conversation from CSV
df = pd.read_csv('reflect_conversation.csv')

# Initialize OpenAI
# openai.api_key = st.secrets["API_KEY"]

# Extract key topics for each emotion
emotion_topics = {}
for emotion in df['Main Emotion'].unique():
    # Filter the conversation for messages related to this emotion
    emotion_conversation = df[df['Main Emotion'] == emotion]['content'].str.cat(sep=' ')
    
    # Use the model to extract key topics
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"The following is a conversation about feeling {emotion}:\n{emotion_conversation}\n\nExtract the key topics related to this emotion:",
        temperature=0.3,
        max_tokens=100,
    )
    key_topics = response.choices[0].text.strip().split(',')
    
    # Store the key topics for this emotion
    emotion_topics[emotion] = key_topics

# Display the key topics for each emotion
for emotion, topics in emotion_topics.items():
    st.markdown(f'{emotion} :{emotion}:')
    for topic in topics:
        st.markdown(f'<div class="custom-list-item">- {topic}</div>', unsafe_allow_html=True)

