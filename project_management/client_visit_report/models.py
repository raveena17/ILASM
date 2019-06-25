from __future__ import unicode_literals
from django.db import models
import datetime
from project_management.users.models import UserProfile
from project_management.business_unit.models import BusinessUnit
from django.contrib.auth import get_user_model
from django.template.loader import get_template
from emailmanager import send
from helpers import get_full_domain
from project_management.projects.models import *
from project_management.users.models import *
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from netifaces import interfaces, ifaddresses, AF_INET


def send_cvrreport_mail(sender, instance=None,
                        created=False, update_fields=None, **kwargs):
    if update_fields:
        if 'is_approved' or 'is_rejected' in update_fields:
            pass
    else:

        user = User.objects.get(username=instance.prepared_by)
        reporting_senior = User.objects.get(
            username=instance.reporting_senior_name.username)
        address = [i['addr'] for i in ifaddresses(
            'eth0').setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        #production -  address = [i['addr'] for i in ifaddresses('eth0').setdefault(AF_INET, [{'addr':'No IP addr'}] )]
        recipient, _ = get_user_model().objects.get_or_create(email=reporting_senior.email, first_name=reporting_senior.first_name,
                                                              username=reporting_senior.username)  # http://127.0.0.1:8000/cvr/edit/id_num
        sender, _ = get_user_model().objects.get_or_create(
            email=user.email, first_name=user.first_name, username=user.username)
        reporting_senior = reporting_senior.first_name+' '+reporting_senior.last_name
	subject = "Approve CVR form"
        template = get_template('cvr_approval.txt')
        text_body = template.render({
            'client_visit_report': instance,
            'recipient': recipient,
            'reporting_senior_name': reporting_senior,
            'full_domain': "http://" + address[0] + ":9073/clientvisitreports/report/" + str(instance.id) + "/",
	    'public_domain': "https://" +"mindshare.fifthgentech.com/clientvisitreports/report/" + str(instance.id) + "/",
            'request_user': instance.prepared_by
        })
        global send
        status = send(recipient, sender, subject, text_body)


class ClientVisitReport(models.Model):

    prepared_by = models.CharField(
        max_length=200,
        blank=False,
        null=False)  # foriegn key to the user
    project_name = models.ForeignKey(
        Project,
        verbose_name=('project name'),
        null=True,
        blank=True)
    client_name = models.ForeignKey(BusinessUnit,
                                    verbose_name=('Client Details'), null=True, blank=True)
    visit_location = models.CharField(max_length=200, blank=False, null=False)
    from_date = models.DateField(null=True, blank=True)
    to_date = models.DateField(null=True, blank=True)
    reason_for_visit = models.TextField(max_length=1500, blank=True, null=True)
    actions_taken_during_the_visit = models.TextField(
        max_length=1500, blank=True, null=True)
    next_plan_of_action = models.TextField(
        max_length=1500, blank=True, null=True)
    comments = models.TextField(max_length=1500, blank=True, null=True)
    reporting_senior_name = models.ForeignKey(User, blank=True, null=True)
    reason_for_reject = models.TextField(max_length=200, blank=True, null=True)
    date_of_approval = models.DateTimeField(null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)

    def __str__(self):
        return self.prepared_by

    def get_absolute_url(self):
        return reverse('cvr-detail', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'ClientVisitReport'
        verbose_name_plural = "clientvisitreports"

models.signals.post_save.connect(send_cvrreport_mail, sender=ClientVisitReport)
