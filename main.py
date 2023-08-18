import re
import nltk
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer

with open("miracle_in_the_andes.txt","r",encoding="utf-8") as file:
    book = file.read()

#Extraction of words
words = re.compile("[a-zA-Z]+")
word_match = re.findall(pattern=words,string=book.lower())
print(len(word_match))

#find occurance of words
d={}
for i in word_match:
    if i in d.keys():
        d[i] = d[i]+1
    else:
        d[i]=1
d_list=[(value,key) for (key,value) in d.items()]
f=sorted(d_list,reverse=True)

#Common english words, like articles and blah blah
english_stopwords = stopwords.words("english")

Actual_words=[]
for i,j in f:
    if j not in english_stopwords:
        Actual_words.append((j,i))

#sentiment analysis of chapters
analyzer = SentimentIntensityAnalyzer()

regular = re.compile("Chapter [0-9]+")
chapter = re.split(regular,book)
chapters = chapter[1:]
for i in chapters:
    scores = analyzer.polarity_scores(i)
    print(scores)
