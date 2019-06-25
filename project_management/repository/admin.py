"""
    Repository Admin
"""

from django.contrib import admin

from project_management.repository.models import RepositoryTags, Repository

admin.site.register(RepositoryTags)
admin.site.register(Repository)
