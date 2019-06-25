"""
   Master Forms
"""
from django.forms import ModelForm

from project_management.projects.models import ProjectType, Project, \
    Domain, Technology, DevelopmentProcess
from project_management.repository.models import Repository, RepositoryTags

class ProjectTypeForm (ModelForm):
    class Meta:
        model = ProjectType
        exclude = ('level')

class RepositoryTagForm (ModelForm):
    class Meta:
        model = RepositoryTags
        exclude = ('sequenceNo')

class DomainForm(ModelForm):
    class Meta:
        model = Domain

class TechnologyForm(ModelForm):
    class Meta:
        model = Technology

class DevelopmentProcessForm(ModelForm):
    class Meta:
        model = DevelopmentProcess

def deleteProjectType(ids):
    delete = [ProjectType.objects.get(pk = each).delete() for each in ids]
    return delete

def deleteRepositoryTag(ids):
    delete = [RepositoryTags.objects.get(pk = each).delete() for each in ids
        if Repository.objects.filter(repositoryTag = each).count() == 0]
    return delete

def deleteDomain(ids):
    delete = [Domain.objects.get(pk = each).delete() for each in ids
                if Project.objects.filter(domain = each).count() == 0]
    return delete

def deleteTechnology(ids):
    to_delete = [Technology.objects.get(pk = each).delete() for each in ids
                if Project.objects.filter(technology = each).count() == 0]
    return to_delete

def delete_development_process(ids):
    delete = [DevelopmentProcess.objects.get(pk = each).delete() for each in ids
            if Project.objects.filter(development_process = each).count() == 0]
    return delete
