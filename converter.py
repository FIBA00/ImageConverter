import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
import tkinter.filedialog

# Set appearance mode and default color theme
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Supported output formats
FORMATS = {
    "PNG": "png",
    "JPEG": "jpg",
    "BMP": "bmp",
    "WEBP": "webp",
    "GIF": "gif",
    "TIFF": "tiff"
}

def convert_batch():
    """
    Handle batch conversion of images to the selected format.
    Opens file dialog for selecting images, then destination folder,
    and converts all selected images to the chosen format.
    """
    # Use system file dialog
    files = tkinter.filedialog.askopenfilenames(
        title="Select Images to Convert",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.gif")]
    )

    if not files:
        return

    output_format = format_var.get()
    extension = FORMATS[output_format]

    # Get output directory using system file dialog
    out_dir = tkinter.filedialog.askdirectory(title="Select Output Folder")
    if not out_dir:
        return

    # Show progress in the UI
    progress_frame.pack(fill="x", padx=10, pady=10)
    progress_bar.set(0)
    status_label.configure(text="Converting images...")
    
    # Process files
    count = 0
    total = len(files)
    for i, file in enumerate(files):
        try:
            img = Image.open(file)
            base_name = os.path.splitext(os.path.basename(file))[0]
            save_path = os.path.join(out_dir, f"{base_name}.{extension}")
            img.save(save_path, format=output_format)
            count += 1
            
            # Update progress
            progress = (i + 1) / total
            progress_bar.set(progress)
            status_label.configure(text=f"Converting: {i+1}/{total}")
            root.update()
            
        except Exception as e:
            print(f"Failed to convert {file}: {e}")

    # Hide progress elements when done
    progress_frame.pack_forget()
    
    messagebox.showinfo("Conversion Complete", f"Converted {count} image(s) to {output_format}.")

# GUI setup
root = ctk.CTk()
root.title("Batch Image Converter")
root.geometry("450x350")
root.minsize(550, 650)

# Create main frame with padding
main_frame = ctk.CTkFrame(root)
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

# Header
header_label = ctk.CTkLabel(
    main_frame, 
    text="Image Converter", 
    font=ctk.CTkFont(size=24, weight="bold")
)
header_label.pack(pady=(0, 20))

# Format selection frame
format_frame = ctk.CTkFrame(main_frame)
format_frame.pack(fill="x", padx=10, pady=10)

format_label = ctk.CTkLabel(format_frame, text="Output Format:")
format_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

format_var = ctk.StringVar(value="PNG")
format_dropdown = ctk.CTkOptionMenu(
    format_frame,
    values=list(FORMATS.keys()),
    variable=format_var,
    width=120
)
format_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Progress indicators (hidden initially)
progress_frame = ctk.CTkFrame(main_frame)
progress_bar = ctk.CTkProgressBar(progress_frame)
progress_bar.pack(fill="x", padx=10, pady=(10, 5))
status_label = ctk.CTkLabel(progress_frame, text="")
status_label.pack(fill="x", padx=10, pady=(0, 10))
# Hide initially
progress_frame.pack_forget()

# Buttons
button_frame = ctk.CTkFrame(main_frame)
button_frame.pack(fill="x", padx=10, pady=20)

convert_button = ctk.CTkButton(
    button_frame,
    text="Select & Convert Images",
    command=convert_batch,
    height=40,
    font=ctk.CTkFont(size=14),
    fg_color="#2D7FF9",
    hover_color="#1E6FE6"
)
convert_button.pack(pady=10, fill="x")

exit_button = ctk.CTkButton(
    button_frame,
    text="Exit",
    command=root.destroy,
    height=40,
    font=ctk.CTkFont(size=14),
    fg_color="#F44336",
    hover_color="#D32F2F"
)
exit_button.pack(pady=10, fill="x")

# Credits at the bottom
credits_label = ctk.CTkLabel(
    main_frame,
    text="Image Converter v2.0",
    font=ctk.CTkFont(size=10),
    text_color="gray"
)
credits_label.pack(side="bottom", pady=(20, 0))

root.mainloop()
