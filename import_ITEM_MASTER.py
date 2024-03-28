import pandas as pd
import pyodbc
from tkinter import Tk, filedialog, messagebox
import os
import shutil  
from datetime import datetime
import sys

UPLOAD_FOLDER = 'uploads'

def choose_excel_file():
    root = Tk()
    root.withdraw()  
    root.wm_attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )

    if not file_path:
        messagebox.showerror("Error", "No file selected. Exiting.")
        return None, None

    filename = os.path.basename(file_path)

    return file_path, filename

def import_excel_to_sql_server(server, database, excel_file_path):
    if not excel_file_path:
        messagebox.showerror("Error", "No file selected. Exiting.")
        return

    try:
        df = pd.read_excel(excel_file_path)
        successful_inserts = 0
        failed_inserts = 0

        connection_string = f'Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;'

        with pyodbc.connect(connection_string) as connection:
            cursor = connection.cursor()

            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            username = sys.argv[1] if len(sys.argv) > 1 else ''

            for index, row in df.iterrows():
                try:
                    cursor.execute("""
                        INSERT INTO ITEM_MASTER (
                            ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE, MANUFACTURER_CODE,
                            ITEM_CATEGORY, CPU, MEMORY, DISKS, UOM, ENABLED_FLAG,
                            CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    str(row['ITEM_NUMBER']), str(row['ITEM_DESCRIPTION']), str(row['ITEM_TYPE']),
                    str(row['MANUFACTURER_CODE']), str(row['ITEM_CATEGORY']), str(row['CPU']),
                    str(row['MEMORY']), str(row['DISKS']), str(row['UOM']), str(row['ENABLED_FLAG']),
                    current_date, username, current_date, username)
                    successful_inserts += 1
                except Exception as ex:
                    print(f"Failed to insert row {index + 2}: {ex}")
                    failed_inserts += 1

            connection.commit()
            messagebox.showinfo("Data Import Summary", 
                                f"Successful inserts: {successful_inserts}\nFailed inserts: {failed_inserts}")

    except Exception as ex:
        messagebox.showerror("Error", f"Error during data import: {ex}")

server_name = 'LAPTOP-687KHBP5\SQLEXPRESS'
database_name = 'InfraDB'

excel_file_path, filename = choose_excel_file()

if excel_file_path and filename:
    destination_path = os.path.join(UPLOAD_FOLDER, filename)
    shutil.copy(excel_file_path, destination_path)
    messagebox.showinfo("Info", f"File saved in {destination_path}")

    import_excel_to_sql_server(server_name, database_name, excel_file_path)

