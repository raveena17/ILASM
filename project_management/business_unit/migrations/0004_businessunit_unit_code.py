# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-12-14 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business_unit', '0003_auto_20180924_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessunit',
            name='unit_code',
            field=models.CharField(default=1, max_length=120, verbose_name='UnitCode'),
            preserve_default=False,
        ),
    ]
