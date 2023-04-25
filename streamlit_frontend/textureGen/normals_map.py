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
