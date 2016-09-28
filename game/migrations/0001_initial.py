# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 04:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Guard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('number', models.CharField(max_length=20)),
                ('address', models.CharField(max_length=120)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='HouseList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=120)),
                ('status', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=250)),
                ('refinedDetail', models.CharField(max_length=250)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]