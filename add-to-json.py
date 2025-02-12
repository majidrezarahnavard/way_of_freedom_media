import json

# Load existing data
try:
    with open("all.json", "r", encoding="utf-8") as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    data = []

# Get user input
title = input("Enter title: ").strip()
description = input("Enter description: ").strip()
file_name = input("Enter file name /source/: ").strip()

# Create new entry
new_entry = {
    "title": title,
    "description": description,
    "file": file_name
}

# Add entry to JSON data
data.append(new_entry)

# Save updated JSON file
with open("all.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("✅ The file has been successfully updated!")
