import requests
from bs4 import BeautifulSoup

url = "https://raw.githubusercontent.com/majidrezarahnavard/way_of_freedom/refs/heads/main/docs/index.md"

response = requests.get(url)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    for img in soup.find_all("img"):
        if "src" in img.attrs:
            old_src = img["src"]
            new_src = "https://raw.githubusercontent.com/majidrezarahnavard/way_of_freedom_media/refs/heads/main/source/" + old_src.split("/")[-1]
            img["src"] = new_src
    
    with open("output.html", "w", encoding="utf-8") as file:
        file.write(str(soup))
    print("فایل output.html با موفقیت ذخیره شد.")
else:
    print("خطا در دریافت صفحه. کد وضعیت:", response.status_code)
