from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from bs4 import BeautifulSoup
from time import time
import random
from kafka import KafkaProducer
import json, time

#Open chrome browser and vist target web topcv.vn
driver = webdriver.Chrome("C:\chromedriver.exe")
url = "https://www.topcv.vn/"
driver.get(url)

# Search for the items we want to buy
# Locate the search bar element
search_field = driver.find_element_by_xpath('//*[@id="keyword"]')

# Input the search query to search bar
search_query = input("What items do you want to scrape? ")
# search_query = Nhân viên kinh doanh
search_field.send_keys(search_query)
sleep(5)

#Search
search_field.send_keys(Keys.RETURN)

def GetURL():    
    page_source = BeautifulSoup(driver.page_source)
    items = page_source.find_all('a', class_ = 'underline-box-job')
    all_item_URL = []
    for item in items:
        item_URL = item.get('href')
        if item_URL not in all_item_URL:
            all_item_URL.append(item_URL)
    return all_item_URL

input_page = int(input('How many pages you want to scrape: '))
URLs_all_page = []
for page in range(input_page):
    URLs_one_page = GetURL()
    sleep(3)
    driver.execute_script('window.scrollTo(0, 3200)') #document.body.scrollHeight
    sleep(2)
    #if next_button is dynamic element instead of next_button = driver.find_element_by_class_name()
    next_button = driver.find_element_by_xpath('//*[@id="main"]/div[1]/div[3]/div[2]/div[3]/div[1]/div[2]/nav/ul/li[13]/a')
    next_button.send_keys(Keys.RETURN)
    URLs_all_page = URLs_all_page + URLs_one_page
URLs_all_page=list(dict.fromkeys(URLs_all_page))
sleep(2)
print("--------SUCCESS-----------")

#Connect your_server kafka
producer = KafkaProducer(bootstrap_servers = ['your_host:9092'],  #change your host
	value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'))

#Take data and send to kafka server
id=0
for topcv_URL in URLs_all_page:
        try:
                driver.get(topcv_URL)
                id = id + 1
                page_source = BeautifulSoup(driver.page_source, "html.parser")
                #Name of company
                name_cp=page_source.find("a",href=True,class_="text-dark-blue").get_text()
                # Work Location:
                local= page_source.select('div.box-address div')
                local= local[0].get_text().replace("\n","")
                # Salary
                salary = page_source.select("div.box-main div.box-item span")[0].get_text().replace("\n","")
                # Experience
                exp =page_source.select("div.box-main div.box-item span")[5].get_text().replace("\n","")
                temp = {
                        "id": id,
                        'URL': topcv_URL,
                        'Name_company': name_cp,
                        'Work_location': local,
                        'Salary': salary,
                        'Experience': exp,
                }
                #Send mesage to server kafka
                producer.send(topic='topcv', value = temp)
                producer.flush()
                print(temp)
        except:
                pass