"""
  Object Based Permission by Admin
"""

from django.contrib import admin

from project_management.access_control.models import ObjectPermission

class ObjectPermissionAdmin(admin.ModelAdmin):
    """
        object based permssion admin.
    """
    list_display = ( 'user', 'can_view', 'can_edit', 'can_delete')

admin.site.register(ObjectPermission, ObjectPermissionAdmin)
