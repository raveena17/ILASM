"""
    Url for business unit application
"""

from django.conf.urls import include, url
from project_management.AMC_Report.views import *


urlpatterns = [
    url(r'^create/$', manage_AMC_Report),
    url(r'^update/(?P<id>\d+)/$', update_amc),
    url(r'^list/$', AMC_Report_list),
    url(r'^renew/(?P<id>\d+)/$', renew_amc),
    url(r'^deactivate/$', manage_user_status,
        {'status': False}, "deactivate-user"),
    url(r'^activate/$', manage_user_status,
        {'status': True}, "activate-user"),

]
