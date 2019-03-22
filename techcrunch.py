import requests
import lxml.html
import time
from selenium import webdriver
from docx import Document
from urllib.parse import urljoin
import os
base_url = "https://techcrunch.com"
url = "https://techcrunch.com/search/"

search_query = input("Please enter the term/terms(space saperated) to search:")
required_url = url + search_query.replace(' ', '%20')
driver = webdriver.Chrome('chromedriver')

driver.maximize_window()
driver.get(required_url)

#GLOBALS
SCROLLS = 5 # How many times to scroll
SCROLL_SLEEP_TIME = 3 # it will wait for 2 seconds after every scroll to load the page properly
SCROLL_TO = 100000 # How much to scroll for each time
try:
    os.mkdir("TechCrunch")
except:
    print ("Directory Already exists")

#Making directory
try:
    os.mkdir("TechCrunch/"+search_query)
except:
    print ("Directory Already exists.")

for i in range(SCROLLS):
    driver.execute_script("window.scrollTo(0,"+str((i+1)*SCROLL_TO)+")")
    print ("Scrolling: "+ str(i+1) +" of "+str(SCROLLS))
    try:
        driver.find_element_by_class_name("load-more").click()
    except:
        break
    time.sleep(SCROLL_SLEEP_TIME)

html = driver.page_source
tree = lxml.html.fromstring(html)

print("Quiting browser")
driver.quit()
css_selector = "a.post-block__title__link"

links = tree.cssselect(css_selector)
links_href = [urljoin(base_url, link.attrib['href']) for link in links]
titles = [x.text_content().strip() for x in links]


def get_techcrunch_pages(links_href, titles):
    for i, link in enumerate(links_href):
        print ("Scrapping: "+ str(i+1)+" of "+str(len(links_href)))
        outputfile = Document()
        try:
            sub_tree = lxml.html.fromstring(requests.get(link).text)
        except:
            print ("Url: "+link+" was unable to open")
        content = sub_tree.cssselect('article.article-container.article--post')[0].text_content().strip()
        outputfile.add_paragraph(content)
        print (content)
        outputfile.save("TechCrunch/"+search_query+"/"+search_query+" "+str(i+1)+".docx")


get_techcrunch_pages(links_href, titles)
print ("Process completed")
