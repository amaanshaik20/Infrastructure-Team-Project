import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys

app = tk.Tk()
app.geometry("700x500")
app.title("INSERT PURCHASE ORDER")

# Label above the frame
instruction_label = ttk.Label(app, text="INSERT THE BELOW FIELDS INTO THE PURCHASE ORDER", foreground="black", font=font.Font(size=11), background="#CCCCCC")
instruction_label.place(relx=0.1, rely=0.1)



# Create a frame to hold the labels and entry fields with a scrollbar
frame = tk.Frame(app, borderwidth=2, relief="groove", border=2, bg="grey")
frame.place(relx=0.1, rely=0.2, relwidth=0.8, relheight=0.6)

canvas = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Function to add labels and entry fields to the scrollable frame
def add_label_and_entry(label_text, row):
    label = ttk.Label(scrollable_frame, text=label_text)
    label.grid(row=row, column=0, sticky='w', padx=10, pady=5)  # Adjusted padx and pady for spacing

    if label_text == "PO STATUS:":
        entry = ttk.Combobox(scrollable_frame)
        entry['values'] = ['Entered', 'Approved', 'Received', 'Invoiced', 'Closed', 'Cancelled']
    else:
        entry = ttk.Entry(scrollable_frame)

        
    entry.grid(row=row, column=1, padx=10, pady=5)  # Adjusted padx and pady for spacing
    return entry

# Labels and entry fields
labels_and_entries = [
    ("PO NUMBER", 14),
    ("PO TYPE:", 15),
    ("PO DESCRIPTION", 16),
    ("VENDOR NAME:", 17),
    ("VENDOR LOCATION", 18),
    ("QUOTE REQUESTED:", 19),
    ("QUOTE NUMBER", 20),
    ("PO STATUS:", 21),
    ("PO DATE:", 22),
    ("PO APPROVED DATE", 23),
    ("PO APPROVED BY:", 24),
    ("PO REQUESTED", 25),
    ("PO REQUESTED BY:", 26),
    ("INVOICE NUMBER:", 27),
    ("INVOICE LINE NUMBER", 28),
    ("INVOICE AMOUNT:", 29),
    ("INVOICE PAID", 30),
    ("SUPPORT START DATE:", 31),
    ("SUPPORT END DATE:", 32),
]

#entry fields
entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)


def insert_inventory_onhand():
    try:
        connection = pyodbc.connect('Driver={SQL Server};'
                        'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                        'Database=InfraDb;'
                        'Trusted_Connection=yes;')
        connection.autocommit = True

        # Get the current date and time as a string
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Assuming username is passed as a command-line argument or an empty string if not provided
        username = sys.argv[1] if len(sys.argv) > 1 else ''

        # Use a tuple to unpack the entry fields for the SQL query
        query_params = tuple(entry.get() for entry in entry_fields)

        # Add current_date and username to the tuple for query_params
        query_params += (current_date, username, current_date, username)

        # Use parameterized query to avoid SQL injection and handle date conversion
        connection.execute("""
            INSERT INTO PO_HEADER 
            (PO_NUMBER, PO_TYPE, PO_DESCRIPTION, VENDOR_NAME, VENDOR_LOCATION, 
            QUOTE_REQUESTED, QUOTE_NUMBER, PO_STATUS, PO_DATE, PO_APPROVED_DATE, PO_APPROVED_BY, PO_REQUESTED, PO_REQUESTED_BY, 
            INVOICE_NUMBER, INVOICE_LINE_NUMBER, INVOICE_AMOUNT, INVOICE_PAID, 
            SUPPORT_START_DATE, SUPPORT_END_DATE, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, query_params)
        info_label_inventory.configure(text="INSERTION COMPLETED!")

    except pyodbc.Error as ex:
        print("CONNECTION FAILED", ex)

def reset():
    # Reset all entry fields to empty strings
    for entry in entry_fields:
        entry.delete(0, tk.END)


def cancel():
    app.destroy()

# Create a new frame for the buttons
button_frame = tk.Frame(app)
button_frame.place(relx=0.1, rely=0.8, relwidth=0.8)

# Function to create bold font
def get_bold_font():
    return font.Font(weight="bold")

# Create buttons with bold text
insert_button = tk.Button(button_frame, text="INSERT", command=insert_inventory_onhand,
                          foreground="black", background="#9ccc65", font=font.Font(size=10, weight="bold"), width=7, height=1)
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="RESET", command=reset,
                         foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="EXIT", command=cancel,
                          foreground="black", background="#ef5350", font=font.Font(size=10, weight="bold"), width=7, height=1)
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)

info_label_inventory = ttk.Label(app, text="3S Technologies - PO HEADER")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

app.mainloop()