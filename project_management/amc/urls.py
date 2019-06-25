from django.conf.urls import url
from amc.views import manage_amc, amc_list, get_service
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^create/$', manage_amc),
    url(r'^update/(?P<id>\d+)/$', manage_amc),
    url(r'^list/$', amc_list),
    url(r'^service', get_service),
]
