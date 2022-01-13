import requests
import re
import json
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

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
    return processed_data
myheader = {"User-Agent": "GoogleBot"}
url="https://amp.reddit.com/r/SecurityAnalysis/comments/5zhbwq/roche_vs_novartis_profitability/"
session = requests.Session()
r = session.get(url)
body=r.text

#pattern_datetime = "\<\/span\> \·(.*?)\<\/a\>\<\/div\>\<amp\-layout"
#post_datetime = re.search(pattern_datetime, body).group()[10:-21]
#print(post_datetime)
pattern_json = "\<script type\=\"application\/ld\+json\"\>(.*?)\<\/script\>"
json_data = re.search(pattern_json, body).group()[35:-9]


if "comment" in json.loads(json_data):
    comments = json.loads(json_data)["comment"]
    output=process_comments(comments)
    with open('output.json', 'w') as jsondumpfile:
        json.dump(output, jsondumpfile)
else:
    print("No comments found in this reddit/Can not load comments from this reddit")
