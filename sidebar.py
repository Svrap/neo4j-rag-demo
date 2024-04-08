from constants import TITLE
import streamlit as st
import streamlit.components.v1 as components

def sidebar():
    with st.sidebar:
        # st.markdown(TITLE,unsafe_allow_html=True)
        st.markdown("""Questions you can ask of the dataset:""", unsafe_allow_html=True)
        st.markdown("""""", unsafe_allow_html=True)
        st.markdown("""
                    <style>
                        div[data-testid="column"] {
                            width: fit-content !important;
                            flex: unset;
                        }
                        div[data-testid="column"] * {
                            width: fit-content !important;
                        }
                    </style>
                    """, unsafe_allow_html=True)


        sample_questions = "Best Resonating Content?","Top 5 most reused Content?","most unsubscribed Content?"

        for text, col in zip(sample_questions, st.columns(len(sample_questions))):
            if col.button(text, key=text):
                st.session_state["sample"] = text