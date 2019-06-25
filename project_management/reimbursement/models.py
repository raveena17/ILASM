from django.db import models
from django.contrib.auth.models import User

from project_management.fields import UUIDField
from project_management.projectbudget.models import *


class Reimbursement(models.Model):
    id = UUIDField(primary_key=True)
    name = models.TextField()
    requested_by = models.ForeignKey(
        User, related_name='requested_by', null=True)
    approved_by = models.ForeignKey(
        User, related_name='approved_by', null=True)
    final_approver = models.ForeignKey(
        User, related_name='final_approver', null=True)
    #requested_date = models.DateField(blank=True, null=True)
    applied_date = models.DateField(blank=True, null=True)
    status = models.ForeignKey(SaveRecordStatus,
                               related_name="%(app_label)s_%(class)s_Reimbursement_status", blank=True, null=True)
    is_int_approved = models.BooleanField(default=False)
    is_ext_approved = models.BooleanField(default=False)
    total_expenditure = models.FloatField(blank=True, null=True)
    rejection_reason = models.TextField()
    modified_on = models.DateTimeField(auto_now=True)


class Expenditure_Reimburs(models.Model):
    id = UUIDField(primary_key=True)
    reimbursement = models.ForeignKey(Reimbursement)
    expenditure_name = models.TextField()
    amount = models.DecimalField(max_digits=20, decimal_places=2)
