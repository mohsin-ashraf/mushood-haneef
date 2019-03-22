import requests
import lxml.html
import time
from docx import Document
from selenium import webdriver
import os

#GLOBALS
SCROLLS = 50 # How many times to scroll
SCROLL_SLEEP_TIME = 2 # it will wait for 2 seconds after every scroll to load the page properly
SCROLL_TO = 10000 # How much to scroll for each time

url = "https://medium.com/search?q="

driver = webdriver.Chrome("chromedriver")
driver.implicitly_wait(10)
driver.maximize_window()
search_query = input("Please enter the term/ terms(space saperated) to search:")
required_url = url + search_query.replace(' ', '%20')
driver.get(required_url)
try:
    os.mkdir("Medium")
except:
    print ("Directory already exists")

#Making directory
try:
    os.mkdir("Medium/"+search_query)
except:
    print ("Directory Already exist.")

print ("Scrolling down to load data")

for i in range(SCROLLS):
    driver.execute_script("window.scrollTo(0,"+str((i+1)*SCROLL_TO)+")")
    print ("Scrolling: "+ str(i+1) +" of "+str(SCROLLS))
    time.sleep(SCROLL_SLEEP_TIME)
html = driver.page_source
print ("Quiting browser")
driver.quit()

tree = lxml.html.fromstring(html)

xpath = "//div[@class='postArticle-content']//a"

links = tree.xpath(xpath)
links_href = [link.attrib['href'].split('?')[0] for link in links]
titles = [x.text_content().strip() for x in links]

print ("Total Topics found: "+str(len(links_href)))


def get_medium_pages(links_href, titles):
    for i, link in enumerate(links_href):
        print ("Scrapping: "+ str(i+1)+" of "+str(len(links_href)))
        outputfile = Document()
        try:
            sub_tree = lxml.html.fromstring(requests.get(link).text)
        except:
            print ("Url: "+link+" was unable to open")
        content = sub_tree.cssselect('div.section-content')[0].text_content()
        outputfile.add_paragraph(content)
        outputfile.save("Medium/"+search_query+"/"+search_query+" "+str(i+1)+".docx")


get_medium_pages(links_href, titles)
print ("Process completed")
