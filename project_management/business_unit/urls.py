"""
    Url for business unit application
"""

# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
# from project_management.business_unit import views as business_unit_views
from project_management.business_unit.views import *


urlpatterns = [
    url(r'^create/$', manage_business_unit),
    url(r'^update/(?P<id>\d+)/$', manage_business_unit),
    url(r'^list/$', business_unit_list),
    url(r'^delete/$', delete_business_unit),
]
