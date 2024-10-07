import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def start_driver(url):
    driver = webdriver.Chrome()  # Adjust the driver path accordingly
    driver.get(url)
    return driver

def extract_member_data(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    members_data = []

    # Find all member cards
    member_cards = soup.find_all('a', class_='card card-member')
    
    for card in member_cards:
        member_info = {}

        # Extract image URL
        image_style = card.find('div', class_='image')['style']
        image_url = image_style.split('url(')[1].split(')')[0].strip()  # Extract the URL from style
        member_info['Image'] = image_url

        # Extract primary information (Name)
        primary_info = card.find('div', class_='primary-info').text.strip()
        member_info['Primary Info'] = primary_info

        # Extract secondary information (Party)
        secondary_info = card.find('div', class_='secondary-info').text.strip()
        member_info['Secondary Info'] = secondary_info

        # Extract indicator label (Constituency)
        indicator_label = card.find('div', class_='indicator indicator-label').text.strip()
        member_info['Indicator Label'] = indicator_label

        members_data.append(member_info)

    return members_data

def go_to_next_page(driver):
    """Navigate to the next page using pagination."""
    try:
        # Wait for the next button to be present in the DOM
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'next'))
        )
        
        next_button = driver.find_element(By.CLASS_NAME, 'next')
        
        # Check if the next button is disabled
        if 'disabled' in next_button.get_attribute('class'):
            return False  # No more pages
        
        next_button.click()
        time.sleep(2)  # Allow time for the page to load
        return True

    except Exception as e:
        print(f"Error navigating to next page: {e}")
        # Print the current page's HTML for debugging
        print(driver.page_source)
        return False

def navigate_and_extract_data(driver):
    all_members_data = []
    
    while True:
        print("Extracting data from current page...")
        member_data = extract_member_data(driver)
        all_members_data.extend(member_data)

        # Navigate to the next page
        if not go_to_next_page(driver):
            break

    return all_members_data

def save_to_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Main process
url = 'https://members.parliament.uk/members/commons'
driver = start_driver(url)
members_data = navigate_and_extract_data(driver)
save_to_json(members_data, 'members_data.json')
driver.quit()
