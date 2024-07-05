import tkinter as tk
from tkinter import filedialog, messagebox

# Create the main application window
root = tk.Tk()
root.title("Basic Text Editor")

# Set a fixed window size to prevent resizing
root.geometry("800x600")  # Adjust as per your preference

# Global variables to track file state
text_widget = None
file_path = None
file_modified = False

# Function to mark the file as modified
def mark_as_modified(event=None):
    global file_modified
    file_modified = True
    file_menu.entryconfig("Save", state="normal")
    file_menu.entryconfig("Save As", state="normal")

# Function to create a new file
def new_file():
    global text_widget, file_path, file_modified
    if text_widget:
        text_widget.pack_forget()
    text_widget = tk.Text(root)
    text_widget.pack(expand=True, fill='both')
    text_widget.delete(1.0, tk.END)
    file_path = None
    file_menu.entryconfig("Save", state="normal")  # Enable the save button in the menu bar
    file_menu.entryconfig("Save As", state="normal")  # Enable the save as button in the menu bar
    file_modified = True

# Function to open an existing file
def open_file():
    global text_widget, file_path, file_modified
    if text_widget:
        text_widget.pack_forget()
    file_path = filedialog.askopenfilename()
    if file_path:
        text_widget = tk.Text(root)
        text_widget.pack(expand=True, fill='both')
        with open(file_path, 'r') as file:
            text_widget.insert(tk.END, file.read())
        file_menu.entryconfig("Save", state="normal")  # Enable the save button when a file is opened
        file_menu.entryconfig("Save As", state="normal")  # Enable the save as button when a file is opened
        file_modified = False

# Function to save the current file
def save_file():
    global file_path, file_modified
    if file_path is None:
        save_file_as()
    else:
        with open(file_path, 'w') as file:
            file.write(text_widget.get(1.0, tk.END))
        file_modified = False
        file_menu.entryconfig("Save", state="disabled")  # Disable save button after saving
        file_menu.entryconfig("Save As", state="disabled")  # Disable save as button after saving

# Function to save the current file as a new file
def save_file_as():
    global file_path, file_modified
    new_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                            filetypes=[("Text files", "*.txt"),
                                                       ("All files", "*.*")])
    if new_path:
        file_path = new_path
        with open(file_path, 'w') as file:
            file.write(text_widget.get(1.0, tk.END))
        file_modified = False
        file_menu.entryconfig("Save", state="disabled")  # Disable save button after saving
        file_menu.entryconfig("Save As", state="disabled")  # Disable save as button after saving

# Function to prompt save before closing
def on_closing():
    global file_modified
    if file_modified:
        result = messagebox.askyesnocancel("Save File", "Do you want to save your changes before closing?")
        if result is None:  # Cancel
            return
        elif result:  # Yes
            save_file()
    root.destroy()

# Create a menu bar for the main window
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file, state="disabled")  # Create a save button in the menu bar (initially disabled)
file_menu.add_command(label="Save As", command=save_file_as, state="disabled")  # Create a save as button (initially disabled)
menu_bar.add_cascade(label="File", menu=file_menu)

# Add the menu bar to the main window
root.config(menu=menu_bar)

# Bind the main window close event
root.protocol("WM_DELETE_WINDOW", on_closing)

# Bind the text widget to mark as modified on any key press
if text_widget:
    text_widget.bind("<<Modified>>", mark_as_modified)

# Run the application
root.mainloop()
