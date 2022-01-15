import json
from datetime import datetime
import re
import matplotlib.pyplot as plt
import numpy as np
import time
import sys
from datetime import datetime
negative=[]
neutral=[]
positive=[]
reddit_mau_values=[46,90,174,199,250,330,430,np.nan,np.nan,np.nan,np.nan]
reddit_mau_years=[2012,2013,2014,2015,2017,2018,2019]
reddit_mau_values_x=[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,430,636,941,1392,2060]
reddit_mau_years_x=[2012,2013,2014,2015,2017,2018,2019]
reddit_mau_values_off=[46,90,174,199,250,330,430]

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def mayer_line():
#avg line droite de MAYER
#definition des groupes
    a=0.0
    b=0.0
    g1_years, g2_years = split_list(reddit_mau_years)
    g1_maus, g2_maus = split_list(reddit_mau_values_off)
    g1_maus_avg=sum(g1_maus)/len(g1_maus)
    g2_maus_avg=sum(g2_maus)/len(g2_maus)
    g1_years_avg=sum(g1_years)/len(g1_years)
    g2_years_avg=sum(g2_years)/len(g2_years)
    g1 = [g1_years_avg, g1_maus_avg]
    g2 = [g2_years_avg, g2_maus_avg]
    #pente a (y1-y2)/(x1-x2)
    a=(float(g2[1])-float(g1[1]))/(float(g2[0])-float(g1[0]))
    #point y lorsque x=0
    b=g2[1]-a*g2[0]
    return a,b

def adjust_inputs(qlist):
    tmp=0
    v=0
    tmp_qlist=qlist
    last_year=qlist[0]["Year"]-1
    if(qlist[0]["Year"]>2012):
        for c in qlist:
            if(2012+v==qlist[v]["Year"]):
                break
            else:
                tmp_qlist.insert(v,{'Year': 2012+v, 'upvoteCount': np.nan, 'count': np.nan})
            v=v+1
    for c in qlist:
        if((c["Year"]-1!=last_year) and (c["Year"]-1!=2011)):
            myaw=0
            for myaw in range(1,c["Year"]-last_year):
                tmp_qlist.insert(tmp,{'Year': myaw+last_year, 'upvoteCount': np.nan, 'count': np.nan})
            last_year=myaw+last_year
        else:
            last_year=c["Year"]
        tmp=tmp+1
    return tmp_qlist

