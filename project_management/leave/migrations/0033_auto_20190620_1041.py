# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-06-20 10:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('leave', '0032_auto_20190612_1758'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lateattendance',
            name='emp_name',
        ),
        migrations.DeleteModel(
            name='LateAttendance',
        ),
    ]
