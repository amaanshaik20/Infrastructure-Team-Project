import tkinter as tk
from tkinter import ttk
import pyodbc
import customtkinter
from datetime import datetime

app = tk.Tk()
app.geometry("700x500")
app.title("INSERT ITEM MASTER")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

# Label for the entry fields
entry_label = ttk.Label(app, text="ENTER THE BELOW FIELDS",  foreground="green")
entry_label.place(relx=0.2, rely=0.1)

# Labels for each entry field
label_ITEM_NUMBER = ttk.Label(app, text="ITEM NUMBER:")
label_ITEM_NUMBER.place(relx=0.1, rely=0.2)

label_ITEM_DESCRIPTION = ttk.Label(app, text="ITEM DESCRIPTION:")
label_ITEM_DESCRIPTION.place(relx=0.1, rely=0.3)

label_ITEM_TYPE = ttk.Label(app, text="ITEM TYPE:")
label_ITEM_TYPE.place(relx=0.1, rely=0.4)

label_MANUFACTURER_CODE = ttk.Label(app, text="MANUFACTURER CODE:")
label_MANUFACTURER_CODE.place(relx=0.1, rely=0.5)

label_ITEM_CATEGORY = ttk.Label(app, text="ITEM CATEGORY:")
label_ITEM_CATEGORY.place(relx=0.1, rely=0.6)

label_CPU = ttk.Label(app, text="CPU:")
label_CPU.place(relx=0.1, rely=0.7)



label_MEMORY = ttk.Label(app, text="MEMORY:")
label_MEMORY.place(relx=0.6, rely=0.2)

label_DISKS = ttk.Label(app, text="DISKS:")
label_DISKS.place(relx=0.6, rely=0.3)

label_UOM = ttk.Label(app, text="UOM:")
label_UOM.place(relx=0.6, rely=0.4)

label_ENABLED_FLAG = ttk.Label(app, text="ENABLED FLAG:")
label_ENABLED_FLAG.place(relx=0.6, rely=0.5)

label_CREATED_BY_USER = ttk.Label(app, text="CREATED BY USER:")
label_CREATED_BY_USER.place(relx=0.6, rely=0.6)

label_LAST_UPDATED_BY_USER = ttk.Label(app, text="LAST UPDATED BY USER:")
label_LAST_UPDATED_BY_USER.place(relx=0.6, rely=0.7)

# Entry fields for each label
entry_ITEM_NUMBER = ttk.Entry(app)
entry_ITEM_NUMBER.place(relx=0.3, rely=0.2)

entry_ITEM_DESCRIPTION = ttk.Entry(app)
entry_ITEM_DESCRIPTION.place(relx=0.3, rely=0.3)

entry_ITEM_TYPE = ttk.Entry(app)
entry_ITEM_TYPE.place(relx=0.3, rely=0.4)

entry_MANUFACTURER_CODE = ttk.Entry(app)
entry_MANUFACTURER_CODE.place(relx=0.3, rely=0.5)

entry_ITEM_CATEGORY = ttk.Entry(app)
entry_ITEM_CATEGORY.place(relx=0.3, rely=0.6)

entry_CPU = ttk.Entry(app)
entry_CPU.place(relx=0.3, rely=0.7)

# New entry fields for additional columns

entry_MEMORY = ttk.Entry(app)
entry_MEMORY.place(relx=0.8, rely=0.2)

entry_DISKS = ttk.Entry(app)
entry_DISKS.place(relx=0.8, rely=0.3)

entry_UOM = ttk.Entry(app)
entry_UOM.place(relx=0.8, rely=0.4)

values = ['Y', 'N']
entry_ENABLED_FLAG = ttk.Combobox(app, values=values, state="readonly")
entry_ENABLED_FLAG.place(relx=0.8, rely=0.5)

entry_CREATED_BY_USER = ttk.Entry(app)
entry_CREATED_BY_USER.place(relx=0.8, rely=0.6)

entry_LAST_UPDATED_BY_USER = ttk.Entry(app)
entry_LAST_UPDATED_BY_USER.place(relx=0.8, rely=0.7)

def insert():
    try:
        connection =pyodbc.connect('Driver={SQL Server};'
                      'Server=AmaanShaik\SQLEXPRESS;'
                      'Database=InfraDB1;'
                      'Trusted_Connection=yes;')

        connection.autocommit = True

        # Get the current date and time
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Include the new columns in the INSERT statement
        connection.execute(f"INSERT INTO ITEM_MASTER (ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE, MANUFACTURER_CODE, ITEM_CATEGORY, ENABLED_FLAG, CREATION_DATE, CPU, MEMORY, DISKS, UOM, CREATED_BY_USER, LAST_UPDATED_BY_USER) VALUES" +
                           f"('{entry_ITEM_NUMBER.get()}', '{entry_ITEM_DESCRIPTION.get()}',"+
                           f"'{entry_ITEM_TYPE.get()}', '{entry_MANUFACTURER_CODE.get()}',"+
                           f"'{entry_ITEM_CATEGORY.get()}','{entry_ENABLED_FLAG.get()}',"+
                           f"'{current_date}', '{entry_CPU.get()}', '{entry_MEMORY.get()}',"+
                           f"'{entry_DISKS.get()}', '{entry_UOM.get()}',"+
                           f"'{entry_CREATED_BY_USER.get()}', '{entry_LAST_UPDATED_BY_USER.get()}')")
        info_label.configure(text="INSERTION COMPLETED!")

    except pyodbc.Error as ex:
        print("CONNECTION FAILED", ex)

# Button and info label
insert_button = ttk.Button(app, text="INSERT", command=insert)
insert_button.place(relx=0.1, rely=0.8)  # Adjusted y-position

info_label = ttk.Label(app, text="3S Technologies - Item Master",  foreground="blue")
info_label.place(relx=0.1, rely=0.9)  # Adjusted y-position

app.mainloop()
