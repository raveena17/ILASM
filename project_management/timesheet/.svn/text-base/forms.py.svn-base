"""
    Forms for timesheet task entry.
"""
from django import forms

from django.db.models import Q
from project_management.timesheet.models import TaskTracking
from project_management.tasks.models import Task
from project_management.projects.models import Project
from project_management.projects.forms import get_values

class PartialTaskTrackingForm(forms.ModelForm):
    """
        A partial (incomplete) form representing the TaskTracking model.
    """
    def save(self, user, force_insert = False, force_update = False, commit = True):
        if not user:
            error = '%s\'s save method requires the logged in user object as an argument.'
            raise TypeError(error %( self.__class__.__name__ ))
        task = self.cleaned_data.get('task')
        is_rework = forms.BooleanField(required = False)
        record = super(PartialTaskTrackingForm, self).save(commit = False)
        record.user = user
        record.program, record.is_program_task = TaskTracking.get_project(task)
        if commit:
            record.save()
        return record

    class Meta:
        model = TaskTracking
        exclude = [ 'user', 'program', ]

class TaskSelectionForm(forms.Form):
    """
        A form representing the selection of task from project.
    """
    project = forms.ChoiceField()
    tasks = forms.MultipleChoiceField()

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        project_id = kwargs.pop('project', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['project'].choices = get_values(Project.objects.filter(
            Q(apex_body_owner=user) | Q(owner=user) |
            Q(team=user)).distinct().filter(is_active = True))

        self.fields['project'].choices.insert(1, ('0', 'NonProjectTask'))
        self.fields['project'].choices.insert(0, ('', '-----------'))
        if project_id:
            if project_id == '0':
                tasks_choices = get_values(Task.objects.filter(project = None))
            else:
                tasks_choices = get_values(Task.objects.filter(project__id
                    = project_id).filter(assigned_resources = user))
            self.fields['tasks'].choices = tasks_choices
