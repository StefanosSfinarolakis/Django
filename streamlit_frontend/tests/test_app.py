import streamlit as st

def test_app():
    with st.echo():
        st.title("My Streamlit App")
        st.write("Hello, world!")
