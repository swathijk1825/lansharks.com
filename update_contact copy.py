#!/usr/bin/env python3
from config import SQL_TABLE_NAME_INCIDENT, CSV_FILE_PATH_poision
from shared_variables import current_user
from helper import  get_details_from_form, transform_username, update_passwd_in_db, upload_data_from_csv, upload_incidents_to_csv_file
import mysql.connector
import cgi, cgitb
import html  # for HTML escaping


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
    host = 'localhost',
    user = 'root',
    password = 'P@ssw0rd',
    database = 'python'
)


# Call the change_password function
get_details_from_form(form, db)

# upload_incidents_to_csv_file(db, CSV_FILE_PATH_poision, SQL_TABLE_NAME_INCIDENT)

upload_data_from_csv()

with open('/var/www/lansharks.com/pageEnd.htm', 'r') as end:
    content = end.readlines()

for i in content:
    print(i.rstrip('\n'))


