# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-11 12:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AMC_Report', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amchistory',
            name='client_name',
        ),
        migrations.RemoveField(
            model_name='amchistory',
            name='project',
        ),
        migrations.RemoveField(
            model_name='reportamc1',
            name='client_name',
        ),
        migrations.RemoveField(
            model_name='reportamc1',
            name='project',
        ),
        migrations.DeleteModel(
            name='AmcHistory',
        ),
        migrations.DeleteModel(
            name='ReportAMC1',
        ),
    ]
