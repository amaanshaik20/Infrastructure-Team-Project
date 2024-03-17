from flask import Flask,render_template,session,request,redirect,url_for,jsonify
import pyodbc
import subprocess
# from datetime import date
app = Flask(__name__) 
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=AJAS-SAMSUNG-BO\MSSQLSERVER01;'
                      'Database=InfraDb;'
                      'Trusted_Connection=yes;')

cursor = conn.cursor()

@app.route("/") 
def index(): 
	return render_template("index.html")

@app.route("/item_details") 
def item_details(): 
	return render_template("item_details.html")

@app.route("/inventory") 
def inventory(): 
	return render_template("inventory.html")

@app.route("/purchase_orders") 
def purchase_orders(): 
	return render_template("purchase_orders.html")

@app.route("/lookup_details") 
def lookup_details(): 
	return render_template("lookup_details.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Assuming you have a users table with columns 'username' and 'password'
        username = request.form.get("username")
        password = request.form.get("password")

    
        # Check the credentials (This is a simple example, not secure for production)
        cursor.execute("SELECT name,username,password FROM users WHERE username = ? AND password = ?", (username, password))
        
        user = cursor.fetchone()
        
        if user:
            session['username'] = username  # Store the username in the session
            session['name'] = user.name
            return redirect(url_for("main"))
        else:
            return render_template("index.html", message="Invalid credentials. Try again.")
    return render_template("main.html")
@app.route("/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route("/get_item_data", methods=["GET"])
def get_item_data():
    # Get filter values from request
    # item_id = request.args.get('item_id', '')
    item_number = request.args.get('item_number', '')
    item_description = request.args.get('item_description', '')
    enabled_flag = request.args.get('enabled_flag', '')
    item_type=request.args.get('item_type','')
    manufacturer_code = request.args.get('manufacturer_code', '')
    item_category = request.args.get('item_category', '')
    cpu = request.args.get('cpu', '')
    memory = request.args.get('memory', '')
    disks = request.args.get('disks', '')
    uom = request.args.get('uom', '')

    # Construct SQL query with WHERE conditions
    query = 'SELECT ITEM_ID, ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE, MANUFACTURER_CODE, ' \
            'ITEM_CATEGORY, CPU, MEMORY, DISKS, UOM,ENABLED_FLAG, CREATION_DATE, CREATED_BY_USER, ' \
            'LAST_UPDATE_DATE, LAST_UPDATED_BY_USER FROM ITEM_MASTER WHERE 1=1'

    conditions = []

    # if item_id:
    #     conditions.append(f"ITEM_ID = '{item_id}'")
    if item_number:
        conditions.append(f"ITEM_NUMBER = '{item_number}'")
    if item_description:
        conditions.append(f"ITEM_DESCRIPTION LIKE '%{item_description}%'")
    if enabled_flag:
        conditions.append(f"ENABLED_FLAG = '{enabled_flag}'")
    if item_type:
        conditions.append(f"ITEM_TYPE LIKE '%{item_type}%'")
    if manufacturer_code:
        conditions.append(f"MANUFACTURER_CODE = '{manufacturer_code}'")
    if item_category:
        conditions.append(f"ITEM_CATEGORY = '{item_category}'")
    if cpu:
        conditions.append(f"CPU = '{cpu}'")
    if memory:
        conditions.append(f"MEMORY = '{memory}'")   
    if disks:
        conditions.append(f"DISKS = '{disks}'")
    if uom:
        conditions.append(f"UOM = '{uom}'")
        
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query)
    data = cursor.fetchall()

    # Format data as HTML for simplicity (you can use JSON for a more structured approach)
    html_data = "<table>\n"
    html_data += "<tr>\n"
    # html_data += "<th>Edit</th>\n"
    html_data += "<th>Sno.</th>\n"
    html_data += "<th>ITEM NUMBER</th>\n"
    html_data += "<th>ITEM DESCRIPTION</th>\n"
    html_data += "<th>ITEM TYPE</th>\n"
    html_data += "<th>MANUFACTURER CODE</th>\n"
    html_data += "<th>ITEM CATEGORY</th>\n"
    html_data += "<th>CPU</th>\n"
    html_data += "<th>MEMORY</th>\n"
    html_data += "<th>DISKS</th>\n"
    html_data += "<th>UOM</th>\n"
    html_data += "<th>ENABLED FLAG</th>\n"
    html_data += "<th>CREATION DATE</th>\n"
    html_data += "<th>CREATED BY</th>\n"
    html_data += "<th>LAST UPDATE DATE</th>\n"
    html_data += "<th>LAST UPDATED BY</th>\n"


    html_data += "</tr>\n"
    for row in data:
        html_data += "<tr>\n"
        # html_data += "<td><button><i class='fa-solid fa-pencil'></i></button></td>\n"
        for item in row:
            html_data += "<td>{}</td>\n".format(item)
        html_data += "</tr>\n"
    html_data += "</table>"
    return html_data

@app.route("/get_inventory_data",methods=["GET"])
def get_inventory_data():
    inventory_id = request.args.get('inventory_id', '')
    install_location = request.args.get('install_location', '')
    project_code = request.args.get('project_code', '')
    quantity = request.args.get('quantity','')
    ip_address = request.args.get('ip_address', '')
    subnet_mask = request.args.get('subnet_mask', '')
    gateway = request.args.get('gateway', '')
    comments = request.args.get('comments', '')
    last_po_num = request.args.get('last_po_num', '')
    last_po_price = request.args.get('last_po_price', '')

    query = 'SELECT INVENTORY_ID, INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS, ' \
            'SUBNET_MASK, GATEWAY, COMMENTS, LAST_PO_NUM, LAST_PO_PRICE, RENEWAL_DATE, NOTES, ' \
            'CREATION_DATE, CREATED_BY_USER,LAST_UPDATE_DATE,LAST_UPDATED_BY_USER FROM INVENTORY_ONHAND WHERE 1=1'

    conditions = []

    if inventory_id:
        conditions.append(f"inventory_id = '{inventory_id}'")
    if install_location:
        conditions.append(f"INSTALL_LOCATION LIKE '%{install_location}%'")
    if project_code:
        conditions.append(f"PROJECT_CODE = '{project_code}'")
    if quantity:
        conditions.append(f"QUANTITY LIKE '%{quantity}%'")
    if ip_address:
        conditions.append(f"IP_ADDRESS = '{ip_address}'")
    if subnet_mask:
        conditions.append(f"SUBNET_MASK = '{subnet_mask}'")
    if gateway:
        conditions.append(f"GATEWAY = '{gateway}'")
    if comments:
        conditions.append(f"COMMENTS = '{comments}'")   
    if last_po_num:
        conditions.append(f"LAST_PO_NUM = '{last_po_num}'")
    if last_po_price:
        conditions.append(f"LAST_PO_PRICE = '{last_po_price}'")
        
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query)
    data=cursor.fetchall()

    html_data = "<table>\n"
    html_data += "<tr>\n"
    html_data += "<th>Sno.</th>\n"
    html_data += "<th>INSTALL LOCATION</th>\n"
    html_data += "<th>PROJECT CODE</th>\n"
    html_data += "<th>QUANTITY</th>\n"
    html_data += "<th>IP ADDRESS</th>\n"
    html_data += "<th>SUBNET MASK</th>\n"
    html_data += "<th>GATEWAY</th>\n"
    html_data += "<th>COMMENTS</th>\n"
    html_data += "<th>LAST PO NUM</th>\n"
    html_data += "<th>LAST PO PRICE</th>\n"
    html_data += "<th>RENEWAL DATE</th>\n"
    html_data += "<th>NOTES</th>\n"
    html_data += "<th>CREATION DATE</th>\n"
    html_data += "<th>CREATED BY</th>\n"
    html_data += "<th>LAST UPDATE DATE</th>\n"
    html_data += "<th>LAST UPDATED BY</th>\n"


    html_data += "</tr>\n"
    for row in data:
        html_data += "<tr>\n"
        for item in row:
            html_data += "<td>{}</td>\n".format(item)
        html_data += "</tr>\n"
    html_data += "</table>"

    return html_data

