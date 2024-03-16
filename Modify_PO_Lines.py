import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys

app = tk.Tk()
app.geometry("700x500")
app.title("MODIFY LOOKUP VALUES")

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

    entry = ttk.Entry(scrollable_frame)  # Default to Entry widget for all fields
    if label_text == "PO_HEADER_ID:":
        # Making PO_HEADER_ID readonly
        entry.config(state="writeonly")  
    entry.grid(row=row, column=1, padx=10, pady=5)  # Adjusted padx and pady for spacing
    return entry


# Labels and entry fields
labels_and_entries = [
    ("PO HEADER ID:", 0),
    ("PO LINE NUMBER:", 1),
    ("ITEM ID:", 2),
    ("PO LINE DESCRIPTION:", 3),
    ("QUANTITY:", 4),
    ("UNIT PRICE:", 5),
    ("LINE TAX AMOUNT:", 6),
    ("SUPPORT START DATE:", 7),
    ("SUPPORT END DATE:", 8),
    ("NEED BY DATE:", 9),
    ("PO LINE STATUS:", 10),
    ("SHIP LOCATION:", 11),
    ("INVOICE NUMBER:", 12),
    ("INVOICE LINE NUMBER:", 13),
    ("INVOICE DATE:", 14),
    ("INVOICE PAID:", 15),
    ("INVOICE AMOUNT:", 16),
    ("PO LINE COMMENTS:", 17)
]


entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)

def fetch_lookup_data(event=None):
    po_header_id = entry_fields[0].get()  # Assuming the PO_HEADER_ID entry field is the first one
    if po_header_id:  # Check if po_header_id is not empty
        try:
            connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                      'Database=InfraDb;'
                            'Trusted_Connection=yes;')
            cursor = connection.cursor()

            # Execute SQL query to fetch data based on PO_HEADER_ID
            cursor.execute("SELECT PO_LINE_NUMBER, ITEM_ID, PO_LINE_DESCRIPTION, QUANTITY, UNIT_PRICE, LINE_TAX_AMOUNT, SUPPORT_START_DATE, SUPPORT_END_DATE, NEED_BY_DATE, PO_LINE_STATUS, SHIP_LOCATION, INVOICE_NUMBER, INVOICE_LINE_NUMBER, INVOICE_DATE, INVOICE_PAID, INVOICE_AMOUNT, PO_LINE_COMMENTS FROM PO_LINES WHERE PO_HEADER_ID = ?", (po_header_id,))
            row = cursor.fetchone()

            # If data is found and PO_LINE_NUMBER has not been fetched yet, populate the entry fields
            if row and not entry_fields[1].get():
                po_line_number, item_id, po_line_description, quantity, unit_price, line_tax_amount, support_start_date, support_end_date, need_by_date, po_line_status, ship_location, invoice_number, invoice_line_number, invoice_date, invoice_paid, invoice_amount, po_line_comments = row
                entry_fields[1].insert(0, po_line_number)  # Populate PO_LINE_NUMBER
                entry_fields[2].insert(0, item_id)  # Populate ITEM_ID
                entry_fields[3].insert(0, po_line_description)  # Populate PO_LINE_DESCRIPTION
                entry_fields[4].insert(0, quantity)  # Populate QUANTITY
                entry_fields[5].insert(0, unit_price)  # Populate UNIT_PRICE
                entry_fields[6].insert(0, line_tax_amount)  # Populate LINE_TAX_AMOUNT
                entry_fields[7].insert(0, support_start_date)  # Populate SUPPORT_START_DATE
                entry_fields[8].insert(0, support_end_date)  # Populate SUPPORT_END_DATE
                entry_fields[9].insert(0, need_by_date)  # Populate NEED_BY_DATE
                entry_fields[10].insert(0, po_line_status)  # Populate PO_LINE_STATUS
                entry_fields[11].insert(0, ship_location)  # Populate SHIP_LOCATION
                entry_fields[12].insert(0, invoice_number)  # Populate INVOICE_NUMBER
                entry_fields[13].insert(0, invoice_line_number)  # Populate INVOICE_LINE_NUMBER
                entry_fields[14].insert(0, invoice_date)  # Populate INVOICE_DATE
                entry_fields[15].insert(0, invoice_paid)  # Populate INVOICE_PAID
                entry_fields[16].insert(0, invoice_amount)  # Populate INVOICE_AMOUNT
                entry_fields[17].insert(0, po_line_comments)  # Populate PO_LINE_COMMENTS
                data_found_label = ttk.Label(scrollable_frame, text="   Data found   ", foreground="green")
                data_found_label.grid(row=0, column=19, padx=(10, 0), pady=5)
            elif not row:
                # Show "data not found" if PO_HEADER_ID doesn't exist
                data_not_found_label = ttk.Label(scrollable_frame, text="Data not found", foreground="red")
                data_not_found_label.grid(row=0, column=19, padx=(10, 0), pady=5)

        except pyodbc.Error as ex:
            print("ERROR:", ex)


