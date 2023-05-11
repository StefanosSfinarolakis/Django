front-end
===============

.. automodule:: Front-end
   :members:

Contents
-------
Front-end was created with streamlit. The Folder contains : pages, textureGen

pages
------

ImageWeave
~~~~~~

.. code-block:: python

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
      st.subheader("PyxelCollective is the creator of this app. The team consists of 3 members (Sfinarolakis Stefanos (front-end), Tripakis Nikos(design,documentation), Kafteranis Konstantinos(back-end.textureGen)).")
      st.divider()
      st.header(":red[Github and Documentation]")
      st.subheader("Github: https://github.com/PYxelcollective/Django")
      st.subheader("Documentation:")    

   st.sidebar.success("Select a mode above.")

This is a Python script that uses the Streamlit library to create a web application for ImageWeave.

The st.set_page_config function sets the page title to "ImageWeave".

The st.title function sets the main title of the web page to "ImageWeave".

The st.tabs function creates tabs for "Get Started", "How to Use", and "About". The contents of each tab are defined within a with tab: block.

Within the with tab: block, st.header is used to create a header, and st.subheader is used to create a subheader. st.divider() is used to create a horizontal line separator.

The st.sidebar.success function sets the content of the sidebar to "Select a mode above".

app
~~~~~~
.. code-block:: python

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

This is a Streamlit app that generates different types of image maps from an uploaded image.

The app first displays a file uploader that allows the user to upload an image. Then, it shows a dropdown menu where the user can select the category of the image. If the user selects "Other," a text input appears so they can enter a new category. After the user selects a category, they can enter a name and caption for the image.

The app also has a sidebar menu that allows the user to select which maps they want to generate: height map, normals map, bump map, and ambient occlusion map. After the user selects the maps they want, they can click the "Generate Maps" button to generate and display the maps.

To generate the maps, the app uses functions from the textureGen module, which contains functions for generating different types of image maps, such as height maps and normal maps. The app converts the uploaded image to a NumPy array, passes it to the appropriate function to generate the selected map, and displays the resulting map using Streamlit's st.image() function.

Editor
~~~~~~~~~
.. code-block:: python

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

It looks like this is a Streamlit app for generating image maps. The user can upload an image, select a category, and generate different types of texture maps from the uploaded image. The app also has a button to redirect to a gallery page. Here's a brief summary of what the code is doing:

Import necessary libraries

Define a list to store generated images

Set the title of the Streamlit app to "Image Maps Generator"

Define the URL of the Django app to submit the image data

Create a dropdown menu to select the category of the image

If the category is "Other", add a text input field for the new category name

If a category is selected, add text input fields for image name and caption, and a button to submit the form

If an image is uploaded, display the uploaded image and show the sidebar menu to select the maps to generate

If the "Generate Maps" button is clicked, generate the selected maps and display them, and add a download button for each generated map

If no image is uploaded, display a warning message

Add a button to redirect to the gallery page.

Gallery
~~~~
.. code-block:: python

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
               image_url = BASE_URL + image["image"]
               image_data = requests.get(image_url).content
               key = f"{image['name']}-{image['caption']}"
               st.image(image_url, use_column_width=True)
               st.download_button(label="Download", data=image_data, file_name=image["name"]+".jpg", mime="image/png", key=key)
               st.write(" Name:", image["name"])
               st.write("  Caption:", image["caption"])
               st.write("  Category:", image["category"])
      else:
         st.write("No images uploaded yet.")

   def load_view():
      count=0 
      add_selectbox = st.sidebar.selectbox("Select Category",("All","Floor","Terrain","Metal","Other"))

      if add_selectbox == "All":
         show_image_list()

      else:
         image_list = get_image_list()
         if len(image_list) > 0:
               st.write("## List of Uploaded Images")
               for image in image_list:
                  if image["category"]==add_selectbox:
                     count+=1
                     image_url = BASE_URL + image["image"]
                     image_data = requests.get(image_url).content
                     key = f"{image['name']}-{image['caption']}"
                     st.image(image_url, use_column_width=True)
                     st.download_button(label="Download", data=image_data, file_name=image["name"]+".jpg", mime="image/png", key=key)
                     st.write(" Name:", image["name"])
                     st.write("  Caption:", image["caption"])
                     st.write("  Category:", image["category"])
               if count==0:
                  st.write("No images in this category.")

   if __name__ == '__main__':
      load_view()
               
