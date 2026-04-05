import tkinter as tk
from tkinter import filedialog, messagebox
from processor import process_file


class DomainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Domain Extractor")

        # Input file
        tk.Label(root, text="Input File:").grid(row=0, column=0, padx=10, pady=5)
        self.input_entry = tk.Entry(root, width=40)
        self.input_entry.grid(row=0, column=1, padx=10)
        tk.Button(root, text="Browse", command=self.select_input_file).grid(row=0, column=2)

        # Output file
        tk.Label(root, text="Output File:").grid(row=1, column=0, padx=10, pady=5)
        self.output_entry = tk.Entry(root, width=40)
        self.output_entry.grid(row=1, column=1, padx=10)
        tk.Button(root, text="Save As", command=self.select_output_file).grid(row=1, column=2)

        # Column name
        tk.Label(root, text="Column Name:").grid(row=2, column=0, padx=10, pady=5)
        self.column_entry = tk.Entry(root, width=40)
        self.column_entry.insert(0, "Domain")  # default
        self.column_entry.grid(row=2, column=1, padx=10)

        # Run button
        tk.Button(root, text="Process", command=self.run_processing,
                  bg="green", fg="white").grid(row=3, column=1, pady=20)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel/CSV files", "*.xlsx *.xls *.csv")]
        )
        if file_path:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, file_path)

    def select_output_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")]
        )
        if file_path:
            self.output_entry.delete(0, tk.END)
            self.output_entry.insert(0, file_path)

    def run_processing(self):
        input_path = self.input_entry.get()
        output_path = self.output_entry.get()
        column_name = self.column_entry.get()

        if not input_path or not output_path:
            messagebox.showerror("Error", "Please select both input and output files.")
            return

        try:
            process_file(input_path, output_path, column_name)
            messagebox.showinfo("Success", "File processed successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))