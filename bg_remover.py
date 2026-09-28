import os
import io
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
from PIL import Image
from rembg import remove

# ---------- Core removal function ----------
def remove_background(input_path, output_path):
    """
    Remove background from an image, preserving its original resolution.
    Returns (success, message).
    """
    try:
        with open(input_path, 'rb') as f:
            input_data = f.read()

        original_img = Image.open(io.BytesIO(input_data))
        original_size = original_img.size

        output_data = remove(input_data)
        result_img = Image.open(io.BytesIO(output_data))

        if result_img.size != original_size:
            result_img = result_img.resize(original_size, Image.LANCZOS)

        result_img.save(output_path, 'PNG')
        return True, f"Success! Saved to {output_path}"
    except Exception as e:
        return False, f"Error: {str(e)}"

# ---------- Tkinter GUI ----------
class BackgroundRemoverApp:
    def __init__(self, root):
        self.root = root
        self.root.title("High‑Resolution Background Remover")
        self.root.geometry("600x250")
        self.root.resizable(False, False)

        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Input
        tk.Label(self.root, text="Input Image:").grid(row=0, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.input_path, width=50).grid(row=0, column=1, padx=5, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=10)

        # Output
        tk.Label(self.root, text="Save As:").grid(row=1, column=0, padx=10, pady=10, sticky='w')
        tk.Entry(self.root, textvariable=self.output_path, width=50).grid(row=1, column=1, padx=5, pady=10)
        tk.Button(self.root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self.root, mode='indeterminate', length=400)
        self.progress.grid(row=2, column=0, columnspan=3, pady=10)

        # Remove button
        self.remove_btn = tk.Button(self.root, text="Remove Background", command=self.start_removal,
                                    bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        self.remove_btn.grid(row=3, column=0, columnspan=3, pady=10)

        # Status
        self.status_label = tk.Label(self.root, text="Ready", fg="blue")
        self.status_label.grid(row=4, column=0, columnspan=3, pady=5)

    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff")]
        )
        if filename:
            self.input_path.set(filename)
            base, _ = os.path.splitext(filename)
            self.output_path.set(f"{base}_no_bg.png")

    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if filename:
            self.output_path.set(filename)

    def start_removal(self):
        input_file = self.input_path.get().strip()
        output_file = self.output_path.get().strip()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        # Disable button and show progress
        self.remove_btn.config(state='disabled')
        self.status_label.config(text="Processing...", fg="orange")
        self.progress.start(10)

        # Run in background thread
        thread = threading.Thread(target=self.process_removal, args=(input_file, output_file))
        thread.daemon = True
        thread.start()

    def process_removal(self, input_file, output_file):
        success, message = remove_background(input_file, output_file)
        self.root.after(0, self.on_removal_done, success, message)

    def on_removal_done(self, success, message):
        self.progress.stop()
        self.remove_btn.config(state='normal')
        if success:
            self.status_label.config(text="Done!", fg="green")
            messagebox.showinfo("Success", message)
        else:
            self.status_label.config(text="Failed", fg="red")
            messagebox.showerror("Error", message)

# ---------- Run the app ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverApp(root)
    root.mainloop()