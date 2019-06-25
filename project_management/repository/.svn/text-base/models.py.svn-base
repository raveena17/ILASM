"""
    Repository Models
"""
from django.db import models

from project_management.projects.models import Project

class RepositoryTags(models.Model):
    """ class representing tags for files upload in repository """
    repositoryTagID =  models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)
    sequenceNo = models.IntegerField(default = 1, null = True)

    def __unicode__(self):
        return self.name

class Repository(models.Model):
    """ class representing uploaded files in repository """
    fileID = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 120)
    fileUploaded = models.ImageField(upload_to = "all files", max_length = 300)
    program = models.ForeignKey(Project)
    repositoryTag = models.ForeignKey(RepositoryTags)

    def __unicode__(self):
        return self.name