@app.route("/get_type_data", methods=["GET"])
def get_type_data():
    # Get filter values from request
    # item_id = request.args.get('item_id', '')
    lookup_type_number = request.args.get('lookup_type_number', '')
    lookup_type = request.args.get('lookup_type', '')
    type_description=request.args.get('type_description','')
    enabled_flag = request.args.get('enabled_flag', '')
    
    # Construct SQL query with WHERE conditions
    query = 'SELECT LOOKUP_TYPE_ID, LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG, CREATION_DATE, ' \
            'CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER FROM LOOKUP_TYPE WHERE 1=1'

    conditions = []

    # if item_id:
    #     conditions.append(f"ITEM_ID = '{item_id}'")
    if lookup_type_number:
        conditions.append(f"LOOKUP_TYPE_ID = '{lookup_type_number}'")
    if lookup_type:
        conditions.append(f"LOOKUP_TYPE LIKE '%{lookup_type}%'")
    if type_description:
        conditions.append(f"TYPE_DESCRIPTION LIKE '%{type_description}%'")
    if enabled_flag:
        conditions.append(f"ENABLED_FLAG = '{enabled_flag}'")    
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query)
    data = cursor.fetchall()

    # Format data as HTML for simplicity (you can use JSON for a more structured approach)
    html_data = "<table>\n"
    html_data += "<tr>\n"
    # html_data += "<th>Edit</th>\n"
    html_data += "<th>Type Number</th>\n"
    html_data += "<th>Lookup Type</th>\n"
    html_data += "<th>Type Description</th>\n"
    html_data += "<th>Enabled Flag</th>\n"
    html_data += "<th>Creation Date</th>\n"
    html_data += "<th>Created By</th>\n"
    html_data += "<th>Last Update Date</th>\n"
    html_data += "<th>Last Updated By</th>\n"


    html_data += "</tr>\n"
    for row in data:
        html_data += "<tr>\n"
        # html_data += "<td><button><i class='fa-solid fa-pencil'></i></button></td>\n"
        for item in row:
            html_data += "<td>{}</td>\n".format(item)
        html_data += "</tr>\n"
    html_data += "</table>"
    return html_data

