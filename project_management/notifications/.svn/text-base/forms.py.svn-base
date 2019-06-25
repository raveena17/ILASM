"""
    forms for event application
"""
from django import forms
from django.contrib.auth.models import User

from project_management.notifications.models import Event

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class':'vDateField'}

class EventForm(forms.ModelForm):

    date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    def save(self, user, commit = True):
        """
            Overriden save method to include creator and attendees in event
        """
        event = super(EventForm, self).save(commit = False)
        event.creator = user
        if commit:
            event.save()
            for user in self.cleaned_data['attendees']:
                event.attendees.add(user)

    def __init__(self, *args, **kwargs):
        """
            Overriden init method to filter only active users
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['attendees'].queryset = User.objects.filter(is_active = True,
                            is_staff = False).order_by('username')

    class Meta:
        model = Event
        fields = ('name', 'date', 'start_time', 'end_time', 'venue',
            'location', 'project', 'type', 'attendees',  'description')
