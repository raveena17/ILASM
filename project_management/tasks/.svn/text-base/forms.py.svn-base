"""
    Forms for Task
"""
from django import forms
from django.contrib.auth.models import User

from project_management.tasks.models import Task, Type, SubType
from project_management.milestone.models import Milestone

from datetime import datetime

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class':'vDateField'}
class TaskForm(forms.ModelForm):
    """
        Form representing task model
    """

    start_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    end_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    def __init__(self, *args, **kwargs):
        """
            Overriden init method to have add project related data to fields
        """
        project = kwargs.pop('project', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Task.tree.root_nodes().filter(project
                                                                    = project)

        self.fields['type'].queryset = Type.objects.filter(is_project_type
                                                                    = True)
        self.fields['owner'].queryset = User.objects.filter(
                    is_active = True, is_staff = False).order_by('username')

        try:
            self.fields['milestone'].queryset =  project.milestone.filter(
                                        category = Milestone.ENGINEERING)

            self.fields['assigned_resources'].queryset = project.team.filter(
                    is_active = True, is_staff = False).order_by('username')
        except:
            self.fields['assigned_resources'].queryset = User.objects.filter(
                    is_active = True, is_staff = False).order_by('username')

    def save(self, user, project, commit = True):
        """
            Overriden save method to save virtual field
            which are not displayed to user
        """
        task = super(TaskForm, self).save(commit = False)
        task.project = project
        task.editor = user
        if not task.id:
            task.author = user
            task.created_at = datetime.now()
        if commit:
            task.save()
        assign_resource = lambda resource : task.assigned_resources.add(resource)
        map(assign_resource, self.cleaned_data['assigned_resources'])
        return task

    class Meta:
        model = Task
        fields = ( 'name', 'owner', 'start_date', 'end_date', 'priority', 'status',
                   'type', 'sub_type', 'milestone', 'parent', 'assigned_resources', 'notes' )

class TypeForm(forms.ModelForm):
    """
        Form representing task type model
    """
    class Meta:
        model = Type

class SubTaskForm(forms.Form):
    """
        Form representing sub task
    """
    sub_tasks = forms.ModelMultipleChoiceField(queryset = Task.objects.none(),
                required = False)

    def __init__(self, *args, **kwargs):
        """
            choice field values willl be filled during form load
        """
        task = kwargs.pop('task', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['sub_tasks'].queryset = Task.objects.filter(parent
            = task) if task else Task.objects.none()

    def save(self, task):
        """
            save the sub task for a task
        """
        sub_tasks = self.cleaned_data['sub_tasks']
        for sub_task in sub_tasks:
            if task.parent == sub_task:
                continue
            sub_task.parent = task
            sub_task.save()

class NonProjectTaskForm(forms.ModelForm):
    """
        Form which represents the non project task.
    """
    start_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    end_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    def save(self, user, commit=True ):
        """
            Overridden save to assign the mandatory fields.
        """
        task = super(NonProjectTaskForm, self).save(commit = False)
        task.editor = user
        task.owner = user
        if not task.id:
            task.author = user
            task.created_at = datetime.now()
        if commit:
            task.save()
        return task


    def __init__(self, *args, **kwargs):
        """
            Overriden init method to filter non project task type
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = Type.objects.filter(is_project_type
                                                                    = False)

    class Meta:
        """
            Defines the configuration for model forms.
        """
        model = Task
        fields = ('name', 'type', 'start_date', 'end_date',  'notes')
