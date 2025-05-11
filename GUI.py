import platform
import tkinter as tk
from tkinter import NW, Canvas, PhotoImage, filedialog, ttk
# Make sure Pillow is installed (pip install pillow)

import os
import sys

import PIL
from PIL import Image, ImageTk
from buildStrings import APP_ICON, APP_IMAGE

icon_path = APP_ICON


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class CSVSelectorGUI:
    def __init__(self, root, guiTitle, process_callback=None):
        self.root = root
        self.root.title(guiTitle)
        self.selected_files = ()
        self.root.geometry("600x500")

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready. Please select CSV files.")

        # Set window icon if provided
        embeddedIconPath = resource_path(icon_path)
        if not embeddedIconPath:
            embeddedIconPath = icon_path
        if embeddedIconPath and os.path.exists(embeddedIconPath):
            try:
                # Use PhotoImage for .gif, .pgm, .ppm formats
                if embeddedIconPath.lower().endswith(('.gif', '.pgm', '.ppm')):
                    icon = tk.PhotoImage(file=embeddedIconPath)
                    self.root.iconphoto(True, icon)
                # For other formats like .ico, .png, etc. (Windows/Linux)
                else:
                    # Try to use different methods based on platform
                    if platform.system() == "Windows":
                        self.root.iconbitmap(embeddedIconPath)
                    else:
                        # For Linux/Mac, convert icon to PhotoImage if possible
                        try:
                            from PIL import Image, ImageTk
                            icon = ImageTk.PhotoImage(
                                Image.open(embeddedIconPath))
                            self.root.iconphoto(True, icon)
                        except ImportError:
                            # If PIL is not available, ignore icon setting
                            print("ICON FAILED TO SET")
                            self.status_var.set("ICON FAILED TO SET")
                            pass
            except Exception as e:
                print(f"Warning: Could not set icon: {e}")

        # Set minimum window size
        self.root.minsize(500, 250)

        # Store the processing callback
        self.process_callback = process_callback

        # Variables to store file paths
        self.csv_file1 = tk.StringVar()
        self.csv_file2 = tk.StringVar()

        # Create a frame with padding
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        title_label = ttk.Label(main_frame, text="Select CSV Files for Processing",
                                font=("Helvetica", 14, "bold"))
        title_label.pack(pady=(0, 20))

        # First file selector
        file1_frame = ttk.Frame(main_frame)
        file1_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file1_frame, text="Source CSV Data:").pack(
            side=tk.LEFT, padx=(0, 10))

        file1_entry = ttk.Entry(
            file1_frame, textvariable=self.csv_file1, width=50)
        file1_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        file1_button = ttk.Button(file1_frame, text="Browse...",
                                  command=lambda: self.browse_file(self.csv_file1))
        file1_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Second file selector
        file2_frame = ttk.Frame(main_frame)
        file2_frame.pack(fill=tk.X, pady=5)

        ttk.Label(file2_frame, text="List of suppliers-country (CSV):").pack(
            side=tk.LEFT, padx=(0, 10))

        file2_entry = ttk.Entry(
            file2_frame, textvariable=self.csv_file2, width=50)
        file2_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        file2_button = ttk.Button(file2_frame, text="Browse...",
                                  command=lambda: self.browse_file(self.csv_file2))
        file2_button.pack(side=tk.RIGHT, padx=(10, 0))

        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(20, 0))

        # Process button
        self.process_button = ttk.Button(buttons_frame, text="Process Files",
                                         command=self.process_files)
        self.process_button.pack(side=tk.RIGHT, padx=5)

        # Exit button
        self.exit_button = ttk.Button(buttons_frame, text="Exit",
                                      command=self.root.destroy)
        self.exit_button.pack(side=tk.RIGHT, padx=5)

        status_bar = ttk.Label(
            root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_file(self, string_var):
        """Open file dialog and store the selected path"""
        filetypes = [("CSV files", "*.csv"), ("All files", "*.*")]
        filename = filedialog.askopenfilename(title="Select a CSV file",
                                              filetypes=filetypes)
        if filename:
            string_var.set(filename)
            self.status_var.set(f"Selected: {os.path.basename(filename)}")

    def process_files(self):
        """Handle the processing of selected files"""
        file1 = self.csv_file1.get()
        file2 = self.csv_file2.get()

        # Validate input
        if not file1 or not os.path.isfile(file1):
            self.status_var.set("Error: First CSV file is invalid!")
            return

        if not file2 or not os.path.isfile(file2):
            self.status_var.set("Error: Second CSV file is invalid!")
            return

        self.status_var.set("Processing files...")

        # Call the processing callback if provided
        if self.process_callback:
            try:
                self.process_callback(file1, file2)
                self.status_var.set("Processing complete!")
            except Exception as e:
                self.status_var.set(f"Error during processing: {str(e)}")
        else:
            # Store the files for retrieval if no callback
            self.selected_files = (file1, file2)


def runCSVguiProcessCallback(process_callback=None, guiTitle="CSVguiSelector"):
    """
    Launch the GUI and either:
    - Return the selected CSV files (if process_callback is None)
    - Pass selected files to the callback function (if provided)

    Args:
        process_callback: Function that takes two parameters (file1, file2)
                         and processes the CSV files

    Returns:
        Tuple of file paths if no callback provided, otherwise None
    """
    root = tk.Tk()
    app = CSVSelectorGUI(root, guiTitle, process_callback)

    # Large image/icon display
    # Replace with your image file
    embeddedImgPath = resource_path(icon_path)
    if not embeddedImgPath:
        embeddedImgPath = APP_IMAGE
    image = PIL.Image.open(embeddedImgPath)
    image = image.resize(
        (200, 200), PIL.Image.Resampling.LANCZOS)  # Resize to fit
    photo = PIL.ImageTk.PhotoImage(image)
    # Create a Label to hold the image
    image_label = tk.Label(root, image=photo)
    image_label.image = photo  # Keep a reference!

    # Place it at the top-left corner
    # image_label.place(x=0, y=0)
    image_label.pack(anchor='s')

    # canvas = Canvas(root,  width=400, height=400)
    # canvas.pack()

    # img = PhotoImage(file=APP_IMAGE)
    # canvas.create_image(10, 10, anchor=NW, image=img)

    root.mainloop()

    # Return the selected files if the process button was pressed and no callback was provided
    if process_callback is None and hasattr(app, 'selected_files'):
        return app.selected_files
    return None, None


# Example usage
if __name__ == "__main__":
    # Example processing function
    def example_process(file1, file2):
        print(f"Processing {file1} and {file2}")
        # Your processing logic would go here

    # Option 1: Get files and process them separately
    # csv_file1, csv_file2 = get_csv_files()
    # if csv_file1 and csv_file2:
    #     example_process(csv_file1, csv_file2)

    # Option 2: Pass a callback to process the files immediately
    runCSVguiProcessCallback(process_callback=example_process)
