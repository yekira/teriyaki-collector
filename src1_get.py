import json
import os
import requests

# Make the API request and get the JSON response
response = requests.get("https://tjadataba.se/api/browse")
json_data = json.loads(response.text)

# Create the zips directory if it doesn't exist
if not os.path.exists("zips"):
    os.makedirs("zips")

# Iterate over the JSON array and download each file
for i, item in enumerate(json_data):
    id = item["_id"]
    url = f"https://tjadataba.se/download/orig/{id}"
    filename = f"zips/{id}.zip"
    response = requests.get(url)

    with open(filename, "wb") as f:
        f.write(response.content)

    print(f"Downloaded {filename} ({1+i} of {len(json_data)})")
