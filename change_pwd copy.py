#!/usr/bin/env python3
from config import SQL_TABLE_NAME_INCIDENT, CSV_FILE_PATH_poision
from helper import get_details_from_form, read_variable, transform_username, update_passwd_in_db
import mysql.connector
import cgi
import html
  # for HTML escaping

def change_password(form, db):
    new_password = form.getvalue('NewPassword')
    confirm_password = form.getvalue('ConfirmPassword')
    variable_file = 'shared_variables.txt'
    key,current_user=read_variable(variable_file)
    print(current_user)
    try:
        if new_password and new_password == confirm_password:
            # Assuming update_passwd_in_db is a function that updates the password in the database
            update_passwd_in_db(db, current_user, new_password)
            print('<h2 class="heading">Password changed successfully</h2>')
            print('<p class="description">Click <a href="http://www.lansharks.com/login.htm" style="color: #FFD700;">here</a> to retry login.</p>')

        else:
            error_message = 'Either your username is invalid or New password and confirm password do not match.'
            print('<h2 class="heading">Either your username is invalid or New password and confirm password do not match</h2>')
            print('<a href="http://www.lansharks.com/change_password.htm" style="color: #FFD700;">Change Password?</a>')

    except Exception as e:
        # Handle exceptions (e.g., database errors) and log them
        error_message = f'An error occurred: {str(e)}'
        print('Content-type: text/html')  # Add this line to print the content-type header
        print()  # Print an empty line to separate headers from content
        print(f'<p class="description" style="color: red;">{html.escape(error_message)}</p>')

if __name__ == "__main__":
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

    form = cgi.FieldStorage()
    db = mysql.connector.connect(
        host='localhost',
        user='root',
        password='P@ssw0rd',
        database='python'
    )

    # Call the change_password function
    change_password(form, db)

    # Close the database connection
    db.close()

    # upload_incidents_to_csv_file(db, CSV_FILE_PATH_poision, SQL_TABLE_NAME_INCIDENT)

    with open('/var/www/lansharks.com/pageEnd.htm', 'r') as end:
        content = end.readlines()

    for i in content:
        print(i.rstrip('\n'))
