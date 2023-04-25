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

