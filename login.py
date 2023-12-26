#!/usr/bin/env python3
from config import SQL_TABLE_NAME_INCIDENT, CSV_FILE_PATH_poision
from helper import  get_details_from_form, load_ARP_To_Attacks_table, load_SYN_Attacks_table, transform_username, update_passwd_in_db, upload_data_from_csv, write_variable
import mysql.connector
import cgi, cgitb


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
current_user = form.getvalue('UserName')
password = form.getvalue('Password')
employee = form.getvalue('employee')



db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'P@ssw0rd',
    database = 'python'
)

# upload_incidents_to_csv_file(db, CSV_FILE_PATH_poision, SQL_TABLE_NAME_INCIDENT)
cursor = db.cursor()


sql = "SELECT * FROM users WHERE userName = '"+str(current_user).lower()+"' AND password = '"+str(password)+"'"
cursor.execute(sql)
results = cursor.fetchall()
if len(results) == 1:
    user_type = results[0][3]
    user_id=results[0][0]
    if(current_user):
        variable_file = 'shared_variables.txt'
    write_variable(variable_file,'current_user',user_id)
    if user_type == 'e' and employee != 'Employee':
        print('<h2 class="heading">Authentication Failed if ur employee please click on the checkbox provided in login page</h2>')
        print('<p class="description">Click <a href="http://www.lansharks.com/login.htm" style="color: #FFD700;">here</a> Click here to retry login.</p>')
    elif user_type == 'e' and employee == 'Employee':

        lastName = transform_username(current_user)
        employeeSQL = "SELECT * FROM employees WHERE lastName = '" + str(lastName) + "'"
        cursor.execute(employeeSQL)
        employee_data = cursor.fetchall()
        if employee_data:
            print('<h2 class="heading">Employee Information</h2>')
            print('<p class="description">userName: {}</p>'.format(current_user))
            print('<p class="description">Position: {}</p>'.format(employee_data[0][2]))
            print('<p class="description">Email: {}</p>'.format(employee_data[0][3]))
            print('<a href="http://www.lansharks.com/change_password.htm" style="color: #FFD700; margin-right: 2px;">Change Password?</a>')
            print('<a href="http://www.lansharks.com/update_contact.htm" style="color: #FFD700; margin-right: 2px;">Update Contact?</a>')
    elif user_type == 'c' and employee != 'employee':
        lastName = transform_username(current_user)
        customerSQL = "SELECT * FROM customers WHERE lastName = '" + str(lastName) + "'"
        cursor.execute(customerSQL)
        customer_data = cursor.fetchall()
        if customer_data:
            customer_id = customer_data[0][0]
            print('<p class="description">{}</p>'.format(customer_data[0][1], customer_data[0][2]))
            print('<p class="description">{} </p>'.format(customer_data[0][3]))
            print('<a href="http://www.lansharks.com/update_contact.htm" style="color: #FFD700;">Update Contact?</a>')
            # upload_data_from_csv()
            # load_ARP_To_Attacks_table(db,customer_id)
            # load_SYN_Attacks_table(db,customer_id)    
            # attacksSQL = "SELECT * FROM attacks WHERE userID = {}".format(customer_id)
            # cursor.execute(attacksSQL)
            # attacks_data = cursor.fetchall()

        # Display attacks informations
        # if attacks_data:
        #     print('<table>')
        #     print('<tr><th>Attack Type</th><th>Info </th><th>Attacks </th><th>Time  </th></tr>')
        #     for attack in attacks_data:
        #         print('<tr>')
        #         print('<td>{} </td>'.format(attack[1]))
        #         print('<td>{} </td>'.format(attack[2]))
        #         print('<td>{} </td>'.format(attack[3]))
        #         print('<td>{} </td>'.format(attack[4]))
        #         print('</tr>')
        #     print('</table>')
            # cal_attacks_from_incident_table()            
else:
    print('<h2 class="heading">Authentication Failed please try again</h2>')
    print('<p class="description">Click <a href="http://www.lansharks.com/login.htm" style="color: #FFD700;">here</a> Click here to retry login.</p>')

with open('/var/www/lansharks.com/pageEnd.htm', 'r') as end:
    content = end.readlines()

for i in content:
    print(i.rstrip('\n'))
cursor.close()
db.close()


