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

PAGES_COUNTS = 1500 # Max pages

url = "https://www.your-move-auction.co.uk/properties"



driver.get(url)
driver.execute_script("window.scrollTo(0,-1000)")
driver.find_element_by_name("location").send_keys(location)
driver.find_element_by_xpath('//*[@id="introduction-properties-form-button"]/input').click()
driver.execute_script('window.scrollTo(0,10000000000)')

with open("your-move-auction "+location+".csv","w",newline='') as outputfile:
    csv_file = csv.writer(outputfile)
    csv_file.writerow(["Price","Location","Postal Code"])
    for i in range(PAGES_COUNTS):
        source = driver.page_source
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
        for price,loc,pos in zip(prices,locations,postals):
            csv_file.writerow([price,loc,pos])
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