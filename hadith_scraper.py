import requests
from bs4 import BeautifulSoup
import json

url = 'https://sunnah.com/bukhari/52'
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')
hadiths = []

hadith_containers = soup.find_all('div', {'class': 'actualHadithContainer'})




for container in hadith_containers:
    # reference_text = container.find_all('tr')[2].find_all('td')[1].text
    # # print(reference_text)
    # hadith_number = reference_text.split(',')[2].split(' ')[2].strip()
    # # print(hadith_number)
    # hadith_english_container = container.find('div', {'class': 'englishcontainer'})
    # hadith_arabic_container = container.find('div', {'class': 'arabic_hadith_full'})
    english_td = container.find('td', text='English translation')
    next_td = english_td.find_next_sibling('td').text
    # print(next_td)
    # reference_text = container.find_all('tr')[0].find_all('td')[1].text
    # print(reference_text)
    hadith_number = next_td.split(',')[2].split(' ')[2].strip()
    # print(hadith_number)
    hadith_english_container = container.find('div', {'class': 'englishcontainer'})
    hadith_arabic_container = container.find('div', {'class': 'arabic_hadith_full'})
    
    narrated_by = hadith_english_container.find('div', {'class': 'hadith_narrated'})
    if narrated_by is not None:
        narrated_by = narrated_by.text.strip()
    else:
        narrated_by = "NARRATOR NOT FOUND"
    
    hadith_english = hadith_english_container.find('div', {'class': 'text_details'})
    if hadith_english is not None:
        hadith_english = hadith_english.text.strip()
    else:
        hadith_english = "ENGLISH TRANSALTION NOT FOUND"
    
    hadith_arabic = hadith_arabic_container
    if hadith_arabic is not None:
        hadith_arabic = hadith_arabic_container.text.strip()
    else:
        hadith_arabic = "ARABIC HADITH NOT FOUND"
    
    book_ref_number = container.find('a', {'name': True}).get('name')

    
    hadith_dict = {
        "hadith_number": hadith_number,
        "book_ref_number": book_ref_number,
        "narrated_by": narrated_by,
        "hadith_english": hadith_english,
        "hadith_arabic": hadith_arabic
    }
    
    hadiths.append(hadith_dict)


with open('witnesses.json', 'w') as f:
    json.dump(hadiths, f, ensure_ascii=False, indent=4)