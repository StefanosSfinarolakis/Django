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

