# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-19 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_userprofile_business_unit_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='business_unit_id',
        ),
    ]
