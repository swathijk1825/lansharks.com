import csv
import datetime
import glob
import mysql.connector
import os
from config import CSV_FILE_PATH_poision
import pandas as pd



def transform_username(input_string):
    if len(input_string) > 1:
        return input_string[1].upper() + input_string[2:]
    else:
        return ''    

def update_passwd_in_db(db,userID,new_password):
    try:
        print(userID)
        print(new_password)
        update_password_sql = "UPDATE users SET password = %s WHERE userID = %s"
        print(update_password_sql)
        cursor = db.cursor()
        cursor.execute(update_password_sql, (new_password, userID))
        db.commit()
        cursor.close()
        db.close()
    except mysql.connector.Error as err:
            print(f"Error: {err}")
    

def change_password(db,new_password,confirm_password,userName):
    if new_password and new_password == confirm_password:
        update_passwd_in_db(db, userName, new_password)
        print('<p class="description">Password changed successfully. Click <a href="http://www.lansharks.com/login.htm" style="color: #FFD700;">here</a> Please login with your new password.</p>')
    else:
        print('<p class="description">Either your username is invalid or New password and confirm password do not match.</p>')


def get_details_from_form(form,dbConnector,customerNumber):
    cursor = dbConnector.cursor()
    update_details_action = form.getvalue('update_concat')
    
    if update_details_action:
        companyName=form.getvalue('company-name')
        address=form.getvalue('address')
        city=form.getvalue('city')
        state=form.getvalue('state')
        zipCode=form.getvalue('zip-code')
        email=form.getvalue('email')
        phone=form.getvalue('phone')
      # Define update query
        update_query = """
            UPDATE customer_table
            SET
                companyName = %(companyName)s,
                address = %(address)s,
                city = %(city)s,
                state = %(state)s,
                zipCode = %(zipCode)s,
                email = %(email)s,
                phone = %(phone)s
            WHERE customerNumber = %(customerNumber)s;
        """

        # Prepare and execute the query
        cursor.execute(update_query, {
            "companyName": companyName,
            "address": address,
            "city": city,
            "state": state,
            "zipCode": zipCode,
            "email": email,
            "phone": phone,
            "customerNumber": customerNumber
        })
        dbConnector.commit()
        cursor.close()
        dbConnector.close()

def upload_data_from_csv():
    # Replace these values with your actual MySQL connection details
    mysql_user = 'root'
    mysql_password = 'P@ssw0rd'
    mysql_host = 'localhost'
    mysql_database = 'python'

    # Establish MySQL connection
    db_connection = mysql.connector.connect(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        database=mysql_database
    )
    # Create a cursor
    cursor = db_connection.cursor()

    # Read CSV file and insert data into 'incidents' table
    sql_table_name = 'incidents'

    # Define column mapping
    column_mapping = {
        "Host": "hostIP",
        "Protocol": "protocol",
        "Source Port": "srcPort",
        "Destination Port": "destPort",
        "Source Mac": "srcMac",
        "Dest Mac": "destMac",
        "Info": "info",
        "Time": "packetDateTime",
        "Source": "srcIP",
        "Destination": "destIP",
    }

    current_dir = os.path.dirname(os.path.realpath(__file__))

    # Define the path to the "logs" subfolder
    logs_folder_path = os.path.join(current_dir, 'logs')

    # Use glob to get a list of all CSV files in the "logs" subfolder
    csv_files = glob.glob(os.path.join(logs_folder_path, '*.csv'))

    if csv_files:
# Process each CSV file in the "logs" subfolder
        for csv_file in csv_files:
            # Extract customer_id from the file name
            customer_id = os.path.splitext(os.path.basename(csv_file))[0].split('_')[0]

            with open(csv_file, 'r') as file:
                csv_reader = csv.DictReader(file)
                # Insert data into 'incidents' table
                for row in csv_reader:
                    # Map CSV column names to table column names
                    mapped_values = {table_column: row[csv_column] for csv_column, table_column in column_mapping.items()}
                    
                    # Add customer_id to the mapped values
                    mapped_values['customerNumber'] = customer_id

                    # Generate the INSERT INTO query dynamically
                    insert_query = f"INSERT INTO {sql_table_name} ({','.join(mapped_values.keys())}) VALUES ({','.join(['%s']*len(mapped_values))})"
                    cursor.execute(insert_query, tuple(mapped_values.values()))

        # Rename the processed CSV file to have a ".csv.old" extension
        filename_without_extension = os.path.splitext(os.path.basename(csv_file))[0]
        today = datetime.datetime.now().strftime("%Y%m%d")
        new_filename = f"{filename_without_extension}_{today}.csv.old"
        os.rename(csv_file, os.path.join(logs_folder_path, new_filename))

    # Commit changes and close connections
    db_connection.commit()
    cursor.close()
    db_connection.close()

    print(f"Data successfully inserted into the '{sql_table_name}' table, and CSV files have been renamed.")



