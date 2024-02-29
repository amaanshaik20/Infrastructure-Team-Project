from flask import Flask,render_template,session,request,redirect,url_for
import pyodbc

app = Flask(__name__) 
app.secret_key = 'your_secret_key'  # Change this to a secure secret key

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=AmaanShaik\SQLEXPRESS;'
                      'Database=InfraDB;'
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

@app.route("/main", methods=["GET", "POST"])
def main():
    if request.method == "POST":
        # Assuming you have a users table with columns 'username' and 'password'
        username = request.form.get("username")
        password = request.form.get("password")

    
        # Check the credentials (This is a simple example, not secure for production)
        cursor.execute("SELECT * FROM admin WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            session['username'] = username  # Store the username in the session
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
            'ITEM_CATEGORY, CPU, MEMORY, DISKS, UOM, CREATION_DATE, CREATED_BY_USER, ' \
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


if __name__ == "__main__": 
	app.run(debug=True) 