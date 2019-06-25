"""
    Url for business unit application
"""

from django.conf.urls import include, url
from project_management.leave.views import *


urlpatterns = [
    url(r'^create/$', manage_leave),
    url(r'^update/(?P<id>\d+)/$', manage_leave),
    url(r'^shortleave/create/$', manage_shortleave),
    url(r'^shortleave/update/(?P<id>\d+)/$', manage_shortleave),
    url(r'^list/$', leave_list),
    url(r'^holiday/$', get_holiday),
    url(r'^get_lop/$', get_lop),
    url(r'^cancel/$', cancel_leave),
    url(r'^shortleave/cancel/$', cancel_shortleave),
    url(r'^request/list/$', get_leave_approval_list),
    url(r'^(?P<id>\d+)/(?P<status>\w+)$', leave_approval_status),
    url(r'^(?P<id>\d+)/(?P<status>\w+)/list$', leave_reject_status),
    url(r'^shortleave/(?P<id>\d+)/(?P<status>\w+)$', shortleave_approval_status),
    url(r'^record/$', leave_record_list),
    url(r'^generate/$', generate_leave),
    url(r'^reports/$', get_reports),
    url(r'^short/leave/reports/$', get_short_leave_reports),
    url(r'^credit/$', leave_credit),
    url(r'^credit/update/(?P<id>\d+)/$', leave_credit),
    url(r'^credit/list/$', leave_credit_list),
    url(r'^consolidated/$', leave_consolidated),
    url(r'^reconciliation/report/$', leave_reconciliation),
    # url(r'^reconciliation/$',get_reconciliation_data),
    url(r'^previous_leave_balance/$', get_previous_leave_balance),
    url(r'^late_attendance/$',get_employees),
    url(r'^late_attendance/(?P<status>\w+)/(?P<id>\d+)$',get_employees),
    
]
