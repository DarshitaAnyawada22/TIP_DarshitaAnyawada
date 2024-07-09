import mysql.connector
import requests
from bs4 import BeautifulSoup

dbname = "extract"
user = "root"
password = "darshita"
host = "localhost"
port = 3306  # Default MySQL port
table_name = "table1"

def connect_to_database(dbname, user, password, host, port):
    # Establish a connection
    conn = mysql.connector.connect(
        database=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

def push_data(data, conn, table_name):
    insert_query = f"""
        INSERT INTO {table_name}
        (Internship_Title, Company_Name, Location, Start_Date, Duration, Stipend)
        VALUES
        (%(Internship_Title)s, %(Company_Name)s, %(Location)s, %(Start_Date)s, %(Duration)s, %(Stipend)s)
    """

    # Create a cursor and execute the insert query
    cursor = conn.cursor()
    cursor.execute(insert_query, data)

    # Commit the changes to the database
    conn.commit()
    cursor.close()

conn = connect_to_database(dbname, user, password, host, port)

def process(num):
    reqUrl = "https://internshala.com/internships/page-{}/".format(num)

    headersList = {
        "Accept": "*/*",
        "User-Agent": "Thunder Client (https://www.thunderclient.com)"
    }

    payload = ""

    response = requests.get(reqUrl, headers=headersList)

    soup = BeautifulSoup(response.content, 'html.parser')

    nested_divs = soup.find_all('div', class_='container-fluid individual_internship visibilityTrackerItem')

    for target_div in nested_divs:
        try:
            internship_title = target_div.select_one('.individual_internship_header .heading_4_5 a').text.strip()
        except:
            internship_title = "None"

        try:
            company_name = target_div.select_one('.company_name a').text.strip()
        except:
            company_name = "None"

        try:
            location = target_div.select_one('#location_names span a').text.strip()
        except:
            location = "None"

        try:
            duration = target_div.select_one('.other_detail_item_row .other_detail_item:nth-child(2) .item_body').text.strip()
        except:
            duration = "None"

        try:
            stipend = target_div.select_one('.stipend_container .item_body').text.strip()
        except:
            stipend = "None"

        start_date_element = target_div.select_one('#start-date-first .start_immediately_desktop')
        start_date = start_date_element.text.strip() if start_date_element else 'Not specified'

        data_dict = {
            'Internship_Title': internship_title,
            'Company_Name': company_name,
            'Location': location,
            'Start_Date': start_date,
            'Duration': duration,
            'Stipend': stipend,
        }

        push_data(data_dict, conn, table_name)

# Example usage
process(1)  # This will process the first page and insert data into the database