def load_ARP_To_Attacks_table(db, user_id):
    try:
        # Insert ARP attack results for the specified customer
        # ...

        # Your SQL query
        sql_query = f"""
            SELECT srcMac, packetDateTime AS date, COUNT(DISTINCT extractedIP) AS unique_ip_count
            FROM (
                SELECT srcMac, packetDateTime, TRIM(BOTH ' ' FROM SUBSTRING_INDEX(SUBSTRING_INDEX(info, ' ', -1), ' ', 1)) AS extractedIP
                FROM incidents
                WHERE protocol = 'ARP' AND customerNumber = {user_id}
            ) AS arp_data
            GROUP BY srcMac, packetDateTime having unique_ip_count > 1;
        """

        cursor = db.cursor()

        # Execute the query
        cursor.execute(sql_query)


        # Fetch all the rows
        results = cursor.fetchall()

        for result in results:
            info=result[0]
            time_value=result[1]
            attacks=f"{int(result[2])-1} attacks" 
            attack_type='ARP'
            sql_query = "INSERT INTO attacks (userID, attack_type, info, attacks, time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_query, (user_id, attack_type, info, attacks, time_value))

        db.commit()
        print("attacks table ARP updated")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the cursor
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
def load_SYN_Attacks_table(db, user_id):
    try:
        # Your SQL query
        sql_query = f"""
            SELECT packetDateTime, destPort, COUNT(*) AS attack_count
            FROM incidents
            WHERE srcIP = destIP AND customerNumber = {user_id} AND info LIKE '%[SYN]%'
            GROUP BY packetDateTime, destPort;
        """
        print('SYN')

        cursor = db.cursor()
        # Execute the query
        cursor.execute(sql_query)

        # Fetch all the rows
        results = cursor.fetchall()

        # Print the results
        print(results)

        for result in results:
            info='PACKET FLAG [SYN]'
            time_value=result[0]
            attacks= f"Port {result[1]} , attacks {result[2]}"
            attack_type='Packet Flood'
            sql_query = "INSERT INTO attacks (userID, attack_type, info, attacks, time) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql_query, (user_id, attack_type, info, attacks, time_value))

        db.commit()
        print("attacks table SYN updated")

        # Insert any additional logic here for processing the SYN attack results

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        # Close the cursor
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

def read_variable(file_path):
     with open(file_path, 'r') as file:
        line = file.readline().strip()
        key, value = line.split('=')
        return key, value
     
def write_variable(file_path, key,value):
    with open(file_path, 'w') as file:
        file.write(f"{key}={value}\n")


def get_customer_details(db_connector, customer_number):
    cursor = db_connector.cursor()
    select_query = "SELECT * FROM customer_table WHERE customerNumber = %s"
    cursor.execute(select_query, (customer_number,))
    customer_data = cursor.fetchone()
    cursor.close()
    return customer_data

def generate_update_form(customer_data):
    # Generate the updated form with pre-filled values
    html_form = """
        <form class="loginform" action="update_contact.py" method="post">
            <!-- Contact Information fields -->
            <!-- Additional Contact Information fields -->
            <label for="company">Company Name: </label>
            <input size="50" type="text" id="company" name="CompanyName" value="%s"/><p/>

            <label for="street">Address: </label>
            <input size="50" type="text" id="street" name="Street" value="%s"/><p/>

            <label for="city">City: </label>;
            <input size="15" type="text" id="city" name="City" value="%s"/><p/>

            <label for="email">E-mail: </label>
            <input required="required" size="30" type="email" id="email" name="Email" value="%s"/><p/>

            <label for="zip">ZIP code: </label>
            <input required="required" size="10" maxlength="5" type="text" id="zip" name="ZIP" value="%s"/><p/>

            <label for="state">State: </label>
            <input size="15" type="text" id="state" name="State" value="%s"/><p/>

            <label for="phone">Phone: </label>
            <input size="10" type="tel" id="phone" name="Phone" value="%s"/><p/>
            <!-- End of Additional Contact Information fields -->
            
            <!-- Submit button -->
            <input class="button btnlogin" type="submit" value="Update contact information" /><p/>
            <input type="hidden" name="update_concat" value="1">
        </form>
    """ % (
        customer_data['companyName'],
        customer_data['address'],
        customer_data['city'],
        customer_data['email'],
        customer_data['zipCode'],
        customer_data['state'],
        customer_data['phone']
    )
    return html_form

    



      