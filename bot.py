import streamlit as st  
from langchain.globals import set_llm_cache
from langchain.cache import InMemoryCache
from agent import generate_response
from sidebar import sidebar
from constants import TITLE
from utils import write_message

# Set page title
st.set_page_config(page_title="Jemika")

# Display title and sidebar
st.markdown(TITLE, unsafe_allow_html=True)
sidebar()

# LangChain caching to reduce API calls
set_llm_cache(InMemoryCache())

#define message placeholder
placeholder = st.empty()
user_placeholder = st.empty()

# Initialize chat history if not exists
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "ai", "content": "Hi! I am JEM-IKA, your assistant to engagement mapping. How can I help you?"}]

# Display chat history
with placeholder.container():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)

# Function to process user input and generate response
def process_input(user_input):
    response = generate_response(user_input)
    if response:
        output = response.get("output", "No response received")
        write_message("assistant", output)
    else:
        write_message("assistant", "Sorry, I couldn't process your request. Please try again.")

# # Collect user input from the sidebar
# selected_question = st.session_state.get("sample")

# # If a sidebar question is selected, use it as the user input
# if selected_question:
#     write_message("user", selected_question)
#     process_input(selected_question)
#     st.session_state["sample"] = None  # Reset sample input after submission

# # Display chat input box
# user_input = st.chat_input("Ask question related to content", key="user_input")

# # If the user enters a question in the chat input box, process it
# if user_input:
#     write_message("user", user_input)
#     process_input(user_input)

if "sample" in st.session_state and st.session_state["sample"] is not None:
    user_input = st.session_state["sample"]
else:
    user_input = st.chat_input("Ask question related to content", key="user_input")

if user_input:
    with user_placeholder.container():
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        
        with st.chat_message("ai"):
            with st.spinner("...."):
                message_placeholder = st.empty()
                thought_continer = st.container()
                agent_response = generate_response(user_input)

                if isinstance(agent_response, dict) is False:
                    agent_response = str(agent_response)

                content = agent_response['output']

                new_message = {"role": "ai", "content": content}
                st.session_state.messages.append(new_message)
            
            message_placeholder.markdown(content)
        
        if "sample" in st.session_state and st.session_state["sample"] is not None:
            st.session_state["sample"] = None
            user_input = st.chat_input(placeholder="Ask question on the SEC Filings", key="user_input")
