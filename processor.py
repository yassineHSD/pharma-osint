import json
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np
negative=[]
neutral=[]
positive=[]
def adjust_inputs(qlist):
    tmp=0
    tmp_qlist=qlist
    last_year=qlist[0]["Year"]-1
    for c in qlist:
        if(c["Year"]-1!=last_year):
            tmp_qlist.insert(tmp,{'Year': c["Year"]-1, 'upvoteCount': np.nan, 'count': np.nan})
            last_year=c["Year"]-1
        else:
            last_year=c["Year"]
        tmp=tmp+1
    return tmp_qlist
def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

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

negative=adjust_inputs(negative)
neutral=adjust_inputs(neutral)
positive=adjust_inputs(positive)
ng_years = [item['Year'] for item in negative]
ng_comments = [item['count'] for item in negative]

pos_years = [item['Year'] for item in positive]
pos_comments = [item['count'] for item in positive]

neut_years = [item['Year'] for item in neutral]
neut_comments = [item['count'] for item in neutral]


reddit_mau_values=[46,90,174,199,250,330,430,np.nan,np.nan,np.nan,np.nan]
reddit_mau_years=[2012,2013,2014,2015,2017,2018,2019]

reddit_mau_values_x=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,430,636,941,1392,2060]
reddit_mau_years_x=[2012,2013,2014,2015,2017,2018,2019]

reddit_mau_values_off=[46,90,174,199,250,330,430]

#avg line droite de MAYER
#definition des groupes

g1_years, g2_years = split_list(reddit_mau_years)
g1_maus, g2_maus = split_list(reddit_mau_values_off)
print(g1_years)
print(g1_maus)
g1_maus_avg=sum(g1_maus)/len(g1_maus)
g2_maus_avg=sum(g2_maus)/len(g2_maus)

g1_years_avg=sum(g1_years)/len(g1_years)
g2_years_avg=sum(g2_years)/len(g2_years)

print(g1_years_avg)
print(g2_years_avg)
print(g1_maus_avg)
print(g2_maus_avg)



g1 = [g1_years_avg, g1_maus_avg]
g2 = [g2_years_avg, g2_maus_avg]

#pente a (y1-y2)/(x1-x2)
a=0.0
print(g1[0])
b=0.0
a=(float(g2[1])-float(g1[1]))/(float(g2[0])-float(g1[0]))
#point y lorsque x=0
b=g2[1]-a*g2[0]

x_values = [g1_years[0], neut_years[len(neut_years)-1]]
y_values = [g1_years[0]*a+b, neut_years[len(neut_years)-1]*a+b]

#reddit estimated values (droite de mayer)

reddit_mau_values_mayer=[46,90,174,199,2016*a+b,250,330,430,2020*a+b,2021*a+b,2022*a+b]
reddit_mau_years_mayer=[2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2021]
#negative comments by 1000 MAU
ng_by_mau = [i / j * 1000 for i, j in zip(ng_comments, reddit_mau_values_mayer)]
#neutral comments by 1000 MAU
neut_by_mau = [i / j * 1000 for i, j in zip(neut_comments, reddit_mau_values_mayer)]
#positive comments by 1000 MAU
pos_by_mau = [i / j * 1000 for i, j in zip(pos_comments, reddit_mau_values_mayer)]
print(ng_by_mau)
print(ng_years)
print(reddit_mau_values_mayer)

fig = plt.figure()
ax1 = fig.add_subplot(111)

fig2 = plt.figure()
ax2 = fig2.add_subplot(111)

ax2.plot(reddit_mau_years_mayer, ng_by_mau,label='Negative comments by 1000 MAU')
ax2.plot(reddit_mau_years_mayer, neut_by_mau,label='neutral comments by 1000 MAU')
ax2.plot(reddit_mau_years_mayer, pos_by_mau,label='positive comments by 1000 MAU')
ax2.axvline(x=2019.5, color='black', linestyle='dashed',label='COVID-19 happened',linewidth=1)
ax1.plot(x_values, y_values,label='Reddit MAU (Mayer est)')

ax1.plot(ng_years, ng_comments,label='Negative comments count')
ax1.plot(pos_years, pos_comments,label='Positive comments count')
ax1.plot(neut_years, neut_comments,label='Positive comments count')
ax1.plot(neut_years, reddit_mau_values,label='Reddit MAU')
ax1.scatter(neut_years, reddit_mau_values_x,label='Reddit MAU (+48% avg est)')
#plt.xticks(np.arange(2012, 2021, step=1))
plt.legend(loc='upper left');
plt.show()
