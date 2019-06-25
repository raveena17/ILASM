"""
Url pattern for projectbudgegt application
"""

from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import include, url
from project_management.alert.views import *


urlpatterns = [

    url(r'^list/$', list),
    url(r'^edit/(?P<id>\w+\d+)/$', edit),
    url(r'^save/$', save),
    url(r'^preview/$', preview),
    url(r'^timesheet_report/$', pay_it_status),
    url(r'^sheet_report/$', sheet_report),
    url(r'^timesheet_xl/$', pay_it_status_days_genrte),
    url(r'^timesheet_hours/$', pay_it_status_hours_genrte),
    url(r'^task_report/$', task_report),
    url(r'^daily_report/$', daily_report),
    url(r'^activate/$', alert_status, {'status': True}, "activate-alert"),
    url(r'^deactivate/$', alert_status, {'status': False}, "deactivate-alert"),
    url(r'^project_report/$', project_report),
    #url(r'^get_perms/$', 'get_perms'),
]
