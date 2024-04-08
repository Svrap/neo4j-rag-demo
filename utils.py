import streamlit as st

def write_message(role, content, save = True):
    if "message" not in st.session_state:
        st.session_state.message = []
        
    if save:
        st.session_state.message.append({"role":role,"content":content})
    
    with st.chat_message(role):
        st.markdown(content)
