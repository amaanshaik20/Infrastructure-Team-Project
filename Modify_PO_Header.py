import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys

app = tk.Tk()
app.geometry("700x500")
app.title("MODIFY PO HEADER")

# Label above the frame
instruction_label = ttk.Label(app, text="ENTER THE LOOKUP TYPE ID TO FETCH THE DATA" , foreground="black", font=font.Font(size=11), background="#CCCCCC")
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

def add_label_and_entry(label_text, row):
    label = ttk.Label(scrollable_frame, text=label_text)
    label.grid(row=row, column=0, sticky='w', padx=10, pady=5)  # Adjusted padx and pady for spacing

    if label_text == "PO_STATUS:":
        entry = ttk.Combobox(scrollable_frame, values = ['Entered', 'Approved', 'Received', 'Invoiced', 'Closed', 'Cancelled'])
    else:
        entry = ttk.Entry(scrollable_frame)
        
    entry.grid(row=row, column=1, padx=10, pady=5)  # Adjusted padx and pady for spacing
    return entry

# Labels and entry fields for PO_HEADER
labels_and_entries = [
    ("PO_NUMBER:", 0),
    ("PO_TYPE:", 1),
    ("PO_DESCRIPTION:", 2),
    ("VENDOR_NAME:", 3),
    ("VENDOR_LOCATION:", 4),
    ("QUOTE_REQUESTED:", 5),
    ("QUOTE_NUMBER:", 6),
    ("PO_STATUS:", 7),
    ("PO_DATE:", 8),
    ("PO_APPROVED_DATE:", 9),
    ("PO_APPROVED_BY:", 10),
    ("PO_REQUESTED:", 11),
    ("PO_REQUESTED_BY:", 12),
    ("INVOICE_NUMBER:", 13),
    ("INVOICE_LINE_NUMBER:", 14),
    ("INVOICE_AMOUNT:", 15),
    ("INVOICE_PAID:", 16),
    ("SUPPORT_START_DATE:", 17),
    ("SUPPORT_END_DATE:", 18)
]

entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)

def fetch_po_data(event=None):
    po_number = entry_fields[0].get()  # Assuming the PO_NUMBER entry field is the first one
    if po_number:  # Check if po_number is not empty
        try:
            connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                            'Database=InfraDb;'
                            'Trusted_Connection=yes;')
            cursor = connection.cursor()

            # Execute SQL query to fetch data based on PO_NUMBER
            cursor.execute("SELECT PO_TYPE, PO_DESCRIPTION, VENDOR_NAME, VENDOR_LOCATION, QUOTE_REQUESTED, QUOTE_NUMBER, PO_STATUS, PO_DATE, PO_APPROVED_DATE, PO_APPROVED_BY, PO_REQUESTED, PO_REQUESTED_BY, INVOICE_NUMBER, INVOICE_LINE_NUMBER, INVOICE_AMOUNT, INVOICE_PAID, SUPPORT_START_DATE, SUPPORT_END_DATE FROM PO_HEADER WHERE PO_NUMBER = ?", (po_number,))
            row = cursor.fetchone()

            # If data is found and PO_TYPE has not been fetched yet, populate the entry fields
            if row and not entry_fields[1].get():
                po_type, po_description, vendor_name, vendor_location, quote_requested, quote_number, po_status, po_date, po_approved_date, po_approved_by, po_requested, po_requested_by, invoice_number, invoice_line_number, invoice_amount, invoice_paid, support_start_date, support_end_date = row
                entry_fields[1].insert(0, po_type)  # Populate PO_TYPE
                entry_fields[2].insert(0, po_description)  # Populate PO_DESCRIPTION
                entry_fields[3].insert(0, vendor_name)  # Populate VENDOR_NAME
                entry_fields[4].insert(0, vendor_location)  # Populate VENDOR_LOCATION
                entry_fields[5].insert(0, quote_requested)  # Populate QUOTE_REQUESTED
                entry_fields[6].insert(0, quote_number)  # Populate QUOTE_NUMBER
                entry_fields[7].set(po_status)  # Populate PO_STATUS
                entry_fields[8].insert(0, po_date)  # Populate PO_DATE
                entry_fields[9].insert(0, po_approved_date)  # Populate PO_APPROVED_DATE
                entry_fields[10].insert(0, po_approved_by)  # Populate PO_APPROVED_BY
                entry_fields[11].insert(0, po_requested)  # Populate PO_REQUESTED
                entry_fields[12].insert(0, po_requested_by)  # Populate PO_REQUESTED_BY
                entry_fields[13].insert(0, invoice_number)  # Populate INVOICE_NUMBER
                entry_fields[14].insert(0, invoice_line_number)  # Populate INVOICE_LINE_NUMBER
                entry_fields[15].insert(0, invoice_amount)  # Populate INVOICE_AMOUNT
                entry_fields[16].insert(0, invoice_paid)  # Populate INVOICE_PAID
                entry_fields[17].insert(0, support_start_date)  # Populate SUPPORT_START_DATE
                entry_fields[18].insert(0, support_end_date)  # Populate SUPPORT_END_DATE
                data_found_label = ttk.Label(scrollable_frame, text="   Data found   ", foreground="green")
                data_found_label.grid(row=0, column=19, padx=(10, 0), pady=5)
            elif not row:
                # Show "data not found" if PO number doesn't exist
                data_not_found_label = ttk.Label(scrollable_frame, text="Data not found", foreground="red")
                data_not_found_label.grid(row=0, column=19, padx=(10, 0), pady=5)

        except pyodbc.Error as ex:
            print("ERROR:", ex)


