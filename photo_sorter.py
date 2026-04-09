import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

try:
    from PIL import Image, ImageTk
except ImportError:
    raise SystemExit(
        "Pillow is not installed. Please install it first with: pip install Pillow"
    )

SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".tif"}


class PhotoSorterApp:
    def __init__(self, root: tk.Tk, source_folder: str):
        self.root = root
        self.source_folder = source_folder
        self.image_paths = self._collect_images(source_folder)
        self.current_index = 0

        self.root.title("Photo Sorter")
        self.root.geometry("1400x800")
        self.root.configure(bg="black")

        # Info label at the top
        self.info_label = tk.Label(
            root,
            text="",
            fg="white",
            bg="black",
            font=("Segoe UI", 12)
        )
        self.info_label.pack(side=tk.TOP, fill=tk.X, padx=10, pady=8)

        # Main frame for listbox and image
        main_frame = tk.Frame(root, bg="black")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

        # Left side: Listbox with filenames
        list_frame = tk.Frame(main_frame, bg="black", width=200)
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)

        list_label = tk.Label(list_frame, text="Remaining Photos:", fg="white", bg="black", font=("Segoe UI", 10))
        list_label.pack(fill=tk.X, pady=5)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.file_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            bg="#333",
            fg="white",
            font=("Segoe UI", 9),
            selectmode=tk.SINGLE
        )
        self.file_listbox.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        scrollbar.config(command=self.file_listbox.yview)

        # Right side: Image
        self.image_label = tk.Label(main_frame, bg="black")
        self.image_label.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=5)

        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Configure>", self.on_resize)

        self.current_pil_image = None
        self.current_tk_image = None

        if not self.image_paths:
            messagebox.showinfo("No Photos", "No photos found in the selected folder.")
            self.root.destroy()
            return

        self._update_file_list()
        self.show_current_image()

    def _collect_images(self, folder: str):
        files = []
        for entry in os.listdir(folder):
            full_path = os.path.join(folder, entry)
            # Only files in root folder, no subdirectories
            if os.path.isfile(full_path):
                _, ext = os.path.splitext(entry)
                if ext.lower() in SUPPORTED_EXTENSIONS:
                    files.append(full_path)
        files.sort()
        return files

    def on_resize(self, _event):
        if self.current_pil_image is not None:
            self._render_current_image()

    def show_current_image(self):
        if self.current_index >= len(self.image_paths):
            messagebox.showinfo("Finished", "All photos have been processed.")
            self.root.destroy()
            return

        current_path = self.image_paths[self.current_index]
        filename = os.path.basename(current_path)
        remaining = len(self.image_paths)
        self.info_label.config(
            text=(
                f"Remaining: {remaining} photo(s)   "
                "→ Press 0-9 to move | ↑↓ = Navigate | ESC = Exit"
            )
        )

        try:
            self.current_pil_image = Image.open(current_path).convert("RGB")
        except Exception as exc:
            messagebox.showwarning("Error", f"Could not load image:\n{current_path}\n\n{exc}")
            self.current_index += 1
            self.show_current_image()
            return

        self._render_current_image()
        self._update_file_list()

    def _update_file_list(self):
        """Update the listbox with remaining filenames."""
        self.file_listbox.delete(0, tk.END)
        for i, path in enumerate(self.image_paths):
            filename = os.path.basename(path)
            self.file_listbox.insert(tk.END, filename)
        
        # Highlight current photo in the list
        if self.current_index < self.file_listbox.size():
            self.file_listbox.selection_set(self.current_index)
            self.file_listbox.see(self.current_index)

    def _render_current_image(self):
        if self.current_pil_image is None:
            return

        label_width = max(self.image_label.winfo_width(), 1)
        label_height = max(self.image_label.winfo_height(), 1)

        image = self.current_pil_image.copy()
        image.thumbnail((label_width, label_height), Image.Resampling.LANCZOS)

        self.current_tk_image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.current_tk_image)

    def on_key_press(self, event):
        if event.keysym == "Escape":
            self.root.destroy()
            return

        # Arrow keys for navigation
        if event.keysym == "Down":
            self.navigate_list(1)
            return
        elif event.keysym == "Up":
            self.navigate_list(-1)
            return

        # Number keys to move photos
        if not event.char or not event.char.isdigit():
            return

        digit = event.char
        self.move_current_image_to_digit_folder(digit)
        
        if self.image_paths:
            self.show_current_image()
        else:
            messagebox.showinfo("Finished", "All photos have been processed.")
            self.root.destroy()

    def navigate_list(self, direction: int):
        """Navigate in the listbox using arrow keys."""
        if not self.image_paths:
            return
        
        new_index = self.current_index + direction
        
        if 0 <= new_index < len(self.image_paths):
            self.current_index = new_index
            
            current_path = self.image_paths[self.current_index]
            try:
                self.current_pil_image = Image.open(current_path).convert("RGB")
                self._render_current_image()
                self._update_file_list()
            except Exception as exc:
                messagebox.showwarning("Error", f"Could not load image:\n{exc}")

    def move_current_image_to_digit_folder(self, digit: str):
        src = self.image_paths[self.current_index]
        target_dir = os.path.join(self.source_folder, digit)
        os.makedirs(target_dir, exist_ok=True)

        filename = os.path.basename(src)
        base, ext = os.path.splitext(filename)
        dest = os.path.join(target_dir, filename)

        counter = 1
        while os.path.exists(dest):
            dest = os.path.join(target_dir, f"{base}_{counter}{ext}")
            counter += 1

        shutil.move(src, dest)
        
        # Remove moved photo from the list
        self.image_paths.pop(self.current_index)
        
        # Set index to next photo or go back if at the end
        if self.current_index >= len(self.image_paths) and self.current_index > 0:
            self.current_index -= 1


def main():
    picker_root = tk.Tk()
    picker_root.withdraw()

    source_folder = filedialog.askdirectory(title="Select the photo folder")
    picker_root.destroy()

    if not source_folder:
        print("Cancelled: No folder selected.")
        return

    app_root = tk.Tk()
    PhotoSorterApp(app_root, source_folder)
    app_root.mainloop()


if __name__ == "__main__":
    main()
