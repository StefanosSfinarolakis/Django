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
