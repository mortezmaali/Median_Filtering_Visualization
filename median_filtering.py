# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 23:03:01 2024

@author: Morteza
"""

import cv2
import numpy as np
import tkinter as tk

# Get the screen size using tkinter
root = tk.Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.withdraw()

# Set the desired block size
desired_block_size = 120

# Calculate the number of blocks that fit within the screen dimensions
image_size_x = screen_width // desired_block_size
image_size_y = screen_height // desired_block_size

# Adjust the block size to fit the screen exactly
block_size = min(screen_width // image_size_x, screen_height // image_size_y)

# Calculate the full image size based on the adjusted block size
full_image_size_x = image_size_x * block_size
full_image_size_y = image_size_y * block_size

# Create a random image
image = np.random.randint(0, 256, (image_size_y, image_size_x), dtype=np.uint8)

# Function to draw the image with large pixels and pixel values
def draw_large_pixels(image, highlight=None):
    large_image = np.zeros((full_image_size_y, full_image_size_x, 3), dtype=np.uint8)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            color = (image[i, j], image[i, j], image[i, j])
            large_image[i*block_size:(i+1)*block_size, j*block_size:(j+1)*block_size] = color
            # Add pixel value text
            cv2.putText(large_image, str(image[i, j]), 
                        (j*block_size + block_size//2 - 20, i*block_size + block_size//2 + 20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    if highlight:
        i, j, i_min, i_max, j_min, j_max = highlight
        cv2.rectangle(large_image, (j_min*block_size, i_min*block_size), 
                      (j_max*block_size, i_max*block_size), (0, 0, 255), 3)
    return large_image

# Function to apply the median filter dynamically
def apply_median_filter(image):
    filtered_image = image.copy()
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            i_min = max(i - 1, 0)
            i_max = min(i + 2, image.shape[0])
            j_min = max(j - 1, 0)
            j_max = min(j + 2, image.shape[1])
            # Extract the 3x3 neighborhood
            neighborhood = image[i_min:i_max, j_min:j_max]
            # Compute the median
            median_value = np.median(neighborhood)
            # Update the center of the neighborhood in the filtered image
            filtered_image[i, j] = median_value
            # Draw the large pixel image with the current 3x3 window highlighted
            large_image = draw_large_pixels(filtered_image, highlight=(i, j, i_min, i_max, j_min, j_max))
            # Display the image
            cv2.imshow('Dynamic Median Filter', large_image)
            cv2.waitKey(200)  # Wait for 200ms to slow down the dynamic effect
    return filtered_image

# Draw the initial image with large pixels
large_image = draw_large_pixels(image)
cv2.imshow('Dynamic Median Filter', large_image)
cv2.waitKey(1000)  # Wait for 1 second to show the initial image

# Apply the median filter dynamically
filtered_image = apply_median_filter(image)

# Show the final image
large_image = draw_large_pixels(filtered_image)
cv2.imshow('Dynamic Median Filter', large_image)
cv2.waitKey(0)  # Wait indefinitely until a key is pressed

# Destroy all OpenCV windows
cv2.destroyAllWindows()
