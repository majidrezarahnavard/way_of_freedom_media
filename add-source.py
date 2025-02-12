import os
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

# URL of the target website
url = input("Enter the website URL: ")

# Create source folder if not exists
if not os.path.exists("source"):
    os.makedirs("source")

# Fetch and parse the webpage
response = requests.get(url)
if response.status_code != 200:
    print("Failed to fetch the webpage.")
    exit()

soup = BeautifulSoup(response.text, "html.parser")

# Load existing data
try:
    with open("all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

# Function to check if file already exists
def file_exists(file_name):
    return os.path.exists(os.path.join("source", file_name))

# Function to download and save files
def download_file(file_url, file_name):
    file_path = os.path.join("source", file_name)

    if file_exists(file_name):
        print(f"⏩ Skipping {file_name} (already downloaded)")
        return file_name, True

    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(file_path, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"✔️ Downloaded: {file_name}")
        return file_name, True
    except requests.RequestException as e:
        print(f"❌ Failed to download {file_url}: {e}")
        return file_name, False

# Extract media files
downloaded_files = []
failed_files = []

for tag in soup.find_all(["img"]):
    src = tag.get("src")
    alt = tag.get("alt", "No description")

    if src:
        file_url = urljoin(url, src)
        file_name = os.path.basename(urlparse(file_url).path)

        saved_file, success = download_file(file_url, file_name)
        if success and not any(entry["file"] == saved_file for entry in data):
            downloaded_files.append(saved_file)
            data.append({
                "title": file_name,
                "description": alt,
                "file": saved_file
            })
        elif not success:
            failed_files.append(saved_file)

# Save updated JSON
with open("all.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# Print summary
print("\n📌 Download Summary:")
print(f"✔️ Downloaded files: {len(downloaded_files)}")
print(f"⏩ Skipped files: {sum(file_exists(f) for f in downloaded_files)}")
if failed_files:
    print(f"❌ Failed files ({len(failed_files)}): {', '.join(failed_files)}")
else:
    print("✅ All files downloaded successfully!")
