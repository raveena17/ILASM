from django import forms
from .models import AmcReport, Project, Milestone, Customer, Service
from django.forms import widgets
from project_management.business_unit.models import BusinessUnit
from django.contrib.auth.models import Group

import datetime

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class': 'vDateField'}


class DateInput(forms.DateInput):

    input_type = 'date'


class NumberInput(forms.NumberInput):

    input_type = 'number'


class TextInput(forms.TextInput):

    input_type = 'text'


class ReportAmcForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['role'] = forms.ModelMultipleChoiceField(
            queryset=Group.objects.all(), widget=forms.SelectMultiple())
        for key, field in self.fields.items():
            if isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'placeholder': "days"})
            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'placeholder': "comments"})
        if 'instance' in kwargs:
            if kwargs['instance']:
                self.fields['customer_name'].disabled = True
                self.fields['project_name'].disabled = True
                self.fields['milestone_name'].disabled = True
                self.fields['Due_date'].disabled = True
                self.fields['AMC_end_date'].disabled = True
                self.fields['notification'].disabled = True
                self.fields['role'].disabled = True
                self.fields['notification'].widget = forms.DateInput()
            else:
                del self.fields['status']

    def save(self, commit=True):
        return super(ReportAmcForm, self).save(commit=commit)

    class Meta:
        model = AmcReport
        exclude = ('created_on', 'created_by', 'updated_on', 'updated_by',)
        widgets = {
            'notification': NumberInput()
        }


class ReportServiceForm(forms.Form):

    repeat = forms.BooleanField(required=False)
    frequency = forms.ModelChoiceField(
        queryset=Service.objects.all(), required=False)
