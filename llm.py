import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

llm = ChatOpenAI(
    openai_api_key = st.secrets["OPENAI_API_KEY"],
    model= st.secrets["OPENAI_MODEL"]
)

embeddings = OpenAIEmbeddings(
    openai_api_key =  st.secrets["OPENAI_API_KEY"]
)