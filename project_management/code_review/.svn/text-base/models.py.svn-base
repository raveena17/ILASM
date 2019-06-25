from django.db import models
from django.contrib.auth.models import User

from project_management.projects.models import Project

class CodeReview(models.Model):
    reviewer = models.ForeignKey(User, related_name='Lead')
    engineer = models.ForeignKey(User, related_name='employee')
    project = models.ForeignKey(Project, related_name='performance project')
    review_date = models.DateField(null=True, blank = True)
    patch_code = models.CharField(max_length = 25)
    patch = models.NullBooleanField(blank=True)
    build = models.NullBooleanField(blank=True)
    test_case = models.NullBooleanField(blank=True)
    comments = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(blank=True, default=True)
    created_on = models.DateField(null=True, blank = True)
    created_by = models.ForeignKey(User, related_name='performance created by')
    modified_on = models.DateTimeField(auto_now=True, null=True, blank = True)
    modified_by = models.ForeignKey(User, related_name='performance modified by')
