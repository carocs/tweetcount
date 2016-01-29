# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-29 00:15
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweeter', '0006_auto_20160128_2214'),
    ]

    operations = [
        migrations.CreateModel(
            name='TweetsByLocal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cidade', models.CharField(max_length=50)),
                ('data', models.DateField(default=None)),
                ('ntweets', models.IntegerField()),
                ('nchars', models.IntegerField()),
                ('nwords', models.IntegerField()),
                ('top3wrds', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=180), size=3)),
            ],
        ),
        migrations.CreateModel(
            name='TweetsByUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('data', models.DateField(default=None)),
                ('ntweets', models.IntegerField()),
                ('nchars', models.IntegerField()),
                ('nwords', models.IntegerField()),
                ('top3wrds', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=180), size=3)),
            ],
        ),
        migrations.DeleteModel(
            name='TweetsLocal',
        ),
        migrations.DeleteModel(
            name='TweetsUser',
        ),
    ]
