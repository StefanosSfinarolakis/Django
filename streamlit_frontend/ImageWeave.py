import streamlit as st

st.set_page_config(
    page_title="ImageWeave",
)

st.title("ImageWeave")
tab1 , tab2, tab3 = st.tabs(["Get Started" , "How to Use" , "About"])
with tab1:

    st.header(":red[Welcome!]")
    st.divider()
    st.subheader("ImageWeave is a minimal texture Generator. It let's you create any image you want to a map.") 

with tab2:
    st.header(":red[How to Use.]")
    st.subheader("Upload your image using the Upload mode on left. Then choose the map you want and enjoy the generated image on our Gallery!")
    st.divider()
    st.header(":red[Dont have an image?]")
    st.subheader("Dont worry we got photos for you! Just select an image from our Gallery by choosing the mode on the left and downloading it.")

with tab3:
    st.header(":red[PyxelCollective]")
    st.subheader("PyxelCollective is the creator of this app. The team consists of 3 members (Sfinarolakis Stefanos (front-end, documentation), Tripakis Nikolaos(documentation, front-end), Kafteranis Konstantinos(back-end, textureGen)).")
    st.divider()
    st.header(":red[Github and Documentation]")
    st.subheader("Github: https://github.com/PYxelcollective/Django")
    st.subheader("Documentation:http://127.0.0.1:3000/docs/_build/html/index.html")    

st.sidebar.success("Select a mode above.")
