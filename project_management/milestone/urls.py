"""
    urls for milestone
"""
# from django.conf.urls.defaults import patterns, url
from django.conf.urls import include, url
# from project_management.milestone import views as milestone_views
from project_management.milestone.views import *


urlpatterns = [
    url(r'^$', milestone_list),
    url(r'^list/$', milestone_list),
    url(r'^list/(?P<pageNo>\d+)/$', milestone_list),
    url(r'^create/$', manage_milestone, name='create-milestone'),
    url(r'^update/(?P<id>\d+)/$', manage_milestone, name='update-milestone'),
    url(r'^delete/$', milestone_delete)
]
