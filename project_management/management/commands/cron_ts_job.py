from datetime import datetime
from django.core.management.base import BaseCommand
from project_management.alert.views import *
from project_management.projectbudget.views import budget_reminder_alertmail


class Command(BaseCommand):
    def handle(self, *args, **options):
        print "Cron run at", datetime.now()
        timesheet_alert(self)
