"""
    urls for the project application
"""
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django.views.generic.list import ListView
from project_management.projects.views import *
from . import views


urlpatterns = [
    url(r'^initiation/$', project_initiation),
    url(r'^list/$', project_list),
    url(r'^list/(?P<page>\d+)/$', project_list),
    url(r'^delete/$', ProgramDelete),
    url(r'^group/$', manage_project_group),
    url(r'^group/(?P<id>\d+)/$', manage_project_group),
    url(r'^request/$', manage_project_initiation_request),
    url(r'^request/(?P<id>\d+)/$', manage_project_initiation_request),
    url(r'^requestlist/$', project_request_list),
    url(r'^update/$', EditProgramDisplayList),
    url(r'^printdetails/(?P<id>\d+)/$', print_project_details),
    url(r'^billing_details/(?P<id>\d+)/$', print_project_billind_details),
    url(r'^plan/$', project_plan),
    url(r'^getclients/$', get_clients),
    url(r'^dev_env/$', manage_development_environment),
    url(r'^dev_env_delete/$', delete_development_environment),
    url(r'^dev_env/(?P<id>\d+)/$', manage_development_environment),
    url(r'^domain/$', manage_domain),
    url(r'^domain/(?P<id>\d+)/$', manage_domain),
    url(r'^project_type/$', manage_project_type),
    url(r'^project_type/(?P<id>\d+)/$', manage_project_type),
    url(r'^business_unit/$', manage_business_unit),
    url(r'^home/', display_project_dashboard),
    url(r'^deactivate/$', manage_project_status,
        {'is_active': False}, "deactivate-project"),
    url(r'^activate/$', manage_project_status,
        {'is_active': True}, "activate-project"),
    url(r'^deleted/$', project_delete),


    #url(r'^group/create/$', 'projects_views.manage_project_group'),
    #url(r'^group/update/$', 'projects_views.manage_project_group'),
    #url(r'^group/list/$', 'projects_views.project_group_list'),
    #url(r'^group/list/(?P<page>\d+)/$', 'projects_views.project_group_list'),
]