# Bind fetch_po_data function to the PO_NUMBER entry field
entry_fields[0].bind("<FocusOut>", fetch_po_data)

# Create the Fetch Data button for PO_HEADER
fetch_button = ttk.Button(scrollable_frame, text="Fetch Data", command=fetch_po_data)
fetch_button.grid(row=0, column=18, padx=(20, 0))  # Adjust position of the button


def modify_po_values():
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

        # Get the PO number from the entry field
        po_number = entry_fields[0].get()

        # Check if the PO number already exists in the database
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM PO_HEADER WHERE PO_NUMBER = ?", (po_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            # If PO number exists, perform update
            query = """
                UPDATE PO_HEADER
                SET PO_TYPE = ?, PO_DESCRIPTION = ?, VENDOR_NAME = ?, VENDOR_LOCATION = ?, QUOTE_REQUESTED = ?, QUOTE_NUMBER = ?, PO_STATUS = ?, PO_DATE = ?, PO_APPROVED_DATE = ?, PO_APPROVED_BY = ?, PO_REQUESTED = ?, PO_REQUESTED_BY = ?, INVOICE_NUMBER = ?, INVOICE_LINE_NUMBER = ?, INVOICE_AMOUNT = ?, INVOICE_PAID = ?, SUPPORT_START_DATE = ?, SUPPORT_END_DATE = ?, LAST_UPDATE_DATE = ?, LAST_UPDATED_BY_USER= ?
                WHERE PO_NUMBER = ?
            """
            query_params = (entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), entry_fields[12].get(), entry_fields[13].get(), entry_fields[14].get(), entry_fields[15].get(), entry_fields[16].get(), entry_fields[17].get(), entry_fields[18].get(), current_date, username, po_number)
        else:
            # If PO number does not exist, perform insert
            query = """
                INSERT INTO PO_HEADER
                (PO_NUMBER, PO_TYPE, PO_DESCRIPTION, VENDOR_NAME, VENDOR_LOCATION, QUOTE_REQUESTED, QUOTE_NUMBER, PO_STATUS, PO_DATE, PO_APPROVED_DATE, PO_APPROVED_BY, PO_REQUESTED, PO_REQUESTED_BY, INVOICE_NUMBER, INVOICE_LINE_NUMBER, INVOICE_AMOUNT, INVOICE_PAID, SUPPORT_START_DATE, SUPPORT_END_DATE, CREATION_DATE, LAST_UPDATE_DATE) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            query_params = (po_number, entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), entry_fields[12].get(), entry_fields[13].get(), entry_fields[14].get(), entry_fields[15].get(), entry_fields[16].get(), entry_fields[17].get(), entry_fields[18].get(), current_date, current_date)

        # Use parameterized query to avoid SQL injection and handle date conversion
        connection.execute(query, query_params)

        info_label_inventory.configure(text="DATA MODIFIED SUCCESSFULLY!!!", foreground="green")

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
insert_button = tk.Button(button_frame, text="MODIFY", command=modify_po_values,
                          foreground="black", background="#9ccc65", font=font.Font(size=10, weight="bold"), width=7, height=1)
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="RESET", command=reset,
                         foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="EXIT", command=cancel,
                          foreground="black", background="#ef5350", font=font.Font(size=10, weight="bold"), width=7, height=1)
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)


info_label_inventory = ttk.Label(app, text="3S Technologies - PO HEADER ")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

app.mainloop()