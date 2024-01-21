import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import sys
from ttkbootstrap import Style

class QACheckerGUI:
    def __init__(self, master, error_file_path):
        self.master = master
        master.title("QA Checker GUI")

        self.error_data = None
        self.solution_data = None

        self.error_file_path = error_file_path

        # Create a ttkbootstrap style with the "superhero" theme
        self.style = Style(theme="superhero")

        self.create_widgets()

    
    def create_widgets(self):
        # Create a frame for the Treeview and Solution Display
        main_frame = ttk.Frame(self.master, padding=(10, 10, 10, 10))
        main_frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Create Treeview for displaying error codes and descriptions
        self.tree = ttk.Treeview(main_frame, columns=("Error Code", "Description", "Help"), show="headings")
        self.tree.heading("Error Code", text="Error Code")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Help", text="Help")
        self.tree.column("Help", width=50)  # Adjust the width as needed
        self.tree.grid(column=0, row=0, padx=10, pady=10, rowspan=2)  # Adjust the rowspan to extend over two rows

        # Create a separator line
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(column=0, row=2, sticky=(tk.W, tk.E), pady=10)

        # Create the Solution Display Area
        self.solution_display = scrolledtext.ScrolledText(main_frame, width=40, height=10, wrap=tk.WORD)
        self.solution_display.grid(column=0, row=3, padx=10, pady=10)  # Adjust the row to be below the separator

        # Load error and solution data
        self.load_data()

    def load_data(self):
        # Load error data from the provided error file
        with open(self.error_file_path, "r") as file:
            self.error_data = [line.strip().split(",") for line in file]

        # Load solution data from the dictionary file
        with open("dictionary_file.txt", "r") as file:
            self.solution_data = dict(line.strip().split(",") for line in file)

        # Display error data in the Treeview
        for error_code, description in self.error_data:
            self.tree.insert("", "end", values=(error_code, description, "Help"), tags=error_code)

        # Set up a binding for the help button
        self.tree.bind("<ButtonRelease-1>", self.show_solution)

    def show_solution(self, event):
        item_id = self.tree.identify_row(event.y)
        error_code = self.tree.item(item_id, "values")[0] if item_id else None

        if error_code and error_code in self.solution_data:
            solution = self.solution_data[error_code]
        else:
            solution = "No solution found."

        self.solution_display.delete(1.0, tk.END)
        self.solution_display.insert(tk.END, solution)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script_name.py <path_to_error_file>")
        sys.exit(1)

    error_file_path = sys.argv[1]

    root = tk.Tk()
    app = QACheckerGUI(root, error_file_path)
    root.mainloop()