# Bind fetch_lookup_data function to the PO_HEADER_ID entry field
entry_fields[0].bind("<FocusOut>", fetch_lookup_data)

# Create the Fetch Data button
fetch_button = ttk.Button(scrollable_frame, text="Fetch Data", command=fetch_lookup_data)
fetch_button.grid(row=0, column=18, padx=(20, 0))  # Adjust position of the button


def Modify_po_lines():
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
        po_header_id = entry_fields[0].get()

        # Check if the PO number already exists in the database
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM PO_LINES WHERE PO_HEADER_ID = ?", (po_header_id,))
        count = cursor.fetchone()[0]
        if count > 0:
            # If PO number exists, perform update
            query = """
                UPDATE PO_LINES
                SET PO_LINE_NUMBER = ?, ITEM_ID = ?, PO_LINE_DESCRIPTION = ?, QUANTITY = ?, UNIT_PRICE = ?, LINE_TAX_AMOUNT = ?, SUPPORT_START_DATE = ?, SUPPORT_END_DATE = ?, NEED_BY_DATE = ?, PO_LINE_STATUS = ?, SHIP_LOCATION = ?, INVOICE_NUMBER = ?, INVOICE_LINE_NUMBER = ?, INVOICE_DATE = ?, INVOICE_PAID = ?, INVOICE_AMOUNT = ?, PO_LINE_COMMENTS = ?, LAST_UPDATE_DATE = ?, LAST_UPDATED_BY_USER= ?
                WHERE PO_HEADER_ID = ?
            """
            query_params = (entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), entry_fields[12].get(), entry_fields[13].get(), entry_fields[14].get(), entry_fields[15].get(), entry_fields[16].get(), entry_fields[17].get(),current_date, username, po_header_id)
        else:
            # If PO number does not exist, perform insert
            query = """
                INSERT INTO PO_LINES
                (PO_HEADER_ID, PO_LINE_NUMBER, ITEM_ID, PO_LINE_DESCRIPTION, QUANTITY, UNIT_PRICE, LINE_TAX_AMOUNT, SUPPORT_START_DATE, SUPPORT_END_DATE, NEED_BY_DATE, PO_LINE_STATUS, SHIP_LOCATION, INVOICE_NUMBER, INVOICE_LINE_NUMBER, INVOICE_DATE, INVOICE_PAID, INVOICE_AMOUNT, PO_LINE_COMMENTS, CREATION_DATE, LAST_UPDATE_DATE) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            query_params = (po_header_id, entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), entry_fields[12].get(), entry_fields[13].get(), entry_fields[14].get(), entry_fields[15].get(), entry_fields[16].get(), entry_fields[17].get(), entry_fields[18].get(), current_date, current_date)

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
insert_button = tk.Button(button_frame, text="MODIFY", command=Modify_po_lines,
                          foreground="black", background="#9ccc65", font=font.Font(size=10, weight="bold"), width=7, height=1)
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="RESET", command=reset,
                         foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="EXIT", command=cancel,
                          foreground="black", background="#ef5350", font=font.Font(size=10, weight="bold"), width=7, height=1)
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)


info_label_inventory = ttk.Label(app, text="3S Technologies - PO LINES ")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

app.mainloop()