This is a Python script that creates a web interface using Streamlit library to display a list of uploaded images and allows the user to filter them by category and download them.

The script starts by importing the necessary libraries, which are Streamlit and Requests. The base URL for the API calls is set to "http://localhost:8000/".

There are two functions defined in this script:

get_image_list(): This function sends a GET request to the API endpoint and retrieves a list of uploaded images. If the response is successful, the JSON data is returned. Otherwise, an empty list is returned.

show_image_list(): This function retrieves the list of uploaded images using the get_image_list() function. It then displays the list of images along with their name, caption, category, and download button. If no images are uploaded, it displays a message saying "No images uploaded yet."

The load_view() function is the main function that creates the web interface. It first creates a select box in the sidebar that allows the user to filter the images by category. If the user selects "All", it calls the show_image_list() function to display all uploaded images. If the user selects a specific category, it filters the images by that category and displays them along with their details and download button. If there are no images in that category, it displays a message saying "No images in this category."

Finally, the __name__ == '__main__' condition checks if the script is being executed as the main program and calls the load_view() function.

textureGen
-----------

ambientocclusionmap
~~~~~~~~~~
.. code-block:: python

   import cv2
   import numpy as np


   def generate_ambient_occlusion_map(image, bias):
      """
      Generates an ambient occlusion map from an input image.
      """
      # Convert image to grayscale
      grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Normalize the grayscale image to [0, 1]
      normalized = grayscale / 255.0

      # Create a depth map from the normalized image
      depth_map = cv2.Laplacian(normalized, cv2.CV_64F)

      # Compute the ambient occlusion map from the depth map
      kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
      occlusion_map = np.ones_like(depth_map)
      for i in range(3):
         dilated = cv2.dilate(normalized, kernel, iterations=i)
         occlusion_map -= dilated
      occlusion_map = np.clip(occlusion_map + depth_map, 0, 1)

      # Normalize the occlusion map to [0, 255]
      occlusion_map = (occlusion_map * 255).astype(np.uint8)

      # Apply bias to the occlusion map
      occlusion_map = cv2.addWeighted(occlusion_map, 1 - bias, np.zeros_like(occlusion_map), bias, 0)

      return occlusion_map

generate_ambient_occlusion_map generates an ambient occlusion map from the input image.


bumpmap
~~~~~~~~~~~~
.. code-block:: python
   
   import cv2
   import numpy as np


   def generate_bump_map(image):
      """
      Generates a bump map from an input image.
      """
      # Convert image to grayscale
      grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Calculate the gradient of the grayscale image
      gradient_x = cv2.Sobel(grayscale, cv2.CV_64F, 1, 0)
      gradient_y = cv2.Sobel(grayscale, cv2.CV_64F, 0, 1)

      # Normalize the gradient
      magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
      gradient_x /= magnitude
      gradient_y /= magnitude

      # Adjust the range of the gradient to [0, 255]
      gradient_x = 0.5 * (gradient_x + 1.0) * 255
      gradient_y = 0.5 * (gradient_y + 1.0) * 255

      # Apply a Sobel filter to the grayscale image to calculate the edges
      edges = cv2.Sobel(grayscale, cv2.CV_64F, 1, 1)

      # Combine the edges and the gradient to create a bump map
      bump_map = np.sqrt(edges**2 + gradient_x**2 + gradient_y**2)

      # Normalize the bump map to [0, 255]
      bump_map = (bump_map / bump_map.max()) * 255

      # Convert the bump map to an 8-bit image and return it
      bump_map = bump_map.astype(np.uint8)
      return bump_map

generate_bump_map generates a bump map from the input image.

