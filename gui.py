import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from paddleocr import PaddleOCR, draw_ocr
import os

# Hardcoded paths to model and dictionary
model_path = "C:\\Users\\aditi\\Desktop\\paddle\\best_model"  # Update with your actual model directory path
dict_path = "C:\\Users\\aditi\\Desktop\\paddle\\en_dict.txt"  # Update with your actual dictionary file path

# Function to initialize OCR with hardcoded paths
def initialize_ocr():
    return PaddleOCR(
        rec_model_dir=model_path,  # Use hardcoded path for model
        use_angle_cls=True,
        lang='en',
        e2e_char_dict_path=dict_path  # Use hardcoded path for dictionary
    )

# Browse for image file
def browse_image():
    img_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    if img_path:
        # Update image label with selected image
        img = Image.open(img_path).convert('RGB')
        update_image_label(img)
        process_button.config(state="normal")
        
        # Save file path for later use
        browse_image.img_path = img_path

# Function to update the image label with the selected image
def update_image_label(img):
    img.thumbnail((root.winfo_width(), root.winfo_height()))  # Resize image to fit the window
    img_display = ImageTk.PhotoImage(img)
    image_label.config(image=img_display)
    image_label.image = img_display

# Process the image and apply OCR
def process_image():
    try:
        # Initialize OCR with the hardcoded paths
        ocr = initialize_ocr()
        
        # Get image path
        img_path = browse_image.img_path
        
        # Perform OCR on the image
        result = ocr.ocr(img_path, cls=True)
        
        # Draw the result
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result[0]]
        txts = [line[1][0] for line in result[0]]
        scores = [line[1][1] for line in result[0]]
        
        # Draw the OCR result on the image
        font_path = "C:\\Windows\\Fonts\\Arial.ttf"  # Adjust font path for Windows
        im_show = draw_ocr(image, boxes, txts, scores, font_path=font_path)
        im_show = Image.fromarray(im_show)
        
        # Save the result image
        result_path = os.path.join(os.path.dirname(img_path), "result.jpg")
        im_show.save(result_path)
        
        # Display the result image
        display_result_image(result_path)

        # Show success message
        messagebox.showinfo("Success", f"OCR result saved as 'result.jpg' at {os.path.dirname(img_path)}")
    
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to display the result image on the UI
def display_result_image(result_path):
    try:
        # Open the result image
        result_image = Image.open(result_path).convert('RGB')
        update_image_label(result_image)
    except Exception as e:
        messagebox.showerror("Error", f"Could not display result image: {str(e)}")

# Set up the main window
root = tk.Tk()
root.title("OCR Image Processing")

# Set the initial window size, but it will be dynamically adjusted
root.geometry("800x600")  # Default window size (you can change this)

# Label to display selected image
image_label = tk.Label(root)
image_label.pack(pady=20, expand=True, fill='both')

# Button to browse and select an image
browse_button = tk.Button(root, text="Browse Image", command=browse_image)
browse_button.pack(pady=10)

# Button to process the image
process_button = tk.Button(root, text="Process Image", command=process_image, state="disabled")
process_button.pack(pady=10)

# Label to display the result image
result_image_label = tk.Label(root)
result_image_label.pack(pady=20, expand=True, fill='both')

# Run the Tkinter event loop
root.mainloop()
