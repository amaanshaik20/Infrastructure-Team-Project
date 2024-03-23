import pandas as pd
import pyodbc
import os
import tkinter as tk
from tkinter import messagebox


def export_sql_server_to_excel(server, database, output_file):
    # Database connection string
    connection_string = f'Driver={{SQL Server}};Server={server};Database={database};Trusted_Connection=yes;'

    # Establish database connection
    connection = pyodbc.connect(connection_string)
    cursor = connection.cursor()

    try:
        # Execute a query to retrieve data from the ITEM_MASTER table
        cursor.execute("SELECT * FROM ITEM_MASTER")
        
        # Fetch the data into a pandas DataFrame
        data = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        df = pd.DataFrame.from_records(data, columns=columns)

        # Get path to the system's downloads folder
        downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
        
        # Construct the full path to the output file in the downloads folder
        output_file_path = os.path.join(downloads_folder, f"{output_file}.xlsx")

        # Check if the file already exists
        if os.path.exists(output_file_path):
            # If file already exists, show a message box
            messagebox.showwarning("File Exists", "A file with the same name already exists in the Downloads folder. Please choose a different name.")
        else:
            # Write DataFrame to Excel file in the downloads folder
            df.to_excel(output_file_path, index=False)
            print(f"Data exported successfully to {output_file_path}")
            messagebox.showinfo("Success", f"Data exported successfully to {output_file_path}")
            window.destroy()

    except pyodbc.Error as ex:
        print("Error during data export:", ex)
        messagebox.showerror("Error", f"Error during data export: {ex}")

    finally:
        # Close the database connection
        connection.close()


def export_data():
    server_name = 'AmaanShaik\SQLEXPRESS'
    database_name = 'InfraDB'
    output_file = file_name_entry.get().strip()

    if output_file:
        export_sql_server_to_excel(server_name, database_name, output_file)
    else:
        messagebox.showerror("Error", "Please enter a file name.")


# Create the GUI window
window = tk.Tk()
window.title("Export SQL Server Data to Excel")
window.geometry("600x350")  # Set window size

# Label and Entry widget for file name input
file_name_label = tk.Label(window, text="Enter File Name:")
file_name_label.pack(pady=(30, 0))

file_name_entry = tk.Entry(window)
file_name_entry.pack(pady=(0, 35))

# Button to trigger export process
export_button = tk.Button(window, text="Export Data", command=export_data)
export_button.pack()

# Run the GUI event loop
window.mainloop()
