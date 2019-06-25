# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-01-31 13:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_userprofile_business_unit_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='type',
            field=models.CharField(blank=True, choices=[(b'E', 'Permanent'), (b'C', 'Contract'), (b'T', 'Trainee'), (b'TP', 'Temporary'), (b'A', 'Employee'), (b'IN', 'Intern'), (b'C', 'Consultant'), (b'CC', 'Customer contact')], max_length=2, null=True, verbose_name='type'),
        ),
    ]