@app.route("/get_value_data", methods=["GET"])
def get_value_data():
    # Get filter values from request
    # item_id = request.args.get('item_id', '')
    lookup_type_number1 = request.args.get('lookup_type_number1', '')
    lookup_code = request.args.get('lookup_code', '')
    lookup_value = request.args.get('lookup_value', '')
    value_description=request.args.get('value_description','')
    enabled_flag1 = request.args.get('enabled_flag1', '')
    
    # Construct SQL query with WHERE conditions
    query = 'SELECT LOOKUP_VALUE_ID, LOOKUP_TYPE_ID, LOOKUP_CODE, LOOKUP_VALUE, VALUE_DESCRIPTION, ' \
            'ENABLED_FLAG, CREATION_DATE, CREATED_BY_USER,LAST_UPDATE_DATE,LAST_UPDATED_BY_USER FROM LOOKUP_VALUES WHERE 1=1'

    conditions = []

    # if item_id:
    #     conditions.append(f"ITEM_ID = '{item_id}'")
    if lookup_type_number1:
        conditions.append(f"LOOKUP_TYPE_ID = '{lookup_type_number1}'")
    if lookup_code:
        conditions.append(f"LOOKUP_CODE LIKE '%{lookup_code}%'")
    if lookup_value:
        conditions.append(f"LOOKUP_VALUE LIKE '%{lookup_value}%'")
    if value_description:
        conditions.append(f"VALUE_DESCRIPTION LIKE '%{value_description}%'")
    if enabled_flag1:
        conditions.append(f"ENABLED_FLAG = '{enabled_flag1}'")    
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query)
    data = cursor.fetchall()

    # Format data as HTML for simplicity (you can use JSON for a more structured approach)
    html_data = "<table>\n"
    html_data += "<tr>\n"
    html_data += "<th>Sno.</th>\n"
    html_data += "<th>Type Number</th>\n"
    html_data += "<th>Lookup Code</th>\n"
    html_data += "<th>Lookup Value</th>\n"
    html_data += "<th>Value Description</th>\n"
    html_data += "<th>Enabled Flag</th>\n"
    html_data += "<th>Creation Date</th>\n"
    html_data += "<th>Created By</th>\n"
    html_data += "<th>Last Update Date</th>\n"
    html_data += "<th>Last Updated By</th>\n"


    html_data += "</tr>\n"
    for row in data:
        html_data += "<tr>\n"
        # html_data += "<td><button><i class='fa-solid fa-pencil'></i></button></td>\n"
        for item in row:
            html_data += "<td>{}</td>\n".format(item)
        html_data += "</tr>\n"
    html_data += "</table>"
    return html_data

