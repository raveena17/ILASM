"""
    project form
"""
from django.forms.formsets import BaseFormSet
from django.forms.models import BaseModelFormSet, HiddenInput, Field
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import mark_safe
from django.db.models import Max
from django.contrib.auth.models import Permission
from django.utils.translation import ugettext_lazy as _

from project_management.projects.models import DevelopmentProcess, \
    Domain, ProjectType, Project, ProjectSchedule
from project_management.projects.models import *
from project_management.milestone.models import InvoiceTerms
from project_management.business_unit.models import BusinessUnit
from project_management.users.models import UserProfile
from django.utils.encoding import smart_str, smart_unicode
from django import forms

import datetime

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class': 'vDateField'}
APPROVAL_TYPE = [('internal', 'internal'), ('external', 'external')]
BILLING_CATEGORY = [('Billed','Billed'),('Unbilled','Unbilled')]

PLANNED_EFFORT = [('DAYS', 'DAYS'), ('MONTHS', 'MONTHS'), ('YEARS', 'YEARS')]
CHOICE_FIELDS = ['project_type', 'business_unit', 'development_process',
                 'customer', 'domain']
EMPTY_LABEL = [('', '---------')]



class DateInput(forms.DateInput):
    input_type = 'date'


def get_values(objects):
    """ return the values in tuples with name and pk for choice field """
    return [(unicode(each.pk).strip(), unicode(each.name).strip())
            for each in objects]

# class HorizRadioRenderer(forms.RadioSelect.renderer):
#     """
#         this overrides widget method to put radio buttons horizontally
#         instead of vertically.
#     """
#     def render(self):
#         """Outputs radios"""
#         return mark_safe(u'\n'.join([u'%s' % w for w in self]))


class HorizontalRadioSelect(forms.RadioSelect):
    template_name = 'horizontal_select.html'


class NewHouseForm(forms.ModelForm):

    class Meta:
        # model = NewHouse
        fields = (
            'rating',)
        widgets = {
            "rating": HorizontalRadioSelect()
        }


def get_dict_from_object(object):
    """ return the dictinary of an object """
    strippedDict = {}
    objDict = object.__dict__
    for key, value in objDict.iteritems():
        strippedDict[key.replace('_id', '', -1)] = value
    return strippedDict


approval_choices = (('internal', 'internal'), ('external', 'external'))
billed_or_not = (('Billed','Billed'),('Unbilled','Unbilled'))
approve_or_not = (('Approve', 'Approve'), ('Reject', 'Reject'))
BILLED_TYPES = (('UB', _('----------')), ('FP', _('Fixed Price')), ('TM', _('Time & Management')),
                      ('SP', _('Support')), ('OR', _('Other')))

category_or_not = (('Monthly', 'Monthly'), ('Bi-Monthly', 'Bi-Monthly'))



