import cv2
import numpy as np
from matplotlib import pyplot as plt

# Load the reference template image (what the image should look like)
template = cv2.imread('C:/Users/ADMIN/Desktop/dverse/square image.jpg', 0)  # Reference image in grayscale

# Load the captured image from the tactile board
captured_image = cv2.imread('C:/Users/ADMIN/Desktop/dverse/square image pixels 2.jpg', 0)  # Captured image in grayscale

# Display the original grayscale images for reference
plt.figure(figsize=(12, 8))
plt.subplot(131), plt.imshow(captured_image, cmap='gray')
plt.title('Grayscale Captured Image'), plt.xticks([]), plt.yticks([])

plt.subplot(132), plt.imshow(template, cmap='gray')
plt.title('Grayscale Template Image'), plt.xticks([]), plt.yticks([])

# Get the dimensions of the template
h, w = template.shape[:2]

# Perform template matching using cv2.TM_CCOEFF_NORMED
result = cv2.matchTemplate(captured_image, template, cv2.TM_CCOEFF_NORMED)

# Set a threshold for the match quality (1.0 is a perfect match)
threshold = 0.8
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# Initialize matched_image
matched_image = None

# If a match is found
if max_val >= threshold:
    print(f"Match found! Similarity: {max_val:.2f}")
    
    # Extract the top-left corner of the matched region
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    # Extract the matched region (this is the cropped grayscale part of the captured image)
    matched_image = captured_image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

    # Draw a rectangle around the matched region on the original captured image
    cv2.rectangle(captured_image, top_left, bottom_right, 255, 2)  # Draw rectangle in white color
else:
    print(f"Match not found. Similarity: {max_val:.2f}")

# Visualize the extracted grayscale region or a message
plt.subplot(133)
if matched_image is not None:
    plt.imshow(matched_image, cmap='gray')
    plt.title('Extracted Grayscale Region'), plt.xticks([]), plt.yticks([])
else:
    # Show a blank image or a message if no match was found
    plt.imshow(np.zeros_like(captured_image), cmap='gray')
    plt.title('No Match Found'), plt.xticks([]), plt.yticks([])

# Show all images
plt.show()