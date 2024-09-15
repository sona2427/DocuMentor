import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from PyPDF2 import PdfReader
import docx 
import csv

# Define the main folder path
main_folder_path = r"New folder/Documentor"
categories = {
    "Legal": "Legal Documents",
    "Education": "Education",
    "Info": "Information",
    "Personal": "Personal",
    "Fun": "Fun"
}

# Define keywords for each category (including Slogams)
category_keywords = {
    "Legal": ["contract", "agreement", "law", "court"],
    "Education": ["university", "course", "research", "study"],
    "Info": ["info", "data", "details", "report"],
    "Personal": ["diary", "letter", "memo", "personal"],
    "Fun": ["joke", "game", "entertainment", "fun"]
}


# Function to extract text from a PDF file
def extract_pdf_text(file_path):
    text = ""
    try:
        with open(file_path, "rb") as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except Exception as e:
        messagebox.showerror("Error", f"Error reading PDF: {e}")
    return text

# Function to extract text from a DOCX file
def extract_docx_text(file_path):
    text = ""
    try:
        doc = docx.Document(file_path)
        for para in doc.paragraphs:
            text += para.text
    except Exception as e:
        messagebox.showerror("Error", f"Error reading DOCX: {e}")
    return text

# Function to extract text from a TXT file
def extract_txt_text(file_path):
    text = ""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    except Exception as e:
        messagebox.showerror("Error", f"Error reading TXT: {e}")
    return text

# Function to categorize file based on its content
def categorize_file(file_path):
    file_extension = os.path.splitext(file_path)[1].lower()
    file_content = ""

    # Extract text based on the file extension
    if file_extension == ".pdf":
        file_content = extract_pdf_text(file_path)
    elif file_extension == ".docx":
        file_content = extract_docx_text(file_path)
    elif file_extension == ".txt":
        file_content = extract_txt_text(file_path)
    else:
        messagebox.showerror("Unsupported File", f"File type {file_extension} is not supported for categorization.")
        return
    
# Function to move the file to the chosen category
def move_file_to_category(file_path, folder_name):
    destination_folder = os.path.join(main_folder_path, folder_name)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    shutil.move(file_path, destination_folder)
    messagebox.showinfo("File Moved", f"File moved to {folder_name}")

# Function to upload and categorize files
def upload_file():
    global file_path  # Define file_path globally to use in folder selection
    file_path = filedialog.askopenfilename(
        title="Select a file to upload",
        filetypes=(("All files", "*.*"),)
    )
    if file_path:
        categorize_file(file_path)

# Function to display available folders
def display_folders():
    for widget in frame_buttons.winfo_children():
        widget.destroy()

    folders = [folder for folder in os.listdir(main_folder_path) if os.path.isdir(os.path.join(main_folder_path, folder))]
    
    if not folders:
        tk.Label(frame_buttons, text="No folders available", font=("Arial", 16)).pack(pady=20)
        return

    for folder in folders:
        btn = tk.Button(frame_buttons, text=folder, font=("Arial", 14), command=lambda f=folder: display_files(f))
        btn.pack(fill='x', pady=5)
def download_file(file_path):
    try:
        # Ask the user where to save the file
        save_path = filedialog.asksaveasfilename(
            initialfile=os.path.basename(file_path),
            title="Download File",
            defaultextension=os.path.splitext(file_path)[1],
            filetypes=(("All files", "*.*"),)
        )
        
        if save_path:
            shutil.copy(file_path, save_path)  # Copy file to the selected location
            messagebox.showinfo("Download", f"File downloaded to {save_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Error downloading file: {e}")


# Function to display files in the selected folder
def display_files(folder_name):
    folder_path = os.path.join(main_folder_path, folder_name)
    for widget in frame_buttons.winfo_children():
        widget.destroy()

    files = os.listdir(folder_path)
    if not files:
        tk.Label(frame_buttons, text="No files available", font=("Arial", 16)).pack(pady=20)
        return

    for file in files:
        file_path = os.path.join(folder_path, file)
        
        # Create a button for each file to view and download
        file_frame = tk.Frame(frame_buttons, bg="white", bd=2)
        file_frame.pack(fill='x', pady=5)

        file_label = tk.Label(file_frame, text=file, font=("Arial", 14))
        file_label.pack(side="left", padx=5)

        view_btn = tk.Button(file_frame, text="View", font=("Arial", 12), command=lambda f=file_path: open_file(f))
        view_btn.pack(side="left", padx=5)

        download_btn = tk.Button(file_frame, text="Download", font=("Arial", 12), command=lambda f=file_path: download_file(f))
        download_btn.pack(side="right", padx=5)

    # Back button to go back to folder view
    tk.Button(frame_buttons, text="Back to Folders", font=("Arial", 14), command=display_folders).pack(pady=10)


# Function to open and display file content
def open_file(file_path):
    try:
        if file_path.lower().endswith(('.txt', '.md')):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            messagebox.showinfo("File Content", content)
        elif file_path.lower().endswith('.pdf'):
            text = extract_pdf_text(file_path)
            messagebox.showinfo("File Content", text)
        elif file_path.lower().endswith('.docx'):
            text = extract_docx_text(file_path)
            messagebox.showinfo("File Content", text)
        else:
            messagebox.showerror("Error", "Unsupported file type for viewing.")
    except Exception as e:
        messagebox.showerror("Error", f"Error opening file: {e}")

# Main GUI Setup
root = tk.Tk()
root.title("Documentor")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}")

# Load background image
bg_image_path = "pic.jpg" 
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

# Create a frame for buttons
frame_buttons = tk.Frame(root, bg='black', bd=5)
frame_buttons.place(relx=0.5, rely=0.5, anchor='center')

# Upload Button
upload_btn = tk.Button(root, text="Upload", font=("Arial", 20), bg='blue', fg='white', command=upload_file)
upload_btn.pack(pady=10, side='left', padx=20)

# Access Button
access_btn = tk.Button(root, text="Access", font=("Arial", 20), bg='black', fg='white', command=display_folders)
access_btn.pack(pady=10, side='right', padx=20)

# Start the GUI
root.mainloop()