class ProjectInitiationForm(forms.Form):
    """
        project initiation form
    """
    code = forms.CharField(widget=forms.HiddenInput(), required=False)
    project_name = forms.CharField(
        max_length=120, error_messages={
            'required': 'Please enter project name'})
    short_name = forms.CharField(max_length=80, required=False)
    apex_body_owner = forms.ModelChoiceField(queryset=User.objects.all())
    approval_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                    required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
    approval_reference = forms.CharField(required=False)
    planned_start_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                         required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
    planned_end_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                       required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
    customer = forms.ChoiceField(required=False)
    domain = forms.ChoiceField(required=False)
    next_invoice_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                        required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
    owner = forms.ModelChoiceField(queryset=User.objects.all(), required=False)
    parent = forms.ModelChoiceField(
        queryset=Project.objects.filter(
            is_project_group=True), required=False)
    business_unit = forms.ChoiceField(required=False)
    project_type = forms.ChoiceField(required=False)
    
    development_process = forms.ChoiceField(required=False)
    planned_effort = forms.DecimalField(max_digits=10, decimal_places=2)
    project_no = forms.IntegerField(required=False)
    planned_effort_unit = forms.ChoiceField(required=False, initial='DAYS')
    approval_type = forms.CharField(widget=forms.RadioSelect(choices=approval_choices,
                                                             ))

    # billing_category = forms.CharField(widget=forms.RadioSelect(choices=billing_category,
    #                                                          ))

    customer_contact = forms.ChoiceField(required=False)
    project_owner = forms.ChoiceField(required=False)
    estimated_time_exceed = forms.BooleanField(required=False)
    #estimation_no = forms.CharField(max_length = 500, required = False)
    #proposal_name = forms.CharField(max_length = 500, required = False, label = _('Proposal Name/ID'))

    def __init__(self, *args, **kwargs):
        '''
            choice field values will be filled during the form load
            new objects created on edit will be included in form load
        '''
        project_objects = {
            'project_type': ProjectType.objects.all(),
            'business_unit': BusinessUnit.objects.exclude(cancel=1).exclude(type__name='Customer'),
            'development_process': DevelopmentProcess.objects.all(),
            'customer': BusinessUnit.objects.filter(type__name='Customer'),
            'domain': Domain.objects.exclude(pk='0'),
            'invoicing_terms': InvoiceTerms.objects.all(),
            # 'delivery_center': BusinessUnit.objects.exclude(type__name='Customer').exclude(name='5g India').exclude(name='5g Canada').exclude(name='5g Europe')
        }

        if kwargs:
            project = kwargs.pop('project', None)
            schedules = kwargs.pop('schedules', None)
            form_args = get_dict_from_object(project) if project else {}
            form_args['project_name'] = project.name if project else None
            if schedules:
                form_args.update(get_dict_from_object(schedules))
            args = (form_args,)
        super(ProjectInitiationForm, self).__init__(*args, **kwargs)

        for each in CHOICE_FIELDS:
            self.fields[each].choices = EMPTY_LABEL + \
                get_values(project_objects[each])
        self.fields['planned_effort_unit'].choices = PLANNED_EFFORT
        self.fields['owner'].queryset = User.objects.filter(
            groups__name__icontains='Manager', is_active=True)
        # self.fields['apex_body_owner'].queryset = User.objects.filter(
        #     groups__name__icontains='Corporate Admin', is_active=True)

        self.fields['apex_body_owner'].queryset = User.objects.filter(
            groups__name__icontains='CEO', is_active=True)

        # self.fields['project_owner'].queryset = User.objects.filter(
        #     groups__name__icontains='Project Owner', is_active=True)

        self.fields['project_owner'].queryset = User.objects.filter(
            groups__name__icontains='CEO', is_active=True)

        self.fields['customer_contact'].choices = EMPTY_LABEL + [(str(profile.pk),
                                                                  str(profile.user.first_name + ' ' + profile.user.last_name))
                                                                 for profile in UserProfile.objects.filter(type='CC')]

    def clean(self):
        """ validate unique project name """
        if 'name' in self.cleaned_data and 'code' in self.cleaned_data:
            name, code = [self.cleaned_data['name'], self.cleaned_data['code']]
            if not code and Project.objects.filter(name=name).count() > 0:
                raise forms.ValidationError("Project name already exist")
        return self.cleaned_data


class VisiblePrimaryKeyFormset(BaseModelFormSet):
    def add_fields(self, form, index):
        """ over ridden add_field to include uuid in form """
        self._pk_field = pk = self.model._meta.pk
        if form.is_bound:
            pk_value = form.instance.pk
        else:
            try:
                pk_value = self.get_queryset()[index].pk
            except IndexError:
                pk_value = None
        form.fields[self._pk_field.name] = Field(initial=pk_value,
                                                 required=False, widget=HiddenInput)
        if 'invoice_terms' in (form.fields):
            form.fields['invoice_terms'] = forms.ModelChoiceField(
                InvoiceTerms.objects.all().order_by('id'), empty_label="select")
        BaseFormSet.add_fields(self, form, index)

    def clean(self):
        """ overridden clean not prevent form unique field checking
            and to change start date and end date format """
        pass



class BusinessUnitForm(forms.ModelForm):
    class Meta:
        model = BusinessUnit
        fields = '__all__'


class ProjectGroupForm(forms.ModelForm):
    def save(self, commit=True):
        project_group = super(ProjectGroupForm, self).save(commit=False)
        project_group.approval_type = Project.EXTERNAL
        project_group.is_project_group = True
        if commit:
            project_group.save()
        return project_group

    class Meta:
        model = Project
        fields = ('name', )


