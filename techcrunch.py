import requests
import lxml.html
import time
from urllib.parse import urljoin

base_url = "https://techcrunch.com"
url = "https://techcrunch.com/search/"



search_query = input("Please enter the term/terms(space saperated) to search:")
required_url = url+search_query.replace(' ','%20')
response = requests.get(required_url)

html = response.text

tree = lxml.html.fromstring(html)

css_selector = "a.post-block__title__link"

links = tree.cssselect(css_selector)
links_href = [urljoin(base_url,link.attrib['href']) for link in links]
titles = [x.text_content().strip() for x in links]


def get_techcrunch_pages(links_href,titles):
    for i,link in enumerate(links_href):
        with open("techcrunch - "+search_query+str(1+i)+'.txt','w', encoding="utf-8") as outputfile:
            sub_tree = lxml.html.fromstring(requests.get(link).text)
            content = sub_tree.cssselect('article.article-container.article--post')[0].text_content().strip()
            outputfile.write(content)
            outputfile.close()

get_techcrunch_pages(links_href,titles)

