import streamlit as st

st.set_page_config(
    page_title="ImageWeave",
)

st.title("ImageWeave")
tab1 , tab2 = st.tabs(["Get Started" , "How to Use"])
with tab1:

    st.header("Welcome!")
    st.divider()
    st.subheader(":blue[ImageWeave is a minimal texture Generator. It let's you create any image you want to a map.]") 

with tab2:
    st.header("How to Use.")
    st.subheader(":blue[Upload your image using the Upload mode on left. Then choose the map you want and enjoy the generated image on our Gallery!]")
    st.divider()
    st.header("Dont have an image?")
    st.subheader(":blue[Dont worry we got photos for you! Just select an image from our Gallery by choosing the mode on the left and downloading it.]") 

st.sidebar.success("Select a mode above.")
