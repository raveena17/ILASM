"""
    Task Tracking By Admin
"""
from django.contrib import admin

from project_management.timesheet.models import TaskTracking

class TaskTrackingAdmin(admin.ModelAdmin):
    list_display = ('user', 'program', 'task', 'time_spent')

admin.site.register(TaskTracking, TaskTrackingAdmin)
