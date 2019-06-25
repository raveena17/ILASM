"""
    Task by Admin
"""
from django.contrib import admin

from project_management.tasks.models import Type, Task, SubType

class TaskAdmin(admin.ModelAdmin):
    """
        Model admin for task.
    """
    list_display = ('name', 'project', 'owner', 'start_date', 'end_date',
        'status', 'priority')

admin.site.register(Type)
admin.site.register(SubType)
admin.site.register(Task, TaskAdmin)
