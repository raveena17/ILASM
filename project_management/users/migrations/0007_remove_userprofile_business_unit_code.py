# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-04 11:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userprofile_business_unit_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='business_unit_code',
        ),
    ]
