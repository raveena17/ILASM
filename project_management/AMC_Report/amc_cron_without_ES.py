from django_cron import CronJobBase, Schedule
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from project_management.users.models import UserProfile, userType
from project_management.users.forms import UserProfileForm, UserForm, MyProfileForm
from django.utils import timezone
from django.core.mail import EmailMessage, EmailMultiAlternatives
import dateutil.relativedelta
import settings
import datetime
from django.template.loader import get_template
from django.template import Context
from collections import defaultdict
import calendar
from project_management.AMC_Report.models import *



# Run Cron: 
# python manage.py runcrons “users.cron.classname”
# EX - python manage.py runcrons AMC_Report.amc_cron.SendAlertMail


Reminder = "This is to bring to your notice that AMC renewel for the below client is due."

REMINDER_DAYS = settings.AMC_REMINDER_DAYS_LIST
TO_EMAIL_LIST = settings.AMC_CRON_REMINDER_MAIL_LIST
CC_EMAIL_LIST = settings.AMC_ADDITIONAL_EMAIL_LIST


class SendAlertMail(CronJobBase):

    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    print "Compiling...... \n\nAMC Cronjob running sucessfully"
    code = 'amc.my_cron_job'

    def do(self):
        today = datetime.date.today()
        for reminder_day in REMINDER_DAYS:
            max_date = (today +dateutil.relativedelta.relativedelta(
                        days=reminder_day)).strftime('%Y-%m-%d')
            amc_list = ReportAMC1.objects.filter(amc_end_date=max_date, is_active=True)
            month = ''
            if len(amc_list) != 0:
                amc_data = self.get_amc_list_data(amc_list)
                self.make_amc_mail_content(amc_data,reminder_day)


    def get_amc_list_data(self,amc_list):
        amc_data_list = []
        amc_dict = {}
        for amc_details in amc_list:
            amc_dict = {
                'project_name' : amc_details.project.name,
                'client_name' : amc_details.client_name.name,
                'start_date' : (amc_details.amc_start_date).strftime('%d-%B-%y'),
                'end_date' : (amc_details.amc_end_date).strftime('%d-%B-%y')
            }
            amc_data_list.append(amc_dict)
        return amc_data_list

    def make_amc_mail_content(self, amc_data,reminder_day):
        now = datetime.datetime.now()
        template_name = 'amc_reminder.html'
        key_name = 'Admin'
        to_mailid_list = TO_EMAIL_LIST
        mailid = CC_EMAIL_LIST

        if len(amc_data) != 0:
            today = datetime.date.today()

            if reminder_day:
                subject = "[Reminder] AMC  Renewal before " + str(reminder_day) + " days"
                content_body = Reminder
    
            amc_html_content = self.make_html_content(
                template_name, {'body': content_body,'month': reminder_day, 'amc_data': amc_data, 'now': now,'reporting_senior': key_name})
            message = self.send_amc_mail_for_alert(
                amc_html_content, subject,to_mailid_list, mailid)


    def make_html_content(self, template_name, context):
        template = get_template(template_name)
        html_content = template.render(context)
        return html_content


    def send_amc_mail_for_alert(self, amc_html_content, subject,to_mailid_list, mailid):
        subject = subject
        from_email = settings.EMAIL_HOST_USER
        to = to_mailid_list
        print mailid
        if mailid == '': 
            msg = EmailMultiAlternatives(subject, amc_html_content, from_email, to)
        else:
            msg = EmailMultiAlternatives(
                subject, amc_html_content, from_email, to, cc=mailid)


        msg.attach_alternative(amc_html_content, "text/html")
        status = msg.send()
        return status
        







    