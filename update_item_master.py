import tkinter as tk
from tkinter import ttk
import pyodbc

def fetch_data(item_number):
    connection_string = 'Driver={SQL Server};' \
                        'Server=LAPTOP-687KHBP5\SQLEXPRESS;' \
                        'Database=InfraDB;' \
                        'Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = f"SELECT * FROM ITEM_MASTER WHERE ITEM_NUMBER = '{item_number}'"
    cursor.execute(query)
    data = cursor.fetchone()
    cursor.close()
    connection.close()
    return data

def update_data(item_number, item_description, item_type, manufacturer_code, item_category, cpu, memory, disks, uom, enabled_flag):
    connection_string = 'Driver={SQL Server};' \
                        'Server=LAPTOP-687KHBP5\SQLEXPRESS;' \
                        'Database=InfraDB;' \
                        'Trusted_Connection=yes;'
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()
    query = f"UPDATE ITEM_MASTER SET ITEM_DESCRIPTION='{item_description}', ITEM_TYPE='{item_type}', " \
            f"MANUFACTURER_CODE='{manufacturer_code}', ITEM_CATEGORY='{item_category}', " \
            f"CPU='{cpu}', MEMORY='{memory}', DISKS='{disks}', UOM='{uom}', ENABLED_FLAG='{enabled_flag}' " \
            f"WHERE ITEM_NUMBER='{item_number}'"
    
    label_update_info.configure(text="Update COMPLETED!")

    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

def on_button_click():
    item_number = entry_item_number.get()
    data = fetch_data(item_number)
    if data:
        entry_item_description.delete(0, tk.END)
        entry_item_description.insert(0, data.ITEM_DESCRIPTION)
        entry_item_type.delete(0, tk.END)
        entry_item_type.insert(0, data.ITEM_TYPE)
        entry_manufacturer_code.delete(0, tk.END)
        entry_manufacturer_code.insert(0, data.MANUFACTURER_CODE)
        entry_item_category.delete(0, tk.END)
        entry_item_category.insert(0, data.ITEM_CATEGORY)
        entry_cpu.delete(0, tk.END)
        entry_cpu.insert(0, data.CPU)
        entry_memory.delete(0, tk.END)
        entry_memory.insert(0, data.MEMORY)
        entry_disks.delete(0, tk.END)
        entry_disks.insert(0, data.DISKS)
        entry_uom.delete(0, tk.END)
        entry_uom.insert(0, data.UOM)
        combo_enabled_flag.set(data.ENABLED_FLAG)

def on_update_button_click():
    item_number = entry_item_number.get()
    item_description = entry_item_description.get()
    item_type = entry_item_type.get()
    manufacturer_code = entry_manufacturer_code.get()
    item_category = entry_item_category.get()
    cpu = entry_cpu.get()
    memory = entry_memory.get()
    disks = entry_disks.get()
    uom = entry_uom.get()
    enabled_flag = combo_enabled_flag.get()
    update_data(item_number, item_description, item_type, manufacturer_code, item_category, cpu, memory, disks, uom, enabled_flag)

def on_reset_button_click():
    entry_item_number.delete(0, tk.END)
    entry_item_description.delete(0, tk.END)
    entry_item_type.delete(0, tk.END)
    entry_manufacturer_code.delete(0, tk.END)
    entry_item_category.delete(0, tk.END)
    entry_cpu.delete(0, tk.END)
    entry_memory.delete(0, tk.END)
    entry_disks.delete(0, tk.END)
    entry_uom.delete(0, tk.END)
    combo_enabled_flag.set('')  # Set to empty string or default value

def exit():
    root.destroy()


root = tk.Tk()
root.title("Fetch and Update Data in Database")

fields_frame = ttk.Frame(root)
fields_frame.grid(row=0, column=0, padx=10, pady=10)

label_item_number = tk.Label(fields_frame, text="ITEM NUMBER:")
label_item_number.grid(row=0, column=0, padx=10, pady=10)
entry_item_number = tk.Entry(fields_frame)
entry_item_number.grid(row=0, column=1, padx=10, pady=10)

button_fetch_data = tk.Button(fields_frame, text="Fetch Data", command=on_button_click)
button_fetch_data.grid(row=0, column=2, padx=10, pady=10)
label_item_description = tk.Label(fields_frame, text="Item Description:")
label_item_description.grid(row=1, column=0, padx=10, pady=10)

entry_item_description = tk.Entry(fields_frame)
entry_item_description.grid(row=1, column=1, padx=10, pady=10)
label_item_type = tk.Label(fields_frame, text="Item Type:")
label_item_type.grid(row=2, column=0, padx=10, pady=10)

entry_item_type = tk.Entry(fields_frame)
entry_item_type.grid(row=2, column=1, padx=10, pady=10)
label_manufacturer_code = tk.Label(fields_frame, text="Manufacturer Code:")
label_manufacturer_code.grid(row=3, column=0, padx=10, pady=10)

entry_manufacturer_code = tk.Entry(fields_frame)
entry_manufacturer_code.grid(row=3, column=1, padx=10, pady=10)
label_item_category = tk.Label(fields_frame, text="Item Category:")
label_item_category.grid(row=4, column=0, padx=10, pady=10)

entry_item_category = tk.Entry(fields_frame)
entry_item_category.grid(row=4, column=1, padx=10, pady=10)
label_cpu = tk.Label(fields_frame, text="CPU:")
label_cpu.grid(row=5, column=0, padx=10, pady=10)

entry_cpu = tk.Entry(fields_frame)
entry_cpu.grid(row=5, column=1, padx=10, pady=10)
label_memory = tk.Label(fields_frame, text="Memory:")
label_memory.grid(row=6, column=0, padx=10, pady=10)

entry_memory = tk.Entry(fields_frame)
entry_memory.grid(row=6, column=1, padx=10, pady=10)
label_disks = tk.Label(fields_frame, text="Disks:")
label_disks.grid(row=7, column=0, padx=10, pady=10)

entry_disks = tk.Entry(fields_frame)
entry_disks.grid(row=7, column=1, padx=10, pady=10)
label_uom = tk.Label(fields_frame, text="UOM:")
label_uom.grid(row=8, column=0, padx=10, pady=10)

entry_uom = tk.Entry(fields_frame)
entry_uom.grid(row=8, column=1, padx=10, pady=10)
label_enabled_flag = tk.Label(fields_frame, text="Enabled Flag:")
label_enabled_flag.grid(row=9, column=0, padx=10, pady=10)

values = ['Y', 'N']
combo_enabled_flag = ttk.Combobox(fields_frame, values=values, state="readonly")
combo_enabled_flag.grid(row=9, column=1, padx=10, pady=10)

button_update_data = tk.Button(root, text="Update", command=on_update_button_click)
button_update_data.grid(row=2, column=0, padx=5, pady=5)

button_reset = tk.Button(root, text="Reset", command=on_reset_button_click)
button_reset.grid(row=2, column=1, padx=5, pady=5)

button_exit = tk.Button(root, text="Exit", command=exit)
button_exit.grid(row=2, column=2, padx=5, pady=5)
label_update_info = tk.Label(root, text="3S-Technologies Update Item Master")
label_update_info.grid(row=3, column=0, pady=10)


root.mainloop()
