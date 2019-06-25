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


REMAINDER_FOR_ROLES = settings.EMPLOYEE_STATUS_REMAINDER_FOR_ROLES
REMAINDER_FOR_USERS = settings.EMPLOYEE_STATUS_REMAINDER_FOR_USERS
DAY = settings.ESCALATION_ALERT_FOR_EMPLOYEMENT_STATUS_CHANGE
REMINDER_DAYS = settings.EMPLOYEMENT_STATUS_CHANGE_REMINDER_DAYS_LIST

""" Mail content """
Reminder = "This is to bring to your notice that the employment-status of the following person(s) \
will be due for change and you are requested to plan accordingly."
MonthEndReminder = "This is to bring to your notice that the employment-status of the following person(s) \
will be due for change in the next month"
MonthEndReminder_Continious = "and you are requested to plan accordingly."
EscalationReminder = "This is to bring to your notice that due date for employement status change has been crossed."


class SendAlertMail(CronJobBase):

    RUN_EVERY_MINS = 1
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    print "Compiling...... \n\nCronjob running sucessfully"
    code = 'users.my_cron_job'

    def do(self):
        today = datetime.date.today()
        for reminder_day in REMINDER_DAYS:
            max_date = (today +dateutil.relativedelta.relativedelta(
                        days=reminder_day)).strftime('%m-%d-%Y')
            user_list = UserProfile.objects.filter(
                probation_end_date=max_date, user__is_active=True).exclude(reporting_senior_name_id__isnull=True)
            content_body = Reminder
            month = ''
            if len(user_list) != 0:
                value = self.get_userlist_based_on_reportingsenior(user_list)
                self.get_user_data_process(value, content_body, reminder_day, month)

        """Get emp list based on 'probhation end date <= today' & send alert notification for every 'monday'"""
        if today.strftime("%A") == DAY:
            emp_list = UserProfile.objects.raw(
                'select * from (SELECT userprofile.id,userprofile.confirmation_status,userprofile.date_of_joining,userprofile.probation_period,DATE_ADD(userprofile.date_of_joining,INTERVAL CONVERT(userprofile.probation_period, SIGNED INTEGER)MONTH) end_date FROM users_userprofile userprofile) as filterd_profile where filterd_profile.probation_period is not null AND filterd_profile.probation_period <> "" AND filterd_profile.date_of_joining is not null AND(filterd_profile.confirmation_status)="ONPROBATION" AND filterd_profile.confirmation_status is not null AND DATE(filterd_profile.end_date)<= now()')
            employee_list = []
            for user in emp_list:
                if user.user.is_active == True:
                    employee_list.append(user)
            if len(employee_list) != 0:
                value = self.get_userlist_based_on_reportingsenior(
                    employee_list)
                content_body = EscalationReminder
                month = ''
                reminder_day = ''
                self.get_user_data_process(value, content_body, reminder_day, month)

        """ Get current month end date"""
        month_end_range = calendar.monthrange(today.year, today.month)
        current_month_end = datetime.date(
            today.year, today.month, month_end_range[1])
        month_end_format = current_month_end.strftime('%m-%d-%Y')

        """ Get next month start date and month end """
        start_date = current_month_end + \
            dateutil.relativedelta.relativedelta(days=1)
        next_month_start = start_date.strftime('%Y-%m-%d')
        month = start_date.strftime('%B')
        end_date_range = calendar.monthrange(start_date.year, start_date.month)
        next_month_end = datetime.date(
            start_date.year, start_date.month, end_date_range[1]).strftime('%Y-%m-%d')

        if month_end_format == today.strftime('%m-%d-%Y'):
            result_set = UserProfile.objects.raw(
                'select * from (SELECT userprofile.id,userprofile.date_of_joining,userprofile.probation_period,DATE_ADD(userprofile.date_of_joining,INTERVAL CONVERT(userprofile.probation_period, SIGNED INTEGER)MONTH) end_date FROM users_userprofile userprofile) as filterd_profile where filterd_profile.probation_period is not null AND filterd_profile.probation_period <> "" AND filterd_profile.date_of_joining is not null AND DATE(filterd_profile.end_date) BETWEEN "%s" AND "%s"' % (next_month_start, next_month_end))
            user_list = []
            for user in result_set:
                if user.user.is_active == True:
                    user_list.append(user)
            if len(user_list) != 0:
                value = self.get_userlist_based_on_reportingsenior(user_list)
                content_body = MonthEndReminder + \
                    '(' + month + ') ' + MonthEndReminder_Continious
                reminder_day = ''
                self.get_user_data_process(value, content_body, reminder_day, month)

    def get_userlist_based_on_reportingsenior(self, user_list):
        adict = {}
        for user in user_list:
            reporting_senior_name = user.reporting_senior_name
            if reporting_senior_name is not None:
                """ A dictionary that maps each key to multiple values """
                adict.setdefault(reporting_senior_name, []).append(user)
        return adict

    def get_user_data_process(self, adict, content_body, reminder_day, month):
        record = []
        for key in adict.keys():
            reporting_senior_roles = self.get_key_role(key)
            mailid = key.email
            value_list = adict[key]
            key_name = key.first_name
            datas = []
            for value in value_list:
                probation_end_date = value.probation_end_date
                if probation_end_date != "":
                    if probation_end_date is not None:
                        enddate_format = datetime.datetime.strptime(
                            str(probation_end_date), '%m-%d-%Y').strftime("%d-%B-%Y")
                        dict_value = {
                            'code': value.code,
                            'type': value.type,
                            'firstname': value.user.first_name,
                            'lastname': value.user.last_name,
                            'joining': (value.date_of_joining).strftime("%d-%B-%Y"),
                            'status': value.confirmation_status,
                            'probation_end_date': enddate_format}
                        datas.append(dict_value)
                        record.append(dict_value)
                        mailid_list = self.get_role_mailid_list()

            if settings.EMPLOYEE_STATUS_REMAINDER_FOR_REPORTING_SENIOR == True:
                self.make_mail_content(content_body, str(reminder_day), month, datas, key_name, mailid_list, mailid,
                                       reporting_senior_roles)
        key_name = 'Admin'
        mailid = ''
        if REMAINDER_FOR_ROLES != '' or REMAINDER_FOR_USERS != '':
            role_mailid = self.get_role_mailid_list()
            user_mailid = REMAINDER_FOR_USERS
            mailid_list = role_mailid + user_mailid
            self.make_mail_content(content_body, str(reminder_day), month, record, key_name, mailid_list, mailid,
                                   reporting_senior_roles)

    def get_key_role(self, key):
        if not isinstance(key, str):
            role_id = key.id
            roles = User.objects.get(id=role_id).groups.all()
            role_list = []
            for role in roles:
                role_list.append(role.name)
            return role_list
        else:
            key_name = 'Admin'

    def get_role_mailid_list(self):
        """Get Mail-Id List for settings.REMAINDER_FOR_ROLES """
        role_mailid_list = []
        for role in REMAINDER_FOR_ROLES:
            users = User.objects.filter(
                groups__name=role, is_active=1)
            for user in users:
                email = user.email
                role_mailid_list.append(email)
        return role_mailid_list

    def make_mail_content(self, content_body, reminder_day, month, datas, key_name, role_mailid_list,
                          mailid='', role_list=''):
        now = datetime.datetime.now()
        template_name = 'user_reminder.html'
        if len(datas) != 0:
            """Sort a list of dictionaries by values of the dictionary"""
            datas = sorted(datas, key=lambda k: k['type'], reverse=True)
            today = datetime.date.today()

            if content_body == EscalationReminder:
                subject = "[Alert] Escalation for employment status change"
            if content_body == Reminder:
                subject = "[Reminder] Employment-status change due in " + reminder_day + " days"
            if reminder_day == '1' and content_body == Reminder:
                subject = "[Reminder] Employment-status change due on Tomorrow"
            if month != '':
                subject = "[Reminder] Employment-status change due on next month(" + month +")"
    
            make_html_content = self.make_html_content(
                template_name, {'body': content_body,'month': month, 'datas': datas, 'reporting_senior': key_name, 'now': now})
            message = self.send_mail_for_alert(
                make_html_content, subject, role_mailid_list, [mailid], role_list)

    def make_html_content(self, template_name, context):
        template = get_template(template_name)
        html_content = template.render(context)
        return html_content

    def send_mail_for_alert(self, html_content, subject,
                            role_mailid_list, mailid, role_list):
        subject = subject
        from_email = settings.EMAIL_HOST_USER
        if mailid == ['']:
            to = role_mailid_list
            msg = EmailMultiAlternatives(subject, html_content, from_email, to)
        else:
            to = mailid
            if REMAINDER_FOR_ROLES in role_list:
                msg = EmailMultiAlternatives(
                    subject, html_content, from_email, to)
            else:
                """ Include (CC = REMAINDER_FOR_USERS) for employee status remainder to reporting senior """
                msg = EmailMultiAlternatives(
                    subject, html_content, from_email, to, cc=REMAINDER_FOR_USERS)

                """ Include (CC = REMAINDER_FOR_ROLES or role_mailid_list) for employee status remainder to reporting senior
                msg = EmailMultiAlternatives(
                    subject, html_content, from_email, to, cc=role_mailid_list)"""

        msg.attach_alternative(html_content, "text/html")
        status = msg.send()
        return status
