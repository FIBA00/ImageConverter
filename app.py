import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import os
from file_manager import CTkFileManagerModal
from config import FORMATS
from logger import get_logger

log = get_logger(__file__)

class ImageConverterApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Batch Image Converter")
        self.root.geometry("450x350")
        self.root.minsize(550, 650)
        
        self.format_var = ctk.StringVar(value="PNG")
        self.selected_files = []
        self.selected_folder = None
        
        self._create_widgets()
        log.info("ImageConverterApp initialized.")
        
    def _create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.header_label = ctk.CTkLabel(
            self.main_frame, 
            text="Image Converter", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.header_label.pack(pady=(0, 20))

        self.format_frame = ctk.CTkFrame(self.main_frame)
        self.format_frame.pack(fill="x", padx=10, pady=10)

        self.format_label = ctk.CTkLabel(self.format_frame, text="Output Format:")
        self.format_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        self.format_dropdown = ctk.CTkOptionMenu(
            self.format_frame,
            values=list(FORMATS.keys()),
            variable=self.format_var,
            width=120
        )
        self.format_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame)
        self.progress_bar.pack(fill="x", padx=10, pady=(10, 5))
        self.status_label = ctk.CTkLabel(self.progress_frame, text="")
        self.status_label.pack(fill="x", padx=10, pady=(0, 10))
        self.progress_frame.pack_forget()

        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(fill="x", padx=10, pady=20)

        self.select_file_button = ctk.CTkButton(
            self.button_frame,
            text="Select Image File(s)",
            command=self.select_files,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.select_file_button.pack(pady=10, fill="x")

        self.select_folder_button = ctk.CTkButton(
            self.button_frame,
            text="Select Destination Folder",
            command=self.select_folder,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.select_folder_button.pack(pady=10, fill="x")

        self.convert_button = ctk.CTkButton(
            self.button_frame,
            text="Convert",
            command=self.convert_images,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#2D7FF9",
            hover_color="#1E6FE6",
            state="disabled"
        )
        self.convert_button.pack(pady=10, fill="x")

        self.exit_button = ctk.CTkButton(
            self.button_frame,
            text="Exit",
            command=self.root.destroy,
            height=40,
            font=ctk.CTkFont(size=14),
            fg_color="#F44336",
            hover_color="#D32F2F"
        )
        self.exit_button.pack(pady=10, fill="x")

        self.info_label = ctk.CTkLabel(self.main_frame, text="No file or folder selected.", font=ctk.CTkFont(size=12))
        self.info_label.pack(pady=(10, 0))

        self.credits_label = ctk.CTkLabel(
            self.main_frame,
            text="Image Converter v2.2",
            font=ctk.CTkFont(size=10),
            text_color="gray"
        )
        self.credits_label.pack(side="bottom", pady=(20, 0))

    def select_files(self):
        log.info("Opening file selection dialog.")
        def on_files_selected(files):
            if files:
                self.selected_files = files
                log.info(f"Files selected: {self.selected_files}")
                self.update_info_label()
                self.check_conversion_readiness()

        file_modal = CTkFileManagerModal(
            self.root,
            select_mode="file",
            filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp *.tiff *.gif *.ico")],
            callback=on_files_selected
        )

    def select_folder(self):
        log.info("Opening folder selection dialog.")
        def on_folder_selected(folders):
            if folders:
                self.selected_folder = folders[0]
                log.info(f"Folder selected: {self.selected_folder}")
                self.update_info_label()
                self.check_conversion_readiness()

        folder_modal = CTkFileManagerModal(
            self.root, 
            select_mode="folder",
            callback=on_folder_selected
        )

    def update_info_label(self):
        if self.selected_files:
            file_text = f"{len(self.selected_files)} file(s) selected."
        else:
            file_text = "No files selected."
        folder_text = f"Destination: {self.selected_folder}" if self.selected_folder else "No destination selected."
        self.info_label.configure(text=f"{file_text}\n{folder_text}")

    def check_conversion_readiness(self):
        if self.selected_files and self.selected_folder:
            self.convert_button.configure(state="normal")
            log.info("Conversion is ready.")
        else:
            self.convert_button.configure(state="disabled")

    def convert_images(self):
        if not self.selected_files or not self.selected_folder:
            messagebox.showwarning("Missing Information", "Please select one or more files and a destination folder.")
            return

        self.perform_conversion(self.selected_files, self.selected_folder)

    def perform_conversion(self, files, out_dir):
        output_format = self.format_var.get()
        extension = FORMATS[output_format]
        log.info(f"Starting conversion to {output_format}.")
        
        self.progress_frame.pack(fill="x", padx=10, pady=10)
        self.progress_bar.set(0)
        self.status_label.configure(text="Converting images...")
        
        count = 0
        total = len(files)
        errors = []
        
        for i, file in enumerate(files):
            try:
                if not os.path.exists(file):
                    errors.append(f"File not found: {file}")
                    log.error(f"File not found: {file}")
                    continue
                    
                if not os.path.isfile(file):
                    errors.append(f"Not a file: {file}")
                    log.error(f"Not a file: {file}")
                    continue
                
                try:
                    img = Image.open(file)
                    img.verify()
                    img = Image.open(file)
                except Exception as e:
                    errors.append(f"Invalid image file {file}: {e}")
                    log.error(f"Invalid image file {file}: {e}")
                    continue
                
                base_name = os.path.splitext(os.path.basename(file))[0]
                save_path = os.path.join(out_dir, f"{base_name}.{extension}")
                
                if os.path.exists(save_path):
                    save_path = os.path.join(out_dir, f"{base_name}_converted.{extension}")
                
                if output_format == "ICO":
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")
                    if img.size != (256, 256):
                        img = img.resize((256, 256), Image.LANCZOS)
                    img.save(save_path, format="ICO", sizes=[(256, 256)])
                else:
                    img.save(save_path, format=output_format)
                
                count += 1
                log.info(f"Converted {file} to {save_path}")
                
                progress = (i + 1) / total
                self.progress_bar.set(progress)
                self.status_label.configure(text=f"Converting: {i+1}/{total}")
                self.root.update()
                
            except Exception as e:
                errors.append(f"Failed to convert {file}: {e}")
                log.error(f"Failed to convert {file}: {e}")
        
        self.progress_frame.pack_forget()
        
        if errors:
            error_message = f"Conversion completed with {len(errors)} error(s):\n\n" + "\n".join(errors[:5])
            if len(errors) > 5:
                error_message += f"\n... and {len(errors) - 5} more errors"
            messagebox.showwarning("Conversion Complete with Errors", error_message)
            log.warning(f"Conversion completed with {len(errors)} errors.")
        else:
            messagebox.showinfo("Conversion Complete", f"Successfully converted {count} image(s) to {output_format}.")
            log.info(f"Successfully converted {count} image(s) to {output_format}.")

    def run(self):
        log.info("Starting ImageConverterApp.")
        self.root.mainloop()