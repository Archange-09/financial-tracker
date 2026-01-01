import tkinter as tk
from tkinter import ttk
from Data_Entry import DataEntry
from Graph import Monthly_Graph
from Annual_Graph import Insight


class Main_UI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.protocol("WM_DELETE_WINDOW", self.on_close_check)
        self.image = tk.PhotoImage(file="logo.png", )
        self.image = self.image.subsample(6, 6)
        self.image_label = ttk.Label(self, image=self.image)
        self.image_label.grid(row=0, column=0, sticky="nw")  # Image is in column 0

        self.iconphoto(False, tk.PhotoImage(file="logo.png"))

        self.title("Expense Tracker")
        self.geometry(f"{1200}x{720}")
        self.style = ttk.Style(self)
        self.tk.call("source", "forest/forest-dark.tcl")
        self.style.theme_use("forest-dark")

        self.grid_rowconfigure(0, weight=0)  # weight for the title row
        self.grid_rowconfigure(1, weight=1)  # weight for the notebook row
        self.grid_columnconfigure(0, weight=1)

        # Title label with increased space below
        self.title_label = ttk.Label(self, image=self.image, text="Expense Tracker", compound="left",
                                     font=("Helvetica", 20, "bold"))
        self.title_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nw")

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Data Entry tab
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Data Entry")
        self.data_entry = DataEntry(tab1)

        # Monthly Graph tab
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Monthly Graph")
        self.graph = Monthly_Graph(tab2)

        # Annual Graph tab
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Annual Graph")
        self.prediction = Insight(tab3)

    def on_close_check(self):

        message = "Do You Want To Close The Program? \nPlease Export Data Before Closing"
        response = tk.messagebox.askyesnocancel("Confirmation", message, icon='warning')

        if response is True:
            if hasattr(self, 'data_entry') and isinstance(self.data_entry, DataEntry):
                self.data_entry.export_data()

            # Close the application after exporting
            self.destroy()
        elif response is False:
            # If the user chooses not to export, show a warning message
            tk.messagebox.showinfo("Warning", "Data was not exported. Closing application.")
            self.destroy()
        else:
            # cancel the closing
            pass


if __name__ == "__main__":
    app = Main_UI()
    app.mainloop()