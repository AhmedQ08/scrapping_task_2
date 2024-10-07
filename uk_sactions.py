import json
from bs4 import BeautifulSoup

def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    data = []

    # Find all sections separated by Unique IDs
    unique_id_sections = soup.find_all('div', text=lambda text: 'Unique ID:' in text)
    
    for section in unique_id_sections:
        # Initialize a dictionary for each Unique ID
        unique_id_data = {
            'Unique ID': None,
            'Regime Name': None,
            'Sanctions Imposed': None,
            'Other Information': None,
            'Names': [],
            'Name non-latin script': None,
            'Addresses': [],
            'Phone Numbers': None,
            'Email Addresses': None,
            'Designation Source': None,
            'Date Designated': None,
            'Last Updated': None,
            'OFSI Group ID': None,
            'UN Reference Number': None
        }

        # Extract Unique ID
        unique_id_data['Unique ID'] = section.find_next('span').text.strip()

        # Extract other details based on labels
        current = section
        while True:
            current = current.find_next()
            if current.name == 'b':
                label = current.get_text(strip=True)
                next_span = current.find_next('span')
                
                if label == 'Regime Name:':
                    unique_id_data['Regime Name'] = next_span.get_text(strip=True)
                elif label == 'Sanctions Imposed:':
                    unique_id_data['Sanctions Imposed'] = next_span.get_text(strip=True)
                elif label == 'Other Information:':
                    unique_id_data['Other Information'] = next_span.get_text(strip=True)
                elif label == 'Name:':
                    name = next_span.get_text(strip=True)
                    name_type = next_span.find_next('span').get_text(strip=True) if next_span.find_next('span') else ''
                    unique_id_data['Names'].append({'Name': name, 'Name Type': name_type})
                elif label == 'Name non-latin script:':
                    unique_id_data['Name non-latin script'] = next_span.get_text(strip=True)
                elif label == 'Address:':
                    address = ""
                    while next_span and next_span.get_text(strip=True) != 'Address Country:':
                        address += f"{next_span.get_text(strip=True)}, "
                        next_span = next_span.find_next('span')
                    address_country = next_span.get_text(strip=True)
                    unique_id_data['Addresses'].append({'Address': address.strip(', '), 'Address Country': address_country})
                elif label == 'Phone Numbers:':
                    unique_id_data['Phone Numbers'] = next_span.get_text(strip=True)
                elif label == 'Email Addresses:':
                    unique_id_data['Email Addresses'] = next_span.get_text(strip=True)
                elif label == 'Designation Source:':
                    unique_id_data['Designation Source'] = next_span.get_text(strip=True)
                elif label == 'Date Designated:':
                    unique_id_data['Date Designated'] = next_span.get_text(strip=True)
                elif label == 'Last Updated:':
                    unique_id_data['Last Updated'] = next_span.get_text(strip=True)
                elif label == 'OFSI Group ID:':
                    unique_id_data['OFSI Group ID'] = next_span.get_text(strip=True)
                elif label == 'UN Reference Number:':
                    unique_id_data['UN Reference Number'] = next_span.get_text(strip=True)

            # Stop when hitting the next 'Unique ID' or end of the section
            if current.name == 'hr':
                break

        # Append this unique ID's data to the list
        data.append(unique_id_data)

    return data

def save_to_json(data, file_name):
    """Saves the extracted data to a JSON file."""
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

# Load the HTML content
with open('UK-Sanctions-List.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML and save to JSON
parsed_data = parse_html(html_content)
save_to_json(parsed_data, 'sanctions_data.json')

print("Data extracted and saved to sanctions_data.json")
