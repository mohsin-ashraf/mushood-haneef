import requests
import lxml.html

url = 'https://www.opentable.com/r/vue-de-monde-melbourne?corrid=780c2b7a-e2f1-496e-9b1b-e5512e26926a'

html = requests.get(url).text
tree = lxml.html.fromstring(html)

review_boxes = tree.cssselect("div.reviewListItem.oc-reviews-91417a38")

for review in review_boxes:
    print (review.cssselect("div.oc-reviews-500374bf")[0].text_content())
    print (review.cssselect("div.oc-reviews-954a6007")[0].text_content())
    print (review.cssselect('p')[0].text_content())
    print ("_____")
