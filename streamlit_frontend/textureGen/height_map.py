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