class ProjectInitiationRequestForm(forms.ModelForm):
    approval_type = forms.CharField(widget=forms.RadioSelect(choices=approval_choices,
                                                             ), label=_('Project Category'))
    is_approvedby = forms.CharField(widget=forms.RadioSelect(choices=approve_or_not,
                                                             ), label=_('Approval Category'), required=False)
    planned_effort = forms.DecimalField(
        label=_('Estimated Effort(man-days)'), required=False)

    project_no = forms.IntegerField(label=_('Project Id'), required=False)

    billing_category = forms.CharField(widget=forms.RadioSelect(choices=billed_or_not,
                                                             ), label=_('Billing Category'), required=False)
    rejection_reason = forms.CharField(
        max_length=150,
        widget=forms.Textarea,
        label=_('Rejection Reason'),
        required=False)

    unbilled_reason = forms.CharField(
        max_length=150,
        widget=forms.Textarea,
        label=_('Note'),
        required=False)

    ex_approval = forms.BooleanField(required=False)

    class Meta:
        model = Project
        fields = ('name', 'approval_type','billing_category','project_type', 'planned_effort','billed_type',
                  'objective', 'business_unit', 'requested_by', 'approved_by',
                  'project_no', 'objective', 'other_project_type','is_approved','is_rejected',
                  'customer', 'apex_body_owner', 'owner', 'project_owner', 'rejection_reason','unbilled_reason',)
        exclude = ('delivery_centre',)

    
    def __init__(self, *args, **kwargs):
        """
            Overriden init method to have add project related data to fields
        """
        user = kwargs.pop('user', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        project = kwargs.pop('instance', None)
        self.fields['business_unit'].queryset = BusinessUnit.objects.exclude(type__name='Customer').exclude(
            name='5G-CG').exclude(name='5G-PCG').exclude(name='5G-PDG').exclude(name='5G-PRG').exclude(name='5G-PSG')

        self.fields['approved_by'].queryset = User.objects.filter(
            groups__name='CEO', is_active=True).order_by('-id')

        self.fields['approved_by'].empty_label = None

        self.fields['owner'].queryset = User.objects.filter(
            groups__name__icontains='Manager', is_active=True)

        self.fields['apex_body_owner'].queryset = User.objects.filter(
            groups__name__icontains='Corporate Admin', is_active=True)

        # self.fields['project_owner'].queryset = User.objects.filter(
        #     groups__name__icontains='Project Owner', is_active=True)

        self.fields['project_owner'].queryset = User.objects.filter(
            groups__name__icontains='CEO', is_active=True)

        self.fields['customer'].queryset = BusinessUnit.objects.filter(
            type__name='Customer')
        self.fields['billed_type'].choices = Project.BILLED_TYPES

        if project:
            self.fields['requested_by'].queryset = User.objects.filter(
                pk=project.requested_by_id)    
        else:
            self.fields['requested_by'].queryset = User.objects.filter(
                pk=user.pk)

    def save(self, schedules, is_approved, is_rejected, ex_approval, commit=True):
        """
            Overriden save method to save virtual field
            which are not displayed to user
        """
        # import pdb;pdb.set_trace()
        project = super(ProjectInitiationRequestForm, self).save(commit=False)
        project.schedules = schedules
        project.is_approved = is_approved
        project.is_rejected = is_rejected
        project.ex_approval = ex_approval
        project.owner = project.requested_by
        project.short_name = project.name
       
        if is_approved:
            project.apex_body_owner = project.approved_by                                         #
            is_active = True
            self.fields['project_no'].initial = Project.objects.aggregate(
                Max('project_no'))['project_no__max'] + 1

        if commit:
            project.save()
        return project


class ProjectSchedulesRequestForm(forms.ModelForm):

    expected_start_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                          required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))

    expected_end_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                        required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))

    initiation_request_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT, '%Y-%m-%d'],
                                              required=False, label=_('Requested On'))

    approved_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT, '%Y-%m-%d'],
                                    required=False, label=_('Approved Date'))

    class Meta:
        model = ProjectSchedule
        fields = ('initiation_request_date', 'expected_start_date',
                  'expected_end_date', 'initiation_request_date')

    def __init__(self, *args, **kwargs):
        """
            Overriden init method to have add project related data to fields
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        schedules = kwargs.pop('instance', None)
        today = datetime.date.today()

        # today = datetime.date.today().strftime(DATE_INPUT_FORMAT)
        # import pdb;pdb.set_trace()
        self.fields['approved_date'].initial = today

        if schedules:
            schedules.planned_start_date = schedules.expected_start_date
            schedules.planned_end_date = schedules.expected_end_date
            schedules.approved_date = self.fields['approved_date'].initial
            if not schedules.initiation_request_date:
                self.fields['initiation_request_date'].initial = today

        else: 
            self.fields['initiation_request_date'].initial = today





class ProjectBillingDetailForm(forms.ModelForm):

    billing_category = forms.CharField(max_length=150,label=_('Category'),required=False)
    planned_days = forms.IntegerField(required=False)
    milestone = forms.CharField(max_length=150,label=_('Milestone'),required=False)
    percentage = forms.IntegerField(required=False)
    from_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                        required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
    to_date = forms.DateField(input_formats=[DATE_INPUT_FORMAT],
                                        required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
    category = forms.CharField(widget=forms.RadioSelect(choices=category_or_not,
                                                             ), label=_('Billing Category'), required=False)
    other = forms.CharField(max_length=150,widget=forms.Textarea,label=_('Note'),required=False)

    class Meta:
        model = ProjectBillingDetails
        fields = ('billing_category','planned_days','milestone','percentage','from_date','to_date','category','other')













































# class ProjectFixedPriceForm(forms.ModelForm):

#     billing_category = forms.CharField(max_length=150,label=_('Category'),required=False)
#     # planed_days = forms.DateField(label=('Planned Days'), input_formats=[DATE_INPUT_FORMAT],
#     #                                       required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
#     planned_days = forms.IntegerField(required=False)
#     milestone = forms.CharField(max_length=150,label=_('Milestone'),required=False)
#     date = forms.DateField(label=('Date'), input_formats=[DATE_INPUT_FORMAT],
#                                           required=False, widget=forms.TextInput(attrs=DATE_FIELD_ATTR))
#     percentage = forms.IntegerField(required=False)

#     class Meta:
#         model = ProjectFixedPrice
#         fields = ('billing_category','planned_days','milestone','date','percentage')
        

#     def __init__(self, *args, **kwargs):
#         """
#             Overriden init method to have add project related data to fields
#         """
#         user = kwargs.pop('user', None)
#         super(self.__class__, self).__init__(*args, **kwargs)
#         price = kwargs.pop('instance', None)
        












