import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def start_driver(url):
    driver = webdriver.Chrome()  # Adjust the path to your chromedriver if necessary
    driver.get(url)
    return driver

def extract_table_content(driver):
    """Extracts data from the visible table."""
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    table = soup.find('table', id='tablepress-12')
    rows = table.find('tbody').find_all('tr')

    data = []
    for row in rows:
        columns = row.find_all('td')
        entry = {
            'Contractor': columns[0].get_text(strip=True),
            'Location': columns[1].get_text(strip=True),
            'Hearing Date': columns[2].get_text(strip=True),
            'Job Number': columns[3].get_text(strip=True),
            'Allegation': columns[4].get_text(strip=True),
            'Action Taken': columns[5].get_text(strip=True)
        }
        data.append(entry)
    return data

def go_to_next_page(driver):
    """Navigate to the next page using pagination."""
    try:
        next_button = driver.find_element(By.ID, 'tablepress-12_next')
        if 'disabled' in next_button.get_attribute('class'):
            return False  # No more pages
        next_button.click()
        time.sleep(2)  # Allow time for the page to load
        return True
    except Exception as e:
        print(f"Error navigating to next page: {e}")
        return False

def save_to_json(data, file_name):
    """Saves the scraped data to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Main process
url = 'https://lslbc.louisiana.gov/violations/'
driver = start_driver(url)

all_data = []

while True:
    # Extract table data from the current page
    page_data = extract_table_content(driver)
    all_data.extend(page_data)

    # Try to go to the next page
    if not go_to_next_page(driver):
        break  # If there's no next page, stop the loop

# Save the extracted data to a JSON file
save_to_json(all_data, 'violations_data.json')

driver.quit()
