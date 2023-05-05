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


