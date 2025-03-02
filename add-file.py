import json
import os
import requests

json_file = "all.json"
source_dir = "source"

os.makedirs(source_dir, exist_ok=True)

try:
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

title = input("Enter title: ").strip()
description = input("Enter description: ").strip()

file_choice = input("Do you want to enter a file name (1) or download from URL (2)? [1/2]: ").strip()

if file_choice == "1":
    file_name = input("Enter file name in /source/: ").strip()
    print(f"use link: https://raw.githubusercontent.com/majidrezarahnavard/way_of_freedom_media/refs/heads/main/{source_dir+"/"+file_name}")
elif file_choice == "2":
    file_url = input("Enter the file URL: ").strip()
    
    file_name = file_url.split("/")[-1]
    file_path = os.path.join(source_dir, file_name)
    
    try:
        print("Downloading file...")
        response = requests.get(file_url, stream=True)
        response.raise_for_status()

        with open(file_path, "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        
        print(f"✅ File downloaded and saved as {file_path}")
        print(f"use link: https://raw.githubusercontent.com/majidrezarahnavard/way_of_freedom_media/refs/heads/main/{file_path}")
    except requests.RequestException as e:
        print(f"❌ Failed to download the file: {e}")
        exit(1)
else:
    print("❌ Invalid choice. Exiting.")
    exit(1)

new_entry = {
    "title": title,
    "description": description,
    "file": file_name
}

data.append(new_entry)

with open(json_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ The file has been successfully updated!")
print("✅ Please push!")
