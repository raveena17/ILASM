# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-09-24 18:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('business_unit', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Requestt',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_date', models.DateField(blank=True, null=True)),
                ('leave_from', models.DateField(blank=True, null=True)),
                ('leave_to', models.DateField(blank=True, null=True)),
                ('no_of_days', models.IntegerField()),
                ('leave_reason', models.TextField(blank=True, max_length=200, null=True)),
                ('approval_status', models.CharField(max_length=200)),
                ('reject_reason', models.TextField(blank=True, max_length=200, null=True)),
                ('lop', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('approved_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_unit_requestt_approved_byy', to=settings.AUTH_USER_MODEL, verbose_name=b'approved_byy')),
                ('empid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_unit_requestt_userr', to=settings.AUTH_USER_MODEL, verbose_name=b'userr')),
            ],
            options={
                'db_table': 'leave_requests_s',
            },
        ),
        migrations.CreateModel(
            name='Statuss',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_leave', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('balance_leave', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'db_table': 'leave_statuses_s',
            },
        ),
        migrations.CreateModel(
            name='Typee',
            fields=[
                ('leave_id', models.AutoField(primary_key=True, serialize=False)),
                ('leave_type', models.CharField(max_length=200)),
                ('no_of_days', models.IntegerField()),
                ('current_year', models.IntegerField()),
                ('leave_status', models.CharField(max_length=200)),
                ('organization', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'leave_types_s',
            },
        ),
        migrations.AddField(
            model_name='statuss',
            name='cur_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_unit_statuss_current_year', to='business_unit.Typee', verbose_name=b'current_year'),
        ),
        migrations.AddField(
            model_name='statuss',
            name='empid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_unit_statuss_empid', to='business_unit.Requestt', verbose_name=b'empid'),
        ),
        migrations.AddField(
            model_name='statuss',
            name='leave_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_unit_statuss_leave_id', to='business_unit.Typee', verbose_name=b'leave_id'),
        ),
        migrations.AddField(
            model_name='requestt',
            name='leave_nature',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='business_unit.Typee'),
        ),
    ]
