# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-14 18:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_unit', '0004_businessunit_unit_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessunit',
            name='unit_code',
        ),
    ]
