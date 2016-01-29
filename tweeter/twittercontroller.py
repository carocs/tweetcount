from twitter import *
from string import replace
import twitterconfig
from django.http import HttpResponse
import models
from dateutil import parser
from datetime import timedelta, datetime
from itertools import islice
from collections import Counter

def search_tweets(coordx, coordy):
    latitude = replace(coordx,',','.')
    longitude = replace(coordy,',','.')

    print latitude

    print longitude

    twitterApi = Api(twitterconfig.consumer_key,twitterconfig.consumer_secret,twitterconfig.access_key, twitterconfig.access_secret)

    result_count = 0

    result_list = []

    buscaInicial = twitterApi.GetSearch(geocode=(latitude,longitude,'1km'), count=1, result_type="recent")
    tweet = models.Tweet()

    for result in buscaInicial:
        tweet.tweet_date = parser.parse(result._created_at)
        tweet.tweet_user = str(result._user._name.encode('utf-8'))
        if result._place:
            tweet.tweet_cidade = str(result._place['name'].encode('utf-8'))
            tweet.tweet_pais = str(result._place['country'].encode('utf-8'))
        tweet.tweet_text = str(result._text.encode('utf-8'))
        tweet.tweet_nchar = tweet.tweet_text.__len__()
        tweet.tweet_nwords = len(tweet.tweet_text.split())
        tweet.save()
        result_list.append(tweet)
        result_count+=1
        print tweet

        print "got %d results" % result_count

    if tweet.tweet_date != None:
        dataPassada = tweet.tweet_date - timedelta(days=6)
    else:
        dataPassada = datetime.now() - timedelta(days=6)

    buscaPassada = twitterApi.GetSearch(geocode=(latitude,longitude,'1km'), count=1, result_type="recent", until=dataPassada.date().isoformat())

    tweet = models.Tweet()

    for result in buscaPassada:
        tweet.tweet_date = parser.parse(result._created_at)
        tweet.tweet_user = str(result._user._name.encode('utf-8'))
        if result._place:
            tweet.tweet_cidade = str(result._place['name'].encode('utf-8'))
            tweet.tweet_pais = str(result._place['country'].encode('utf-8'))
        tweet.tweet_text = str(result._text.encode('utf-8'))
        tweet.tweet_nchar = tweet.tweet_text.__len__()
        tweet.tweet_nwords = len(tweet.tweet_text.split())
        tweet.save()
        result_list.append(tweet)
        result_count+=1
        print tweet

        print "got %d results" % result_count

    return result_list


def search_tweets_week(coordx, coordy):
    latitude = replace(coordx,',','.')
    longitude = replace(coordy,',','.')

    twitterApi = Api(twitterconfig.consumer_key,twitterconfig.consumer_secret,twitterconfig.access_key, twitterconfig.access_secret)

    result_count = 0

    result_list = []


    while result_count < 7:
        if result_count != 0 :
            busca = twitterApi.GetSearch(geocode=(latitude,longitude,'1km'), count=10, until=dataPassada.date().isoformat())
        else:
            busca = twitterApi.GetSearch(geocode=(latitude,longitude,'1km'), count=10, result_type="recent")

        last_place = None

        for result in busca:
            tweet = models.Tweet()
            tweet.tweet_date = parser.parse(result._created_at)
            tweet.tweet_user = str(result._user._name.encode('utf-8'))
            if result._place:
                tweet.tweet_cidade = str(result._place['name'].encode('utf-8'))
                tweet.tweet_pais = str(result._place['country'].encode('utf-8'))
                last_place = result._place
            elif last_place:
                tweet.tweet_cidade = str(last_place['name'].encode('utf-8'))
                tweet.tweet_pais = str(last_place['country'].encode('utf-8'))

            tweet.tweet_text = str(result._text.encode('utf-8'))
            tweet.tweet_nchar = tweet.tweet_text.__len__()
            tweet.tweet_nwords = len(tweet.tweet_text.split())
            tweet.save()
            result_list.append(tweet)

            print tweet


            dataPassada = tweet.tweet_date - timedelta(days=1)

        result_count+=1

    update_report_tables()

def update_report_tables():
    update_pordata()
    update_poruser()
    update_porlocal()

def update_pordata():
    for datas in models.Tweet.objects.order_by('tweet_date').distinct('tweet_date'):
        if models.TweetsPorData.objects.filter(data=datas.tweet_date).exists():
            row = models.TweetsPorData.objects.get(data=datas.tweet_date)
        else:
            row = models.TweetsPorData(data=datas.tweet_date)

        row.nchars = 0
        row.nwords = 0
        row.ntweets = 0

        words = []
        topwrds = []

        for tweet in models.Tweet.objects.filter(tweet_date=datas.tweet_date):
            row.nchars += tweet.tweet_nchar
            row.nwords += tweet.tweet_nwords
            row.ntweets += 1
            for word in tweet.tweet_text.split():
                words.append(word)

        for wrd in Counter(words).most_common(3):
            topwrds.append(wrd[0])

        row.top3wrds = topwrds
        row.save()

    print 'fim update por data'

def update_poruser():
    datas = models.TweetsPorData.objects.all().values_list("data").distinct()
    for users in models.Tweet.objects.order_by('tweet_user').distinct('tweet_user'):
        for data in datas:
            words = []
            topwrds = []

            if models.TweetsByUser.objects.filter(user=users.tweet_user).exists():
                row = models.TweetsByUser.objects.get(user=users.tweet_user)
            else:
                row = models.TweetsByUser(user=users.tweet_user)

            row.nchars = 0
            row.nwords = 0
            row.ntweets = 0
            row.data = data[0]
            row.user = users.tweet_user

            for tweet in models.Tweet.objects.filter(tweet_user=users.tweet_user, tweet_date = data[0]):
                row.nchars += tweet.tweet_nchar
                row.nwords += tweet.tweet_nwords
                row.ntweets += 1

                for word in tweet.tweet_text.split():
                    words.append(word)

            for wrd in Counter(words).most_common(3):
                topwrds.append(wrd[0])

            row.top3wrds = topwrds
            row.save()
    print 'fim update por user'

def update_porlocal():
    for locais in models.Tweet.objects.order_by('tweet_cidade').distinct('tweet_cidade'):

        datas = models.TweetsPorData.objects.all().values_list("data").distinct()
        for data in datas:
            words = []
            topwrds = []
            if models.TweetsByLocal.objects.filter(cidade=locais.tweet_cidade).exists():
                row = models.TweetsByLocal.objects.get(cidade=locais.tweet_cidade)
            else:
                row = models.TweetsByLocal(cidade=locais.tweet_cidade)
            row.nchars = 0
            row.nwords = 0
            row.ntweets = 0
            row.data = data[0]
            row.cidade = locais.tweet_cidade

            for tweet in models.Tweet.objects.filter(tweet_cidade=locais.tweet_cidade, tweet_date=data[0]):

                row.nchars += tweet.tweet_nchar
                row.nwords += tweet.tweet_nwords
                row.ntweets += 1
                for word in tweet.tweet_text.split():
                    words.append(word)

            for wrd in Counter(words).most_common(3):
                topwrds.append(wrd[0])

            row.top3wrds = topwrds
            row.save()

    print 'fim update por local'
