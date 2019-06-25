"""
Url pattern for projectbudgegt application
"""

# from django.conf.urls.defaults import patterns
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.conf.urls import include, url
# from project_management.projectbudget import views as projectbudget_views
from project_management.projectbudget.views import *
from project_management.projectbudget.budgetmasters import *


urlpatterns = [
    url(r'^create/$', create),
    url(r'^list/$', list),
    url(r'^save/$', save),
    url(r'^export_budget/$', export_budget),
    url(r'^phase/$', phase_list),
    url(r'^phase/delete/$', delete_phase),
    url(r'^phase/add/$', create_phase),
    url(r'^cost/$', cost_listpage),
    url(r'^cost/delete/$', delete_cost),
    url(r'^cost/add/$', add_cost),
    url(r'^cost/cancel/$', cancel),
]
