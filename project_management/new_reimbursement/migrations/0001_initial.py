# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2018-11-22 17:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Allowance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('expenditure', models.DecimalField(decimal_places=2, max_digits=20)),
                ('bill_availability', models.BooleanField(verbose_name='Bills')),
                ('bill_checking', models.BooleanField()),
                ('bill_location', models.FileField(blank=True, null=True, upload_to='reimbursement_bills')),
            ],
            options={
                'db_table': 'new_reimbursement_allowance',
                'verbose_name_plural': 'Allowance',
            },
        ),
        migrations.CreateModel(
            name='BudgetType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=20)),
            ],
            options={
                'db_table': 'new_reimbursement_budgettype',
                'verbose_name_plural': 'BudgetType',
            },
        ),
        migrations.CreateModel(
            name='Reimbursement_new',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('created_on', models.DateField()),
                ('client_visit_report', models.CharField(max_length=100)),
                ('details', jsonfield.fields.JSONField()),
                ('special_approval', models.BooleanField()),
                ('notes', models.TextField()),
                ('approver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reporting_senior', to=settings.AUTH_USER_MODEL)),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'new_reimbursement__new',
                'verbose_name_plural': 'Reimbursement_new',
            },
        ),
        migrations.CreateModel(
            name='ReimbursementStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'new_reimbursement__status',
                'verbose_name_plural': 'ReimbursementStatus',
            },
        ),
        migrations.CreateModel(
            name='ReimbursementType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'new_reimbursement__type',
                'verbose_name_plural': 'ReimbursementType',
            },
        ),
        migrations.AddField(
            model_name='reimbursement_new',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_reimbursement.ReimbursementStatus'),
        ),
        migrations.AddField(
            model_name='reimbursement_new',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_reimbursement.ReimbursementType'),
        ),
        migrations.AddField(
            model_name='allowance',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_reimbursement.BudgetType'),
        ),
        migrations.AddField(
            model_name='allowance',
            name='reimbursement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='new_reimbursement.Reimbursement_new'),
        ),
    ]
