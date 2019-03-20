from selenium import webdriver
import lxml.html
import time
import os
import requests
import csv

location = input("Please enter the location: ")
location = "Nottinghamshire"
driver = webdriver.Chrome(os.getcwd()+"/chromedriver")
driver.maximize_window()
driver.implicitly_wait(60)
PAGES_COUNTS = 1500 # Max pages

url = "https://www.sdlauctions.co.uk/"



driver.get(url)
driver.execute_script("window.scrollTo(0,-1000)")
driver.find_element_by_name("location").send_keys(location)
driver.find_element_by_id('searchProperty').click()
driver.execute_script('window.scrollTo(0,10000000000)')
all_selector = "body > section > div:nth-child(2) > div.search-header > div.column.medium-6.medium-text-right.search-filter-options > div > ul:nth-child(1) > li:nth-child(6) > a"
print("Waiting to load all the data at once")
time.sleep(5)
driver.execute_script("document.querySelector('"+all_selector+"').click()")

# You can change it if you want it depends of the internet speed
print ("Waiting to load all the data")
time.sleep(10)


def get_locations_postal_codes(addresses):
    locations = []
    postals = []
    for address in addresses:
        temp_location = address.split(' ')[:len(address.split(' '))-2]
        temp_postal = address.split(' ')[len(address.split(' '))-2:]
        temp_location = " ".join(temp_location)
        temp_postal = " ".join(temp_postal)
        locations.append(temp_location)
        postals.append(temp_postal)
    return locations,postals

with open("sdlauctions " + location + ".csv","w",newline="") as outputfile:
    csv_file = csv.writer(outputfile)
    csv_file.writerow(["Price","Location","Postal Code"])
    html = driver.page_source
    tree = lxml.html.fromstring(html)
    property_desc = tree.cssselect('div.property-tile div.property-desc')
    addresses = [p.cssselect("p")[len(p.cssselect('p'))-1].text_content() for p in property_desc]
    prices = [price.text_content() for price in tree.cssselect('div.property-tile div.property-price span')]
    locations,postals = get_locations_postal_codes(addresses)
    for price,loc,pos in zip(prices,locations,postals):
            csv_file.writerow([price,loc,pos])

print ("Process completed")
outputfile.close()
print ("Quiting Browser")
driver.quit()
