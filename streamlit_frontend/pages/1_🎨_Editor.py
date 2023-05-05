import streamlit as st
from PIL import Image
import numpy as np
import requests
from io import BytesIO
from textureGen import height_map, normals_map, bump_map, ambient_occlusion_map, displacement_map, diffusion_map 
import base64

generated_images = []

# Title of the app
st.title("Image Maps Generator")

# URL of the Django app
django_url = "http://localhost:8000/"

# Define the options for the dropdown menu
options = ["Select category", "Floor", "Terrain", "Metal", "Other"]

# Upload an image
uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Check if an image was uploaded
if uploaded_image is not None:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Add a dropdown menu for selecting the category
    category = st.selectbox("Select category", options)

    # If the user has selected "Other", display a text input for a new category
    if category == "Other":
        category = st.text_input("Enter new category")

    # If the user has selected a category, display the form
    if category != "Select category":
        name = st.text_input("Name")
        caption = st.text_input("Caption")
        if st.button("Submit"):
            # Convert the image to a file-like object
            img_bytes = BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes.seek(0)

            # Submit the form data and the image to the Django app
            data = {
                "name": name,
                "category": category,
                "caption": caption,
            }
            files = {"image": ("image.jpg", img_bytes)}
            response = requests.post(django_url + "image-upload/", data=data, files=files)

            # Display the response from the Django app
            if response.ok:
                parent_image_id = response.json()["id"]
                print(response.content)###
                st.success("Image Map created!")
            else:
                st.error("Failed to create Image Map")



    # Sidebar menu to select the maps to generate
    st.sidebar.title("Select Maps")
    height_map_checkbox = st.sidebar.checkbox("Height Map")
    normals_map_checkbox = st.sidebar.checkbox("Normals Map")
    bump_map_checkbox = st.sidebar.checkbox("Bump Map")
    ambient_occlusion_map_checkbox = st.sidebar.checkbox("Ambient Occlusion Map")
    displacement_map_checkbox = st.sidebar.checkbox("Displacement Map")
    diffusion_map_checkbox = st.sidebar.checkbox("Diffusion Map")
    #generated_images = []

    # Generate and display the selected maps
    if st.button("Generate Maps"):
        def get_image_download_link(img, filename, text):
            pil_img = Image.fromarray(np.uint8(img))
            buffered = BytesIO()
            pil_img.save(buffered, format="JPEG", quality=100)
            img_str = base64.b64encode(buffered.getvalue()).decode()
            href = f'<a href="data:file/jpg;base64,{img_str}" download="{filename}">{text}</a>'
            return href
        # Convert the image to a numpy array
        img_array = np.array(image)

       # generated_images = []

        # Generate the height map
        if height_map_checkbox:
            height = height_map.generate_height_map(img_array)
            st.image(height, caption="Height Map", use_column_width=True)
            generated_images.append(("height_map", height))
            # Add a download button for the generated texture maps
            for map_type, image in generated_images:
                st.markdown(get_image_download_link(image, f"{name}_{map_type}.jpg", f"Download {map_type.capitalize()} Map"), unsafe_allow_html=True)

        # Generate the normals map
        if normals_map_checkbox:
            normals = normals_map.generate_normal_map(img_array)
            st.image(normals, caption="Normals Map", use_column_width=True)
            generated_images.append(("normals_map", normals))

        # Generate the bump map
        if bump_map_checkbox:
            bump = bump_map.generate_bump_map(img_array)
            st.image(bump, caption="Bump Map", use_column_width=True)
            generated_images.append(("bump_map", bump))

        # Generate the ambient occlusion map
        if ambient_occlusion_map_checkbox:
            ao = ambient_occlusion_map.generate_ambient_occlusion_map(img_array, 0.5)
            st.image(ao, caption="Ambient Occlusion Map", use_column_width=True)
            generated_images.append(("ambient_occlusion_map", ao))
            # Generate the displacement map
        if displacement_map_checkbox:
            displacement_map = displacement_map.generate_displacement_map(img_array)
            st.image(displacement_map, caption="Displacement Map", use_column_width=True)
            generated_images.append(("displacement_map", displacement_map))

        # Generate the diffusion map
        if diffusion_map_checkbox:
            diffusion_map = diffusion_map.generate_diffusion_map(img_array)
            st.image(diffusion_map, caption="Diffusion Map", use_column_width=True)
            generated_images.append(("diffusion_map", diffusion_map))
else:
    st.warning("Please upload an image")

# Gallery redirect
st.subheader("or select from our Gallery")
if st.button("Click me!"):
    js = f"window.location.href='http://localhost:8501/Gallery'"
    html = f"<head><meta http-equiv='refresh' content='0; URL=http://localhost:8501/Gallery' /></head>"
    st.markdown(html, unsafe_allow_html=True)