def fetch_years(qual,sorted_comments):
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
def draw_charts(negative,neutral,positive):
    ng_years = [item['Year'] for item in negative]
    ng_comments = [item['count'] for item in negative]

    pos_years = [item['Year'] for item in positive]
    pos_comments = [item['count'] for item in positive]

    neut_years = [item['Year'] for item in neutral]
    neut_comments = [item['count'] for item in neutral]

    neg_upvotes = [item['upvoteCount'] for item in negative]
    neut_upvotes = [item['upvoteCount'] for item in neutral]
    pos_upvotes = [item['upvoteCount'] for item in positive]


    #finding 2 extreme point on the mayer line
    x_values = [neut_years[0], neut_years[len(neut_years)-1]]
    y_values = [neut_years[0]*a+b, neut_years[len(neut_years)-1]*a+b]


    #negative comments by 1000 MAU
    ng_by_mau = [i / j * 1000 for i, j in zip(ng_comments, reddit_mau_values_mayer)]
    #neutral comments by 1000 MAU
    neut_by_mau = [i / j * 1000 for i, j in zip(neut_comments, reddit_mau_values_mayer)]
    #positive comments by 1000 MAU
    pos_by_mau = [i / j * 1000 for i, j in zip(pos_comments, reddit_mau_values_mayer)]

    ng_upv_by_mau = [i / j * 1000 for i, j in zip(neg_upvotes, reddit_mau_values_mayer)]
    neut_upv_by_mau = [i / j * 1000 for i, j in zip(neut_upvotes, reddit_mau_values_mayer)]
    pos_upv_by_mau = [i / j * 1000 for i, j in zip(pos_upvotes, reddit_mau_values_mayer)]




    fig = plt.figure(figsize=(10,10))
    ax1 = fig.add_subplot(221)
    ax3 = fig.add_subplot(222)
    ax4 = fig.add_subplot(223)
    ax2 = fig.add_subplot(224)

    ax1.plot(x_values, y_values,label='Reddit MAU (Mayer est)')
    ax1.plot(ng_years, ng_comments,label='Negative comments count')
    ax1.plot(pos_years, pos_comments,label='Positive comments count')
    ax1.plot(neut_years, neut_comments,label='Positive comments count')
    ax1.plot(neut_years, reddit_mau_values,label='Reddit MAU')
    ax1.scatter(neut_years, reddit_mau_values_x,label='Reddit MAU (+48% avg est)')
    ax1.axvline(x=2019.5, color='black', linestyle='dashed',label='COVID-19 happened',linewidth=1)
    #plt.xticks(np.arange(2012, 2021, step=1))
    ax1.legend(loc='upper left')


    ax2.plot(reddit_mau_years_mayer, ng_by_mau,label='Negative upvotes by 1000 MAU')
    ax2.plot(reddit_mau_years_mayer, neut_by_mau,label='Neutral upvotes by 1000 MAU')
    ax2.plot(reddit_mau_years_mayer, pos_by_mau,label='Positive upvotes by 1000 MAU')
    ax2.axvline(x=2019.5, color='black', linestyle='dashed',label='COVID-19 happened',linewidth=1)

    ax2.legend(loc='upper left')
    ax3.plot(ng_years, neg_upvotes,label='Negative upvotes')
    ax3.plot(neut_years, neut_upvotes,label='Negative upvotes')
    ax3.plot(pos_years, pos_upvotes,label='Negative upvotes')

    ax3.legend(loc='upper left');

    ax4.plot(reddit_mau_years_mayer, ng_upv_by_mau,label='Negative comments by 1000 MAU')
    ax4.plot(reddit_mau_years_mayer, neut_upv_by_mau,label='Neutral comments by 1000 MAU')
    ax4.plot(reddit_mau_years_mayer, pos_upv_by_mau,label='Positive comments by 1000 MAU')
    ax4.axvline(x=2019.5, color='black', linestyle='dashed',label='COVID-19 outbreak',linewidth=1)

    ax4.legend(loc='upper left');

    plt.draw()
    fig.savefig('./charts/'+data_set.replace('/','-')+"-"+str(timestamp)+'.png', dpi=300)
    print("[+] Charts saved to: ./charts/"+data_set.replace('/','-')+"-"+str(timestamp)+".png")
    plt.show()

def sort_comments(comments):
    for comment in comments:
        match = re.search(r'\d{4}-\d{2}-\d{2}', comment['dateModified'])
        date = datetime.strptime(match.group(), '%Y-%m-%d').date()
        comment['dateModified']=date
    sorted_comments = sorted(comments, key=lambda x: x['dateModified'])

    return sorted_comments
def sort_qlist(qlist):
    sorted_qlist = sorted(qlist, key=lambda x: x["Year"])
    return sorted_qlist

if(len(sys.argv)>1):
    if(sys.argv[1]=="--help"):
                print("Usage:")
                print("\t python3 processor.py <dataset1> <dataset2> <dataset3> ....")
                print("\t Options: --help : to show this message")
    else:
        data_sets=sys.argv[1:]
        for data_set in data_sets:
            now = datetime.now()
            timestamp = datetime.timestamp(now)
            with open(data_set,'r') as output_json:
                comments = json.load(output_json)
                #format date-time and sort the entries according to date-time
                sorted_comments=sort_comments(comments)
            a,b=mayer_line()
            #reddit estimated values (droite de mayer)
            reddit_mau_values_mayer=[46,90,174,199,2016*a+b,250,330,430,2020*a+b,2021*a+b,2022*a+b]
            reddit_mau_years_mayer=[2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2021]
            negative=fetch_years("Negative",sorted_comments)
            positive=fetch_years("Positive",sorted_comments)
            neutral=fetch_years("Neutral",sorted_comments)
            negative=adjust_inputs(negative)
            neutral=adjust_inputs(neutral)
            positive=adjust_inputs(positive)
            negative=sort_qlist(negative)
            neutral=sort_qlist(neutral)
            positive=sort_qlist(positive)
            draw_charts(negative,neutral,positive)
else:
    print("Usage:")
    print("\t python3 processor.py <dataset1> <dataset2> <dataset3> ....")
    print("\t Options: --help : to show this message")
