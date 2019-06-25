# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _
from project_management.customer.models import Customer
from project_management.projects.models import Project
from project_management.milestone.models import Milestone
from project_management.business_unit.models import BusinessUnit
from django.contrib.auth.models import Group, User
import datetime


class ReportAMC1(models.Model):

    id = models.AutoField(primary_key=True)

    client_name = models.ForeignKey(
        BusinessUnit, verbose_name='Client Name', null=True, blank=True, related_name="ClientName",on_delete=models.CASCADE)
    
    project = models.ForeignKey(
        Project, verbose_name='Project Name', null=True, blank=True, related_name="ProjectName",on_delete=models.CASCADE)
    
    description = models.TextField(_('Description'),max_length=200)
    
    amc_start_date = models.DateField(null=True,blank=True)

    frequency = models.IntegerField(null=True,blank=True)

    amc_end_date = models.DateField(null=True,blank=True)

    document = models.FileField(upload_to='Amc_documents/', blank=True, null=True)

    is_active = models.BooleanField(_('Is Active'),default=True)

    amc_created_date = models.DateField(null=True,blank=True)


    def __unicode__(self):
    	return str(self.project)

    class Meta:
        db_table = 'AMC'
        verbose_name_plural = "AMC Report"

    

class AmcHistory(models.Model):

    id = models.AutoField(primary_key=True)

    amc_id = models.IntegerField(null=True, blank=True)

    client_name = models.ForeignKey(
        BusinessUnit, verbose_name='AMC_Clients', null=True, blank=True, related_name="amc_client_names",on_delete=models.CASCADE)
    
    project = models.ForeignKey(
        Project, verbose_name='AMC_Project Names', null=True, blank=True,related_name="amc_project_names",on_delete=models.CASCADE)
    
    description = models.TextField(_('AMC_description'),max_length=200)

    amc_start_date = models.DateField(null=True,blank=True)

    frequency = models.CharField(_('AMC_frequency period(in Months)'),
                                        max_length=10, null=True, blank=True)

    amc_end_date = models.DateField(null=True,blank=True)

    file_document = models.FileField(upload_to='AmcHistory', blank=True, null=True)

    is_active = models.BooleanField(_('Is Active'),default=True)

    amc_renewal_date = models.DateField(null=True,blank=True)

    
    def __unicode__(self):
    	return str(self.project)

    class Meta:
        db_table = 'AMC_History'
        verbose_name_plural = "AMC Report"



     
    
     

	


