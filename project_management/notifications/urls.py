"""
    urls for event application
"""
# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
# from project_management.notifications import views as notifications_views
from project_management.notifications.views import *
from project_management.notifications.eventviews import *


urlpatterns = [
    url(r'^create/$', manage_event),
    url(r'^update/(?P<id>\d+)/$', manage_event),
    url(r'^list/$', event_list),
    url(r'^delete/$', delete_event),

]
