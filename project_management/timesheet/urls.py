"""
    Timesheet urls
"""
# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
# from project_management.timesheet import views as timesheet_views
from project_management.timesheet.views import *


urlpatterns = [
    url(r'^$', task_tracking),
    url(r'lookup/$', task_lookup),
    url(r'lookup/daywiseTasks/$', daywise_task_lookup),
    url(r'total/timeSpent/$', total_time_spent),
    url(r'addtask/$', add_task_to_task_pane),
    url(r'gettask/$', get_tasks_for_project),
]
