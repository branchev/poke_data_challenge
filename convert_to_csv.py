import json
import csv

# Load JSON data
with open('pokemon_details.json', 'r') as json_file:
    data = json.load(json_file)

# Prepare CSV data
csv_data = [['id', 'name', 'height', 'weight', 'bmi']]  # Header row
for pokemon_id, details in data.items():
    csv_row = [pokemon_id, details['name'], details['height'], details['weight'], details['bmi']]
    csv_data.append(csv_row)

# Write to CSV
with open('pokemon_details.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)

print("CSV file created successfully.")