# Step 1: Include 4 row in AlertDataConfiguration table in backend

# INSERT INTO `AlertDataConfiguration` (`id`,`name`,`alert_type`,`action`,`days`,`frequency`,`subject_fields`,
# `body_fields`,`subject`,`body`,`is_email`,`is_screen`,`is_active`,`is_lock`,`created_by_id`,`created_on`,`modified_by_id`,`modified_on`) 
# VALUES ('alertdataconfig41','Project  Initiation Request','Event','Update','0','1','','approved_by.first_name,name,requested_by.first_name,schedules.initiation_request_date,requested_by.first_name,schedules.initiation_request_date,business_unit.name,name,approval_type,project_type,schedules.expected_start_date,schedules.expected_end_date,planned_effort,objective','Project initiation request','Dear %s<br><br>\n   Project  %s has been initiated by %s on %s.<br><br>\n\nRequested by     :     %s<br><br>\nRequested on  :     %s<br><br>\nBusiness Unit      :     %s.<br> <br>\nProject Name      :     %s <br> <br>\nProject Category     :     %s<br>   <br>\nProject Type :     %s<br>    <br>\nExpected Start Date   :     %s<br>   <br>\nExpected End Date  :%s<br>   <br>\nEstimated Efforts(man-days)    :     %s<br>   <br>\nObjectives :    %s<br>    <br><br>', '1', '1', '1', '1', NULL, NULL, NULL, '2013-01-22 15:20:43'); 

