import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import openpyxl


class DataEntry:
    def __init__(self, root):
        self.root = root
        self.setup_ui()

    def setup_ui(self):

        self.style = ttk.Style(self.root)

        self.style.theme_use("forest-dark")  # Default theme

        self.frame = ttk.Frame(self.root, width=1200, height=1000)
        self.frame.grid(row = 0, column=0)

        # Label
        self.widgets_frame = ttk.LabelFrame(self.frame, text="Insert Data", padding=20, height=50)
        self.widgets_frame.grid(row=0, column=0, padx=20, pady=10)

        def handle_placeholder(entry_or_combobox, placeholder_text):
            def on_focus_out(event):
                if not entry_or_combobox.get():
                    entry_or_combobox.insert(0, placeholder_text)

            def on_focus_in(event):
                if entry_or_combobox.get() == placeholder_text:
                    entry_or_combobox.delete('0', 'end')

            entry_or_combobox.insert(0, placeholder_text)
            entry_or_combobox.bind("<FocusOut>", on_focus_out)
            entry_or_combobox.bind("<FocusIn>", on_focus_in)

        
        row_val=0

        budget_title_label = ttk.Label(self.widgets_frame, text="Bill Types", font=("Arial", 12, "bold"))
        budget_title_label.grid(row=0, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)

        self.radio_var_category = tk.StringVar()  # Initialize radio_var_category
        self.radio_var_category.set("Essentials")  # Set the default radio button selection to "Essentials"


        # Bill Name/Type
        self.Essentials_combobox = ttk.Combobox(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.Essentials_combobox, "Essentials")
        self.Essentials_combobox['values'] = ['Groceries','Housing (Rent or Payment)','Allowance',
                                             'Electricity','Transportation','Gas','Water' 
                                             'Internet','Supplies','Payments','Utilities','--Insert Others--']  
        self.Essentials_combobox.grid(row=row_val+1, column=0, padx=5, pady=(0, 5), sticky="ew")
        

        # Bill Name/Type
        self.Miscellaneous_combobox = ttk.Combobox(self.widgets_frame, font=("Arial", 12))
        handle_placeholder(self.Miscellaneous_combobox, "Miscellaneous")
        self.Miscellaneous_combobox['values'] = ['Subscriptions','Shopping', 
                                                 'Apparel/Clothing', 'Meals','--Insert Others--']  
        self.Miscellaneous_combobox.grid(row=row_val + 1, column=0, padx=5, pady=(0, 5), sticky="ew")

        self.Miscellaneous_combobox.grid_remove()

        self.radio_var_category.set("Essentials")  # Default Radiobutton
        self.toggle_combobox()  


        # Radio button for Essentials
        self.radio_var_category = tk.StringVar()
        self.radio_var_category.set("Essentials")  # Default value
        self.radio_essentials = ttk.Radiobutton(
            self.widgets_frame, text="Show Essentials", variable=self.radio_var_category, value="Essentials", command=self.toggle_combobox)
        self.radio_essentials.grid(row=row_val + 2, column=0, padx=(5, 20), pady=5, sticky="w")

        # Radio button for Miscellaneous
        self.radio_miscellaneous = ttk.Radiobutton(
            self.widgets_frame, text="Show Miscellaneous", variable=self.radio_var_category, value="Miscellaneous", command=self.toggle_combobox)
        self.radio_miscellaneous.grid(row=row_val + 2, column=0, padx=(20, 5), pady=5, sticky="e")

        self.separator = ttk.Separator(self.widgets_frame)
        self.separator.grid(row=row_val+3, column=0, padx=(20, 10), pady=10, sticky="ew")


        # Currency selection for "Bill Type"
        self.currency_list = [
            "₱", # PHP
            "€",  # EUR
            "£",  # GBP
            "¥",  # JPY
            "$",  # USD
            "CNY(¥)",   # CNY
            "Insert",  # None
        ]
        # Creating a nested frame to hold the comboboxes
        nested_frame = ttk.Frame(self.widgets_frame)
        nested_frame.grid(row=row_val + 7, column=0, pady=5)

        # Currency selection Combobox
        self.currency_combobox = ttk.Combobox(
            nested_frame,
            values=self.currency_list,
            font=("Arial", 12),
            width=4
        )
        self.currency_combobox.current(0)  # Setting default selection
        self.currency_combobox.grid(row=0, column=0, padx=(1, 1), pady=5, sticky="w")

        # Cost Spinbox
        self.cost_combobox = ttk.Spinbox(
            nested_frame,
            from_=0,
            to=9999999999999999999,
            font=("Arial", 12),
            width=25
        )
        handle_placeholder(self.cost_combobox, "Cost")
        self.cost_combobox.grid(row=0, column=1, padx=(1, 1), pady=5, sticky="w")


        self.separator = self.create_separator(row_val+9, 0)


        budget_title_label = ttk.Label(self.widgets_frame, text="Budget Limit", font=("Arial", 12, "bold"))
        budget_title_label.grid(row=row_val+10, column=0, padx=5, pady=(10, 5), sticky="nsew", columnspan=2)  # Span across columns

        # Budget Limit
        self.budget_spinbox = ttk.Spinbox(self.widgets_frame, from_=0, to=9999999999999999999, font=("Arial", 12))
        handle_placeholder(self.budget_spinbox, "Set Budget")
        self.budget_spinbox.grid(row=row_val+11, column=0, padx=5, pady=5, sticky="ew")


        self.separator = self.create_separator(row_val+12, 0)


        # Add row
        self.button = ttk.Button(self.widgets_frame, text="Insert Row", command=self.insert_row, width=20)
        self.button.grid(row=row_val+13, column=0, padx=5, pady=5, sticky="nsew")

        self.separator = self.create_separator(row_val+14, 0)

        # Frame to group buttons
        button_group_frame = ttk.Frame(self.widgets_frame)
        button_group_frame.grid(row=row_val + 15, column=0, padx=5, pady=5, sticky="nsew")

        # Clear Table button
        self.clear_table_button = ttk.Button(button_group_frame, text="Clear Table", command=self.clear_table, width=20)
        self.clear_table_button.grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")

        # Delete button
        self.delete_button = ttk.Button(button_group_frame, text="Delete Row", command=self.delete_row, width=20)
        self.delete_button.grid(row=0, column=1, padx=(5, 0), pady=5, sticky="e")


        # Table
        self.treeFrame = ttk.Frame(self.frame, height=40)
        self.treeFrame.grid(row=0, column=1, pady=10)
        self.treeScroll = ttk.Scrollbar(self.treeFrame)
        self.treeScroll.pack(side="right", fill="y")

        self.treeview_style = ttk.Style()
        self.treeview_style.configure("Treeview", font=("Arial", 14))

        # Table Headings
        col = ("Bill Name", "Total Cost", "Type")
        self.treeview = ttk.Treeview(
            self.treeFrame, show="headings",
            yscrollcommand=self.treeScroll.set, columns=col, height=25, style="Treeview"
        )
        for c in col:
            self.treeview.heading(c, text=c, anchor="w", command=lambda c=c: self.treeview_sort_column(c, False))
            self.treeview.column(c, width=220, anchor='w')  # Adjust column width

        self.treeview.pack()
        self.treeScroll.config(command=self.treeview.yview)

        self.treeview_style = ttk.Style()
        self.treeview_style.configure("Treeview", font=("Arial", 13))  # Adjust font size

        # Alternate row colors
        self.treeview.tag_configure("oddrow", background="#2C3539")
        self.treeview.tag_configure("evenrow", background="#40404F")
        self.treeview.bind("<ButtonRelease-1>", self.update_row_colors)  # To update colors on selection

        
        # Total cost label
        self.sum_label = ttk.Label(self.frame, text="Total Cost: 0", font=("Arial", 14, "bold"))
        self.sum_label.grid(row=1, column=1, padx=5, pady=5, sticky="se")  # Placed on the lower right

        self.update_total_cost()  # Update total cost label initially

        self.separator = self.create_separator(row_val+16, 0)

        # Export button
        self.export_button = ttk.Button(self.widgets_frame, text="Export to Excel", command=self.export_data, width=20)
        self.export_button.grid(row=row_val+17, column=0, padx=5, pady=5, sticky="nsew")

        self.widgets_frame = ttk.LabelFrame(self.frame, text="Insert")
        self.widgets_frame.grid(row=0, column=0, padx=20, pady=10)



    def toggle_combobox(self):
        selected_category = self.radio_var_category.get()

        if selected_category == "Essentials":
            self.Essentials_combobox.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")
            self.Miscellaneous_combobox.grid_remove()  # Hide Miscellaneous combobox
        elif selected_category == "Miscellaneous":
            self.Miscellaneous_combobox.grid(row=1, column=0, padx=5, pady=(0, 5), sticky="ew")  # Show Miscellaneous combobox
            self.Essentials_combobox.grid_remove()  # Hide Essentials combobox


    def update_total_cost(self):
        selected_currency = self.currency_list[self.currency_combobox.current()]
        total_cost = sum(int(self.treeview.item(child)['values'][1]) for child in self.treeview.get_children())
        self.sum_label.config(text=f"Total Cost: {selected_currency} {total_cost}", font=("Arial", 14, "bold"))

        stated_budget_str = self.budget_spinbox.get()

        if stated_budget_str.strip() and stated_budget_str.isdigit():
            stated_budget = int(stated_budget_str)
            if total_cost > stated_budget:
                exceeded_amount = total_cost - stated_budget
                messagebox.showwarning("Budget Exceeded", f"Total cost has exceeded the stated budget by {selected_currency} {exceeded_amount}")
        elif not stated_budget_str.strip():
            messagebox.showinfo("No Budget", "No budget limit has been set.")

    # Export to Excel
    def export_data(self):
        columns = [self.treeview.heading(col)['text'] for col in self.treeview['columns']]

        new_workbook = openpyxl.Workbook()
        new_sheet = new_workbook.active

        new_sheet.append(columns)

        self.update_total_cost()  # Update total cost label after exporting data

        for child in self.treeview.get_children():
            values = [self.treeview.item(child)['values']]
            new_sheet.append(values[0])

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

        if file_path:  # Check if a file path was selected
            new_workbook.save(file_path)
            messagebox.showinfo("Success", "File has been exported successfully!")

    def insert_row(self):
        selected_category = self.radio_var_category.get()
        bill_name = ""
        if selected_category == "Essentials":
            bill_name = self.Essentials_combobox.get()
        elif selected_category == "Miscellaneous":
            bill_name = self.Miscellaneous_combobox.get()

        cost = self.cost_combobox.get()  # Retrieve cost

        if bill_name.strip() and cost.strip():  # Check if both bill name and cost are provided
            try:
                cost = int(cost)  # Convert cost to integer
                selected_currency = self.currency_list[self.currency_combobox.current()]
                bill_type = selected_category

                row_val = [bill_name, cost, bill_type]
                self.treeview.insert('', tk.END, values=row_val)

                # Update total cost label and row colors
                self.update_total_cost()
                self.update_row_colors()

            except ValueError:
                messagebox.showwarning("Warning!", "Please enter a valid cost")
        else:
            messagebox.showwarning("Warning!", "Please enter both Bill Name and Cost")


    def update_row_colors(self):
        for idx, child in enumerate(self.treeview.get_children()):
            if idx % 2 == 0:
                self.treeview.item(child, tags=("evenrow",))
            else:
                self.treeview.item(child, tags=("oddrow",))

    def delete_row(self):
        selected_items = self.treeview.selection()
        if selected_items:
            for item in selected_items:
                self.treeview.delete(item)
            self.update_total_cost()
        else:
            messagebox.showwarning("Warning!", "Please Select A Row")

    def clear_table(self):
        confirmation = messagebox.askyesno("ATTENTION", "Are you sure you want to clear the table?")
        if confirmation:
            # Delete all entries in the Treeview
            for child in self.treeview.get_children():
                self.treeview.delete(child)
            
            # Update the total cost label
            self.update_total_cost()

    def create_separator(self, row, column, padx=(20, 10), pady=10, sticky="ew"):
        separator = ttk.Separator(self.widgets_frame)
        separator.grid(row=row, column=column, padx=padx, pady=pady, sticky=sticky)
        return separator
    


if __name__ == "__main__":
    root = tk.Tk()
    app = DataEntry(root)
    root.mainloop()