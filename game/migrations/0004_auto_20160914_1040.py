# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-14 10:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='User',
            new_name='UserInfo',
        ),
    ]
