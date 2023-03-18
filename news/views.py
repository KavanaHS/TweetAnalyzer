from django.shortcuts import render
from . import views
import sys
import tweepy
import json
import nltk
import numpy as np
import random
import string
import matplotlib.pyplot as plt
from tkinter import messagebox
import wordninja  # split tag
from textblob import TextBlob
from langdetect import detect
from translate import Translator  # for hindi translation in tweets
import re
from profanityfilter import ProfanityFilter
from django.contrib import messages
import smtplib
import plotly.graph_objects as go
from django.http import*
from news.models import*



pf = ProfanityFilter()
translation = ''
dst = ''


# Create your views here.
def extract(request):
    diction = {}
    if request.method == 'POST':
        place = request.POST['place']
        if (place == "World"):
            WOE_ID = 1
        elif (place == "India"):
            WOE_ID = 23424848
        elif (place == "Bangalore"):
            WOE_ID = 2295420
        elif (place == "Lucknow"):
            WOE_ID = 2295377
        elif (place == "Chennai"):
            WOE_ID = 2295424
        elif (place == "Lahore"):
            WOE_ID = 2211177
        elif (place == "Paris"):
            WOE_ID = 615702
        else:
            return render(request,"index.html",{"error":"Enter valid place !!!"})

            print('Enter valid place !!!')
        
        consumer_key = 'D0n4iN0FEkq4a2VsxH75ITMgf'
        consumer_secret = 'o5tAZC71J8B1vINvqjnzrVVav0d46NnYYoG9CRkCs4RcGbwOZf'
        access_token = '1248982265809362944-Eo28Ybo80etLEsL17H6E6ahduIjPMQ'
        access_token_secret = 'YrKD2deiEnb0tacaI3GERiTKRlI5ESkYBbAnRQ57ArD7s'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)

        api2 = TwitterClient()

        trends = api.get_place_trends(WOE_ID)
        trends = json.loads(json.dumps(trends, indent=1))
        print("*"*30)
        print(trends)
        print("*"*30)
        newscount = 0
        trendCount = 0
        api = TwitterClient()
        for trend in trends[0]["trends"]:
           
            trendCount += 1
            if (trendCount > 10):
                break
            #public_tweets = api.search(trends["name"].strip('#'),count=2)
            #dict[trend["name"].strip('#')] = []
           
            for t in api.get_tweets(trend["name"].strip('#'),10):
                
                diction[trend["name"].strip('#')] = t

                
        return render(request, 'extract.html', {'dict': diction})
    else:
        return render(request, 'index.html')


# return html page with context dictionary of tweets

class TwitterClient(object):
    def __init__(self):
        consumer_key = 'D0n4iN0FEkq4a2VsxH75ITMgf'
        consumer_secret = 'o5tAZC71J8B1vINvqjnzrVVav0d46NnYYoG9CRkCs4RcGbwOZf'
        access_token = '1248982265809362944-Eo28Ybo80etLEsL17H6E6ahduIjPMQ'
        access_token_secret = 'YrKD2deiEnb0tacaI3GERiTKRlI5ESkYBbAnRQ57ArD7s'
        try:
            self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            self.auth.set_access_token(access_token, access_token_secret)
            self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
            print("Successfully Authenticated")
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment 
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count=5):
        tweets = []
        try:
            # call twitter api to fetch tweets 
            fetched_tweets = self.api.search_tweets(q=query, count=count)

            # parsing tweets one by one 
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet 
                parsed_tweet = {}

                # saving text of tweet
                translation = ''
                dst = ''
                lang = detect(tweet.text)
                if (lang == 'en'):
                    analysis = TextBlob(tweet.text)
                    translation = tweet.text
                    dst = '\n <ALREADY IN ENGLISH>'
                else:
                    if lang == 'hi':  # try this out #it does not translate if hindi words are lesser than english
                        translator = Translator(from_lang="hindi", to_lang="english")
                        translation = translator.translate(tweet.text)
                        dst = '\n <THIS IS TRANSLATED FROM HINDI> \n'
                    if lang == 'fr':
                        translator = Translator(from_lang="french", to_lang="english")
                        translation = translator.translate(tweet.text)
                        dst = '\n <THIS IS TRANSLATED FROM FRENCH> \n'
                    if lang == 'ta':
                        translator = Translator(from_lang="tamil", to_lang="english")
                        translation = translator.translate(tweet.text)
                        dst = '\n <THIS IS TRANSLATED FROM TAMIL> \n'
                analysis = TextBlob(translation)
                parsed_tweet['text'] = analysis
                # saving sentiment of tweet 
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
                parsed_tweet['lang'] = dst

                # appending parsed tweet to tweets list 
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once 
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)
            return tweets
        except Exception as e:
            # print error (if any) 
            print("Error : " + str(e))
