"""
Url pattern for Reimbursement application
"""

# from django.conf.urls.defaults import *
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from project_management.travel import views as travel_views


uuid_regex = '[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}'

urlpatterns = [
    url(r'^create/$', 'travel_views.create', name="create"),
    url(r'^list/$', 'travel_views.list', name="list"),
    url(r'^save/$', 'travel_views.save', name="save"),
]
