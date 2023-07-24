import streamlit as st
import openai
import pandas as pd
#extras
from streamlit_extras.switch_page_button import switch_page

# Set Streamlit page configuration
st.set_page_config(page_title='Reflect - Emotional Exploration', layout='wide')

# Ask the user to enter their OpenAI API key
API_O = st.sidebar.text_input("API-KEY", type="password")

#titles
st.title("Reflect Chat :wind_blowing_face:")
st.markdown("""
Let's start our journey. 
In this session, you'll chat with our AI to better understand your feelings. 
When you're ready to end the session, simply type 'stop'. Let's get started! :rocket:
""")

#Creating bot
#openai.api_key = st.secrets["API_KEY"]
openai.api_key = API_O

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

#Calling OpenAI
if API_O:
    if prompt := st.chat_input("Start by describing your feelings..."):
        st.session_state.messages.append({"role": "user", "content": prompt})

        full_response = ""
        conversation = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]

        # Adding a prompt for the model
        model_prompt = f"""
        You are an AI trained to help people understand their emotions. The user named {st.session_state.data['User Name']} has just said: '{prompt}'. 
        They are currently feeling {st.session_state.data['Main Emotion']} at an intensity level of {st.session_state.data['Emotion Intensity']}. 
        The context they provided is: {st.session_state.data['Emotion Context']}. 
        Help them explore why they might be feeling this way, asking open-ended questions to encourage deeper reflection.
        """
        conversation.append({"role": "system", "content": model_prompt})

        for response in openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=conversation,
            temperature=0.35,
            max_tokens=1003,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["stop"],
            stream=True,):
            full_response += response.choices[0].delta.get("content", "")
        st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.sidebar.warning('API key required to try this app.The API key is not stored in any form.')
    # st.stop()

# Create two columns for the flashcards
col1, col2 = st.columns(2)

# Display the most recent question and response in the flashcards
if st.session_state.messages:
    last_question = st.session_state.messages[-1]["content"] if st.session_state.messages[-1]["role"] == "assistant" else ""
    last_response = st.session_state.messages[-2]["content"] if st.session_state.messages[-2]["role"] == "user" else ""

    col1.markdown(f"**{st.session_state.data['User Name']}:**\n\n{last_response}")
    col2.markdown(f"**Our Reflection Question:**\n\n{last_question}")

# Save conversation to DataFrame when user types 'stop'
if prompt is not None and prompt.lower() == 'stop':
    df = pd.DataFrame(st.session_state.messages)
    
    # Add additional columns
    df['User Name'] = st.session_state.data['User Name'] 
    df['Main Emotion'] = st.session_state.data['Main Emotion']
    df['Emotion Intensity'] = st.session_state.data['Emotion Intensity']
    df['Emotion Context'] = st.session_state.data['Emotion Context']
    
    df.to_csv('reflect_conversation.csv', index=False)
    st.success('Conversation saved to DataFrame.')

# Add button to go to the next page
if st.button('NEXT'):
    switch_page('second')
