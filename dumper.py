from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import time
import requests
import re
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import sys
#global variables
nltk.download('vader_lexicon')
url_list=[]
driver_path = "/usr/local/bin/chromedriver"
brave_path = "/usr/bin/brave-browser"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
option.add_argument("--incognito")
option.add_argument("--tor")
#option.add_argument('--headless')
browser = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
action = webdriver.ActionChains(browser)

now = datetime.now()
timestamp = datetime.timestamp(now)
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

def more_results():
    try:
        browser.find_element_by_class_name('result--more__btn')
    except NoSuchElementException:
        return False
    return True
if(len(sys.argv)>1):
    if(sys.argv[1]=="--help"):
        print("Usage:")
        print("\t python3 dumper.py <target1> <target2> <target3> ....")
        print("\t Options: --help : to show this message")
    else:
        search_targets=sys.argv[1:]
        for target in search_targets:
            print("[+] Target: "+str(target))
            browser.get("https://duckduckgo.com/?q=site%3Areddit.com+AND+intitle%3A"+str(target)+"+AND+inurl%3Acomments+%22"+str(target)+"%22&t=h_&ia=web")
            while more_results():
                    element = browser.find_element_by_class_name('result--more__btn')
                    action.move_to_element(element)
                    action.perform()
                    element.click()
                    time.sleep(1)
            html_source = browser.page_source
            soup = BeautifulSoup(html_source,'lxml')
            count_result=0
            for a in soup.findAll('a', attrs={'class':'result__a'}):
                count_result=count_result+1
                url_list.append(a['href'])
                f = open("./log/"+str(target)+"-url_list-"+str(timestamp)+".txt", "a")
                f.write(a['href']+"\n")
                f.close()
            print("[+] Results found: "+str(count_result))
            myheader = {"User-Agent": "GoogleBot"}
            final_output=[]
            i=0
            for url in url_list:
                i=i+1
                print("[+]Fetching comments in reddit ("+str(i)+"/"+str(len(url_list))+"):"+str(url),end='\r',flush=True)
                session = tor_session()
                url=url.replace("//www.","//amp.")
                r = session.get(url)
                body=r.text
                #sys.stdout.flush()
                pattern_json = "\<script type\=\"application\/ld\+json\"\>(.*?)\<\/script\>"

                if re.search(pattern_json, body):
                    json_data = re.search(pattern_json, body).group()[35:-9]

                if "comment" in json.loads(json_data):
                    comments = json.loads(json_data)["comment"]
                    final_output=final_output+process_comments(comments)
                else:
                    print("No comments found in this reddit/Can not load comments from this reddit " +url)
            with open('./log/'+str(target)+'-output-'+str(timestamp)+'.json', 'a') as jsondumpfile:
                json.dump(final_output, jsondumpfile,indent=4)
            print("\n",flush=True)
            print("[+] Comments dumped to "+str(target)+'-output-'+str(timestamp)+'.json' )
            print("[+] URLs dumped to "+str(target)+'-url_list-'+str(timestamp)+'.txt' )
        print("[+] To process the data please run process.py <data-file.json>")
else:
    print("Usage:")
    print("\t python3 dumper.py <target1> <target2> <target3> ....")
    print("\t Options: --help : to show this message")
browser.close()
