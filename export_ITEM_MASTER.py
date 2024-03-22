import pandas as pd
import pyodbc


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

        # Write DataFrame to Excel file
        df.to_excel(output_file, index=False)
        print(f"Data exported successfully to {output_file}")

    except pyodbc.Error as ex:
        print("Error during data export:", ex)

    finally:
        # Close the database connection
        connection.close()

# Specify the database information
server_name = 'LAPTOP-687KHBP5\SQLEXPRESS'
database_name = 'InfraDB'

# Specify the output Excel file path
export_file_path = "exported_data.xlsx"

# Call the function to export data from SQL Server to Excel
export_sql_server_to_excel(server_name, database_name, export_file_path)



