"""
    Project Admin
"""
from django.contrib import admin

from project_management.projects.models import ProjectType, DevelopmentProcess, \
    Domain, Technology, DevelopmentEntity, ProjectSchedule, Project, \
    ProjectMembership, ProjectRole

class ProjectScheduleAdmin(admin.ModelAdmin):
    list_display = ('expected_start_date', 'expected_end_date',
        'planned_start_date', 'planned_end_date', 'approval_date',
        'actual_start_date', 'actual_end_date')

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'apex_body_owner', 'owner', 'domain',
        'project_type')

admin.site.register(ProjectType)
admin.site.register(DevelopmentProcess)
admin.site.register(Domain)
admin.site.register(Technology)
admin.site.register(DevelopmentEntity)
admin.site.register(ProjectSchedule, ProjectScheduleAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectMembership)
admin.site.register(ProjectRole)

