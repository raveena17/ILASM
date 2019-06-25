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
from project_management.leave.choices import STATUS_CHOICES, MONTH_CHOICES, LEAVE_CHOICES
from project_management.leave.models import *
from project_management.leave.views import *


DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class': 'vDateField'}


class DateInput(forms.DateInput):

    input_type = 'date'


class LeaveReportForm(forms.ModelForm):
    """
        form which represents the leave_application.
    """

    def __init__(self, user, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.user = user
        self.initial['empid'] = user
        self.fields['empid'].empty_label = None
        self.fields['approved_by'].empty_label = None

        if not self.instance.request_id:

            self.fields['empid'].queryset = User.objects.filter(id=user.id)
            reporting_senior_name = UserProfile.objects.get(
                user=user).reporting_senior_name
            self.fields['approved_by'].queryset = User.objects.filter(
                id=reporting_senior_name.id)
            self.initial['approved_by'] = reporting_senior_name.id

            self.fields['leave_from'].required = True
            self.fields['leave_to'].required = True
            self.fields['no_of_days'].required = True
            self.fields['leave_nature'].required = True
            self.fields['leave_reason'].required = True
        else:
            today = datetime.date.today()
            self.fields['empid'].queryset = User.objects.filter(
                id=self.instance.empid.id)
            self.initial['empid'] = self.instance.empid

            self.fields['approved_by'].queryset = User.objects.filter(
                id=self.instance.approved_by.id)
            self.initial['approved_by'] = self.instance.approved_by

            if self.instance.approved_by.id == user.id:
                self.fields['empid'].disabled = True
                self.fields['leave_from'].disabled = True
                self.fields['leave_to'].disabled = True
                self.fields['no_of_days'].disabled = True
                self.fields['leave_nature'].disabled = True
                self.fields['leave_reason'].disabled = True
                self.fields['approved_by'].disabled = True
                self.fields['lop'].disabled = True

        self.fields['no_of_days'].widget.attrs['readonly'] = 'readonly'
        self.fields['lop'].widget.attrs['readonly'] = 'readonly'
        self.fields['lop'].label = "LOP"

        """ Changed by field name in leave form"""
        self.fields['empid'].label = "Name"
        self.fields['leave_from'].label = "From Date"
        self.fields['leave_to'].label = "To Date"
        self.fields['no_of_days'].label = "No of days"
        self.fields['leave_nature'].label = "Type"
        self.fields['leave_reason'].label = "Reason"
        self.fields['approved_by'].label = "Reporting Senior"

        today = datetime.date.today()

        # import pdb;pdb.set_trace()
        bucode = UserProfile.objects.get(user_id=user.id).business_unit_code_id
        leavenature = Type.objects.filter(current_year=today.year, organization=bucode)
        self.fields['leave_nature'].queryset = leavenature
        self.fields['leave_nature'].empty_label = None

        if self.initial['empid'] == self.initial['approved_by']:
            self.initial['empid'].disabled = True

    def save(self, commit=True):
        leave = super(LeaveReportForm, self).save(commit=False)

        if commit:
            leave.save()
        return leave

    class Meta:
        model = LeaveRequest
        exclude = (
            'request_id',
            'request_date',
            'approval_status',
            'reject_reason'
        )


class ShortLeaveRequestForm(forms.ModelForm):
    """
        form which represents the leave_application.
    """

    def __init__(self, user, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.user = user
        self.initial['empid'] = user
        self.fields['empid'].empty_label = None
        self.fields['approved_by'].empty_label = None

        if not self.instance.request_id:
            self.fields['empid'].queryset = User.objects.filter(id=user.id)
            reporting_senior_name = UserProfile.objects.get(
                user=user).reporting_senior_name
            self.fields['approved_by'].queryset = User.objects.filter(
                id=reporting_senior_name.id)
            self.initial['approved_by'] = reporting_senior_name.id

            self.fields['leave_date'].required = True
            self.fields['leave_reason'].required = True
            self.fields['no_of_hours'].required = True

        else:
            today = datetime.date.today()
            self.fields['empid'].queryset = User.objects.filter(
                id=self.instance.empid.id)
            self.initial['empid'] = self.instance.empid

            self.fields['approved_by'].queryset = User.objects.filter(
                id=self.instance.approved_by.id)
            self.initial['approved_by'] = self.instance.approved_by

            if self.instance.approved_by.id == user.id:
                self.fields['leave_date'].disabled = True
                self.fields['empid'].disabled = True
                self.fields['leave_reason'].disabled = True
                self.fields['approved_by'].disabled = True
                self.fields['no_of_hours'].disabled = True

        """ Changed by field name in shortleave form"""
        self.fields['leave_date'].label = "Date"
        self.fields['empid'].label = "Name"
        self.fields['leave_reason'].label = "Reason"
        self.fields['approved_by'].label = "Reporting Senior"
        self.fields['no_of_hours'].label = "No of hours"

    class Meta:
        model = ShortLeaveRequest
        exclude = (
            'request_id',
            'request_date',
            'reject_reason',
            'approval_status')


class LeaveCreditForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)

        self.user = user
        self.initial['empid'] = user

        """ Changed by field name in leave credit form"""
        self.fields['empid'].label = "Employee"
        self.fields['leave_id'].label = "Leave Type"
        self.fields['no_of_days'].label = "No of days"
        self.fields['cur_year'].label = "Year"

        today = datetime.date.today()
        self.fields['empid'].queryset = User.objects.filter(is_active=1)
        self.fields['empid'].empty_label = None
        leavetype = Type.objects.filter(current_year=today.year)
        self.fields['leave_id'].queryset = leavetype
        self.fields['leave_id'].empty_label = None
        self.fields['cur_year'].initial = int(datetime.date.today().year)

    class Meta:
        model = LeaveCredit
        fields = '__all__'


class SettingsForm(forms.Form):
    half = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "Leave"}))
    short = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={
                "class": "Leave"}))


class ReportForm(forms.Form):

    month = forms.ChoiceField(choices=MONTH_CHOICES)
    year = forms.CharField(max_length=100)
    employee = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True), empty_label='All')
    leave = forms.ChoiceField(choices=LEAVE_CHOICES)
    status = forms.ChoiceField(choices=STATUS_CHOICES)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['month'].initial = [self.get_current_month()]
        self.fields['year'].initial = settings.CURRENT_YEAR
        # self.fields['year'].initial = int(datetime.date.today().year)
        self.fields['year'].widget.attrs['readonly'] = 'readonly'

    def get_current_month(self):

        current_year_month = int(datetime.date.today().month)
        current_month = None
        for month in MONTH_CHOICES:
            if month[0] == current_year_month:
                current_month = month[0]
                break
        return current_month


class ReconciliationForm(forms.Form):

    username = forms.ModelChoiceField(
        queryset=User.objects.filter(
            is_active=True))
    cur_year = forms.CharField(max_length=200)

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['cur_year'].initial = settings.CURRENT_YEAR
        self.fields['cur_year'].label = "Year"
        self.fields['cur_year'].widget.attrs['readonly'] = 'readonly'

        self.fields['username'].label = "Username"
        self.fields['username'].empty_label = None


class LateAttendanceForm(forms.ModelForm):

    late_attendance_count = forms.IntegerField()
    
    class Meta:
        model = LateAttendance
        fields = ['late_attendance_count']

