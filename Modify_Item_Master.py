import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys

app = tk.Tk()
app.geometry("700x500")
app.title("MODIFY ITEM MASTER")

# Label above the frame
instruction_label = ttk.Label(app, text="ENTER THE ITEM ID TO FETCH THE DATA" , foreground="black", font=font.Font(size=11), background="#CCCCCC")
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

    if label_text == "ENABLED FLAG:":
        entry = ttk.Combobox(scrollable_frame, values=['Y', 'N'])
    else:
        entry = ttk.Entry(scrollable_frame)
        
    entry.grid(row=row, column=1, padx=10, pady=5)  # Adjusted padx and pady for spacing
    return entry

# Labels and entry fields
labels_and_entries = [
    ("ITEM NUMBER:", 0),
    ("ITEM DESCRIPTION:", 1),
    ("ITEM TYPE:", 2),
    ("MANUFACTURER CODE:", 3),
    ("ITEM CATEGORY:", 4),
    ("CPU:", 5),
    ("MEMORY:", 6),
    ("DISKS:", 7),
    ("UOM:", 8),
    ("ENABLED FLAG:", 9)
]

entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)

def fetch_item_data(event=None):
    item_number = entry_fields[0].get()  # Assuming the ITEM_NUMBER entry field is the first one
    if item_number:  # Check if item_number is not empty
        try:
            connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                            'Database=InfraDb;'
                            'Trusted_Connection=yes;')
            cursor = connection.cursor()

            # Execute SQL query to fetch data based on ITEM_NUMBER
            cursor.execute("SELECT ITEM_DESCRIPTION, ITEM_TYPE, MANUFACTURER_CODE, ITEM_CATEGORY, CPU, MEMORY, DISKS, UOM, ENABLED_FLAG FROM ITEM_MASTER WHERE ITEM_NUMBER = ?", (item_number,))
            row = cursor.fetchone()

            # If data is found and ITEM_DESCRIPTION has not been fetched yet, populate the entry fields
            if row and not entry_fields[1].get():
                item_description, item_type, manufacturer_code, item_category, cpu, memory, disks, uom, enabled_flag = row
                entry_fields[1].insert(0, item_description)  # Populate ITEM_DESCRIPTION
                entry_fields[2].insert(0, item_type)  # Populate ITEM_TYPE
                entry_fields[3].insert(0, manufacturer_code)  # Populate MANUFACTURER_CODE
                entry_fields[4].insert(0, item_category)  # Populate ITEM_CATEGORY
                entry_fields[5].insert(0, cpu)  # Populate CPU
                entry_fields[6].insert(0, memory)  # Populate MEMORY
                entry_fields[7].insert(0, disks)  # Populate DISKS
                entry_fields[8].insert(0, uom)  # Populate UOM
                entry_fields[9].set(enabled_flag)  # Set the value of ENABLED_FLAG ComboBox
                data_found_label = ttk.Label(scrollable_frame, text="   Data found   ", foreground="green")
                data_found_label.grid(row=0, column=10, padx=(10, 0), pady=5)
            elif not row:
                # Show "data not found" if item number doesn't exist
                data_not_found_label = ttk.Label(scrollable_frame, text="Data not found", foreground="red")
                data_not_found_label.grid(row=0, column=10, padx=(10, 0), pady=5)

        except pyodbc.Error as ex:
            print("ERROR:", ex)


# Bind fetch_item_data function to the ITEM_NUMBER entry field
entry_fields[0].bind("<FocusOut>", fetch_item_data)

# Create the Fetch Data button
fetch_button = ttk.Button(scrollable_frame, text="Fetch Data", command=fetch_item_data)
fetch_button.grid(row=0, column=9, padx=(20, 0))  # Adjust position of the button


def modify_item_master():
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

        # Get the item number from the entry field
        item_number = entry_fields[0].get()

        # Check if the item number already exists in the database
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM ITEM_MASTER WHERE ITEM_NUMBER = ?", (item_number,))
        count = cursor.fetchone()[0]

        if count > 0:
            # If item number exists, perform update
            query = """
                UPDATE ITEM_MASTER
                SET ITEM_DESCRIPTION = ?, ITEM_TYPE = ?, MANUFACTURER_CODE = ?, ITEM_CATEGORY = ?, CPU = ?, MEMORY = ?, DISKS = ?, UOM = ?, ENABLED_FLAG = ?, LAST_UPDATE_DATE = ?, LAST_UPDATED_BY_USER = ?
                WHERE ITEM_NUMBER = ?
            """
            query_params = (entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), current_date, username, item_number)
        else:
            # If item number does not exist, perform insert
            query = """
                INSERT INTO ITEM_MASTER
                (ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE, MANUFACTURER_CODE, ITEM_CATEGORY, CPU, MEMORY, DISKS, UOM, ENABLED_FLAG, CREATION_DATE, LAST_UPDATE_DATE) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            query_params = (item_number, entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), current_date, current_date)

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
insert_button = tk.Button(button_frame, text="UPDATE", command=modify_item_master,
                          foreground="black", background="#9ccc65", font=font.Font(size=10, weight="bold"), width=7, height=1)
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="RESET", command=reset,
                         foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="EXIT", command=cancel,
                          foreground="black", background="#ef5350", font=font.Font(size=10, weight="bold"), width=7, height=1)
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)


info_label_inventory = ttk.Label(app, text="3S Technologies - ITEM MASTER")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

app.mainloop()