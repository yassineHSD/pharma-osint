import json
from datetime import datetime
import re
import matplotlib.pyplot as plt

negative=[]
neutral=[]
positive=[]

def fetch_years(qual):
    counter=0
    tmp_i=0
    qlist=[]
    for i in range(0,len(sorted_comments)):
        if(sorted_comments[i]['Qualification']==qual):
            counter=counter+1
            if(counter==1):
                qlist.append(
                {
                "Year":sorted_comments[i]['dateModified'].year,
                "upvoteCount":sorted_comments[i]['upvoteCount'],
                "count":1
                })
                tmp_i=i
            else:
                if(sorted_comments[i]['dateModified'].year==sorted_comments[tmp_i]['dateModified'].year):
                    qlist[len(qlist)-1]["upvoteCount"]=qlist[len(qlist)-1]["upvoteCount"]+sorted_comments[i]["upvoteCount"]
                    qlist[len(qlist)-1]["count"]=qlist[len(qlist)-1]["count"]+1
                else:
                    tmp_i=i
                    qlist.append(
                    {
                    "Year":sorted_comments[i]['dateModified'].year,
                    "upvoteCount":sorted_comments[i]['upvoteCount'],
                    "count":1
                    })
    return qlist
with open('output.json','r') as output_json:
    comments = json.load(output_json)
    #format date-time
    for comment in comments:
        match = re.search(r'\d{4}-\d{2}-\d{2}', comment['dateModified'])
        date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        comment['dateModified']=date
    sorted_comments = sorted(comments, key=lambda x: x['dateModified'])
    print(sorted_comments[1]['dateModified'])
    print(sorted_comments[len(sorted_comments)-1]['dateModified'])
negative=fetch_years("Negative")
positive=fetch_years("Positive")
neutral=fetch_years("Neutral")
print(negative)
print(positive)
print(neutral)


ng_years = [item['Year'] for item in negative]
ng_comments = [item['count'] for item in negative]

pos_years = [item['Year'] for item in positive]
pos_comments = [item['count'] for item in positive]

neut_years = [item['Year'] for item in neutral]
neut_comments = [item['count'] for item in neutral]

fig = plt.figure()
ax1 = fig.add_subplot(111)

ax1.plot(ng_years, ng_comments,label='Negative comments count')
ax1.plot(pos_years, pos_comments,label='Positive comments count')
ax1.plot(neut_years, neut_comments,label='Positive comments count')
plt.legend(loc='upper left');
plt.show()
