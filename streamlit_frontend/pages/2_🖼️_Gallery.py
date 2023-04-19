import streamlit as st
import requests

# Set the base URL for the API calls
BASE_URL = "http://localhost:8000/"

# Define the function to retrieve a list of uploaded images
def get_image_list():
    # Send the GET request to the API endpoint
    response = requests.get(BASE_URL + "image-list/")
    # If the response is successful, return the JSON data
    if response.status_code == 200:
        return response.json()
    # If the response is not successful, return an empty list
    else:
        return []

# Define the function to display the list of uploaded images
def show_image_list():
    # Retrieve the list of uploaded images
    image_list = get_image_list()
    # Display the list of images
    if len(image_list) > 0:
        st.write("## List of Uploaded Images")
        for image in image_list:
            st.write("- **Name:**", image["name"])
            st.write("  **Caption:**", image["caption"])
            st.write("  **Category:**", image["category"])
            st.image(BASE_URL + image["image"], use_column_width=True)
    else:
        st.write("No images uploaded yet.")