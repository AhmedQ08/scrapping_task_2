import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def start_driver(url):
    driver = webdriver.Chrome()  # Adjust driver path accordingly
    driver.get(url)
    return driver

def extract_dynamic_content(driver, wait_time=10):
    # Wait for the content to load
    WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'col-md-4'))
    )
    time.sleep(2)  # Adjust based on page load time
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return soup

def parse_data(soup):
    data = {}
    groups = soup.find_all('div', class_='col-md-4 col-xs-4')

    for group in groups:
        group_name = group.find('h3').text.strip()
        members = group.find_all('div', class_='rowdata row')

        member_names = []
        for member in members:
            member_name = member.find('a').text.strip()
            member_names.append(member_name)

        data[group_name] = member_names

    return data

def save_to_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Main process
url = 'https://www.parlament.mt/en/14th-leg/political-groups/'
driver = start_driver(url)
soup = extract_dynamic_content(driver)
if soup:
    extracted_data = parse_data(soup)
    save_to_json(extracted_data, 'political_groups.json')
driver.quit()
