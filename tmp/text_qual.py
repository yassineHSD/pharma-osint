import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
comment=""
ss = sid.polarity_scores(comment)
print(ss)
if ss['compound'] >= 0.05 :
    qual="Positive"
elif ss['compound'] <= - 0.05 :
    qual="Negative"
else :
    qual="Neutral"
print(qual)
