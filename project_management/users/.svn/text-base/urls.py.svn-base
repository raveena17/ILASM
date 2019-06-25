"""
    urls required the user application.
"""

from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('project_management.users',
    (r'^create/$', 'views.manage_user'),
    (r'^update/(?P<pid>\d+)/$', 'views.manage_user'),
    (r'^list/$', 'views.user_list'),
    (r'^deactivate/$', 'views.manage_user_status',
                {'status': False}, "deactivate-user"),
    (r'^activate/$', 'views.manage_user_status',
                {'status': True}, "activate-user"),
    (r'^myprofile/$', 'views.manage_myprofile'),
    
)
