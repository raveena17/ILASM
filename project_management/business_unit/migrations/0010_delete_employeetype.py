# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-31 13:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('business_unit', '0009_employeetype'),
    ]

    operations = [
        migrations.DeleteModel(
            name='EmployeeType',
        ),
    ]
