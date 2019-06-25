from django import forms
from matplotlib.table import Table
from django import forms
from django.contrib.auth.models import User, Group
from .models import ClientVisitReport
from project_management.projects.models import *


class DateInput(forms.DateInput):
    input_type = 'date'


class CvrTableForm(forms.ModelForm):
    project_name = Project.objects.all()

    def __init__(self, *args, **kwargs):
        super(CvrTableForm, self).__init__(*args, **kwargs)
        if self.initial:
            self.fields['project_name'].queryset = Project.objects.all()
            self.fields['project_name'].initial = self.initial['project_name']

    class Meta:
        model = ClientVisitReport

        fields = ('project_name', 'client_name', 'visit_location', 'from_date', 'to_date',
                  'reason_for_visit', 'actions_taken_during_the_visit', 'next_plan_of_action', 'comments', 'reporting_senior_name', 'reason_for_reject')

        Table.exclude = ('project_id',)
        widgets = {
            'date_of_visit': DateInput(),
            'comments': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'reason_for_visit': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'actions_taken_during_the_visit': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'next_plan_of_action': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'arrival_time': forms.TimeInput(attrs={'placeholder': 'HH:MM AM/PM'}),
            'departure_time': forms.TimeInput(attrs={'placeholder': 'HH:MM AM/PM'}),
        }
