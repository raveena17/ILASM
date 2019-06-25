from django_cron import CronJobBase, Schedule
from .models import AmcReport, Project
from django.core.mail import send_mail, EmailMultiAlternatives
from django_cron import CronJobBase, Schedule
import datetime
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.response import Response
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.http import HttpResponse
import dateutil.relativedelta
from django.db.models.query import QuerySet

today = datetime.date.today()



class SendMail(CronJobBase):

    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    print "compiling......"
    code = 'amc.my_cron_job'

    def do(self):

        for amc in AmcReport.objects.all():
            date = amc.Due_date - dateutil.relativedelta.relativedelta(days=1)
            if amc.notification == today:
                user, role_mail_list, escalation_role_mail_list, project = get_mail(
                    amc)
                escalation_role_mail_list.append(str(user.email))
                if today == date:
                    send_mail(role_mail_list,
                              escalation_role_mail_list, project, amc)
                else:
                    send_mail(role_mail_list, [str(user.email)], project, amc)
            elif amc.Due_date > today and amc.notification < today:
                user, role_mail_list, escalation_role_mail_list, project = get_mail(
                    amc)
                escalation_role_mail_list.append(str(user.email))
                if today == date:
                    send_mail(role_mail_list,
                              escalation_role_mail_list, project, amc)
                else:
                    send_mail(role_mail_list, [str(user.email)], project, amc)


def get_mail(amc):

    for project in Project.objects.all():
        if project == amc.project_name:
            amc_project = project
            user = User.objects.get(username=project.owner)
    role_mail_list, escalation_role_mail_list = get_role_mail(amc)
    return user, role_mail_list, escalation_role_mail_list, amc_project


def get_role_mail(amc):

    role_mail_list = []
    escalation_role_mail_list = []
    for role in amc.role.all():
        users = User.objects.filter(groups=role)
        if users:
            for user in users:
                role_mail_list.append(str(user.email))
    users = User.objects.filter(groups=amc.escalation_role)
    if users:
        for user in users:
            escalation_role_mail_list.append(str(user.email))
    return role_mail_list, escalation_role_mail_list


def send_mail(role_mail_list, toaddr, project, amc):

    if amc.status != "Completed" and amc.status != "Initiated":
        days = amc.Due_date - today
        if str(days) != '0:00:00':
            days = amc.Due_date - amc.notification
            msg = EmailMultiAlternatives(
                subject='AMC',
                to=toaddr,
                bcc=role_mail_list,
                body='Hello {project_manager},\n\nThe AMC for the {project_name} is due on {due_date} {days} remaining.\n\nPlease initiate the process within {due_date}.\n\nBest Regards,\n\nAdmin'.format(
                    project_manager=project.owner, project_name=project.name, due_date=amc.Due_date, days=str(days).split(',')[0])
            )
            msg.send()
        else:
            msg = EmailMultiAlternatives(
                subject='AMC',
                to=toaddr,
                bcc=role_mail_list,
                body='Hello {project_manager},\n\nThe AMC for the {project_name} is due on today.\n\nPlease initiate the process within {due_date}.\n\nBest Regards,\n\nAdmin'.format(
                    project_manager=project.owner, project_name=project.name, due_date=amc.Due_date)
            )
            msg.send()
