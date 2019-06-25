"""
    Url for the task application
"""
from django.conf.urls.defaults import patterns

urlpatterns = patterns('project_management.tasks',
    (r'^$', 'views.manage_task'),
    (r'^save/$', 'views.manage_task'),
    (r'^(?P<tid>\d+)/$', 'views.manage_task'),
    (r'^list/$', 'views.task_list'),
    (r'^list/(?P<page>\d+)/$', 'views.task_list'),
    (r'^create_type/$', 'views.manage_type'),
    (r'^manage_type/(?P<id>\d+)/$', 'views.manage_type'),
    (r'^delete_type/(?P<id>\d+)/$', 'views.delete_task_type'),
    (r'^getsubtype/$', 'views.get_sub_type'),
    (r'^delete/$', 'views.delete_task',
        { 'is_project_task': True }, "project-task-delete"),
    (r'^nonproject/delete/$', 'views.delete_task',
        { 'is_project_task': False }, "non-project-task-delete"),
    (r'^nonproject/create/$', 'views.manage_non_project_task'),
    (r'^nonproject/update/(?P<id>\d+)/$', 'views.manage_non_project_task'),
    (r'^nonproject/list/$', 'views.non_project_task_list'),
)
