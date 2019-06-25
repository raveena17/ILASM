"""
    cron that send email for approval of the project
"""
from django_cron import cronScheduler, Job
from project_management.Utility import Email
from project_management.projects.models import Project

import datetime

CONTENT_TYPE = 'html'

class ProjectMail(Job):
    """
        Cron Job that checks the lgr users mailbox and adds any approved senders' attachments to the db
    """

    # run every 43200 seconds (12 minutes)
    run_every = 43200

    def job(self):
        # This will be executed every 1 minutes
        programs = Project.objects.filter(approvalDate = (datetime.date.today()))
        owner_email = [ each for each in programs ]
        email_subject = 'approval mail'
        emailMessage = 'Today is the project approval due date for ' + str(each.name) + '.'
        for each in owner_email :
            message = emailMessage
            try:
                Email().send_email(email_subject, message,
                    [each.apexBodyOwner.userProfile.authUser.email],
                    CONTENT_TYPE)
            except Exception, e :
                errMessage = 'Email Sending failed \n %s' % (Exception)
        allprograms = Project.objects.filter(nextInvoiceDate = (datetime.date.today()))
        invoice_email = [ each for each in allprograms ]
        invoice_subject = 'invoice mail'
        invoicemail = 'Invoice date due for ' + str(each.name) + '.'
        for eachProgram in invoice_email:
            message = invoicemail
            try:
                Email().send_email(invoice_subject, message,
                    [each.apexBodyOwner.userProfile.authUser.email],
                    CONTENT_TYPE)
            except Exception, e :
                errMessage = 'Email Sending failed \n %s' % (Exception)

cronScheduler.register(ProjectMail)
