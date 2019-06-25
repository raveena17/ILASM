"""
    Timesheet urls
"""
# from django.conf.urls.defaults import patterns
from django.conf.urls import include, url
# from project_management.timesheetnew import views as timesheetnew_views
from project_management.timesheetnew.views import *


urlpatterns = [
    url(r'save/$', task_tracking),
    url(r'edit/$', edit),
    #    url(r'lookup/daywiseTasks/$', daywise_task_lookup),
    #    url(r'total/timeSpent/$', Total_Time_Spent),
    #    url(r'addtask/$', add_task_to_task_pane),
    #    url(r'gettask/$', get_task),
]
