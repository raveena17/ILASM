"""
    Milestone forms
"""
from django import forms

from project_management.milestone.models import Milestone

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class':'vDateField'}

class EngineeringMilestoneForm(forms.ModelForm):
    '''
        form representing engineering milestone
    '''

    start_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget=forms.TextInput(attrs = DATE_FIELD_ATTR))

    end_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required=False, widget=forms.TextInput(attrs = DATE_FIELD_ATTR))

    class Meta:
        model = Milestone
        fields = ['name', 'start_date', 'end_date', 'notes']

    def save(self, project, id, commit=True):
        milestone = super(EngineeringMilestoneForm, self).save(commit=False)
        milestone.category = Milestone.category_choices[1][1]
        if commit:
            milestone.save()
            if not id:
                project.milestone.add(milestone)
        return milestone
