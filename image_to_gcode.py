import cv2
import numpy as np
import matplotlib.pyplot as plt

def image_to_gcode(image_path, output_gcode_path, threshold=100):
    # Load the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    
    # Apply edge detection
    edges = cv2.Canny(image, threshold, threshold * 2)
    
    # Invert the colors to get the outline
    outline = cv2.bitwise_not(edges)
    
    # Get the image dimensions
    height, width = outline.shape
    
    # Prepare G-code commands
    gcode_commands = []
    gcode_commands.append("G21 ; Set units to millimeters\n")
    gcode_commands.append("G90 ; Use absolute coordinates\n")
    gcode_commands.append("G0 Z5 ; Lift pen\n")
    
    # Traverse the image and generate G-code for outline
    for y in range(height):
        for x in range(width):
            if outline[y, x] == 255:
                gcode_commands.append(f"G1 X{x} Y{height - y} Z0 ; Move to ({x}, {height - y}) and draw\n")
            else:
                gcode_commands.append(f"G0 X{x} Y{height - y} Z5 ; Move to ({x}, {height - y}) without drawing\n")
    
    gcode_commands.append("G0 Z5 ; Lift pen\n")
    gcode_commands.append("M2 ; End of program\n")
    
    # Write G-code to file
    with open(output_gcode_path, 'w') as f:
        f.writelines(gcode_commands)
    
    return image, outline

# Define paths
image_path = 'C:/Users/ADMIN/Desktop/dverse/Carimage.jpg'  # Replace with your image path
output_gcode_path = 'output.gcode'

# Convert image to G-code and get the outline
original_image, outline_image = image_to_gcode(image_path, output_gcode_path)

# Display original and outline images
plt.figure(figsize=(10, 5))

# Original Image
plt.subplot(1, 2, 1)
plt.title("Original Image")
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
plt.axis('off')

# Outline Image
plt.subplot(1, 2, 2)
plt.title("G-code Outline")
plt.imshow(outline_image, cmap='gray')
plt.axis('off')

plt.show()
