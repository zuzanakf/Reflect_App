import streamlit as st
from streamlit_extras.switch_page_button import switch_page

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

# Emotional state inputs
st.header("Your current emotional state")
emotion_intensity = st.select_slider(
    "Intensity of this emotion",
    options=[1, 2, 3, 4, 5],
    help="On a scale of 1-5, how intense is this emotion? 1 being mild and 5 being very strong.")
emotion_duration = st.selectbox(
    "Duration of this emotion",
    ('Just now', 'A few hours', 'A day', 'A few days', 'A week or more'),
    help="Approximately how long have you been feeling this way?")
emotion_context = st.text_area("Context", value="", height=100, help="Can you briefly describe the situation or event that led to this emotion?")

# Update session state
st.session_state.data.update({
    'Emotion Intensity': emotion_intensity,
    'Emotion Duration': emotion_duration,
    'Emotion Context': emotion_context
})

if st.button('NEXT :arrow_right:'):
    switch_page('first')
