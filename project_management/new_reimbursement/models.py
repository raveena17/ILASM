# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
# from project_management.client_visit_report.models import *
# from project_management.client_visit_report.models import ClientVisitReport
import client_visit_report

# Create your models here.

class BudgetType(models.Model):

    type = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
		return str(self.type)


    class Meta:
        db_table = 'new_reimbursement_budgettype'
        verbose_name_plural = "BudgetType"


class ReimbursementType(models.Model):

	type = models.CharField(max_length=100)

	def __str__(self):
		return str(self.type)

	class Meta:
		db_table = 'new_reimbursement__type'
		verbose_name_plural = "ReimbursementType"


class ReimbursementStatus(models.Model):

	status = models.CharField(max_length=100)

	def __str__(self):
		return str(self.status)

	class Meta:
		db_table = 'new_reimbursement__status'
		verbose_name_plural = "ReimbursementStatus"

class Reimbursement_new(models.Model):

	name = models.ForeignKey(User, related_name='user')
	approver = models.ForeignKey(User, related_name='reporting_senior')
	type = models.ForeignKey(ReimbursementType)
	total_amount = models.DecimalField(max_digits=20, decimal_places=2)
	status = models.ForeignKey(ReimbursementStatus)
	created_on = models.DateField()
	client_visit_report = models.CharField(max_length=100)
	details = JSONField()
	special_approval = models.BooleanField()
	# client_visit_report = models.ForeignKey(client_visit_report.models.ClientVisitReport, null=True, on_delete=models.CASCADE)
	# bill_location = models.FileField(upload_to='reimbursement_bills', null=True, blank=True)
	notes = models.TextField()
	approved_on = models.DateField(blank=True, null=True)
	processed_on = models.DateField(blank=True, null=True)

	def __str__(self):
		return str(self.name)

	class Meta:
		db_table = 'new_reimbursement__new'
		verbose_name_plural = "Reimbursement_new"

class Allowance(models.Model):
 
	reimbursement = models.ForeignKey(Reimbursement_new)
	date = models.DateField()
	category = models.ForeignKey(BudgetType)
	description = models.TextField()
	expenditure = models.DecimalField(max_digits=20, decimal_places=2)
	bill_availability = models.BooleanField(blank=True, verbose_name='Bills')
	bill_checking =  models.BooleanField(blank=True)
	bill_location = models.FileField(upload_to='reimbursement_bills', null=True, blank=True)
	
	# notes = models.TextField()

	def __str__(self):
		return str(self.reimbursement)

	class Meta:
		db_table = 'new_reimbursement_allowance'
		verbose_name_plural = "Allowance"

# # class Travel(models.Model):
# # 	form = models.ForeignKey(Allowance)
# # 	start = models.CharField(max_length=100)
# # 	end = models.CharField(max_length=100)
# # 	distance = models.DecimalField(max_digits=20, decimal_places=2)