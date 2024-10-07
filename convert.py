import pandas as pd
import json

# Load the JSON data
with open('violations_data.json') as file:
    data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(data)

# Save to CSV file
df.to_csv('violations_data.csv', index=False)
