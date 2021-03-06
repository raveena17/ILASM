# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2019-02-22 18:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectBillingDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.IntegerField(blank=True, null=True)),
                ('billing_category', models.CharField(blank=True, max_length=255, null=True)),
                ('planned_days', models.IntegerField(blank=True, null=True)),
                ('milestone', models.CharField(blank=True, max_length=255, null=True)),
                ('percentage', models.IntegerField(blank=True, null=True)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('to_date', models.DateField(blank=True, null=True)),
                ('category', models.CharField(blank=True, choices=[(b'Monthly', b'Monthly'), (b'Bi-Monthly', b'Bi-Monthly')], max_length=120, null=True, verbose_name='Category')),
                ('other', models.TextField(blank=True, max_length=1500, null=True)),
            ],
            options={
                'db_table': 'project_billing_details',
                'verbose_name_plural': 'Project Billing Details',
            },
        ),
        migrations.AddField(
            model_name='project',
            name='billed_type',
            field=models.CharField(blank=True, choices=[(b'UB', '----------'), (b'FP', 'Fixed Price'), (b'TM', 'Time & Management'), (b'SP', 'Support'), (b'OR', 'Other')], max_length=2, null=True, verbose_name='billed_type'),
        ),
        migrations.AddField(
            model_name='project',
            name='billing_category',
            field=models.CharField(choices=[(b'Billed', b'Billed'), (b'Unbilled', b'Unbilled')], default=1, max_length=120, verbose_name='Billing Category'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='is_rejected',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='project',
            name='unbilled_reason',
            field=models.TextField(blank=True, max_length=1500, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
