from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from project_management.customer.models import Customer
from project_management.projects.models import Project
from project_management.milestone.models import Milestone
from project_management.business_unit.models import BusinessUnit
from django.contrib.auth.models import Group, User
import datetime


class Service(models.Model):

    service_period = models.CharField(
        null=False, max_length=30, verbose_name='Service period')

    def __str__(self):
        return str(self.service_period)


class Status(models.Model):

    status = models.CharField(
        max_length=20, default=False, blank=False, null=False, verbose_name='Status')

    def __str__(self):
        return str(self.status)


class AmcReport(models.Model):
    customer_name = models.ForeignKey(
        BusinessUnit, verbose_name='Customer', null=True, blank=True, related_name="customet_name")
    project_name = models.ForeignKey(
        Project, verbose_name='Project', null=True, blank=True, related_name="solution_name")
    milestone_name = models.ForeignKey(
        Milestone, verbose_name='Milestone', null=True, blank=True, related_name="milestone_name")
    Due_date = models.DateField()
    AMC_end_date = models.DateField()
    status = models.ForeignKey(Status, verbose_name='Status')
    notification = models.DateField()
    role = models.ManyToManyField(
        Group, verbose_name='Role', null=True, blank=True)
    escalation_role = models.ForeignKey(
        Group, verbose_name='Escalation role', related_name="escalation_role", null=True)
    remarks = models.TextField(max_length=50)
    created_on = models.DateTimeField(blank=True, null=True)
    created_by = models.CharField(max_length=20, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    updated_by = models.CharField(max_length=20, null=True)

    def __str__(self):
        return str(self.customer_name)
