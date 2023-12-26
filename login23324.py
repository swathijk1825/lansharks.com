#!/usr/bin/env python3
import cgi

import mysqlx
from config import DATABASE_CONFIG, SQL_TABLE_NAME_INCIDENT, CSV_FILE_PATH_poision
from helper import transform_username, upload_incidents_to_csv_file


print('Content-type:text/html')
print('')
print('')
print('')
print('<html>')
print('<head>')
print('<meta http-equiv="content-type" content="text/html; charset=utf-8">')
print('<link rel="stylesheet" type="text/css" href="styles.css">')
print('<title>LAN Sharks App</title>')
print('</head>')

# Read content from a file (you can customize this part)
with open('/var/www/lansharks.com/pageStart.htm', 'r') as end:
    content = end.readlines()

# Iterate over the content and print each line
for line in content:
    print(line.rstrip('\n'))

# Get form data
form = cgi.FieldStorage()
userName = form.getvalue('UserName')
password = form.getvalue('Password')
employee = form.getvalue('employee')

connection_string = f"mysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}/{DATABASE_CONFIG['database']}"

db = mysqlx.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'P@ssw0rd',
    database = 'python'
)
upload_incidents_to_csv_file(db, CSV_FILE_PATH_poision, SQL_TABLE_NAME_INCIDENT)

engine = create_engine(db)

cursor = db.cursor()

sql = "SELECT * FROM users WHERE userName = '"+str(userName).lower()+"' AND password = '"+str(password)+"'"
cursor.execute(sql)
results = cursor.fetchall()


sql = "SELECT * FROM users WHERE userName = %s AND password = %s"
cursor.execute(sql, (str(userName).lower(), str(password)))

results = cursor.fetchone()  # Use fetchone() to get a single row

print(results)


# Process user based on the authentication results
if len(results) == 1:
    user_type = results[0][3]
    print(user_type)
    if user_type == 'e' and employee == 'Employee':
        lastName = transform_username(userName)
        print(lastName)
        employeeSQL = "SELECT * FROM employees WHERE lastName = '" + str(lastName) + "'"
        print(employeeSQL)
        cursor.execute(employeeSQL)
        employee_data = cursor.fetchall()

        print(employee_data)
        if employee_data:
            print('<h2 class="heading">Employee Information</h2>')
            print('<p class="description">Name: {} {}</p>'.format(employee_data[0][0], employee_data[0][1]))
            print('<p class="description">Position: {}</p>'.format(employee_data[0][2]))
            print('<p class="description">Email: {}</p>'.format(employee_data[0][3]))
            print('<p class="description">userName: {}</p>'.format(userName))

            # Add link to change password
            print('<a href="http://www.lansharks.com/change_password.htm" style="color: #FFD700;">Change Password</a>')
        else:
            print('<h2 class="heading">Employee Data Not Found</h2>')
    elif user_type == 'e' and employee != 'employee':
        print('<h2 class="heading">Authentication Failed</h2>')
        print('<p class="description">Sorry, if you are an employee, please click the checkbox. If you are not an employee, please ignore. Click <a href="http://www.lansharks.com/login.htm" style="color: #FFD700;">here</a> to retry.</p>')
    elif user_type == 'c' and employee != 'employee':
        lastName = transform_username(userName)
        customerSQL = "SELECT * FROM customers WHERE lastName = '" + str(lastName) + "'"
        cursor.execute(customerSQL)
        customer_data = cursor.fetchall()

        if customer_data:
            customer_id = customer_data[0][0]
            print('<h2 class="heading">Customer Information</h2>')
            print('<p class="description">Name: {} {}</p>'.format(customer_data[0][1], customer_data[0][2]))
            print('<p class="description">Position: {}</p>'.format(customer_data[0][3]))
            print('<p class="description">Email: {}</p>'.format(customer_data[0][4]))

            # Assuming customer_id is an integer, adjust as needed
            incidentSQL = "SELECT * FROM incidents WHERE customerNumber = " + str(customer_id)
            incident_data = cursor.execute(incidentSQL)
            if incident_data:
                attack_type = incident_data[0]['incidentID']
                print(attack_type)
else:
    print('<h2 class="heading">Authentication Failed</h2>')
    print('<p class="description">Click <a href="http://www.lansharks.com/login.htm" style="color: #FFD700;">here</a> to retry.</p>')

with open('/var/www/lansharks.com/pageEnd.htm', 'r') as end:
    content = end.readlines()

for i in content:
    print(i.rstrip('\n'))
cursor.close()
db.close()


