import time
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_driver(url):
    driver = webdriver.Chrome()  # Adjust driver path if necessary
    driver.get(url)
    return driver

def extract_dynamic_content(driver, wait_time=10):
    try:
        # Example for handling dynamic elements like clicks or tabs (if required)
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'table.table-bordered')))
        
        time.sleep(2)  # Adjust this wait time based on how long the content takes to load
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        return soup
    except Exception as e:
        print(f"Error in extracting content: {e}")
        return None

def parse_data(soup):
    members = []
    
    # Find the table with the relevant data
    table = soup.find('table', class_='table table-bordered table-condensed')
    if not table:
        print("No table found")
        return []

    # Loop through each row (skip the header row)
    rows = table.find_all('tr')[1:]
    for row in rows:
        data = {}

        columns = row.find_all('td')
        if len(columns) < 7:  # If not enough columns, skip the row
            continue

        # Extract name
        name_tag = columns[1].find('a')
        data['Name'] = name_tag.get_text(strip=True) if name_tag else 'N/A'
        
        # Extract contact information
        contact_info = columns[4].get_text(strip=True)
        data['Contact Information'] = contact_info if contact_info else 'N/A'
        
        # Extract image URL
        image_tag = columns[6].find('img')
        data['Image URL'] = image_tag['src'] if image_tag else 'N/A'
        
        # Extract occupation (Constituency)
        occupation = columns[2].get_text(strip=True)
        data['Occupation'] = occupation if occupation else 'N/A'
        
        # Extract political party affiliation
        party_tag = columns[3].find('a')
        data['Political Party'] = party_tag.get_text(strip=True) if party_tag else 'N/A'

        # Extract party image URL
        party_image_tag = columns[3].find('img')
        data['Party Image URL'] = party_image_tag['src'] if party_image_tag else 'N/A'

        # Add extracted data to list
        members.append(data)

    return members

def save_to_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Main process
url = 'https://www.pap.gov.pk/members/contactdetails/en/21?bycontact=true'
driver = start_driver(url)
soup = extract_dynamic_content(driver)
if soup:
    extracted_data = parse_data(soup)
    if extracted_data:
        save_to_json(extracted_data, 'output.json')
    else:
        print("No data extracted")
driver.quit()
