"""
    Announcement Admin
"""
from django.contrib import admin

from announcements.models import Announcement

class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'creation_date')

admin.site.register(Announcement, AnnouncementAdmin)
