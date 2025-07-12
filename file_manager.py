import customtkinter as ctk
import os
from logger import get_logger

log = get_logger(__file__)

class CTkFileManagerModal(ctk.CTkToplevel):
    def __init__(self, master, select_mode="file", filetypes=None, callback=None):
        super().__init__(master)
        self.title("Select Files" if select_mode == "file" else "Select Folder")
        self.geometry("600x450")
        self.select_mode = select_mode
        self.filetypes = filetypes or [("All Files", "*.* ")]
        self.callback = callback
        self.current_path = os.path.expanduser("~")
        self.file_list = []
        self.selected_indices = set()
        self.focused_index = 0
        self.multi_select_mode = False

        self.transient(master)
        self.focus_set()
        self._create_widgets()
        self._load_current_directory()
        self.update()
        self.grab_set()
        log.info(f"FileManager initialized in {select_mode} mode.")

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        path_frame = ctk.CTkFrame(main_frame)
        path_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(path_frame, text="Path:").pack(side="left", padx=5)
        self.path_var = ctk.StringVar(value=self.current_path)
        self.path_entry = ctk.CTkEntry(path_frame, textvariable=self.path_var, width=400)
        self.path_entry.pack(side="left", padx=5, fill="x", expand=True)
        ctk.CTkButton(path_frame, text="Go", command=self._navigate_to_path, width=60).pack(side="left", padx=5)
        ctk.CTkButton(path_frame, text="Up", command=self._go_up, width=60).pack(side="left", padx=5)

        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        ctk.CTkLabel(list_frame, text="Files & Folders", font=ctk.CTkFont(weight="bold")).pack(pady=5)
        self.file_listbox = ctk.CTkTextbox(list_frame, wrap="none", height=15, cursor="hand2")
        self.file_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.file_listbox.configure(state="disabled")
        self.file_listbox.bind("<Button-1>", self._on_click)
        self.file_listbox.bind("<Double-Button-1>", self._on_double_click)
        self.file_listbox.bind("<Return>", self._on_enter)
        self.file_listbox.bind("<Up>", self._on_up)
        self.file_listbox.bind("<Down>", self._on_down)

        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(button_frame, text="Cancel", command=self.destroy, width=100).pack(side="right", padx=5)
        self.select_button = ctk.CTkButton(button_frame, text="Select", command=self._confirm_selection, width=100)
        self.select_button.pack(side="right", padx=5)

        if self.select_mode == 'file':
            self.multi_select_button = ctk.CTkButton(button_frame, text="Start Multi-Select", command=self._toggle_multi_select, width=140)
            self.multi_select_button.pack(side="right", padx=5)
        elif self.select_mode == 'folder':
            ctk.CTkButton(button_frame, text="Select Current", command=self._select_current_folder, width=120).pack(side="right", padx=5)

    def _load_current_directory(self):
        self.path_var.set(self.current_path)
        self.file_list = []
        try:
            items = os.listdir(self.current_path)
            log.info(f"Loading directory: {self.current_path}")
        except Exception as e:
            log.error(f"Error loading directory {self.current_path}: {e}")
            self.file_listbox.configure(state="normal")
            self.file_listbox.delete("1.0", "end")
            self.file_listbox.insert("end", f"Error: {e}\n")
            self.file_listbox.configure(state="disabled")
            return

        folders = sorted([(item, True) for item in items if os.path.isdir(os.path.join(self.current_path, item))])
        files = sorted([(item, False) for item in items if os.path.isfile(os.path.join(self.current_path, item)) and (self.select_mode != 'file' or self._is_image_file(item))])
        
        self.file_list = folders + files
        self.selected_indices.clear()
        self.focused_index = 0
        self._render_file_list()

    def _render_file_list(self):
        self.file_listbox.configure(state="normal")
        self.file_listbox.delete("1.0", "end")
        
        if not self.file_list:
            self.file_listbox.insert("end", "<empty>")
            self.file_listbox.configure(state="disabled")
            return

        for idx, (name, is_dir) in enumerate(self.file_list):
            icon = "📁" if is_dir else "🖼️"
            focus_char = ">" if idx == self.focused_index else " "
            select_char = "*" if idx in self.selected_indices else " "
            line_text = f"{focus_char}{select_char} {icon} {name}\n"
            self.file_listbox.insert("end", line_text)
        
        self.file_listbox.configure(state="disabled")
        self.file_listbox.see(f"{self.focused_index + 1}.0")

    def _toggle_multi_select(self):
        self.multi_select_mode = not self.multi_select_mode
        if self.multi_select_mode:
            log.info("Started multi-select mode.")
            self.multi_select_button.configure(text="Confirm Selection")
            self.select_button.configure(state="disabled")
        else:
            log.info("Ended multi-select mode.")
            self.multi_select_button.configure(text="Start Multi-Select")
            self.select_button.configure(state="normal")
            self._confirm_selection() # Confirm selection when mode is toggled off

    def _on_click(self, event):
        index = int(self.file_listbox.index(f"@{event.x},{event.y}").split('.')[0]) - 1
        if 0 <= index < len(self.file_list):
            self.focused_index = index
            if self.multi_select_mode:
                if index in self.selected_indices:
                    self.selected_indices.remove(index)
                else:
                    self.selected_indices.add(index)
            self._render_file_list()

    def _on_double_click(self, event):
        index = int(self.file_listbox.index(f"@{event.x},{event.y}").split('.')[0]) - 1
        if 0 <= index < len(self.file_list):
            name, is_dir = self.file_list[index]
            if is_dir:
                self.current_path = os.path.join(self.current_path, name)
                self._load_current_directory()

    def _on_enter(self, event):
        if self.file_list:
            self._confirm_selection()

    def _on_up(self, event):
        if self.file_list and self.focused_index > 0:
            self.focused_index -= 1
            self._render_file_list()

    def _on_down(self, event):
        if self.file_list and self.focused_index < len(self.file_list) - 1:
            self.focused_index += 1
            self._render_file_list()

    def _navigate_to_path(self):
        new_path = self.path_var.get().strip()
        if os.path.isdir(new_path):
            self.current_path = new_path
            self._load_current_directory()
            log.info(f"Navigating to: {new_path}")

    def _go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent != self.current_path:
            self.current_path = parent
            self._load_current_directory()
            log.info(f"Navigating up to: {parent}")

    def _select_current_folder(self):
        if self.callback:
            log.info(f"Current folder selected: {self.current_path}")
            self.callback([self.current_path])
        self.destroy()

    def _is_image_file(self, filename):
        image_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.webp', '.tiff', '.gif', '.ico'}
        return any(filename.lower().endswith(ext) for ext in image_extensions)

    def _confirm_selection(self):
        if not self.file_list:
            return

        if self.multi_select_mode:
            selected_paths = [os.path.join(self.current_path, self.file_list[i][0]) for i in self.selected_indices if not self.file_list[i][1]]
            if selected_paths:
                log.info(f"Confirmed multi-selection: {selected_paths}")
                if self.callback:
                    self.callback(selected_paths)
                self.destroy()
            return

        name, is_dir = self.file_list[self.focused_index]
        path = os.path.join(self.current_path, name)

        if is_dir:
            self.current_path = path
            self._load_current_directory()
        elif self.select_mode == 'file':
            log.info(f"Selected file: {path}")
            if self.callback:
                self.callback([path])
            self.destroy()
