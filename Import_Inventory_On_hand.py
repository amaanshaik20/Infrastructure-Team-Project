import pandas as pd
import pyodbc
from tkinter import Tk, filedialog
import os
import shutil  # Import the shutil module for file operations
from datetime import datetime
import sys

# SQL Server connection details
server_name = 'AJAS-SAMSUNG-BO\MSSQLSERVER01'
database_name = 'InfraDb'

# Get the current date and time as a string
current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Assuming username is passed as a command-line argument or an empty string if not provided
username = sys.argv[1] if len(sys.argv) > 1 else ''

# Function to open file dialog and return selected file path
def choose_excel_file():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel Files", "*.xlsx;*.xls")]
    )
    return file_path

# Connection string for SQL Server
connection_string = f'DRIVER={{SQL Server}};SERVER={server_name};DATABASE={database_name};Trusted_Connection=yes;'

# Establishing connection to SQL Server
conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Reading Excel file into a pandas DataFrame
excel_file_path = choose_excel_file()
if not excel_file_path:
    print("No file selected. Exiting.")
    exit()

excel_data = pd.read_excel(excel_file_path)
# Get the current date and time as a string
current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# Assuming username is passed as a command-line argument or an empty string if not provided
username = sys.argv[1] if len(sys.argv) > 1 else ''

# Save the imported file in the "uploads" folder
uploads_folder = 'uploads'
os.makedirs(uploads_folder, exist_ok=True)
imported_file_path = os.path.join(uploads_folder, 'imported_data.xlsx')
excel_data.to_excel(imported_file_path, index=False)

# Inserting data into the SQL Server table
for index, row in excel_data.iterrows():
    sql_query = '''
    INSERT INTO Inventory_Onhand (
        ITEM_ID, INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS,
        SUBNET_MASK, GATEWAY, COMMENTS, LAST_PO_NUM, LAST_PO_PRICE,
        RENEWAL_DATE, NOTES,
        CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    '''

    params = (
        row['ITEM_ID'], row['INSTALL_LOCATION'], row['PROJECT_CODE'],
        row['QUANTITY'], row['IP_ADDRESS'], row['SUBNET_MASK'],
        row['GATEWAY'], row['COMMENTS'], row['LAST_PO_NUM'],
        row['LAST_PO_PRICE'], row['RENEWAL_DATE'], row['NOTES'],
        current_date, username, current_date, username
    )

    cursor.execute(sql_query, params)
    conn.commit()

# Closing the connections
cursor.close()
conn.close()

print(f"Data imported successfully and saved in '{imported_file_path}'.")
