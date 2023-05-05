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