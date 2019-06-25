# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-11-05 12:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0015_auto_20181105_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leavecredit',
            name='leave_id',
            field=models.ForeignKey(db_column='leave_id', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leave_leavecredit_leave_type', to='leave.Type', verbose_name='leave_type'),
        ),
    ]
