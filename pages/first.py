#import streamlit as st

#import openai
#import pandas as pd

#extras
# Import necessary libraries
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

# Set Streamlit page configuration
st.set_page_config(page_title='🧠MemoryBot🤖', layout='wide')

# Initialize session states
if "generated" not in st.session_state:
    st.session_state["generated"] = ""
if "input_text" not in st.session_state:
    st.session_state["input_text"] = ""

# Define function to get user input
def get_text():
    """
    Get the user input text.

    Returns:
        (str): The text entered by the user
    """
    return st.text_input("You: ", st.session_state["input_text"], key="input_text",
                            placeholder="Your AI assistant here! Ask me anything ...", 
                            label_visibility='hidden')


# Define function to start a new chat
def new_chat():
    """
    Clears session state and starts a new chat.
    """
    st.session_state["generated"] = ""
    st.session_state["input_text"] = ""
    st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=20)
    st.session_state.entity_memory.buffer.clear()


# Ask the user to enter their OpenAI API key
API_O = st.sidebar.text_input("API-KEY", type="password")

# Session state storage would be ideal
if API_O:
    # Create an OpenAI instance
    llm = OpenAI(temperature=0,
                openai_api_key=API_O, 
                model_name='gpt-3.5-turbo', 
                verbose=False) 

    # Create a ConversationEntityMemory object if not already created
    if 'entity_memory' not in st.session_state:
            st.session_state.entity_memory = ConversationEntityMemory(llm=llm, k=20 )
        
        # Create the ConversationChain object with the specified configuration
    Conversation = ConversationChain(
            llm=llm, 
            prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
            memory=st.session_state.entity_memory
        )  
else:
    st.sidebar.warning('API key required to try this app.The API key is not stored in any form.')

# Add a button to start a new chat
st.sidebar.button("New Chat", on_click = new_chat, type='primary')

# Get the user input
user_input = get_text()

# Check if the user input is different from the current session state value
if user_input != st.session_state["input_text"]:
    # Update the session state value
    st.session_state["input_text"] = user_input

# Generate the output using the ConversationChain object and the user input, and add the input/output to the session
if user_input:
    output = Conversation.run(input=user_input)  
    st.session_state["generated"] = output



# Display the conversation
col1, col2 = st.columns(2)
with col1:
    st.info(st.session_state["input_text"])
with col2:
    st.success(st.session_state["generated"])


'''#Page configurations
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
'''
'''# Save conversation to DataFrame when user types 'stop'
if prompt is not None and prompt.lower() == 'stop':
    df = pd.DataFrame(st.session_state.messages)
    
    # Add additional columns
    df['User Name'] = st.session_state.data['User Name'] 
    df['Main Emotion'] = st.session_state.data['Main Emotion']
    df['Emotion Intensity'] = st.session_state.data['Emotion Intensity']
    df['Emotion Context'] = st.session_state.data['Emotion Context']
    
    df.to_csv('reflect_conversation.csv', index=False)
    st.success('Conversation saved to DataFrame.')
'''


# Add button to go to the next page
if st.button('NEXT'):
    switch_page('second')
