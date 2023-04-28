import streamlit as st
from PIL import Image
import numpy as np
import cv2
from textureGen import height_map, normals_map, bump_map, ambient_occlusion_map

# Title of the app
st.title("Image Maps Generator")

# Upload an image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Check if an image was uploaded
if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

        # Define the options for the dropdown menu
    options = ["Select category", "Floor", "Terrain", "Metal", "Other"]

    # Add a dropdown menu for selecting the category
    category = st.selectbox("Select category", options)
   
    # If the user has selected "Other", display a text input for a new category
    if category == "Other":
        category = st.text_input("Enter new category")

    # If the user has selected a category, display the form
    if category != "Select category":
        name = st.text_input("Name")
        caption = st.text_input("Caption")
        category = st.write(f"Category: {category}")

    # Sidebar menu to select the maps to generate
    st.sidebar.title("Select Maps")
    height_map_checkbox = st.sidebar.checkbox("Height Map")
    normals_map_checkbox = st.sidebar.checkbox("Normals Map")
    bump_map_checkbox = st.sidebar.checkbox("Bump Map")
    ambient_occlusion_map_checkbox = st.sidebar.checkbox("Ambient Occlusion Map")

    # Generate and display the selected maps
    if st.button("Generate Maps"):
        # Convert the image to a numpy array
        img_array = np.array(image)

        # Generate the height map
        if height_map_checkbox:
            height = height_map.generate_height_map(img_array)
            st.image(height, caption="Height Map", use_column_width=True)

        # Generate the normals map
        if normals_map_checkbox:
            normals = normals_map.generate_normal_map(img_array)
            st.image(normals, caption="Normals Map", use_column_width=True)

        # Generate the bump map
        if bump_map_checkbox:
            bump = bump_map.generate_bump_map(img_array)
            st.image(bump, caption="Bump Map", use_column_width=True)

        # Generate the ambient occlusion map
        if ambient_occlusion_map_checkbox:
             ao = ambient_occlusion_map.generate_ambient_occlusion_map(img_array,0.5)
             st.image(ao, caption="Ambient Occlusion Map", use_column_width=True)
