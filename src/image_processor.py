# src/image_processor.py

import cv2
import numpy as np
import random


def apply_preprocessing(image):
    """Applies brightness/contrast adjustment and sharpening."""
    # Contrast control (1.0 = no change)
    alpha = random.uniform(0.95, 1.05)
    # Brightness control (0 = no change)
    beta = random.randint(-10, 10)
    processed_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Sharpening kernel
    kernel = np.array([[0, -0.5, 0], [-0.5, 3, -0.5], [0, -0.5, 0]])
    processed_image = cv2.filter2D(processed_image, -1, kernel)

    return processed_image


def apply_postprocessing(image):
    """Applies Gaussian blur to the image."""
    return cv2.GaussianBlur(image, (5, 5), 0)
