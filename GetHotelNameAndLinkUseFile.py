from bs4 import BeautifulSoup
import json
import os
import openpyxl
# Stroe to json
html_dir = "./hotel/"
json_path = "./output.json"
data = []
workbook = openpyxl.Workbook()
sheet = workbook.active
for filename in os.listdir(html_dir):
    if filename.endswith(".html"):
        # Open the file and parse the HTML using BeautifulSoup
        with open(os.path.join(html_dir, filename), encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
        div_elements = soup.find_all("div", {"data-automation": "hotel-card-title"})
        
        for div_element in div_elements:
            link_elements = div_element.find_all("a")
            for link_element in link_elements:
                target = link_element.get("href")
                name = link_element.get_text(strip=True)
                # data.append({"target": target, "name": name})
                sheet.append([filename, target, name])
print('sheet')
# with open(json_path, "w") as f:
#     json.dump(data, f)
# Stroe to exel
workbook.save("output1.xlsx")