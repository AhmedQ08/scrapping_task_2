import requests
import json
import pandas as pd

# API Endpoint and Key
api_url = "https://apigwext.worldbank.org/dvsvc/v1.0/json/APPLICATION/ADOBE_EXPRNCE_MGR/FIRM/SANCTIONED_FIRM"
api_key = "z9duUaFUiEUYSHs97CU38fcZO7ipOPvm"

# Headers
headers = {
    "apikey": api_key
}

def fetch_data_from_api():
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def extract_firm_data(json_data):
    firms = []
    if json_data and "response" in json_data:
        for firm in json_data["response"]["ZPROCSUPP"]:
            firm_data = {
                "Firm Name": firm.get("SUPP_NAME", "N/A") + (firm.get("ADD_SUPP_INFO", "") or ""),
                "Address": format_address(firm),
                "Country": firm.get("COUNTRY_NAME", "N/A"),
                "Ineligibility Period (From)": firm.get("DEBAR_FROM_DATE", "N/A"),
                "Ineligibility Period (To)": firm.get("DEBAR_TO_DATE", "Ongoing" if firm.get("INELIGIBLY_STATUS") == "Permanent" else firm.get("DEBAR_TO_DATE", "N/A")),
                "Grounds": firm.get("DEBAR_REASON", "N/A")
            }
            firms.append(firm_data)
    return firms

def format_address(firm):
    address = firm.get("SUPP_ADDR", "")
    city = firm.get("SUPP_CITY", "")
    state = firm.get("SUPP_STATE_CODE", "")
    zip_code = firm.get("SUPP_ZIP_CODE", "")
    full_address = ', '.join(filter(None, [address, city, state, zip_code]))
    return full_address or "N/A"

def save_to_json(data, file_name):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=4)

def save_to_csv(data, file_name):
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False)

# Main script
if __name__ == "__main__":
    json_data = fetch_data_from_api()
    if json_data:
        firms_data = extract_firm_data(json_data)
        save_to_json(firms_data, 'debarred_firms.json')
        save_to_csv(firms_data, 'debarred_firms.csv')
        print("Data saved successfully!")
    else:
        print("Failed to fetch or process data.")
