import requests
from bs4 import BeautifulSoup
import time
import json
import os
import re
import openpyxl
headers = {
       "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }
baseUrl = "https://www.tripadvisor.com"
with open('output.json') as file:
    json_data = json.load(file)
workbook = openpyxl.Workbook()
sheet = workbook.active
Data=[]
num=0
for item in json_data:
    Name=item['name']
    url=baseUrl+item['target']
    session = requests.Session()
    response = requests.get(url,headers=headers)  
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    # Address
    Address=''
    address_elements = soup.find("span", {"class": "oAPmj"})
    if address_elements:
        Address=address_elements.get_text(strip=True)
    # Rating/Score of Reviews
    RatingOfReviews=''
    rating_score_of_reviews_elements = soup.find("span", {"class": "uwJeR"})
    if rating_score_of_reviews_elements:
        RatingOfReviews=rating_score_of_reviews_elements.get_text(strip=True)
    # Hotel Class/Star Rating
    hotelClass_starRating_element = soup.find("span", {"class": "S2"})
    if hotelClass_starRating_element:
        if hotelClass_starRating_element.svg:
            hotelClassStarRatings=hotelClass_starRating_element.svg['aria-label']
            if hotelClassStarRatings:
                hotelClassStarRating=hotelClassStarRatings.split('of ',1)[0]
    # Price Range Location ...
    location_elements = soup.find("div", {"class": "GFCJJ"})
    location_element_keys = location_elements.find_all("div", {"class": "mpDVe"})
    location_element_values = location_elements.find_all("div", {"class": "IhqAp"})
    # Price Range
    PriceRange=''
    AlsoKnownAs=''
    FormerlyKnownAs=''
    Location=''
    NumberRooms=''
    for index,key in enumerate(location_element_keys):
        if key.get_text(strip=True)=="PRICE RANGE":
            if index < len(location_element_values):
                PriceRanges=location_element_values[index].get_text(strip=True)
                if PriceRanges:
                    PriceRanger=PriceRanges.split('-',1)
                    if PriceRanger:
                        PriceRange = str("".join(filter(str.isdigit, PriceRanger[0])))+'-'+str("".join(filter(str.isdigit, PriceRanger[1])))
        elif key.get_text(strip=True)=="ALSO KNOWN AS":
            if index < len(location_element_values):
                AlsoKnownAs=location_element_values[index].get_text(strip=True)
        elif key.get_text(strip=True)=="FORMERLY KNOWN AS":
            if index < len(location_element_values):
                FormerlyKnownAs=location_element_values[index].get_text(strip=True)
        elif key.get_text(strip=True)=="LOCATION":
            if index < len(location_element_values):
                Location=location_element_values[index].get_text(strip=True)
        elif key.get_text(strip=True)=="NUMBER OF ROOMS":
            if index < len(location_element_values):
                NumberRooms=location_element_values[index].get_text(strip=True)
    # Phone Number 
    PhoneNumber=''
    phone_number_elements = soup.find("div", {"class": "UJWmn" })
    if phone_number_elements:
        phone_number_element = phone_number_elements.find("div", {"data-blcontact": "PHONE "})
        if phone_number_element:
            PhoneNumber=phone_number_element.get_text(strip=True) 
    # Languages Spoken
    HotelStyle=''
    LanguageSpoken=''
    languages_spoken_elements = soup.find("div", {"class": "ui_columns is-mobile" })
    if languages_spoken_elements:
        languages_spoken_element = languages_spoken_elements.find_all("div", {"class": "ui_column" }) 
        for index,item in enumerate(languages_spoken_element):
            key=item.find("div", {"class": "kttOG" })
            if key.get_text(strip=True)=='HOTEL STYLE' or key.get_text(strip=True)=='HOTEL CLASS': 
                HotelStyles=languages_spoken_element[index].find_all('div',{"class":'euDRl'})
                for j,style in enumerate(HotelStyles):
                    if j>0:
                        HotelStyle+=style.get_text(strip=True)
                        if len(HotelStyles)-1>j:
                            HotelStyle+=', '
            elif key.get_text(strip=True)=='Languages Spoken':
                LanguageSpoken=languages_spoken_element[index].find('div',{"class":'euDRl'}).get_text(strip=True)
    # ReviewNumber hkxYU
    ReviewNumber=''
    review_number_element = soup.find("span", {"class": "hkxYU" })
    if review_number_element:
        ReviewNumbers = review_number_element.get_text(strip=True)
        if ReviewNumbers:
            ReviewNumber=int("".join(filter(str.isdigit, ReviewNumbers)))
    parts = Name.split(".", 1)
    No = parts[0]
    HotelName = parts[1]
    num+=1
    print(num)
    Data.append({
        "No":No,
        "HotelName":HotelName,
        "Address":Address,
        "RatingOfReviews":RatingOfReviews,
        "ReviewNumber":ReviewNumber,
        "hotelClassStarRating":hotelClassStarRating,
        "PriceRange":PriceRange,
        "Location":Location,
        "PhoneNumber":PhoneNumber,
        "NumberRooms":NumberRooms,
        "LanguageSpoken":LanguageSpoken,
        "HotelStyle":HotelStyle,
        "AlsoKnownAs":AlsoKnownAs,
        "FormerlyKnownAs":FormerlyKnownAs,
        "url":url
        })
    sheet.append([No,HotelName,Address,RatingOfReviews,ReviewNumber,hotelClassStarRating,PriceRange,Location,PhoneNumber,NumberRooms,LanguageSpoken,HotelStyle,AlsoKnownAs,FormerlyKnownAs,url])
out_json_path='./hotelAllInfos.json'
out_exel_path='hotelAllInfos.xlsx'
with open(out_json_path, "w") as f:
    json.dump(Data, f)
workbook.save(out_exel_path)