def index(req):
    return render(req,'index.html')

def main(req): 
    # creating object of TwitterClient Class 
    api = TwitterClient() 
    # calling function to get tweets
    if(req.GET.get('keyword')):
        query = req.GET.get('keyword')
    
    #input("What to search for? ")

        tweets = api.get_tweets(query , count = 200) 
      
        # picking positive tweets from tweets 
        ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
        # percentage of positive tweets 
        print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
        #f.write(format(100*len(ptweets)/len(tweets))) 
        # picking negative tweets from tweets 
        ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
        # percentage of negative tweets 
        print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
        # percentage of neutral tweets 
        print("Neutral tweets percentage: {} %".format((100*len(tweets)-100*len(ntweets)-100*len(ptweets))/len(tweets)))
        ptperc = 100*len(ptweets)/len(tweets)
        ntperc = 100*len(ntweets)/len(tweets)
       
        
        # printing first 5 positive tweets 
        print("\n\nPositive tweets:") 
        for tweet in ptweets[:10]: 
            print(tweet['text']) 
      
        # printing first 5 negative tweets 
        print("\n\nNegative tweets:") 
        for tweet in ntweets[:10]: 
            print(tweet['text']) 

        #f.close()
        slices_tweets = [format(100*len(ptweets)/len(tweets)), format(100*len(ntweets)/len(tweets)), format((100*len(tweets)-100*len(ntweets)-100*len(ptweets))/len(tweets))]
        analysis = ['Positive', 'Negative', 'Neutral']
        colors = ['g', 'r', 'y']
        return render(req,"chart.html",{"values":slices_tweets,"labels":analysis,"ptweets":tweets,})
    else:
        return render(req,"chart.html")
'''
    plt.pie(slices_tweets, labels=analysis, startangle=-40, autopct='%.1f%%')
    plt.savefig(query)
    plt.title("Tweet Report")
    plt.show()
    return ptperc,ntperc;
'''

if __name__ == "__main__": 
    # calling main function 
    main() 

def index1(req):
    return render(req,'index1.html')


def smtp_sendmail(email,subject,body):
    server=smtplib.SMTP("smtp.gmail.com",587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login("gagannov1999@gmail.com","wuhoburgtppqpfwz")

    message=f"subject:{subject}\n\n{body}"
    server.sendmail("gagannov1999@gmail.com",email,message)
    server.quit()
    print("mail sent")

def submit(req):
    email=req.POST.get('email')
    subject=req.POST.get('name')
    body=subject,"Thank You For Subscription(-_-)"
    ulist=sub.objects.all().values()
    unamelist=[]
    for i in ulist:
        unamelist.append(i['email'])
        if(email in unamelist):
            return render(req,'index.html',{'error1':'You Allredy Subsribed (-_-)'})

    x=sub(name=subject,email=email)
    x.save()
    smtp_sendmail(email,subject,body)
    return render(req,'send.html')

def send(req):
    return render(req,'send.html')
'''
def list1(req):
    x=sub.objects.all()
    list1=x.values()
    return render(req,"sub.html",{"list":list1})

def admin(req):
    name=req.POST.get('aname')
    pwd=req.POST.get('apwd')
    x=alogin(Name=name,Pass=pwd)
    x.save()
    return HttpResponse("registerd")

def login11(req):
    name=req.POST.get('name')
    pwd=req.POST.get('pwd')
    ulist=alogin.objects.all().values()
    uname_list=[]
    for i in ulist:
        password=alogin.objects.get(Name=name)
        if(password.Pass==pwd):
            return render(req,'sub.html')
        else:
            return render(req,'login1.html')
            
def login1(req):
    return render(req,'login1.html')


def sub1(req):
    return render(req,'sub.html')

def admin1(req):
    return render(req,'admin.html')
    '''