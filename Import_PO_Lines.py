import pandas as pd
import pyodbc
from tkinter import Tk, filedialog, messagebox
import os
import shutil
from datetime import datetime
import sys

UPLOAD_FOLDER = 'uploads'
# Get the current date and time as a string
current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Assuming username is passed as a command-line argument or an empty string if not provided
username = sys.argv[1] if len(sys.argv) > 1 else ''


def choose_excel_file():
    root = Tk()
    root.withdraw()  # Hide the main window
    root.wm_attributes("-topmost", True)

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )

    if not file_path:
        messagebox.showerror("Error", "No file selected. Exiting.")
        return None, None

    # Extract the filename from the full file path
    filename = os.path.basename(file_path)

    return file_path, filename


def import_excel_to_sql_server(server, database, excel_file_path):
    if not excel_file_path:
        messagebox.showerror("Error", "No file selected. Exiting.")
        return

    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)

    # Database connection string
    connection_string = f'Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;'

    # Establish database connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    successful_inserts = 0
    failed_inserts = 0

    try:
        # Iterate through each row in the DataFrame and insert into the PO_LINES table
        for index, row in df.iterrows():
            try:
                cursor.execute("""
                    INSERT INTO PO_LINES (
                        PO_HEADER_ID, PO_LINE_NUMBER, ITEM_ID, QUANTITY, UNIT_PRICE, PO_LINE_STATUS
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                               str(row['PO_HEADER_ID']), str(row['PO_LINE_NUMBER']), str(row['ITEM_ID']),
                               str(row['QUANTITY']), str(row['UNIT_PRICE']), str(row['PO_LINE_STATUS']),
                                current_date, username, current_date, username)
                successful_inserts += 1
            except Exception as ex:
                print(f"Failed to insert row {index + 2}: {ex}")
                failed_inserts += 1

        # Commit the transaction
        connection.commit()

        messagebox.showinfo("Data Import Summary",
                            f"Successful inserts: {successful_inserts}\nFailed inserts: {failed_inserts}")

    except pyodbc.Error as ex:
        messagebox.showerror("Error", f"Error during data import: {ex}")
        connection.rollback()

    finally:
        # Close the database connection
        connection.close()


# Specify the database information
server_name = 'LAPTOP-687KHBP5\SQLEXPRESS'
database_name = 'InfraDB'

# Call the function to choose the Excel file
excel_file_path, filename = choose_excel_file()

# Save the uploaded file in the "uploads" folder
if excel_file_path and filename:
    destination_path = os.path.join(UPLOAD_FOLDER, filename)
    shutil.copy(excel_file_path, destination_path)
    messagebox.showinfo("Info", f"File saved in {destination_path}")

    # Call the function to import data from Excel to SQL Server
    import_excel_to_sql_server(server_name, database_name, excel_file_path)