@app.route("/get_header_data", methods=["GET"])
def get_header_data():
    # Get filter values from request
    # item_id = request.args.get('item_id', '')
    po_number = request.args.get('po_number', '')
    po_type = request.args.get('po_type', '')
    po_description = request.args.get('po_description', '')
    vendor_name=request.args.get('vendor_name','')
    vendor_location = request.args.get('vendor_location', '')
    quote_requested = request.args.get('quote_requested', '')
    quote_number = request.args.get('quoted_number', '')
    po_status = request.args.get('po_status', '')
    po_requested = request.args.get('po_requested', '')
    invoice_number = request.args.get('invoice_number', '')
    invoice_line_number = request.args.get('invoice_line_number', '')
    invoice_paid = request.args.get('invoice_paid', '')

    
    
    # Construct SQL query with WHERE conditions
    query = 'SELECT PO_HEADER_ID, PO_NUMBER, PO_TYPE, PO_DESCRIPTION, VENDOR_NAME, ' \
            'VENDOR_LOCATION, QUOTE_REQUESTED, QUOTE_NUMBER,PO_STATUS,PO_DATE,PO_APPROVED_DATE,'\
            'PO_APPROVED_BY, PO_REQUESTED,PO_REQUESTED_BY,INVOICE_NUMBER,INVOICE_LINE_NUMBER,INVOICE_AMOUNT,INVOICE_PAID,SUPPORT_START_DATE,SUPPORT_END_DATE,CREATION_DATE,CREATED_BY_USER,LAST_UPDATE_DATE,LAST_UPDATED_BY_USER FROM PO_HEADER WHERE 1=1'

    conditions = []

    # if item_id:
    #     conditions.append(f"ITEM_ID = '{item_id}'")
    if po_number:
        conditions.append(f"PO_NUMBER = '{po_number}'")
    if po_type:
        conditions.append(f"PO_TYPE LIKE '%{po_type}%'")
    if po_description:
        conditions.append(f"PO_DESCRIPTION LIKE '%{po_description}%'")
    if vendor_name:
        conditions.append(f"VENDOR_NAME LIKE '%{vendor_name}%'")
    if vendor_location:
        conditions.append(f"VENDOR_LOCATION = '{vendor_location}'")  
    if quote_requested:
        conditions.append(f"QUOTE_REQUESTED = '{quote_requested}'")  
    if quote_number:
        conditions.append(f"QUOTE_NUMBER = '{quote_number}'")  
    if po_status:
        conditions.append(f"PO_STATUS = '{po_status}'")
    if po_requested:
        conditions.append(f"PO_REQUESTED = '{po_requested}'")  
    if invoice_number:
        conditions.append(f"INVOICE_NUMBER = '{invoice_number}'")  
    if invoice_line_number:
        conditions.append(f"INVOICE_LINE_NUMBER = '{invoice_line_number}'")  
    if invoice_paid:
        conditions.append(f"INVOICE_PAID = '{invoice_paid}'")      
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query)
    data = cursor.fetchall()

    # Format data as HTML for simplicity (you can use JSON for a more structured approach)
    html_data = "<table>\n"
    html_data += "<tr>\n"
    html_data += "<th>Sno.</th>\n"
    html_data += "<th>PO Number</th>\n"
    html_data += "<th>PO Type</th>\n"
    html_data += "<th>PO Description</th>\n"
    html_data += "<th>Vendor Name</th>\n"
    html_data += "<th>Vendor Location</th>\n"
    html_data += "<th>Quote Requested</th>\n"
    html_data += "<th>Quote Number</th>\n"
    html_data += "<th>PO Status</th>\n"
    html_data += "<th>PO Date</th>\n"
    html_data += "<th>PO Approved Date</th>\n"
    html_data += "<th>PO Approved By</th>\n"
    html_data += "<th>PO Requested</th>\n"
    html_data += "<th>PO Requested By</th>\n"
    html_data += "<th>Invoice Number</th>\n"
    html_data += "<th>Invoice Line Number</th>\n"
    html_data += "<th>Invoice Amount</th>\n"
    html_data += "<th>Invoice Paid</th>\n"
    html_data += "<th>Support Start Date</th>\n"
    html_data += "<th>Support End Date</th>\n"
    html_data += "<th>Creation Date</th>\n"
    html_data += "<th>Created By</th>\n"
    html_data += "<th>Last Update Date</th>\n"
    html_data += "<th>Last Updated By</th>\n"



    html_data += "</tr>\n"
    for row in data:
        html_data += "<tr>\n"
        # html_data += "<td><button><i class='fa-solid fa-pencil'></i></button></td>\n"
        for item in row:
            html_data += "<td>{}</td>\n".format(item)
        html_data += "</tr>\n"
    html_data += "</table>"
    return html_data

