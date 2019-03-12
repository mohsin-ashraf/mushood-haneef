import requests
import lxml.html
import time

url = "https://medium.com/search?q="



search_query = input("Please enter the term/ terms(space saperated) to search:")
required_url = url+search_query.replace(' ','%20')
response = requests.get(required_url)

html = response.text

tree = lxml.html.fromstring(html)

xpath = "//div[@class='postArticle-content']//a"

links = tree.xpath(xpath)
links_href = [link.attrib['href'].split('?')[0] for link in links]
titles = [x.text_content().strip() for x in links]
def get_medium_pages(links_href,titles):
    for i,link in enumerate(links_href):
        with open("Medium - "+search_query+str(1+i)+'.txt','w', encoding="utf-8") as outputfile:
            sub_tree = lxml.html.fromstring(requests.get(link).text)
            content = sub_tree.cssselect('div.section-content')[0].text_content()
            outputfile.write(content)
            outputfile.close()

get_medium_pages(links_href,titles)
