#!/usr/bin/env python3
import cgi
import mysql.connector
import json
from helper import read_variable



def get_customer_details_from_db(db_connector, customer_number):
    cursor = db_connector.cursor()
    select_query = "SELECT * FROM customers WHERE customerNumber = %s"
    cursor.execute(select_query, (customer_number,))
    customer_data = cursor.fetchone()
    cursor.close()
    return customer_data


def update_customer_details_in_db(form,dbConnector,customerNumber):
        cursor = dbConnector.cursor()
        print("Updating customer details")
        companyName = form.getvalue('CompanyName')
        address = form.getvalue('Street')
        city = form.getvalue('City')
        email = form.getvalue('Email')
        zipCode = form.getvalue('ZIP')
        state = form.getvalue('State')
        phone = form.getvalue('Phone')
      # Define update query
        update_query = """
            UPDATE customers
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
        print('<h2 class="heading">Contact information updated successfully</h2>')

        # Commit changes and close connection
        dbConnector.commit()
        cursor.close()
        dbConnector.close()

def generate_update_sform(customer_data):
        
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

def generate_update_form(customer_data):
    # Escape customer data for HTML
    escaped_company_name = cgi.escape(customer_data['companyName'])
    escaped_address = cgi.escape(customer_data['address'])
    escaped_city = cgi.escape(customer_data['city'])
    escaped_email = cgi.escape(customer_data['email'])
    escaped_zip_code = cgi.escape(customer_data['zipCode'])
    escaped_state = cgi.escape(customer_data['state'])
    escaped_phone = cgi.escape(customer_data['phone'])

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
        escaped_company_name,
        escaped_address,
        escaped_city,
        escaped_email,
        escaped_zip_code,
        escaped_state,
        escaped_phone
    )
    return html_form




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
    variable_file = 'shared_variables.txt'
    key,customer_number=read_variable(variable_file)
    print(customer_number)
    customer_data=get_customer_details_from_db(db,customer_number)
    form_update_html=generate_update_form(customer_data)
    
    print(form_update_html)


    if form.getvalue('update_concat'):
        print('form action has been done')

        update_customer_details_in_db(form, db, customer_number)
        customer_data = get_customer_details_from_db(db, customer_number)
        print(customer_data)
    else:
        print('form action has not been done')

    # Retrieve customer details from the database
        
    with open('/var/www/lansharks.com/pageEnd.htm', 'r') as end:
        content = end.readlines()

    for i in content:
        print(i.rstrip('\n'))
