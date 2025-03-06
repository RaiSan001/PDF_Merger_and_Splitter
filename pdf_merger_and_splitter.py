from operator import index
from importlib.metadata import files
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, simpledialog
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import os

class PDFapp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger/Splitter")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        self.root.configure(bg = "#f0f0f0")

        # Simple Styling
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", padding=6, font=('Segoe UI', 10), background="#4CAF50", foreground="white")
        self.style.map("TButton", background=[('active', '#45a049')])
        self.style.configure("TFrame", background="#f0f0f0")
        self.style.configure("TListbox", font=('Segoe UI', 10), background="white")

        self.selected_files = []

        self.ui_setup()

    def ui_setup(self):
        # Load icons
        self.icon_add = ImageTk.PhotoImage(Image.open("icons/add.png").resize((24, 24)))
        self.icon_merge = ImageTk.PhotoImage(Image.open("icons/merge.png").resize((24, 24)))
        self.icon_split = ImageTk.PhotoImage(Image.open("icons/split.png").resize((24, 24)))
        self.icon_extract = ImageTk.PhotoImage(Image.open("icons/extract.png").resize((24, 24)))

        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Toolbar frame
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=tk.X, pady=10)

        # Buttons with icons
        buttons = [
            (self.icon_add, "Add PDF", self.add_pdf),
            (self.icon_merge, "Merge PDF", self.merge_pdf),
            (self.icon_split, "Split PDF", self.split_pdf),
            (self.icon_extract, "Extract Pages", self.extract_pages)
        ]

        for icon, text, cmd in buttons:
            button = tk.Button(
                toolbar_frame,
                image=icon,
                text=text,
                compound=tk.LEFT,
                command=cmd,
                bg="#2196F3",
                fg="white",
                activebackground="#1976D2",
                activeforeground="white",
                font=('Segoe UI', 10),
                relief=tk.FLAT,
                padx=10,
                pady=5
            )
            button.pack(side=tk.LEFT, padx=5)

        # Listbox with scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(
            list_frame,
            bg="white",
            font=('Segoe UI', 10),
            selectbackground="#4CAF50",
            selectmode=tk.SINGLE
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.configure(yscrollcommand=scrollbar.set)

        # Reorder buttons
        reorder_frame = ttk.Frame(main_frame)
        reorder_frame.pack(pady=10)

        self.button_up = ttk.Button(reorder_frame, text="↑ Move Up", command=self.move_up)
        self.button_up.pack(side=tk.LEFT, padx=5)

        self.button_down = ttk.Button(reorder_frame, text="↓ Move Down", command=self.move_down)
        self.button_down.pack(side=tk.LEFT, padx=5)

        # Status bar
        self.status = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        # Custom styles
        self.style.configure("Accent.TButton", background="#2196F3", foreground="white")
        self.style.map("Accent.TButton", background=[('active', '#1976D2')])

    #function to add files
    def add_pdf(self):
        try:
            files = filedialog.askopenfilenames(title= "Select Files", filetypes= [("PDF Files", "*.pdf")])
            if files:
                self.selected_files.extend(files)
                self.update_listbox()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to add files: {str(e)}")

    #function to merge files
    def merge_pdf(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No file selected. Please attach files.")
            return

        output_path = filedialog.asksaveasfilename(defaultextension= ".pdf", filetypes= [("PDF Files", "*.pdf")])
        if not output_path:
            return

        try:
            merger = PdfMerger()
            for pdf in self.selected_files:
                merger.append(pdf)
            merger.write(output_path)
            merger.close()
            messagebox.showinfo("Success", "PDFs merged")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge: {str(e)}")


    #function to split files
    def split_pdf(self):
        if not self.selected_files:
            messagebox.showerror("Error", "No file selected. Please attach files.")
            return

        input_path = self.selected_files[0]
        output_dir = filedialog.askdirectory(title= "Select output folder")
        if not output_dir:
            return

        try:
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)

            # Split all pages
            for page_num in range(total_pages):
                writer = PdfWriter()
                writer.add_page(reader.pages[page_num])
                output_path = os.path.join(output_dir, f"page_{page_num + 1}.pdf")
                with open(output_path, "wb") as f:
                    writer.write(f)

            messagebox.showinfo("Success", f"Split into {total_pages} pages!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to split: {str(e)}")

    #function to extract pages
    def extract_pages(self):
        input_path = filedialog.askopenfilename(title= "Select PDF to extract pages", filetypes= [("PDF Files", "*.pdf")])
        if not input_path:
            return

        #get page number from user
        pages = tk.simpledialog.askstring("Pages", "Enter page numbers (e.g., 1,3,5):")
        if not pages:
            return

        #validating the pages
        try:
            page = [int(p.strip()) - 1 for p in pages.split(",")]
        except ValueError:
            messagebox.showerror("Error", "Invalid page numbers. Use commas (e.g., 1,3,5):")
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if not output_path:
            return

        #extracting pages
        try:
            reader = PdfReader(input_path)
            total_pages = len(reader.pages)

            # Validate page numbers
            for p in page:
                if p < 0 or p >= total_pages:
                    messagebox.showerror("Error", f"Page {p + 1} is out of range (1-{total_pages}).")
                    return

            writer = PdfWriter()
            for p in page:
                writer.add_page(reader.pages[p])

            with open(output_path, "wb") as f:
                writer.write(f)

            messagebox.showinfo("Success", "Pages extracted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract pages: {str(e)}")

    #function to update listbox
    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for file in self.selected_files:
            fname = os.path.basename(file)
            self.listbox.insert(tk.END, fname)


    #function to move file up
    def move_up(self):
        select = self.listbox.curselection()
        if not select:
            return

        index = select[0]
        if index > 0:
            self.selected_files[index], self.selected_files[index - 1 ] = self.selected_files[index - 1], self.selected_files[index]
            self.update_listbox()
            self.listbox.select_set(index - 1)

    # function to move file down
    def move_down(self):
        select = self.listbox.curselection()
        if not select:
            return

        index = select[0]
        if index < len(self.selected_files):
            self.selected_files[index], self.selected_files[index + 1] = self.selected_files[index + 1], self.selected_files[index]
            self.selected_files[index]
            self.update_listbox()
            self.listbox.select_set(index + 1)


root = tk.Tk()
app = PDFapp(root)
root.mainloop()