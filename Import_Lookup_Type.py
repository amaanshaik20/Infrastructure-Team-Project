import pandas as pd
import pyodbc
from tkinter import Tk, filedialog
import os
import shutil  # Import the shutil module for file operations
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

    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx;*.xls")]
    )

    if not file_path:
        print("No file selected. Exiting.")
        return None, None

    # Extract the filename from the full file path
    filename = os.path.basename(file_path)

    return file_path, filename

def import_excel_to_sql_server(server, database, excel_file_path):
    if not excel_file_path:
        print("No file selected. Exiting.")
        return

    # Read Excel file into a pandas DataFrame
    df = pd.read_excel(excel_file_path)

    # Database connection string
    connection_string = f'Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;'

    # Establish database connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    try:
        # Iterate through each row in the DataFrame and insert into the LOOKUP_TYPE table
        for index, row in df.iterrows():
            cursor.execute("""
                INSERT INTO LOOKUP_TYPE (
                    LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG
                ) VALUES (?, ?, ?)
            """,
            str(row['LOOKUP_TYPE']), str(row['TYPE_DESCRIPTION']), str(row['ENABLED_FLAG']))

        # Commit the transaction
        connection.commit()
        print("Data imported successfully.")

    except pyodbc.Error as ex:
        print("Error during data import:", ex)
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
    print(f"File saved in {destination_path}")

    # Call the function to import data from Excel to SQL Server
    import_excel_to_sql_server(server_name, database_name, excel_file_path)
