import pandas as pd
import pyodbc
import os
import tkinter as tk
from tkinter import messagebox, filedialog


def export_sql_server_to_excel(server, database, output_file, output_folder):
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

        # Construct the full path to the output file in the specified folder
        output_file_path = os.path.join(output_folder, f"{output_file}.xlsx")

        # Check if the file already exists
        if os.path.exists(output_file_path):
            # If file already exists, show a message box
            messagebox.showwarning("File Exists", "A file with the same name already exists in the specified folder. Please choose a different name.")
        else:
            # Write DataFrame to Excel file in the specified folder
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
    # Prompt user to select output folder
    output_folder = filedialog.askdirectory()
    if output_folder:
        # Prompt user to select output file name
        output_file = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")], initialdir=output_folder)
        if output_file:
            # Database information
            server_name = 'AmaanShaik\SQLEXPRESS'
            database_name = 'InfraDB'
            # Get file name without extension
            output_file_name = os.path.splitext(os.path.basename(output_file))[0]
            # Export data
            export_sql_server_to_excel(server_name, database_name, output_file_name, output_folder)
        else:
            messagebox.showerror("Error", "Please enter a file name.")
    else:
        messagebox.showerror("Error", "Export canceled. No folder selected.")
        window.destroy()


# Create the GUI window
# window = tk.Tk()
# window.title("Export SQL Server Data to Excel")
# window.geometry("0x0")
# Call export_data immediately when the script starts
export_data()

# Run the GUI event loop
# window.mainloop()
