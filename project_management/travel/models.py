from django.db import models
from django.contrib.auth.models import User

from project_management.fields import UUIDField
from project_management.projectbudget.models import *


class Travel(models.Model):
    '''
    Travel Request
    '''
    TWO_WHEELER = 'two_wheeler'
    FOUR_WHEELER = 'four_wheeler'

    VEHICLE_CHOICES = (
        (TWO_WHEELER, 'two_wheeler'),
        (FOUR_WHEELER, 'four_wheeler'),
    )

    id = UUIDField(primary_key=True)
    name = models.TextField()
    requested_by = models.ForeignKey(
        User, null=True, related_name='travel_requested_by')
    approved_by = models.ForeignKey(
        User, null=True, related_name='travel_approved_by')
    final_approver = models.ForeignKey(
        User, null=True, related_name='travel_final_approver')
    claim_to_date = models.DateField(blank=True, null=True)
    claim_from_date = models.DateField(blank=True, null=True)
    applied_date = models.DateField(blank=True, null=True)
    vehicle = models.CharField(max_length=120, choices=VEHICLE_CHOICES)
    status = models.ForeignKey(SaveRecordStatus,
                               blank=True, null=True)
    is_int_approved = models.BooleanField(default=False)
    is_ext_approved = models.BooleanField(default=False)
    total_km = models.IntegerField(blank=True, null=True)
    total_rs = models.IntegerField(blank=True, null=True)
    rejection_reason = models.TextField()
    modified_on = models.DateTimeField(auto_now=True)


class Expenditure(models.Model):
    '''
    Travel Expenditure details
    '''
    id = UUIDField(primary_key=True)
    travel = models.ForeignKey(Travel)
    expend_date = models.DateField(blank=True, null=True)
    client_name = models.TextField()
    destination = models.TextField()
    km = models.IntegerField(blank=True, null=True)


class ClaimAmount(models.Model):
    '''
    Define the claim amount for km
    '''
    vehicle = models.TextField()
    amount = models.IntegerField(blank=True, null=True)