diffusionmap
~~~~~~~~~~~
.. code-block:: python

   import cv2
   import numpy as np

   def generate_diffusion_map(image):
      # Convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Apply bilateral filtering to the grayscale image
      filtered = cv2.bilateralFilter(gray, 9, 75, 75)

      # Compute the difference between the filtered image and the grayscale image
      diff = cv2.absdiff(filtered, gray)

      # Normalize the difference to the range [0, 255]
      diff_norm = cv2.normalize(diff, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

      # Create the diffusion map by setting the x and y channels to the difference
      diffusion_map = cv2.merge((diff_norm, diff_norm, np.full_like(diff_norm, 255, dtype=np.uint8)))

      return diffusion_map

The generate_diffusion_map function takes in an RGB image and returns a diffusion map.

displacementmap
~~~~~~~~~~~~~~~
.. code-block:: python
   
   import cv2
   import numpy as np

   def generate_displacement_map(image):
      # Convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Apply Laplacian edge detection
      laplacian = cv2.Laplacian(gray, cv2.CV_64F)

      # Normalize the Laplacian to the range [0, 255]
      laplacian_norm = cv2.normalize(laplacian, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

      # Create the displacement map by setting the x and y channels to the Laplacian
      displacement_map = cv2.merge((laplacian_norm, laplacian_norm, np.full_like(laplacian_norm, 255, dtype=np.uint8)))

      return displacement_map

The generate_displacement_map function takes an input image and generates a displacement map.

heightmap
~~~~~~~~~~~~~~
.. code-block:: python
   
   import cv2
   import numpy as np

   def generate_height_map(image):
      # Convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Apply Sobel edge detection in the x and y directions
      sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
      sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

      # Compute the gradient magnitude
      magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

      # Normalize the magnitude to the range [0, 255]
      normalized_magnitude = cv2.normalize(magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

      # Invert the image so that white areas correspond to higher heights
      inverted = cv2.bitwise_not(normalized_magnitude)

      return inverted

This function generates a height map from an input image by computing the gradient magnitude of the image using Sobel edge detection in the x and y directions. The resulting magnitude image is then normalized to the range [0, 255] and inverted so that white areas correspond to higher heights.

The generated height map can be used to simulate a 3D terrain from a 2D image, where the height of each point on the terrain corresponds to the intensity of the corresponding pixel on the height map. This technique is commonly used in video games and other computer graphics applications to generate realistic-looking terrain.

loadimage
~~~~~~~~~~~~~
.. code-block:: python
   
   import cv2

   def load_image(file_path):
      img = cv2.imread(file_path)
      return img

normals_map
~~~~~~~~~~~~~
.. code-block:: python

   import cv2
   import numpy as np

   def generate_normal_map(image):
      # Convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Apply Sobel edge detection in the x and y directions
      sobel_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
      sobel_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)

      # Compute the normal vectors
      normal_x = cv2.normalize(sobel_x, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
      normal_y = cv2.normalize(sobel_y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
      normal_z = np.full_like(normal_x, 255, dtype=np.uint8)

      # Combine the normal vectors into a 3-channel image
      normal_map = cv2.merge((normal_x, normal_y, normal_z))

      return normal_map

This code generates a normal map from an input image. 

roughnessmap
~~~~~~~~~~~~~~~~
.. code-block:: python
   
   import cv2
   import numpy as np

   def generate_roughness_map(image):
      # Convert the image to grayscale
      gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Apply the Laplacian operator
      laplacian = cv2.Laplacian(gray, cv2.CV_64F)

      # Compute the variance of the Laplacian
      variance = np.var(laplacian)

      # Normalize the variance to the range [0, 255]
      normalized_variance = cv2.normalize(variance, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)

      # Invert the image so that white areas correspond to rough surfaces
      inverted = cv2.bitwise_not(normalized_variance)

      return inverted

The generate_roughness_map() function takes an input image and generates a roughness map based on the variance of the Laplacian of the grayscale version of the input image.

specularmap
~~~~~~~~~~~~~~
.. code-block:: python
   
   import cv2
   import numpy as np


   def generate_specular_map(image):
      """
      Generates a specular map from an input image.
      """
      # Convert image to grayscale
      grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

      # Apply a bilateral filter to smooth the image
      smoothed = cv2.bilateralFilter(grayscale, 9, 75, 75)

      # Calculate the gradient of the smoothed image
      gradient_x = cv2.Sobel(smoothed, cv2.CV_64F, 1, 0)
      gradient_y = cv2.Sobel(smoothed, cv2.CV_64F, 0, 1)

      # Normalize the gradient
      magnitude = np.sqrt(gradient_x**2 + gradient_y**2)
      gradient_x /= magnitude
      gradient_y /= magnitude

      # Calculate the specular map using the normalized gradient
      specular_map = np.power(np.maximum(0, gradient_y), 4)

      # Normalize the specular map to [0, 255]
      specular_map = (specular_map / specular_map.max()) * 255

      # Convert the specular map to an 8-bit image and return it
      specular_map = specular_map.astype(np.uint8)
      return specular_map

This code defines a function generate_specular_map that takes an input image as a parameter and returns a specular map.




