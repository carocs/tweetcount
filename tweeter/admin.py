from django.contrib import admin

from .models import Tweet,TweetText

# Register your models here.
admin.site.register(Tweet)
admin.site.register(TweetText)