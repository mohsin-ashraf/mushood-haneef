from selenium import webdriver
import lxml.html
import time
import os
import requests
import csv
from selenium.webdriver.support.ui import Select


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
select = Select(driver.find_element_by_id('radius'))
select.select_by_visible_text('40 miles')

driver.find_element_by_id('searchProperty').click()
driver.execute_script('window.scrollTo(0,10000000000)')
all_selector = "body > section > div:nth-child(2) > div.search-header > div.column.medium-6.medium-text-right.search-filter-options > div > ul:nth-child(1) > li:nth-child(6) > a"
print("Waiting to load all the data at once")
time.sleep(2)
driver.execute_script("document.querySelector('"+all_selector+"').click()")

time.sleep(5)
select = Select(driver.find_element_by_id('auction'))
select.select_by_visible_text('Online')


#############                   ZOOPLA FUNCTIONS ######################
def get_zoopla_url(location,postal):
    start = location.split(',')[0].strip().replace(' ','-').lower()
    if location.split(',')[len(location.split(','))-1].strip().replace(' ','-').lower() != '':
        end = location.split(',')[len(location.split(','))-1].strip().replace(' ','-').lower()
    else:
        end = location.split(',')[len(location.split(','))-2].strip().replace(' ','-').lower()
    postal = postal.replace(' ','-').lower()
    return 'https://www.zoopla.co.uk/property/'+start+'/'+end+'/'+postal

def get_zoopla_home_values(html):
    tree = lxml.html.fromstring(html)
    property_prices = tree.cssselect('span.browse-estimate-value span.browse-estimate-value')
    property_prices = [price.text_content().strip() for price in property_prices]
    return property_prices

def get_all_homes_url(html):
    tree = lxml.html.fromstring(html)
    links_to_homes = tree.cssselect('td.browse-cell-address > a')
    links_to_homes = ["https://www.zoopla.co.uk"+link.attrib['href'] for link in links_to_homes if "property" in link.attrib['href']]
    return links_to_homes

def get_range_and_confidence(html):
    tree = lxml.html.fromstring(html)
    try:
        es_range = tree.cssselect("#main-content > div.pdp-columns-wrap > div > div:nth-child(2) > section.pdp-estimate > div.pdp-estimate__types > div > div > p.pdp-estimate__range")[0].text_content().strip().split(":")[1].split('-')
    except:
        print ("No Estimation on Zoopla for ranges and confidence")
        return None
    try:
        confi = tree.cssselect("span.pdp-confidence-rating__copy b")[0].text_content().strip()
    except:
        print ("No Estimation on Zoopla for ranges and confidence")
        return None
    return es_range,confi


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
    csv_file.writerow(["Link To Home","End Auction Time","Price","Location","Postal Code","Perperty Value","Low Range","High Range","Confidence"])
    html = driver.page_source
    auction_end_time = []
    es_ranges = []
    confidences = []
    tree = lxml.html.fromstring(html)
    property_desc = tree.cssselect('div.property-tile div.property-desc')
    addresses = [p.cssselect("p")[len(p.cssselect('p'))-1].text_content() for p in property_desc]
    property_values = []
    prices = [price.text_content() for price in tree.cssselect('div.property-tile div.property-price span')]
    locations,postals = get_locations_postal_codes(addresses)
    location_counter = 1
    links_to_homes = tree.cssselect("div.property-tile.past-property")
    links_to_homes = [home.cssselect('div > a') for home in links_to_homes]
    links_to_homes = [link[0] for link in links_to_homes]
    print ("Total Homes Found: "+str(len(links_to_homes)))
    links_to_homes = [link.attrib['href'] for link in links_to_homes]
    sub_driver = webdriver.Chrome('chromedriver')
    for home_number,sub_link in enumerate(links_to_homes):
        print ("Home number "+str(home_number+1)+" out of "+str(len(links_to_homes)))
        try:
            sub_driver.get(sub_link)
            time.sleep(2)# This time sleep is for loading acution time Since it is rendered from the server its speed depends upon internet you can change this time to 1 or you can complelty remove it.
            sub_tree = lxml.html.fromstring(sub_driver.page_source)
        except:
            print ("Error: Page not found")
        try:
            end_time = sub_tree.xpath('//*[@id="bidding-panel"]/div[4]/div[1]/div[2]')[0].text_content().strip()
            #print (end_time)
            auction_end_time.append(end_time)
        except:
            print ("End time not available")
            auction_end_time.append("End Time not Available")
    sub_driver.quit()
    for location,postal in zip(locations,postals):
        link = get_zoopla_url(location,postal)
        zoopla_html = requests.get(link).text
        property_price = get_zoopla_home_values(zoopla_html)
        property_values.append(property_price)
        print ("Location number "+str(location_counter)+" out of "+str(len(locations)))
        location_counter+=1
        urls_to_homes = get_all_homes_url(zoopla_html)
        for sub_link_no , sub_link in enumerate(urls_to_homes):
            sub_html = requests.get(sub_link).text
            print ("House number "+str(sub_link_no+1)+" out of "+str(len(urls_to_homes)))
            if get_range_and_confidence(sub_html) != None:
                es_range,confi = get_range_and_confidence(sub_html)
            else:
                print ("Unable to  find the range")
                es_range = ["None","None"]
                confi = "None"
            es_ranges.append(es_range)
            confidences.append(confi)
    inner_counter = 0
    for link,ac_end,price,loc,pos in zip(links_to_homes,auction_end_time,prices,locations,postals):
        for p_value,es_range,confi in zip(property_values[inner_counter],es_ranges,confidences):
            csv_file.writerow([link,ac_end,price,loc,pos,p_value,es_range[0],es_range[1],confi])
        inner_counter+=1

print ("Process completed")
outputfile.close()
print ("Quiting Browser")
driver.quit()
