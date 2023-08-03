import requests
from bs4 import BeautifulSoup
import time
import json
import os
import openpyxl
workbook = openpyxl.Workbook()
sheet = workbook.active
def getData(url):
    response = requests.get(url, headers=headers)
    # with open("./hotels/response.html", "r", encoding="utf-8") as file:
    #     html_content = file.read()
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    div_elements = soup.find_all("div", {"data-automation": "hotel-card-title"})
    return div_elements
def addData(new_data):
    if os.path.exists('output1.json'):
        with open('output1.json', 'r') as file:
            existing_data = file.read()
            if existing_data:
                try:
                    parsed_data = json.loads(existing_data)
                except json.JSONDecodeError:
                    parsed_data = []
            else:
                parsed_data = []
            parsed_data.extend(new_data)
        with open('output1.json', 'w') as file:
            json.dump(parsed_data, file)
    else:
        with open('output1.json', 'w') as file:
            json.dump(new_data, file)
    # with open('output1.json',"r") as file:
    #     existing_data = json.load(file)
    # parsed_data = json.loads(existing_data)
    # parsed_data.append(new_data)

data = []
new_data=[] 
for i in range(573):
    print(i+1)
    headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"
    }
    if i == 0:
        url = "https://www.tripadvisor.com/Attractions-g293915-Activities-a_allAttractions.true-Thailand.html"
    #     response = requests.get(url,headers=headers)
    else:
        url = "https://www.tripadvisor.com/Attractions-g293915-Activities-oa"+str(i*30)+"-Thailand.html"
    session = requests.Session()
    response = requests.get(url,headers=headers)  
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    div_elements = soup.find_all("header", {"class": "VLKGO"})
    if div_elements:
        for div_element in div_elements:
            link_elements = div_element.find_all("a")
            target = link_elements[0].get("href")
            Name = link_elements[0].get_text(strip=True)
            parts = Name.split(".", 1)
            No = parts[0]
            name = parts[1]
            new_data.append({"target": target, "name": name})
            sheet.append([No, target, name])
    else:
        print("No div elements found.")
with open("activitiesNameAndUrl.json", "w") as file:
    json.dump(new_data, file)
workbook.save('activitiesNameAndUrl.xlsx')


