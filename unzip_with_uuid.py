import os
import zipfile
import uuid

# Define the paths to the directories
zips_dir = 'zips'
flat_dir = 'flat'

# Create the flat directory if it does not exist
if not os.path.exists(flat_dir):
    os.mkdir(flat_dir)

# Loop through all the files in the zips directory
for filename in os.listdir(zips_dir):
    # Check if the file is a zip file
    if filename.endswith('.zip'):
        # Extract the name of the zip file (without the extension)
        zip_name = str(uuid.uuid4())
        
        # Create a directory with the same name as the zip file (without the extension)
        flat_path = os.path.join(flat_dir, zip_name)
        if not os.path.exists(flat_path):
            os.mkdir(flat_path)
        
        # Extract the contents of the zip file to the directory
        zip_path = os.path.join(zips_dir, filename)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(flat_path)
