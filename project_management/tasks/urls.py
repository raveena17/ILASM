"""
    Url for the task application
"""
# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
from project_management.tasks import views as tasks_views
from project_management.tasks.views import *


urlpatterns = [
    url(r'^$', manage_task),
    url(r'^save/$', manage_task),
    url(r'^(?P<tid>\d+)/$', manage_task),
    url(r'^list/$', task_list),
    url(r'^list/(?P<page>\d+)/$', task_list),
    url(r'^create_type/$', manage_type),
    url(r'^manage_type/(?P<id>\d+)/$', manage_type),
    url(r'^delete_type/(?P<id>\d+)/$', delete_task_type),
    url(r'^getsubtype/$', get_sub_type),
    url(r'^delete/$', delete_task,
        {'is_project_task': True}, "project-task-delete"),
    url(r'^nonproject/delete/$', delete_task,
        {'is_project_task': False}, "non-project-task-delete"),

    url(r'^nonproject/create/$', manage_non_project_task),

    url(r'^nonproject/update/(?P<id>\d+)/$', manage_non_project_task),
    url(r'^nonproject/list/$',
        non_project_task_list,
        name='non_project_task_list'),
]
