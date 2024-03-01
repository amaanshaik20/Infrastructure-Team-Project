import tkinter as tk
from tkinter import ttk
import pyodbc
import customtkinter
from datetime import datetime

app = tk.Tk()
app.geometry("700x600")
app.title("INSERT INVENTORY ONHAND")

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("blue")

entry_label = ttk.Label(app, text="ENTER THE BELOW FIELDS",  foreground="green")
entry_label.place(relx=0.2, rely=0.1)

label_ITEM_ID = ttk.Label(app, text="ITEM ID:")
label_ITEM_ID.place(relx=0.1, rely=0.2)

label_INSTALL_LOCATION = ttk.Label(app, text="INSTALL LOCATION:")
label_INSTALL_LOCATION.place(relx=0.1, rely=0.3)

label_PROJECT_CODE = ttk.Label(app, text="PROJECT CODE:")
label_PROJECT_CODE.place(relx=0.1, rely=0.4)

label_QUANTITY = ttk.Label(app, text="QUANTITY:")
label_QUANTITY.place(relx=0.1, rely=0.5)

label_IP_ADDRESS = ttk.Label(app, text="IP ADDRESS:")
label_IP_ADDRESS.place(relx=0.1, rely=0.6)

label_SUBNET_MASK = ttk.Label(app, text="SUBNET MASK:")
label_SUBNET_MASK.place(relx=0.1, rely=0.7)

label_GATEWAY = ttk.Label(app, text="GATEWAY:")
label_GATEWAY.place(relx=0.1, rely=0.8)

label_COMMENTS = ttk.Label(app, text="COMMENTS:")
label_COMMENTS.place(relx=0.6, rely=0.2)

label_LAST_PO_NUM = ttk.Label(app, text="LAST PO NUM:")
label_LAST_PO_NUM.place(relx=0.6, rely=0.3)

label_LAST_PO_PRICE = ttk.Label(app, text="LAST PO PRICE:")
label_LAST_PO_PRICE.place(relx=0.6, rely=0.4)

label_RENEWAL_DATE = ttk.Label(app, text="RENEWAL DATE:")
label_RENEWAL_DATE.place(relx=0.6, rely=0.5)

label_NOTES = ttk.Label(app, text="NOTES:")
label_NOTES.place(relx=0.6, rely=0.6)

label_CREATED_BY_USER_INV = ttk.Label(app, text="CREATED BY USER:")
label_CREATED_BY_USER_INV.place(relx=0.6, rely=0.7)


label_LAST_UPDATED_BY_USER_INV = ttk.Label(app, text="LAST UPDATED BY USER:")
label_LAST_UPDATED_BY_USER_INV.place(relx=0.6, rely=0.8)

entry_ITEM_ID = ttk.Entry(app)
entry_ITEM_ID.place(relx=0.3, rely=0.2)

entry_INSTALL_LOCATION = ttk.Entry(app)
entry_INSTALL_LOCATION.place(relx=0.3, rely=0.3)

entry_PROJECT_CODE = ttk.Entry(app)
entry_PROJECT_CODE.place(relx=0.3, rely=0.4)

entry_QUANTITY = ttk.Entry(app)
entry_QUANTITY.place(relx=0.3, rely=0.5)

entry_IP_ADDRESS = ttk.Entry(app)
entry_IP_ADDRESS.place(relx=0.3, rely=0.6)

entry_SUBNET_MASK = ttk.Entry(app)
entry_SUBNET_MASK.place(relx=0.3, rely=0.7)

entry_GATEWAY = ttk.Entry(app)
entry_GATEWAY.place(relx=0.3, rely=0.8)

entry_COMMENTS = ttk.Entry(app)
entry_COMMENTS.place(relx=0.8, rely=0.2)

entry_LAST_PO_NUM = ttk.Entry(app)
entry_LAST_PO_NUM.place(relx=0.8, rely=0.3)

entry_LAST_PO_PRICE = ttk.Entry(app)
entry_LAST_PO_PRICE.place(relx=0.8, rely=0.4)

entry_RENEWAL_DATE = ttk.Entry(app)
entry_RENEWAL_DATE.place(relx=0.8, rely=0.5)

entry_NOTES = ttk.Entry(app)
entry_NOTES.place(relx=0.8, rely=0.6)

entry_CREATED_BY_USER_INV = ttk.Entry(app)
entry_CREATED_BY_USER_INV.place(relx=0.8, rely=0.7)


entry_LAST_UPDATED_BY_USER_INV = ttk.Entry(app)
entry_LAST_UPDATED_BY_USER_INV.place(relx=0.8, rely=0.8)

def insert_inventory_onhand():
    try:
        connection =pyodbc.connect('Driver={SQL Server};'
                      'Server=AmaanShaik\SQLEXPRESS;'
                      'Database=InfraDB1;'
                      'Trusted_Connection=yes;')
        connection.autocommit = True

        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Use parameterized query to avoid SQL injection and handle date conversion
        connection.execute("""
            INSERT INTO Inventory_Onhand 
            (ITEM_ID, INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS, SUBNET_MASK, GATEWAY, COMMENTS, 
             LAST_PO_NUM, LAST_PO_PRICE, RENEWAL_DATE, NOTES, CREATION_DATE, CREATED_BY_USER, 
             LAST_UPDATE_DATE, LAST_UPDATED_BY_USER) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, GETDATE(), ?)
        """,
        entry_ITEM_ID.get(), entry_INSTALL_LOCATION.get(), entry_PROJECT_CODE.get(), entry_QUANTITY.get(),
        entry_IP_ADDRESS.get(), entry_SUBNET_MASK.get(), entry_GATEWAY.get(), entry_COMMENTS.get(),
        entry_LAST_PO_NUM.get(), entry_LAST_PO_PRICE.get(), entry_RENEWAL_DATE.get(), entry_NOTES.get(),
        current_date, entry_CREATED_BY_USER_INV.get(), entry_LAST_UPDATED_BY_USER_INV.get())
        info_label_inventory.configure(text="INSERTION COMPLETED!")

    except pyodbc.Error as ex:
        print("CONNECTION FAILED", ex)

insert_button_inventory = ttk.Button(app, text="INSERT", command=insert_inventory_onhand)
insert_button_inventory.place(relx=0.1, rely=0.9)

info_label_inventory = ttk.Label(app, text="3S Technologies - Inventory Onhand", foreground="blue")
info_label_inventory.place(relx=0.1, rely=0.95)  # Adjusted y-position

# Add a style for the blue button
style = ttk.Style()
style.configure('Blue.TButton', background='red', foreground='Blue')

app.mainloop()
