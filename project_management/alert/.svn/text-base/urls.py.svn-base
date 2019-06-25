"""
Url pattern for projectbudgegt application
"""

from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('project_management.alert.views',   
    (r'^list/$', 'list'),
    (r'^edit/(?P<id>\w+\d+)/$', 'edit'),
    (r'^save/$', 'save'),
    (r'^preview/$', 'preview'),
    (r'^payitstatus/$', 'pay_it_status'),
    (r'^payitstatus_xl/$', 'pay_it_status_days_genrte'),
    #(r'^payitstatus_hours/$', 'pay_it_status_hours_genrte'),
    (r'^activate/$', 'alert_status',{'status': True}, "activate-alert"),
    (r'^deactivate/$', 'alert_status',{'status': False}, "deactivate-alert")
)
