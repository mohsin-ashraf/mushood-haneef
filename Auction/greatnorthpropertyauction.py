from selenium import webdriver
import lxml.html
import time
import os
import requests
import csv

location = input("Please enter the location: ")
#location = "Nottinghamshire"
driver = webdriver.Chrome(os.getcwd()+"/chromedriver")
driver.maximize_window()
driver.implicitly_wait(50)
PAGES_COUNTS = 1500 # Max pages

url = "https://www.greatnorthpropertyauction.co.uk/properties"



driver.get(url)
driver.execute_script("window.scrollTo(0,-1000)")
driver.find_element_by_name("location").send_keys(location)
driver.find_element_by_xpath('//*[@id="introduction-properties-form-button"]/input').click()
driver.execute_script('window.scrollTo(0,10000000000)')

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

with open("greatnorthpropertyauction "+location+".csv","w",newline='') as outputfile:
    csv_file = csv.writer(outputfile)
    csv_file.writerow(["Auction Link","Time Left","Price","Location","Postal Code","Perperty Value","Low Range","High Range","Confidence"])
    for i in range(PAGES_COUNTS):
        source = driver.page_source
        es_ranges = []
        confidences = []
        property_values = []
        tree = lxml.html.fromstring(source)
        prices = tree.cssselect("span.properties-preview-content-price-figure")
        prices = [price.text_content() for price in prices]
        addresses = tree.cssselect('div.properties-preview-content-details')
        addresses = [address.text_content() for address in addresses]
        addresses = [address.split(',') for address in addresses]
        for i in range(len(addresses)):
            addresses[i] = [x.strip() for x in addresses[i]]
            print (addresses[i])
        locations = [address[0] + ", "+ address[1] for address in addresses]
        print (locations)
        postals = tree.cssselect('span.properties-preview-content-details-address.details-address-postcode')
        postals = [postal.text_content() for postal in postals]
        location_counter = 1
        links_to_homes = tree.cssselect('div.properties-preview-position div.properties-preview > a')
        links_to_homes = ["https://www.iamsold.co.uk"+link.attrib['href'] for link in links_to_homes]
        for j,link in enumerate(links_to_homes):            
            print ("Auction time from home number: "+str(j+1))
            sub_tree = lxml.html.fromstring(requests.get(link).text)
            try:
                auction_time = sub_tree.cssselect('span.end_time_auto_time.stat-value.stat-value--large')[0].text_content()
            except:
                auction_time = "No information available for time."
            end_time_auction.append(auction_time)
            print (auction_time)
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
                    es_range = ["None","None"]
                    confi = "None"
                es_ranges.append(es_range)
                confidences.append(confi)
        inner_counter = 0
        for end_time,link_to_auction,price,loc,pos in zip(end_time_auction,links_to_homes,prices,locations,postals):
            print (loc)
            for p_value,es_range,confi in zip(property_values[inner_counter],es_ranges,confidences):
                csv_file.writerow([link_to_auction,end_time,price,loc,pos,p_value,es_range[0],es_range[1],confi])
            inner_counter+=1
            
        try:
            driver.execute_script('document.querySelectorAll("div#pagination-count a")['+str(i)+'].click()')
            print ("Next page: "+str(i+1))
            print ("Waiting for page to load the data: ")
            time.sleep(5)
        except:
            print ("No more pages")
            break

print ("Process completed")
outputfile.close()
print ("Quiting Browser")
driver.quit()