@app.route("/get_lines_data", methods=["GET"])
def get_lines_data():
    # Get filter values from request
    # item_id = request.args.get('item_id', '')
    po_header_number = request.args.get('po_header_number', '')
    po_line_number = request.args.get('po_line_number', '')
    item_number = request.args.get('item_number', '')
    po_line_description=request.args.get('po_line_description','')
    po_line_status = request.args.get('po_line_status', '')
    ship_location = request.args.get('ship_location', '')
    invoice_number1 = request.args.get('invoice_number1', '')
    invoice_line_number1 = request.args.get('invoice_line_number1', '')
    invoice_paid1 = request.args.get('invoice_paid1', '')
    po_line_comments = request.args.get('po_line_comments', '')

    
    
    # Construct SQL query with WHERE conditions
    query = 'SELECT PO_LINE_ID,PO_HEADER_ID, PO_LINE_NUMBER, ITEM_ID, PO_LINE_DESCRIPTION, QUANTITY, ' \
            'UNIT_PRICE, LINE_TAX_AMOUNT,SUPPORT_START_DATE,SUPPORT_END_DATE,NEED_BY_DATE,'\
            'PO_LINE_STATUS, SHIP_LOCATION,INVOICE_NUMBER,INVOICE_LINE_NUMBER,INVOICE_DATE,INVOICE_PAID,INVOICE_AMOUNT,PO_LINE_COMMENTS,CREATION_DATE,CREATED_BY_USER,LAST_UPDATE_DATE,LAST_UPDATED_BY_USER FROM PO_LINES WHERE 1=1'

    conditions = []

    # if item_id:
    #     conditions.append(f"ITEM_ID = '{item_id}'")
    if po_header_number:
        conditions.append(f"PO_HEADER_ID = '{po_header_number}'")
    if po_line_number:
        conditions.append(f"PO_LINE_NUMBER = '{po_line_number}'")
    if item_number:
        conditions.append(f"ITEM_ID LIKE '%{item_number}%'")
    if po_line_description:
        conditions.append(f"PO_LINE_DESCRIPTION LIKE '%{po_line_description}%'")
    if po_line_status:
        conditions.append(f"PO_LINE_STATUS = '{po_line_status}'")  
    if ship_location:
        conditions.append(f"SHIP_LOCATION = '{ship_location}'")  
    if invoice_number1:
        conditions.append(f"INVOICE_NUMBER = '{invoice_number1}'")  
    if invoice_line_number1:
        conditions.append(f"INVOICE_LINE_NUMBER = '{invoice_line_number1}'")
    if invoice_paid1:
        conditions.append(f"INVOICE_PAID = '{invoice_paid1}'")  
    if po_line_comments:
        conditions.append(f"PO_LINE_COMMENTS = '{po_line_comments}'")        
    if conditions:
        query += " AND " + " AND ".join(conditions)

    cursor.execute(query)
    data = cursor.fetchall()

    # Format data as HTML for simplicity (you can use JSON for a more structured approach)
    html_data = "<table>\n"
    html_data += "<tr>\n"
    html_data += "<th>Sno.</th>\n"
    html_data += "<th>PO Header Number</th>\n"
    html_data += "<th>PO Line Number</th>\n"
    html_data += "<th>Item Number</th>\n"
    html_data += "<th>PO Line Description</th>\n"
    html_data += "<th>Quantity</th>\n"
    html_data += "<th>Unit Price</th>\n"
    html_data += "<th>Line Tax Amount</th>\n"
    html_data += "<th>Support Start Date</th>\n"
    html_data += "<th>Support End Date</th>\n"
    html_data += "<th>Need By Date</th>\n"
    html_data += "<th>PO Line Status</th>\n"
    html_data += "<th>Ship Location</th>\n"
    html_data += "<th>Invoice Number</th>\n"
    html_data += "<th>Invoice Line Number</th>\n"
    html_data += "<th>Invoice Date</th>\n"
    html_data += "<th>Invoice Paid</th>\n"
    html_data += "<th>Invoice Amount</th>\n"
    html_data += "<th>PO Line Comments</th>\n"
    html_data += "<th>Creation Date</th>\n"
    html_data += "<th>Created By</th>\n"
    html_data += "<th>Last Update Date</th>\n"
    html_data += "<th>Last Updated By</th>\n"
    html_data += "</tr>\n"
    for row in data:
        html_data += "<tr>\n"
        # html_data += "<td><button><i class='fa-solid fa-pencil'></i></button></td>\n"
        for item in row:
            html_data += "<td>{}</td>\n".format(item)
        html_data += "</tr>\n"
    html_data += "</table>"
    return html_data


