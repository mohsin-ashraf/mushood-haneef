from selenium import webdriver
import lxml.html
import time
import csv



#utility funcitons
def term_exist(terms,video_title):
    for term in terms:
        if term in video_title:
            return True
    return False

#channels will have a list of channels listed in the file
channels = open('channels.txt').readlines()

#related links to youtube videos list
related_videos = [] #this list will store the links to the videos that user searched for.

#removing all the line breaks charactors i.e \n
channels = [channel.replace('\n','') for channel in channels if channel !='\n']

#Taking input from the user for the search term
search_term = input('Please enter the term sapareted by space: ')

#initializing the selenium webdriver
driver = webdriver.Chrome('chromedriver.exe')

driver.implicitly_wait(10) # it will wait for 10 seconds to load data if the data is loaded before it would not
#                            wait you can also you time.sleep(x) for waiting x number of seconds
driver.maximize_window()

#Converting the string search_input into a list of search terms by spliting on space
search_terms = search_term.split(' ')

#convering the terms in the list to lower case to make case insensitive comparison with the list of videos
search_terms = [term.lower() for term in search_terms]

for channel_link in channels:
    #chech to see if the the link is youtube channel or not
    if 'youtube' in channel_link and 'user' in channel_link:
        # getting to the url channel in the browser
        driver.get(channel_link)
        #following for loop is used to scroll the page untill all the videos are loading I am using 10 scrolls you can increase or decrease it as you need.
        for i in range(10):
            driver.execute_script('window.scrollTo(0,'+str(i*1000)+')')
            #waiting for two seconds for every load since ajax calls might take some time.
            time.sleep(2)
        html = driver.page_source
        tree = lxml.html.fromstring(html)
        videos = tree.xpath("//a[@id='video-title']")
        videos = [(x.text_content().strip(),x.attrib['href']) for x in videos]
        for video in videos:
            if term_exist(search_terms,video[0]):
                related_videos.append((video[0],'https://www.youtube.com'+video[1]))
    print (related_videos)

with open(search_term+'.csv', 'w', newline='') as outputfile:
    csv_file = csv.writer(outputfile)
    csv_file.writerow(['Title','Link'])
    for video in related_videos:
        csv_file.writerow([video[0],video[1]])
    outputfile.close()

