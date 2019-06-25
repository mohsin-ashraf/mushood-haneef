import requests
import lxml.html


url = "https://www.tripadvisor.com/AttractionProductReview-g32482-d11445987-Healdsburg_Wine_Tasting_and_Food_Pairing_Guided_Walking_Tour-Healdsburg_Sonoma_Coun.html"

html = requests.get(url).text
tree = lxml.html.fromstring(html)

review_containers = tree.cssselect('div.review-container')

file = open('output.txt','w')
for container in review_containers:
    name = "None"
    try:
        name = container.cssselect('div.userLoc')[0].text_content()
        name=name.encode('unicode-escape').decode('utf-8')
    except:
        continue
    date = "None"
    try:
        date = container.cssselect('span.ratingDate')[0].attrib['title']
        date=date.encode('unicode-escape').decode('utf-8')
    except:
        continue
    if '2019' in date:
        print()
    else:
        continue
    review = "None"
    try:
        review = container.cssselect('p.partial_entry')[0].text_content()
        review=review.encode('unicode-escape').decode('utf-8')
    except:
        continue
    print (name)
    print (date)
    print (review)
    file.write(name+"\n")
    file.write(date+"\n")
    file.write(review+"\n")
    file.write('\n\n\n')
file.close()
