import streamlit as st
import requests
from PIL import Image
from io import BytesIO

BASE_URL = "http://localhost:8000/"
UPLOAD_URL = BASE_URL + "image-upload/"

# Define the Streamlit app pages
def upload_page():
    st.title("Upload Image")
    st.write("Please upload an image file")

    # Allow the user to upload an image
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(BytesIO(uploaded_file.read()))

        # Display the uploaded image
        st.image(image, caption="Uploaded image", use_column_width=True)

        # Allow the user to enter image information
        name = st.text_input("Name")
        caption = st.text_area("Caption")
        category = st.text_input("Category")

        # Allow the user to submit the image and information to the Django app
        if st.button("Submit"):
            data = {
                "name": name,
                "caption": caption,
                "category": category
            }
            files = {
                "image": uploaded_file.getvalue()
            }
            response = requests.post(UPLOAD_URL, data=data, files=files)

            if response.status_code == 200:
                st.success("Image uploaded successfully!")
            else:
                st.error("Error uploading image")

def view_page():
    st.title("View Images")
    st.write("This page is under construction.")

# Define the Streamlit app navigation
app_pages = {
    "Upload": upload_page,
    "View": view_page
}

# Define the Streamlit app sidebar
st.sidebar.title("Navigation")
selection = st.sidebar.radio("Go to", list(app_pages.keys()), index=0)

# Run the Streamlit app
app_pages[selection]()
