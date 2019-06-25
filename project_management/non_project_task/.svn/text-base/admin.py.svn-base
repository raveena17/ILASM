"""
    Non project task by Admin
"""
from django.contrib import admin

from project_management.non_project_task.models import NonProjectTask, \
    NonProjectTaskAssignees

class NonProjectTaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'plannedStartDate', 'plannedEndDate', 'owner')

class NonProjectTaskAssigneesAdmin(admin.ModelAdmin):
    list_display = ('non_project_taskID', 'actualstartDate', 'actualendDate',
        'user', 'status')

admin.site.register(NonProjectTask, NonProjectTaskAdmin)
admin.site.register(NonProjectTaskAssignees, NonProjectTaskAssigneesAdmin)
