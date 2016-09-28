# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 10:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('title', models.CharField(blank=True, max_length=20)),
                ('countHouse', models.IntegerField(default=0)),
            ],
        ),
    ]