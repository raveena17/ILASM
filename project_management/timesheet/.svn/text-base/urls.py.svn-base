"""
    Timesheet urls
"""
from django.conf.urls.defaults import patterns

urlpatterns = patterns('project_management.timesheet.views',
    (r'^$', 'task_tracking'),
    (r'lookup/$', 'task_lookup'),
    (r'lookup/daywiseTasks/$', 'daywise_task_lookup'),
    (r'total/timeSpent/$', 'total_time_spent'),
    (r'addtask/$', 'add_task_to_task_pane'),
    (r'gettask/$', 'get_tasks_for_project'),
)
