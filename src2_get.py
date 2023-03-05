import os
import requests
from bs4 import BeautifulSoup

# Create an empty array to hold the unique href values
hrefs = []

# Define the URLs to scrape
urls = ['https://taikosanjiro-humenroom.net/original/?sort=rdm',
        'https://taikosanjiro-humenroom.net/created/?sort=rdm']

class_names = [
    "original-list-contents-main-a",
    "created-list-a"
]

GOAL = 423+262

while len(set(hrefs)) < GOAL:
    for i, url in enumerate(urls):
        print(f"Scraping {url}...")
        # Send a request to the website
        response = requests.get(url)

        # Parse the HTML content of the website
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all the <a> tags with class "original-list-contents-main-a"
        a_tags = soup.find_all('a', class_=class_names[i])

        # Loop through each <a> tag and extract the href value
        for a_tag in a_tags:
            href = a_tag.get('href')
            # Add the href value to the array if it's not already in the array
            if href not in hrefs:
                hrefs.append(href)

    # Deduplicate the hrefs array
    hrefs = list(set(hrefs))

    # Print the number of unique hrefs collected so far
    print(f"Total unique hrefs: {len(hrefs)}")

# Print the final number of unique hrefs collected
print(f"Total unique hrefs: {len(hrefs)}")

# Define base URL
base_url = 'https://taikosanjiro-humenroom.net'

# Define dictionaries to map URLs to checkbox class names and download parameters
checkbox_classes = {'/o': 'original-checkbox', '/c': 'created-checkbox'}
download_params = {'/o': 'or-dl', '/c': 'cr-dl'}

# Define list to hold download URLs
download_urls = []

# Loop through each URL and scrape for download URLs
for href in hrefs:
    # Construct full URL
    full_url = base_url + href
    
    # Get page content
    response = requests.get(full_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all input tags with matching class name and download parameter
    checkbox_class = checkbox_classes.get(href[:2], '')
    download_param = download_params.get(href[:2], '')
    checkboxes = soup.find_all('input', {'class': checkbox_class})
    
    # Loop through checkboxes and construct download URLs
    for checkbox in checkboxes:
        download_url = full_url + f'?{download_param}=true&{checkbox["name"]}={checkbox["value"]}'
        download_urls.append(download_url)
        print(download_url, "added")

print(f"Total download urls: {len(download_urls)}")

zip_urls = []

# Loop through URLs and extract download links
for url in download_urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    meta_tag = soup.find('meta', {'http-equiv': 'Refresh'})

    if meta_tag:
        # Extract URL from the meta tag
        refresh_content = meta_tag['content']
        zip_url = refresh_content.split('URL=')[1]
        print(zip_url)
        zip_urls.append(zip_url)
    else:
        raise ValueError('oh no! this url is cant be download.' + url)

print(f'Found {len(zip_urls)} zip URLs!')

# Create folder to store downloaded zip files
folder_name = 'zips'
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Download zip files and save them to the folder
for i, url in enumerate(zip_urls):
    response = requests.get(url)
    file_name = os.path.join(folder_name, f'humenroom-{i+1}.zip')
    with open(file_name, 'wb') as f:
        f.write(response.content)
    print(f'Downloaded {file_name}')

print('All zip files downloaded!')
