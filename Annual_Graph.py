import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
import os
from natsort import natsorted
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.ensemble import RandomForestRegressor
import numpy as np

class Insight(ttk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.data = None
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
        message = ("The predicted sum that you are seeing "
                "is not 100% precisely the cost you will "
                "have next month. "
                "Please note that there "
                "could be an error margin of 1-15% based on the predicted value. Thank You").upper()
        
        messagebox.showinfo("ATTENTION", "It Would Be Best To Upload Numerous Files\nSo That The Program Will "
                                    "Have Sufficient Data To Analyze\n\n"+message)

        file_paths = filedialog.askopenfilenames(filetypes=[("Excel files", "*.xlsx;*.xls")])
        if file_paths:
            file_names = [os.path.splitext(os.path.basename(file))[0] for file in file_paths]
            total_sums = []

            for file_path in file_paths:
                data = pd.read_excel(file_path)
                total_sums.append(data['Total Cost'].sum())

            file_names, total_sums = zip(*natsorted(zip(file_names, total_sums)))
            self.train_model(len(file_names), total_sums)  # Train the model
            predicted_next_sum = self.predict_next_sum(len(file_names), total_sums)
            self.plot_data(file_names, total_sums, predicted_next_sum)


    def train_model(self, num_months, total_sums):
        X_train = np.arange(1, num_months+1).reshape(-1, 1) # No. of months/files
        y_train = np.array(total_sums) # Sums of each month

        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)

    def predict_next_sum(self, num_months, total_sums):
        next_feature = np.array([[num_months + 1]])  # Use the next month as the feature
        predicted_next_sum = self.model.predict(next_feature)

        return predicted_next_sum
    

    def plot_data(self, x_data, y_data, predicted_next_sum):
        plt.figure(figsize=(10, 6))

        plt.bar(np.arange(len(x_data)), y_data, color='#4C2A85', label='Total Sum per Month')

        plt.bar(len(x_data), predicted_next_sum, color='red', label='Predicted Next Total Cost')

        custom_labels = [f'{file}\n{total}' for file, total in zip(x_data, y_data)]

        plt.title('Total Cost per Month with Predicted Next Total Cost')
        plt.xlabel('Months')
        plt.ylabel('Total Sum')
        plt.xticks(np.arange(len(x_data) + 1), list(custom_labels) + [f' Predicted\nTotal Cost of Next Month \n{predicted_next_sum}'], rotation=45)
        plt.legend()

        canvas = FigureCanvasTkAgg(plt.gcf(), master=self.frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        plt.tight_layout()

        

    def reset(self):
        self.data = None
        for widget in self.frame.winfo_children():
            widget.destroy()
    


if __name__ == "__main__":
  root = tk.Tk()
  excel_plotter = Insight(root)
  root.mainloop()