import tkinter as tk
from tkinter import ttk, font
import pyodbc
from datetime import datetime
import sys

app = tk.Tk()
app.geometry("700x500")
app.title("MODIFY INVENTORY ONHAND")

# Label above the frame
instruction_label = ttk.Label(app, text="ENTER THE SERIAL NUMBER TO FETCH THE DATA" , foreground="black", font=font.Font(size=11), background="#CCCCCC")
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
    label.grid(row=row, column=0, sticky='w', padx=10, pady=5)  

    if label_text == "ENABLED FLAG:":
        entry = ttk.Combobox(scrollable_frame, values=['Y', 'N'])
    else:
        entry = ttk.Entry(scrollable_frame)
        
    entry.grid(row=row, column=1, padx=10, pady=5)  
    return entry

labels_and_entries = [
    ("SERIAL NUMBER:", 0),
    ("INSTALL LOCATION:", 1),
    ("PROJECT CODE:", 2),
    ("QUANTITY:", 3),
    ("IP ADDRESS:", 4),
    ("SUBNET MASK:", 5),
    ("GATEWAY:", 6),
    ("COMMENTS:", 7),
    ("LAST PO NUM:", 8),
    ("LAST PO PRICE:", 9),
    ("RENEWAL DATE:", 10),
    ("NOTES:", 11)
]

entry_fields = []
for label_text, row in labels_and_entries:
    entry = add_label_and_entry(label_text, row)
    entry_fields.append(entry)

def fetch_inventory_data(event=None):
    inventory_id = entry_fields[0].get()
    if inventory_id:  
        try:
            connection = pyodbc.connect('Driver={SQL Server};'
                            'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                            'Database=InfraDb;'
                            'Trusted_Connection=yes;')
            cursor = connection.cursor()

            cursor.execute("SELECT INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS, SUBNET_MASK, GATEWAY, COMMENTS, LAST_PO_NUM, LAST_PO_PRICE, RENEWAL_DATE, NOTES FROM Inventory_Onhand WHERE INVENTORY_ID = ?", (inventory_id,))
            row = cursor.fetchone()

            # Clear entry fields before populating with new data
            for entry in entry_fields[1:]:
                entry.delete(0, tk.END)

            if row:
                install_location, project_code, quantity, ip_address, subnet_mask, gateway, comments, last_po_num, last_po_price, renewal_date, notes = row
                entry_fields[1].insert(0, install_location)  
                entry_fields[2].insert(0, project_code)  
                entry_fields[3].insert(0, quantity)  
                entry_fields[4].insert(0, ip_address)  
                entry_fields[5].insert(0, subnet_mask)  
                entry_fields[6].insert(0, gateway)  
                entry_fields[7].insert(0, comments)  
                entry_fields[8].insert(0, last_po_num)  
                entry_fields[9].insert(0, last_po_price)  
                entry_fields[10].insert(0, renewal_date)  
                entry_fields[11].insert(0, notes)  
                data_found_label = ttk.Label(scrollable_frame, text="Data found", foreground="green")
                data_found_label.grid(row=0, column=12, padx=(10, 0), pady=5)
            else:
                data_not_found_label = ttk.Label(scrollable_frame, text="Data not found", foreground="red")
                data_not_found_label.grid(row=0, column=12, padx=(10, 0), pady=5)

        except pyodbc.Error as ex:
            print("ERROR:", ex)

entry_fields[0].bind("<FocusOut>", fetch_inventory_data)

# Create the Fetch Data button
fetch_button = ttk.Button(scrollable_frame, text="Fetch Data", command=fetch_inventory_data)
fetch_button.grid(row=0, column=9, padx=(20, 0))  # Adjust position of the button


def modify_inventory_values():
    try:
        connection = pyodbc.connect('Driver={SQL Server};'
                        'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                        'Database=InfraDb;'
                        'Trusted_Connection=yes;')
        connection.autocommit = True

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        username = sys.argv[1] if len(sys.argv) > 1 else ''

        inventory_id = entry_fields[0].get()

        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM Inventory_Onhand WHERE INVENTORY_ID = ?", (inventory_id,))
        count = cursor.fetchone()[0]

        if count > 0:
            query = """
                UPDATE Inventory_Onhand
                SET INSTALL_LOCATION = ?, PROJECT_CODE = ?, QUANTITY = ?, IP_ADDRESS = ?, SUBNET_MASK = ?, GATEWAY = ?, COMMENTS = ?, LAST_PO_NUM = ?, LAST_PO_PRICE = ?, RENEWAL_DATE = ?, NOTES = ?, LAST_UPDATE_DATE = ?,LAST_UPDATED_BY_USER = ?
                WHERE INVENTORY_ID = ?
            """
            query_params = (entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), current_date, username, inventory_id)
        else:
            query = """
                INSERT INTO Inventory_Onhand
                (INVENTORY_ID, INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS, SUBNET_MASK, GATEWAY, COMMENTS, LAST_PO_NUM, LAST_PO_PRICE, RENEWAL_DATE, NOTES, CREATION_DATE, LAST_UPDATE_DATE) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            query_params = (inventory_id, entry_fields[1].get(), entry_fields[2].get(), entry_fields[3].get(), entry_fields[4].get(), entry_fields[5].get(), entry_fields[6].get(), entry_fields[7].get(), entry_fields[8].get(), entry_fields[9].get(), entry_fields[10].get(), entry_fields[11].get(), current_date, current_date)

        connection.execute(query, query_params)

        info_label_inventory.configure(text="DATA MODIFIED SUCCESSFULLY!!!", foreground="green")


    except pyodbc.Error as ex:
        print("CONNECTION FAILED", ex)

def reset():
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
insert_button = tk.Button(button_frame, text="MODIFY", command=modify_inventory_values,
                          foreground="black", background="#9ccc65", font=font.Font(size=10, weight="bold"), width=7, height=1)
insert_button.grid(row=0, column=0, pady=(10, 5), padx=50)

reset_button = tk.Button(button_frame, text="RESET", command=reset,
                         foreground="black", background="#64b5f6", font=font.Font(size=10, weight="bold"), width=7, height=1)
reset_button.grid(row=0, column=1, pady=(10, 5), padx=50)

cancel_button = tk.Button(button_frame, text="EXIT", command=cancel,
                          foreground="black", background="#ef5350", font=font.Font(size=10, weight="bold"), width=7, height=1)
cancel_button.grid(row=0, column=2, pady=(10, 5), padx=50)


info_label_inventory = ttk.Label(app, text="3S Technologies - INVENTORY ONHAND")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

app.mainloop()