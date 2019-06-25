from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from project_management.conferenceroombooking.models import ConferenceRoom, BookConference
import datetime

from project_management.templatecalendar import __getTimes__

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class':'vDateField'}

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """
        this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s' % w for w in self]))

class ConferenceRoomForm(forms.ModelForm):
    """
        form which represents the business unit.
    """
    name = forms.CharField(label='Conference Room Name')
    location = forms.CharField(required = False)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        
    def save(self, commit = True):
        conference_room = super(ConferenceRoomForm, self).save(commit = False)
        if commit:
            conference_room.save()
            for each in self.cleaned_data['equipments_required']:
                conference_room.equipments_required.add(each)
        return conference_room

    class Meta:
        model = ConferenceRoom
        
        
approve_or_not = (('Approve', 'Approve'), ('Reject', 'Reject'))
class BookConferenceRoomForm(forms.ModelForm):
    """
        form which represents the business unit.
    """
    meeting_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = True)
    
    requesting_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, label = _('Requested On'))

    approved_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, label = _('Approved Date'))
    is_approvedby = forms.CharField(label='',widget = forms.RadioSelect(choices = approve_or_not,
                                    renderer = HorizRadioRenderer ), required = False) 

    
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        #book_conference_room = kwargs.pop('instance', None)
        super(self.__class__, self).__init__(*args, **kwargs)        
        self.fields['requested_by'].queryset = User.objects.filter(pk = user.pk)
        self.fields['approved_by'].queryset = User.objects.filter(groups__name = 'Corporate Admin', is_active = True)
        
        #if book_conference_room:
        #    self.fields['requested_by'].queryset = User.objects.filter(pk
        #                                            = book_conference_room.requested_by_id)
        #else:
        #    self.fields['requested_by'].queryset = User.objects.filter(
        #                                                        pk = user.pk)
               
    def save(self,commit = True):
        book_conference_room = super(BookConferenceRoomForm, self).save(commit = False)
        if book_conference_room.is_approvedby == 'Approve':
            book_conference_room.is_approved = True
        if book_conference_room.attendence_needed:
            attendence_needed = 1
        else:
            attendence_needed = 0
        if commit:
            book_conference_room.save()
            for each in self.cleaned_data['equipments_required']:
                book_conference_room.equipments_required.add(each)
        return book_conference_room

    class Meta:
        model = BookConference
        exclude = ('is_approved')
        