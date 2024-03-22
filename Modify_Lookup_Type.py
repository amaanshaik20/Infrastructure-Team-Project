import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys

app = tk.Tk()
app.geometry("700x500")
app.title("MODIFY LOOKUP TYPE")

# Label above the frame
instruction_label = ttk.Label(app, text="ENTER THE TYPE NUMBER TO FETCH THE DATA" , foreground="black", font=font.Font(size=11), background="#CCCCCC")
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

    if label_text == "ENABLED FLAG:":
        entry = ttk.Combobox(scrollable_frame, values=['Y', 'N'])
    else:
        entry = ttk.Entry(scrollable_frame)
        
    entry.grid(row=row, column=1, padx=10, pady=5)  # Adjusted padx and pady for spacing
    return entry

# Labels and entry fields
labels_and_entries = [
    ("TYPE NUMBER:", 0),
    ("LOOKUP TYPE:", 1),
    ("TYPE DESCRIPTION", 2),
    ("ENABLED FLAG:", 3)
]


entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)

def fetch_lookup_data(event=None):
    lookup_type_id = entry_fields[0].get()  # Assuming the LOOKUP_TYPE entry field is the first one
    if lookup_type_id:  # Check if lookup_type is not empty
        try:
            connection = pyodbc.connect('Driver={SQL Server};'
                           'Server=LAPTOP-687KHBP5\SQLEXPRESS;'
                      'Database=InfraDB;'
                            'Trusted_Connection=yes;')
            cursor = connection.cursor()

            # Execute SQL query to fetch data based on LOOKUP_TYPE
            cursor.execute("SELECT LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG FROM Lookup_Type WHERE LOOKUP_TYPE_ID = ?", (lookup_type_id,))
            row = cursor.fetchone()

            # If data is found and TYPE_DESCRIPTION has not been fetched yet, populate the entry fields
            if row and not entry_fields[1].get():
                lookup_type, type_description, enabled_flag = row
                entry_fields[1].insert(0,lookup_type)
                entry_fields[2].insert(0, type_description)  # Populate TYPE_DESCRIPTION
                entry_fields[3].set(enabled_flag)  # Set the value of ENABLED_FLAG ComboBox
                data_found_label = ttk.Label(scrollable_frame, text="   Data found   ", foreground="green")
                data_found_label.grid(row=0, column=5, padx=(10, 0), pady=5)
            elif not row:
                # Show "data not found" if lookup type doesn't exist
                data_not_found_label = ttk.Label(scrollable_frame, text="Data not found", foreground="red")
                data_not_found_label.grid(row=0, column=5, padx=(10, 0), pady=5)

        except pyodbc.Error as ex:
            print("ERROR:", ex)


# Bind fetch_lookup_data function to the LOOKUP_TYPE entry field
entry_fields[0].bind("<FocusOut>", fetch_lookup_data)

# Create the Fetch Data button
fetch_button = ttk.Button(scrollable_frame, text="Fetch Data", command=fetch_lookup_data)
fetch_button.grid(row=0, column=4, padx=(20, 0))  # Adjust position of the button




# Bind fetch_lookup_data function to the LOOKUP_TYPE entry field
entry_fields[0].bind("<FocusOut>", fetch_lookup_data)

# Create the Fetch Data button
fetch_button = ttk.Button(scrollable_frame, text="Fetch Data", command=fetch_lookup_data)
fetch_button.grid(row=0, column=4, padx=(20, 0))  # Adjust position of the button

def Modify_lookup_type():
    try:
        connection = pyodbc.connect('Driver={SQL Server};'
                        'Server=LAPTOP-687KHBP5\SQLEXPRESS;'
                      'Database=InfraDB;'
                        'Trusted_Connection=yes;')
        connection.autocommit = True

        # Get the current date and time as a string
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Assuming username is passed as a command-line argument or an empty string if not provided
        username = sys.argv[1] if len(sys.argv) > 1 else ''

        # Get the lookup type from the entry field
        lookup_type_id = entry_fields[0].get()

        # Check if the lookup type already exists in the database
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Lookup_Type WHERE LOOKUP_TYPE_ID = ?", (lookup_type_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            # If lookup type exists, perform update
            query = """
                UPDATE Lookup_Type
                SET LOOKUP_TYPE = ?, TYPE_DESCRIPTION = ?, ENABLED_FLAG = ?, LAST_UPDATE_DATE = ?, LAST_UPDATED_BY_USER= ?
                WHERE LOOKUP_TYPE_ID = ?
            """
            query_params = (entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), current_date, username, lookup_type_id)
        

        # Use parameterized query to avoid SQL injection and handle date conversion
        connection.execute(query, query_params)

        info_label_invent = ttk.Label(app, text="DATA MODIFIED SUCCESSFULLY", foreground="GREEN")
        info_label_invent.place(relx=0.1, rely=0.90)  # Adjusted y-position
        reset()


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
insert_button = tk.Button(button_frame, text="UPDATE", command=Modify_lookup_type,
                          foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="CLEAR", command=reset,
                         foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="CANCEL", command=cancel,
                          foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)


info_label_inventory = ttk.Label(app, text="3S Technologies - LOOKUP TYPE")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

app.mainloop()
