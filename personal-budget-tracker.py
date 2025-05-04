import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime


class BudgetTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Budget Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f4f8")  # Light gray-blue background

        # Create CSV file if it doesn't exist
        self.filename = "budget_data.csv"
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Date", "Category", "Description", "Amount", "Type"])

        # Variables
        self.amount_var = tk.DoubleVar()
        self.category_var = tk.StringVar()
        self.description_var = tk.StringVar()
        self.type_var = tk.StringVar(value="Expense")
        self.search_var = tk.StringVar()
        self.filter_category_var = tk.StringVar(value="All")
        self.filter_type_var = tk.StringVar(value="All")

        # Categories
        self.categories = [
            "Food", "Transportation", "Housing", "Utilities",
            "Entertainment", "Healthcare", "Education", "Shopping",
            "Income", "Savings", "Other"
        ]

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Modern theme
        self.configure_styles()

        # Create GUI
        self.create_widgets()
        self.load_data()

    def configure_styles(self):
        # Configure general widget styles
        self.style.configure('TLabel', background='#f0f4f8', foreground='#2c3e50', font=('Helvetica', 10))
        self.style.configure('TButton', padding=6, font=('Helvetica', 10, 'bold'))
        self.style.map('TButton',
                       background=[('active', '#3498db'), ('!disabled', '#2980b9')],
                       foreground=[('active', 'white'), ('!disabled', 'white')])
        self.style.configure('TEntry', padding=5)
        self.style.configure('TCombobox', padding=5)

        # LabelFrame style
        self.style.configure('TLabelframe', background='#dfe6e9', foreground='#2c3e50')
        self.style.configure('TLabelframe.Label', background='#dfe6e9', foreground='#2c3e50',
                             font=('Helvetica', 10, 'bold'))
        self.style.configure('TLabelframe', relief='groove', borderwidth=2)  # Visual border effect

        # Treeview style
        self.style.configure('Treeview',
                             background='#ffffff',
                             foreground='#2c3e50',
                             rowheight=25,
                             fieldbackground='#ffffff')
        self.style.configure('Treeview.Heading',
                             background='#3498db',
                             foreground='white',
                             font=('Helvetica', 10, 'bold'))
        self.style.map('Treeview',
                       background=[('selected', '#3498db')],
                       foreground=[('selected', 'white')])

        # Custom tag for alternating rows
        self.tree_tag = {'even': {'background': '#ecf0f1'}, 'odd': {'background': '#ffffff'}}

    def create_widgets(self):
        # Frame for entry form
        entry_frame = ttk.LabelFrame(self.root, text="Add New Transaction", padding=(10, 5))
        entry_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Amount
        ttk.Label(entry_frame, text="Amount:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(entry_frame, textvariable=self.amount_var).grid(row=0, column=1, sticky="ew", padx=5, pady=2)

        # Category
        ttk.Label(entry_frame, text="Category:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Combobox(entry_frame, textvariable=self.category_var, values=self.categories).grid(row=1, column=1,
                                                                                               sticky="ew", padx=5,
                                                                                               pady=2)

        # Description
        ttk.Label(entry_frame, text="Description:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(entry_frame, textvariable=self.description_var).grid(row=2, column=1, sticky="ew", padx=5, pady=2)

        # Type (Income/Expense)
        ttk.Label(entry_frame, text="Type:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        ttk.Combobox(entry_frame, textvariable=self.type_var, values=["Income", "Expense"]).grid(row=3, column=1,
                                                                                                 sticky="ew", padx=5,
                                                                                                 pady=2)

        # Add button
        ttk.Button(entry_frame, text="Add Transaction", command=self.add_transaction).grid(row=4, column=0,
                                                                                           columnspan=2, pady=10)

        # Frame for search/filter
        filter_frame = ttk.LabelFrame(self.root, text="Search & Filter", padding=(10, 5))
        filter_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Search
        ttk.Label(filter_frame, text="Search:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(filter_frame, textvariable=self.search_var).grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        ttk.Button(filter_frame, text="Search", command=self.load_data).grid(row=0, column=2, padx=5, pady=2)

        # Filter by category
        ttk.Label(filter_frame, text="Category:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        ttk.Combobox(filter_frame, textvariable=self.filter_category_var,
                     values=["All"] + self.categories).grid(row=1, column=1, sticky="ew", padx=5, pady=2)

        # Filter by type
        ttk.Label(filter_frame, text="Type:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        ttk.Combobox(filter_frame, textvariable=self.filter_type_var,
                     values=["All", "Income", "Expense"]).grid(row=1, column=3, sticky="ew", padx=5, pady=2)

        # Apply filters button
        ttk.Button(filter_frame, text="Apply Filters", command=self.load_data).grid(row=1, column=4, padx=5, pady=2)

        # Frame for transactions
        transactions_frame = ttk.LabelFrame(self.root, text="Transactions", padding=(10, 5))
        transactions_frame.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")
        self.root.rowconfigure(2, weight=1)

        # Treeview for transactions
        self.tree = ttk.Treeview(transactions_frame, columns=("Date", "Category", "Description", "Amount", "Type"),
                                 show="headings")

        # Define columns
        self.tree.heading("Date", text="Date")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Description", text="Description")
        self.tree.heading("Amount", text="Amount")
        self.tree.heading("Type", text="Type")

        # Set column widths
        self.tree.column("Date", width=100)
        self.tree.column("Category", width=120)
        self.tree.column("Description", width=200)
        self.tree.column("Amount", width=100)
        self.tree.column("Type", width=80)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(transactions_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Frame for summary
        summary_frame = ttk.LabelFrame(self.root, text="Summary", padding=(10, 5))
        summary_frame.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

        # Summary labels with colored text
        ttk.Label(summary_frame, text="Total Income:", foreground="#27ae60").grid(row=0, column=0, sticky="w", padx=5)
        self.total_income_label = ttk.Label(summary_frame, text="$0.00", foreground="#27ae60")
        self.total_income_label.grid(row=0, column=1, sticky="w", padx=10)

        ttk.Label(summary_frame, text="Total Expenses:", foreground="#c0392b").grid(row=0, column=2, sticky="w", padx=5)
        self.total_expense_label = ttk.Label(summary_frame, text="$0.00", foreground="#c0392b")
        self.total_expense_label.grid(row=0, column=3, sticky="w", padx=10)

        ttk.Label(summary_frame, text="Balance:", foreground="#2c3e50").grid(row=0, column=4, sticky="w", padx=5)
        self.balance_label = ttk.Label(summary_frame, text="$0.00", foreground="#2c3e50")
        self.balance_label.grid(row=0, column=5, sticky="w", padx=10)

        # Delete button
        ttk.Button(summary_frame, text="Delete Selected", command=self.delete_transaction).grid(row=0, column=6,
                                                                                                padx=10, pady=5)

    def add_transaction(self):
        # Validate inputs
        try:
            amount = float(self.amount_var.get())
            if amount <= 0:
                raise ValueError("Amount must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive amount")
            return

        if not self.category_var.get():
            messagebox.showerror("Error", "Please select a category")
            return

        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Save to CSV
        with open(self.filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                current_date,
                self.category_var.get(),
                self.description_var.get(),
                amount,
                self.type_var.get()
            ])

        # Clear fields
        self.amount_var.set(0)
        self.description_var.set("")

        # Reload data
        self.load_data()
        messagebox.showinfo("Success", "Transaction added successfully")

    def load_data(self):
        # Clear treeview
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Initialize totals
        total_income = 0
        total_expense = 0
        row_count = 0

        # Read from CSV
        try:
            with open(self.filename, 'r') as file:
                reader = csv.DictReader(file)

                # Apply search and filters
                search_term = self.search_var.get().lower()
                filter_category = self.filter_category_var.get()
                filter_type = self.filter_type_var.get()

                for row in reader:
                    # Skip header
                    if row["Date"] == "Date":
                        continue

                    # Apply filters
                    if filter_category != "All" and row["Category"] != filter_category:
                        continue

                    if filter_type != "All" and row["Type"] != filter_type:
                        continue

                    # Apply search
                    if search_term and (search_term not in row["Description"].lower() and
                                        search_term not in row["Category"].lower()):
                        continue

                    # Determine row tag for alternating colors
                    tag = 'even' if row_count % 2 == 0 else 'odd'
                    row_count += 1

                    # Add to treeview with tag
                    self.tree.insert("", "end", values=(
                        row["Date"],
                        row["Category"],
                        row["Description"],
                        f"${float(row['Amount']):.2f}",
                        row["Type"]
                    ), tags=(tag,))

                    # Calculate totals
                    amount = float(row["Amount"])
                    if row["Type"] == "Income":
                        total_income += amount
                    else:
                        total_expense += amount

        except FileNotFoundError:
            pass

        # Configure tags for alternating row colors
        self.tree.tag_configure('even', background=self.tree_tag['even']['background'])
        self.tree.tag_configure('odd', background=self.tree_tag['odd']['background'])

        # Update summary
        self.total_income_label.config(text=f"${total_income:.2f}")
        self.total_expense_label.config(text=f"${total_expense:.2f}")
        self.balance_label.config(text=f"${(total_income - total_expense):.2f}")

    def delete_transaction(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a transaction to delete")
            return

        # Get selected transaction details
        item_data = self.tree.item(selected_item)['values']

        # Read all transactions
        transactions = []
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                transactions.append(row)

        # Find and remove the selected transaction
        new_transactions = []
        deleted = False
        for row in transactions:
            # Skip header
            if row[0] == "Date":
                new_transactions.append(row)
                continue

            # Compare with selected item
            if (row[0] == item_data[0] and
                    row[1] == item_data[1] and
                    row[2] == item_data[2] and
                    f"${float(row[3]):.2f}" == item_data[3] and
                    row[4] == item_data[4]):
                deleted = True
            else:
                new_transactions.append(row)

        # Write back to file
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(new_transactions)

        if deleted:
            messagebox.showinfo("Success", "Transaction deleted successfully")
            self.load_data()
        else:
            messagebox.showerror("Error", "Failed to delete transaction")


if __name__ == "__main__":
    root = tk.Tk()
    app = BudgetTracker(root)
    root.mainloop()
