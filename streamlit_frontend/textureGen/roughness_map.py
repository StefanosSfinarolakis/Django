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
