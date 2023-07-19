import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import openai
import pandas as pd

#Page configurations
st.set_page_config(page_title="Reflect - Emotional Exploration", page_icon=":brain:", initial_sidebar_state="collapsed")

#App introduction and description
st.title("Reflect :brain:")
st.markdown("""
Welcome back to Reflect! Let's continue our journey of emotional exploration. 
In this session, you'll chat with our AI assistant to delve deeper into your feelings. 
When you're ready to end the session, simply type 'stop'. Let's get started! :rocket:
""")

#Creating bot
openai.api_key = st.secrets["API_KEY"]

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

#Calling OpenAI
if prompt := st.chat_input("Start by describing your feelings..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
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
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Save conversation to DataFrame when user types 'stop'
if prompt is not None and prompt.lower() == 'stop':
    df = pd.DataFrame(st.session_state.messages)
    df.to_csv('reflect_conversation.csv', index=False)
    st.success('Conversation saved to DataFrame.')


# Add button to go to the next page
if st.button('NEXT'):
    switch_page('second')