# INSERT INTO `AlertDataConfiguration` (`id`,`name`,`alert_type`,`action`,`days`,`frequency`,`subject_fields`,
# `body_fields`,`subject`,`body`,`is_email`,`is_screen`,`is_active`,`is_lock`,`created_by_id`,`created_on`,`modified_by_id`,`modified_on`) 
# VALUES ('alertdataconfig42', 'Project  Initiation Request', 'Event', 'Update', '0', '1', '', 'requested_by.first_name,name,schedules.initiation_request_date,requested_by.first_name,schedules.initiation_request_date,business_unit.name,name,approval_type,project_type,schedules.expected_start_date,schedules.expected_end_date,planned_effort,objective', 'Project initiation request details', 'Dear %s<br><br>\n   Project  %s has been initiated  on %s.<br><br>\n\nRequested by     :     %s<br><br>\nRequested on  :     %s<br><br>\nBusiness Unit      :     %s.<br> <br>\nProject Name      :     %s <br> <br>\nProject Category     :     %s<br>   <br>\nProject Type :     %s<br>    <br>\nExpected Start Date   :     %s<br>   <br>\nExpected End Date  :%s<br>   <br>\nEstimated Efforts(man-days)    :     %s<br>   <br>\nObjectives :    %s<br>    <br><br>', '1', '1', '1', '1', NULL, NULL, NULL, '2013-01-22 15:20:43'); 

# INSERT INTO `AlertDataConfiguration` (`id`,`name`,`alert_type`,`action`,`days`,`frequency`,`subject_fields`,
# `body_fields`,`subject`,`body`,`is_email`,`is_screen`,`is_active`,`is_lock`,`created_by_id`,`created_on`,`modified_by_id`,`modified_on`) 
# VALUES ('alertdataconfig43','Project  Approval Status','Event','Update','0','1','','name,approved_by.first_name,schedules.initiation_request_date,requested_by.first_name,schedules.initiation_request_date,business_unit.name,name,approval_type,project_type,schedules.expected_start_date,schedules.expected_end_date,planned_effort,objective','Project Approval Status','Project  %s was approved by %s upon customer approval on %s.<br><br>\n\n\nRequested by     :     %s<br><br>\nRequested on  :     %s<br><br>\nBusiness Unit      :     %s.<br>   <br>\nProject Name      :     %s <br> <br>\nProject Category     :     %s<br>   <br>\nProject Type :     %s<br>    <br>\nExpected Start Date   :     %s<br>   <br>\nExpected End Date  :%s<br>   <br>\nEstimated Efforts(man-days)    :     %s<br>   <br>\nObjectives :    %s<br>    <br><br>','1', '1', '1', '1', NULL, NULL, NULL, '2013-01-22 15:20:43');


# INSERT INTO `AlertDataConfiguration` (`id`,`name`,`alert_type`,`action`,`days`,`frequency`,`subject_fields`,
# `body_fields`,`subject`,`body`,`is_email`,`is_screen`,`is_active`,`is_lock`,`created_by_id`,`created_on`,`modified_by_id`,`modified_on`) 
# VALUES ('alertdataconfig44','Project  Approval Status','Event','Update','0','1','','name,approved_by.first_name,schedules.initiation_request_date,requested_by.first_name,schedules.initiation_request_date,business_unit.name,name,approval_type,project_type,schedules.expected_start_date,schedules.expected_end_date,planned_effort,objective','Project Approval Status','Project  %s was approved by %s pending customer approval on %s.<br><br>\n\n\nRequested by     :     %s<br><br>\nRequested on  :     %s<br><br>\nBusiness Unit      :     %s.<br>   <br>\nProject Name      :     %s <br> <br>\nProject Category     :     %s<br>   <br>\nProject Type :     %s<br>    <br>\nExpected Start Date   :     %s<br>   <br>\nExpected End Date  :%s<br>   <br>\nEstimated Efforts(man-days)    :     %s<br>   <br>\nObjectives :    %s<br>    <br><br>','1', '1', '1', '1', NULL, NULL, NULL, '2013-01-22 15:20:43');


# desc AlertDataConfiguration;
# select * from AlertDataConfiguration;