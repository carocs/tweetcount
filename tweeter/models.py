from __future__ import unicode_literals

from django.db import models

from django.contrib.postgres import fields

# Create your models here.
class Tweet(models.Model):
    tweet_date = models.DateField('data de publicacao')
    tweet_user = models.CharField(max_length=50)
    tweet_cidade = models.CharField(max_length=50)
    tweet_pais = models.CharField(max_length=50)
    tweet_nchar = models.IntegerField(default=0)
    tweet_nwords = models.IntegerField(default=0)
    tweet_text = models.CharField(max_length=150, default='')

class TweetText(models.Model):
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    tweet_text = models.CharField(max_length=150)

class TweetsPorData(models.Model):
    data = models.DateField()
    ntweets = models.IntegerField()
    nchars = models.IntegerField()
    nwords = models.IntegerField()
    top3wrds = fields.ArrayField(models.CharField(max_length=180),size=3)

    def __str__(self):
        return self.data

class TweetsByUser(models.Model):
    user = models.CharField(max_length=50)
    data = models.DateField(default=None)
    ntweets = models.IntegerField()
    nchars = models.IntegerField()
    nwords = models.IntegerField()
    top3wrds = fields.ArrayField(models.CharField(max_length=180),size=3)

    def __str__(self):
        return self.user

class TweetsByLocal(models.Model):
    cidade = models.CharField(max_length=50)
    data = models.DateField(default=None)
    ntweets = models.IntegerField()
    nchars = models.IntegerField()
    nwords = models.IntegerField()
    top3wrds = fields.ArrayField(models.CharField(max_length=180),size=3)

    def __str__(self):
        return self.cidade