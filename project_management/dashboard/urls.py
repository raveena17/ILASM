"""
    Url for dasboard application
"""

# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
from project_management.dashboard.views import *


urlpatterns = [
    url(r'^$', manage_dashboard),
    url(r'^(?P<id>\d+)/$', manage_dashboard),
    url(r'^charts/$', manage_charts),
    
]
