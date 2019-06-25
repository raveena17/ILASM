"""
    urls for the project application
"""
from django.conf.urls.defaults import patterns
from django.views.generic.simple import direct_to_template, redirect_to

urlpatterns = patterns('project_management.projects',
    (r'^initiation/$', 'views.project_initiation'),
    (r'^list/$', 'views.project_list'),
    (r'^list/(?P<page>\d+)/$', 'views.project_list'),
    (r'^delete/$', 'views.ProgramDelete'),
    (r'^group/$', 'views.manage_project_group'),
    (r'^group/(?P<id>\d+)/$', 'views.manage_project_group'),
    (r'^request/$', 'views.manage_project_initiation_request'),
    (r'^request/(?P<id>\d+)/$', 'views.manage_project_initiation_request'),
    (r'^requestlist/$',  'views.project_request_list'),
    #(r'^group/create/$', 'views.manage_project_group'),
    #(r'^group/update/$', 'views.manage_project_group'),
    #(r'^group/list/$', 'views.project_group_list'),
    #(r'^group/list/(?P<page>\d+)/$', 'views.project_group_list'),
    (r'^update/$', 'views.EditProgramDisplayList'),
    (r'^printdetails/(?P<id>\d+)/$', 'views.print_project_details'),
    (r'^plan/$',  'views.project_plan'),
    (r'^getclients/$',  'views.get_clients'),
    (r'^dev_env/$','views.manage_development_environment'),
    (r'^dev_env_delete/$','views.delete_development_environment'),
    (r'^dev_env/(?P<id>\d+)/$', 'views.manage_development_environment'),
    (r'^domain/$', 'views.manage_domain'),
    (r'^domain/(?P<id>\d+)/$', 'views.manage_domain'),
    (r'^project_type/$', 'views.manage_project_type'),
    (r'^project_type/(?P<id>\d+)/$', 'views.manage_project_type'),
    (r'^business_unit/$', 'views.manage_business_unit'),
    (r'^home/', 'views.display_project_dashboard'),
    (r'^deactivate/$', 'views.manage_project_status',
                {'is_active': False}, "deactivate-project"),
    (r'^activate/$', 'views.manage_project_status',
                {'is_active': True}, "activate-project"),
)

