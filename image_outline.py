import os
import cv2
import numpy as np
from tkinter import Tk, Button, filedialog
from PIL import Image

def select_images():
    # Open a file dialog and select multiple images
    paths = filedialog.askopenfilenames(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    
    if len(paths) > 0:
        # Process each selected image
        for path in paths:
            process_and_save_image(path)

def select_folder():
    # Open a file dialog to select a folder
    folder_path = filedialog.askdirectory()
    
    if folder_path:
        # Process each image in the folder
        for filename in os.listdir(folder_path):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(folder_path, filename)
                process_and_save_image(image_path)

def process_and_save_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Edge detection using Canny
    edges = cv2.Canny(blurred, 50, 150)

    # Perform morphological operations to refine the edges
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.dilate(edges, kernel, iterations=1)
    edges = cv2.erode(edges, kernel, iterations=1)

    # Create a mask for the borders
    border_mask = np.zeros_like(image)
    border_mask[edges > 0] = [255, 255, 255]  # Make borders white

    # Convert to PIL format and save
    border_image = Image.fromarray(border_mask)

    # Create a directory to save the extracted border images
    save_dir = 'extracted_borders'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Get the base name of the original image (without the extension)
    base_name = os.path.splitext(os.path.basename(image_path))[0]

    # Save the border image as a PNG file
    save_path = os.path.join(save_dir, f'{base_name}_border.png')
    border_image.save(save_path)
    print(f"Image saved to {save_path}")

# Initialize the window toolkit and the root window
root = Tk()
root.title("Border Extraction Tool")
root.geometry("400x200")

# Create a button to select multiple images
select_images_button = Button(root, text="Select Images", command=select_images, font=("Helvetica", 14))
select_images_button.pack(pady=10)

# Create a button to select a folder
select_folder_button = Button(root, text="Select Folder", command=select_folder, font=("Helvetica", 14))
select_folder_button.pack(pady=10)

# Start the GUI
root.mainloop()
