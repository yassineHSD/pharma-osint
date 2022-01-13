from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import requests
import re
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

url_list=[]

nltk.download('vader_lexicon')

def tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def qualify(comment,ss):
    if ss['compound'] >= 0.05 :
        qual="Positive"
    elif ss['compound'] <= - 0.05 :
        qual="Negative"
    else :
        qual="Neutral"
    return qual
def process_comments(comments):
    processed_data=[]
    for comment in comments:
        if "text" in comment:
            sid = SentimentIntensityAnalyzer()
            ss = sid.polarity_scores(comment["text"])
            Qualification=qualify(comment["text"],ss)
            print(comment["dateModified"])
            print(comment["text"])
            print(Qualification)
            print("_____________________________")
            row={
            "Comment":comment["text"],
            "dateModified":comment["dateModified"],
            "Qualification":Qualification,
            "upvoteCount":comment["upvoteCount"],
            "username":comment["author"]["name"],
            "author.type":comment["author"]["@type"],
            "url":comment["url"],
            }
            processed_data.append(row)
        else:
            continue
    return processed_data

driver_path = "/usr/local/bin/chromedriver"
brave_path = "/usr/bin/brave-browser"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--incognito")
option.add_argument("--tor")

browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)


action = webdriver.ActionChains(browser)
def more_results():
    try:
        browser.find_element_by_class_name('result--more__btn')
    except NoSuchElementException:
        return False
    return True

browser.get("https://duckduckgo.com/?q=site%3Areddit.com+AND+intitle%3ANovartis+AND+inurl%3Acomments&t=h_&ia=web")
while more_results():
        element = browser.find_element_by_class_name('result--more__btn')
        action.move_to_element(element)
        action.perform()
        element.click()
        time.sleep(1)
html_source = browser.page_source
soup = BeautifulSoup(html_source,'lxml')

for a in soup.findAll('a', attrs={'class':'result__a'}):
    url_list.append(a['href'])
f = open("url_list.txt", "w")
f.write(str(url_list))
f.close()

myheader = {"User-Agent": "GoogleBot"}

final_output=[]
for url in url_list:
    print(url)
    session = tor_session()
    url=url.replace("//www.","//amp.")
    r = session.get(url)
    body=r.text

    pattern_json = "\<script type\=\"application\/ld\+json\"\>(.*?)\<\/script\>"

    if re.search(pattern_json, body):
        json_data = re.search(pattern_json, body).group()[35:-9]

    if "comment" in json.loads(json_data):
        comments = json.loads(json_data)["comment"]
        final_output=final_output+process_comments(comments)
    else:
        print("No comments found in this reddit/Can not load comments from this reddit")
with open('output.json', 'a') as jsondumpfile:
    json.dump(final_output, jsondumpfile,indent=4)
