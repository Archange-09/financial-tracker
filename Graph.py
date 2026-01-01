import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class Monthly_Graph(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.fig = None
        self.canvas = None
        self.create_gui()

    def create_gui(self):
        self.style = ttk.Style(self.root)
        self.style.theme_use("forest-dark")

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.frame = ttk.Frame(main_frame, width=400, height=300)
        self.frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Frame for buttons below the graph
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side=tk.TOP, fill=tk.X)

        delete_button = ttk.Button(button_frame, text="Delete Graph", command=self.reset)
        delete_button.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.X)

        upload_button = ttk.Button(button_frame, text="Upload Excel Files", command=self.upload_and_plot)
        upload_button.pack(padx=5, pady=5, side=tk.RIGHT, fill=tk.X)

    def upload_and_plot(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_path:
            data = pd.read_excel(file_path)
            bill_names = data['Bill Name']
            total_costs = data['Total Cost']
            total_sum = total_costs.sum()
            
            file_name, _ = os.path.splitext(os.path.basename(file_path))  # Extract file name without extension
            self.plot_data(bill_names, total_costs, total_sum, file_name)  # Pass file_name

    def plot_data(self, x_data, y_data, total_sum, file_name):
        plt.figure(figsize=(10, 6))
        plt.bar(x_data, y_data, color='#4C2A85', zorder=2)

        title = f'Total Costs of Bills of {file_name} - Total Sum: $\\bf{{{total_sum}}}$'
        plt.title(title, fontsize=13)

        plt.xlabel('Bill Names')
        plt.ylabel('Total Cost')
        plt.xticks(rotation=45)
        plt.grid(axis='y')

        # Custom labels below x-axis
        custom_labels = [f'{file}\n{total}' for file, total in zip(x_data, y_data)]
        plt.gca().set_xticklabels(custom_labels, rotation=45, ha='right')

        plt.tight_layout()

        # Embedded Graph
        self.canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


    def reset(self):
        self.data = None
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    excel_plotter = Monthly_Graph(root)
    root.mainloop()