#all Add items present here

@app.route('/execute', methods=['POST'])
def execute():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "insert_item_master.py", username])
        return render_template("item_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"



@app.route('/execute1',methods=['POST'])
def execute1():
    try:
        username = session.get('username', '') 
        subprocess.run(["python","insert_inventory.py",username])
        return render_template("inventory.html")
    except Exception as e:
        return f"Error during execution:{str(e)}"


@app.route('/execute2', methods=['POST'])
def execute2():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Insert_Loookup_Type.py", username])
        return render_template("lookup_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"
    
@app.route('/execute3', methods=['POST'])
def execute3():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Insert_Lookup_Values.py", username])
        return render_template("lookup_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"

   
@app.route('/execute4', methods=['POST'])
def execute4():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Insert_PO_Header.py", username])
        return render_template("purchase_orders.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"
    
   
@app.route('/execute5', methods=['POST'])
def execute5():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Insert_PO_Lines.py", username])
        return render_template("purchase_orders.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"



    
@app.route('/update', methods=['POST'])
def update():
    try:
        username = session.get('username', '')
        subprocess.run(["python", "Modify_Item_Master.py", username])
        return render_template("item_details.html")
    except Exception as e:
        return f"Error during execution: {str(e)}"


    
@app.route('/update1', methods=['POST'])
def update1():
    try:
        username = session.get('username', '')
        subprocess.run(["python", "Modify_Inventory_On_Hand.py", username])
        return render_template("inventory.html")
    except Exception as e:
        return f"Error during execution: {str(e)}"
    
    
@app.route('/update2', methods=['POST'])
def update2():
    try:
        username = session.get('username', '')
        subprocess.run(["python", "Modify_Lookup_Type.py", username])
        return render_template("lookup_details.html")
    except Exception as e:
        return f"Error during execution: {str(e)}"

    
@app.route('/update3', methods=['POST'])
def update3():
    try:
        username = session.get('username', '')
        subprocess.run(["python", "Moidfy_Lookup_Values.py", username])
        return render_template("lookup_details.html")
    except Exception as e:
        return f"Error during execution: {str(e)}"

    
@app.route('/update4', methods=['POST'])
def update4():
    try:
        username = session.get('username', '')
        subprocess.run(["python", "Modify_PO_Header.py", username])
        return render_template("purchase_orders.html")
    except Exception as e:
        return f"Error during execution: {str(e)}"

    
@app.route('/update5', methods=['POST'])
def update5():
    try:
        username = session.get('username', '')
        subprocess.run(["python", "Modify_PO_Lines.py", username])
        return render_template("purchase_orders.html")
    except Exception as e:
        return f"Error during execution: {str(e)}"
    

 


@app.route('/upload', methods=['POST'])
def upload():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "import_ITEM_MASTER.py", username])
        return render_template("item_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"
    


@app.route('/upload1', methods=['POST'])
def upload1():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Import_Inventory_On_hand.py", username])
        return render_template("inventory.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"

@app.route('/upload2', methods=['POST'])
def upload2():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Import_Lookup_Type.py", username])
        return render_template("lookup_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"

@app.route('/upload3', methods=['POST'])
def upload3():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Import_Lookup_Values.py", username])
        return render_template("lookup_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"

@app.route('/upload4', methods=['POST'])
def upload4():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Import_PO_Header.py", username])
        return render_template("purchase_orders.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"

@app.route('/upload5', methods=['POST'])
def upload5():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "Import_PO_Lines.py", username])
        return render_template("purchase_orders.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"
   
    

@app.route('/extract', methods=['POST'])
def extract():
    try:
        username = session.get('username', '')  # Get the username from the session
        subprocess.run(["python", "export_ITEM_MASTER.py", username])
        return render_template("item_details.html")
    except Exception as e:
         return f"Error during execution: {str(e)}"


# @app.route("/insert_data", methods=["POST"])
# def insert_data():
#     try:
#         # Receive data from the client
#         data = request.get_json()
#         # Extract data fields
#         # name = data.get("name")
#         username = data.get("username")
#         email = data.get("email")
#         password = data.get("password")
#         phonenumber = data.get("phonenumber")
        
#         # Execute your SQL query to insert data into the database
#         cursor.execute("INSERT INTO Users ( username, email, password,phonenumber) VALUES (?, ?, ?, ?);",
#                        (username, email, phonenumber,password))
#         conn.commit()

#         return jsonify({"message": "registered successfully"})
    
#     except Exception as e:
#         return jsonify({"error": str(e)})
@app.route("/insert_data", methods=["POST"])
def insert_data():
    try:
        # Receive data from the client
        data = request.get_json()
        # Extract data fields
        name = data.get("name")
        email = data.get("email")
        phonenumber = data.get("phonenumber")
        username = data.get("username")
        password = data.get("password")
        
        # Execute your SQL query to insert data into the database
        cursor.execute("INSERT INTO users (name, email, phonenumber, username, password) VALUES (?, ?, ?, ?, ?);",
                       (name, email, phonenumber, username, password));
        conn.commit()

        return jsonify({"message": "registered successfully"})
    
    except Exception as e:
        return jsonify({"error": str(e)})



@app.route("/insert_data1", methods=["POST"])
def insert_data1():
    try:
        # Receive data from the client
        data = request.get_json()
        # Extract data fields
        ITEM_NUMBER = data.get("ITEM_NUMBER")
        ITEM_DESCRIPTION = data.get("ITEM_DESCRIPTION")
        ITEM_TYPE = data.get("ITEM_TYPE")
        MANUFACTURER_CODE = data.get("MANUFACTURER_CODE")
        ITEM_CATEGORY = data.get("ITEM_CATEGORY")
        CPU = data.get("CPU")
        MEMORY = data.get("MEMORY")
        DISKS = data.get("DISKS")
        UOM = data.get("UOM")
        ENABLED_FLAG = data.get("ENABLED_FLAG")
        CREATION_DATE = data.get("CREATION_DATE")
        CREATED_BY_USER=session['username']
        LAST_UPDATE_DATE = data.get("LAST_UPDATE_DATE")
        LAST_UPDATE_BY_USER=session['username']
        # Execute your SQL query to insert data into the database
        cursor.execute("INSERT INTO ITEM_MASTER (ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE,MANUFACTURER_CODE, ITEM_CATEGORY, CPU,MEMORY,DISKS,UOM,ENABLED_FLAG, CREATION_DATE,CREATED_BY_USER, LAST_UPDATE_DATE,LAST_UPDATED_BY_USER) VALUES (?,?,?, ?, ?, ?, ?, ?, ?, ?,?,?,?,?);",
                       (ITEM_NUMBER, ITEM_DESCRIPTION, ITEM_TYPE,MANUFACTURER_CODE, ITEM_CATEGORY,CPU, MEMORY, DISKS,UOM,ENABLED_FLAG,CREATION_DATE,CREATED_BY_USER,LAST_UPDATE_DATE,LAST_UPDATE_BY_USER))
        conn.commit()

        return jsonify({"message": "Data inserted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/insert_data2", methods=["POST"])
def insert_data2():
    try:
        # Receive data from the client
        data = request.get_json()
        # current_date = date.now().strftime('%Y-%m-%d')
        # Extract data fields
        LOOKUP_TYPE = data.get("LOOKUP_TYPE")
        TYPE_DESCRIPTION = data.get("TYPE_DESCRIPTION")
        ENABLED_FLAG = data.get("ENABLED_FLAG")
        CREATION_DATE = data.get("CREATION_DATE")
        CREATED_BY_USER=session['username']
        LAST_UPDATE_DATE = data.get("LAST_UPDATE_DATE")
        LAST_UPDATE_BY_USER=session['username']
        # Execute your SQL query to insert data into the database
        cursor.execute("INSERT INTO LOOKUP_TYPE (LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG,CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE,LAST_UPDATED_BY_USER) VALUES (?,?,?, ?, ?, ?, ? );",
                       (LOOKUP_TYPE, TYPE_DESCRIPTION, ENABLED_FLAG,CREATION_DATE, CREATED_BY_USER,LAST_UPDATE_DATE, LAST_UPDATE_BY_USER))
        conn.commit()

        return jsonify({"message": "Data inserted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/insert_data3", methods=["POST"])
def insert_data3():
    try:
        # Receive data from the client
        data = request.get_json()
        # current_date = date.now().strftime('%Y-%m-%d')
        # Extract data fields
        LOOKUP_TYPE_NUMBER = data.get("LOOKUP_TYPE_NUMBER")
        LOOKUP_CODE = data.get("LOOKUP_CODE")
        LOOKUP_VALUE = data.get("LOOKUP_VALUE")
        VALUE_DESCRIPTION = data.get("VALUE_DESCRIPTION")
        ENABLED_FLAG1 = data.get("ENABLED_FLAG1")
        CREATION_DATE2 = data.get("CREATION_DATE2")
        CREATED_BY_USER=session['username']
        LAST_UPDATE_DATE2 = data.get("LAST_UPDATE_DATE2")
        LAST_UPDATE_BY_USER=session['username']
        # Execute your SQL query to insert data into the database
        cursor.execute("INSERT INTO LOOKUP_VALUES (LOOKUP_TYPE_ID,LOOKUP_CODE,LOOKUP_VALUE, VALUE_DESCRIPTION, ENABLED_FLAG,CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE,LAST_UPDATED_BY_USER) VALUES (?,?,?, ?, ?, ?, ? ,?,?);",
                       (LOOKUP_TYPE_NUMBER,LOOKUP_CODE,LOOKUP_VALUE ,VALUE_DESCRIPTION, ENABLED_FLAG1,CREATION_DATE2, CREATED_BY_USER,LAST_UPDATE_DATE2, LAST_UPDATE_BY_USER))
        conn.commit()

        return jsonify({"message": "Data inserted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/insert_data4", methods=["POST"])
def insert_data4():
    try:
        # Receive data from the client
        data = request.get_json()
        # current_date = date.now().strftime('%Y-%m-%d')
        # Extract data fields
        ITEM_NUMBER = data.get("ITEM_NUMBER")
        INSTALL_LOCATION = data.get("INSTALL_LOCATION")
        PROJECT_CODE = data.get("PROJECT_CODE")
        QUANTITY = data.get("QUANTITY")
        IP_ADDRESS = data.get("IP_ADDRESS")
        SUBNET_MASK = data.get("SUBNET_MASK")
        GATEWAY = data.get("GATEWAY")
        COMMENTS = data.get("COMMENTS")
        LAST_PO_NUM = data.get("LAST_PO_NUM")
        LAST_PO_PRICE = data.get("LAST_PO_PRICE")
        RENEWAL_DATE = data.get("RENEWAL_DATE")
        NOTES = data.get("NOTES")
        CREATION_DATE = data.get("CREATION_DATE")
        CREATED_BY_USER=session['username']
        LAST_UPDATE_DATE = data.get("LAST_UPDATE_DATE")
        LAST_UPDATED_BY_USER=session['username']
        # Execute your SQL query to insert data into the database
        cursor.execute("INSERT INTO INVENTORY_ONHAND (ITEM_ID, INSTALL_LOCATION, PROJECT_CODE, QUANTITY, IP_ADDRESS, SUBNET_MASK, GATEWAY, COMMENTS, LAST_PO_NUM, LAST_PO_PRICE, RENEWAL_DATE, NOTES, CREATION_DATE, CREATED_BY_USER, LAST_UPDATE_DATE, LAST_UPDATED_BY_USER) VALUES (?,?,?,?,?, ?, ?, ?, ? ,?,?,?,?,?,?,?);",
                       (ITEM_NUMBER,INSTALL_LOCATION,PROJECT_CODE ,QUANTITY, IP_ADDRESS,SUBNET_MASK, GATEWAY,COMMENTS, LAST_PO_NUM,LAST_PO_PRICE,RENEWAL_DATE,NOTES,CREATION_DATE,CREATED_BY_USER,LAST_UPDATE_DATE,LAST_UPDATED_BY_USER))
        conn.commit()

        return jsonify({"message": "Data inserted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__": 
	app.run(debug=True) 
