"""
Url pattern for projectbudgegt application
"""

# from django.conf.urls.defaults import patterns
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import include, url


urlpatterns = ['project_management.alert.views',   
    url(r'^list/$', 'list'),
    url(r'^edit/(?P<id>\w+\d+)/$', 'edit'),
    url(r'^save/$', 'save'),
    url(r'^preview/$', 'preview'),
    url(r'^payitstatus/$', 'pay_it_status'),
    url(r'^payitstatus_xl/$', 'pay_it_status_days_genrte'),
    url(r'^payitstatus_hours/$', 'pay_it_status_hours_genrte'),
    url(r'^activate/$', 'alert_status',{'status': True}, "activate-alert"),
    url(r'^deactivate/$', 'alert_status',{'status': False}, "deactivate-alert")
    #url(r'^get_perms/$', 'get_perms'),
]
