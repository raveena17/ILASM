"""
    Leave Application forms
"""
from django import forms
from .models import *
from django.contrib.auth.models import User, Group
from project_management.users.models import UserProfile, userType
from project_management.users.forms import UserProfileForm, UserForm, MyProfileForm
import datetime
from django.core.mail import EmailMessage
import settings
from django.contrib import messages

from project_management.dashboard.views import *
from project_management.alert.models import *



DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class': 'vDateField'}


class DateInput(forms.DateInput):

    input_type = 'date'

class ReportForm(forms.Form):
    emailomission = Emailomission.objects.all().values('adsslogin')
    # Users = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_active=True).exclude(username__in=emailomission), empty_label=request.user.username)
    Users = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True).order_by('username').exclude(username__in=emailomission))
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        

   