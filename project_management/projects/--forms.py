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

from project_management.projects.models import  DevelopmentProcess, \
    Domain, ProjectType, Project, ProjectSchedule
from project_management.milestone.models import InvoiceTerms
from project_management.business_unit.models import BusinessUnit
from project_management.users.models import UserProfile

import datetime

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class':'vDateField'}
APPROVAL_TYPE = [('internal','internal'), ('external', 'external')]
PLANNED_EFFORT = [('DAYS', 'DAYS'), ('MONTHS', 'MONTHS'), ('YEARS', 'YEARS')]
CHOICE_FIELDS = ['project_type', 'business_unit', 'development_process','delivery_center',
                'customer','domain']
EMPTY_LABEL = [('','---------')]

def get_values(objects):
    """ return the values in tuples with name and pk for choice field """
    return [(unicode(each.pk).strip(), unicode(each.name).strip()) for each in objects]

class HorizRadioRenderer(forms.RadioSelect.renderer):
    """
        this overrides widget method to put radio buttons horizontally
        instead of vertically.
    """
    def render(self):
        """Outputs radios"""
        return mark_safe(u'\n'.join([u'%s' % w for w in self]))

def get_dict_from_object(object):
    """ return the dictinary of an object """
    strippedDict = {}
    objDict = object.__dict__
    for key, value in objDict.iteritems():
        strippedDict[key.replace('_id', '', -1)] = value
    return strippedDict

approval_choices = (('internal','internal'), ('external', 'external'))
approve_or_not = (('Approve', 'Approve'), ('Reject', 'Reject'))
class ProjectInitiationForm(forms.Form):
    """
        project initiation form
    """ 
    code = forms.CharField(widget=forms.HiddenInput(), required=False)
    project_name = forms.CharField(max_length = 120, error_messages
                    = {'required': 'Please enter project name'})
    short_name = forms.CharField(max_length = 80, required = False)
    apex_body_owner = forms.ModelChoiceField(queryset = User.objects.all())
    approval_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required=False, widget=forms.TextInput(attrs = DATE_FIELD_ATTR))
    approval_reference = forms.CharField(required = False)
    planned_start_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required=False, widget=forms.TextInput(attrs = DATE_FIELD_ATTR))
    planned_end_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required=False, widget=forms.TextInput(attrs = DATE_FIELD_ATTR))
    customer = forms.ChoiceField(required=False)
    domain = forms.ChoiceField(required=False)
    next_invoice_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required=False, widget=forms.TextInput(attrs = DATE_FIELD_ATTR))
    owner = forms.ModelChoiceField(queryset = User.objects.all(), required=False)
    parent = forms.ModelChoiceField(queryset
        = Project.objects.filter(is_project_group = True), required = False)
    business_unit = forms.ChoiceField(required=False)
    
    delivery_center = forms.ChoiceField(required=False) 
    project_type = forms.ChoiceField(required=False)
    is_approvedby = forms.CharField(widget = forms.RadioSelect(choices = approve_or_not,
                                    renderer = HorizRadioRenderer ), required = False)
    development_process = forms.ChoiceField(required=False)
    planned_effort =  forms.DecimalField(max_digits = 10, decimal_places = 2)
    project_no = forms.IntegerField(required = False)
    planned_effort_unit = forms.ChoiceField(required = False, initial='DAYS')
    approval_type = forms.CharField(widget = forms.RadioSelect(choices = approval_choices,
        renderer = HorizRadioRenderer))
    customer_contact = forms.ChoiceField(required=False)
    project_owner = forms.ChoiceField(required=False)
    estimated_time_exceed = forms.BooleanField(required = False)
    estimation_no = forms.CharField(max_length = 500, required = False)
    proposal_name = forms.CharField(max_length = 500, required = False, label = _('Proposal Name/ID'))
   

    def __init__(self, *args, **kwargs):
        '''
            choice field values will be filled during the form load
            new objects created on edit will be included in form load
        '''
        project_objects = {
            'project_type': ProjectType.objects.all(),
            'business_unit': BusinessUnit.objects.exclude(cancel
                                    = 1).exclude(type__name = 'Customer'),
            'development_process': DevelopmentProcess.objects.all(),
            'customer': BusinessUnit.objects.filter(type__name = 'Customer'),
            'domain': Domain.objects.exclude(pk = '0'),
            'invoicing_terms': InvoiceTerms.objects.all(),
            'delivery_center': BusinessUnit.objects.exclude(type__name = 'Customer').exclude(name = '5g India').exclude(name = '5g Canada').exclude(name = '5g Europe')
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
            self.fields[each].choices = EMPTY_LABEL + get_values(project_objects[each])
        self.fields['planned_effort_unit'].choices = PLANNED_EFFORT
        self.fields['owner'].queryset = User.objects.filter(
                groups__name__icontains = 'Manager', is_active = True)
        self.fields['apex_body_owner'].queryset = User.objects.filter(
                groups__name__icontains = 'Corporate Admin', is_active = True)
        self.fields['project_owner'].queryset = User.objects.filter(
                groups__name__icontains = 'Project Owner', is_active = True)
        self.fields['customer_contact'].choices = EMPTY_LABEL+[(str(profile.pk),
            str(profile.user.first_name + ' ' + profile.user.last_name))
            for profile in UserProfile.objects.filter(type = 'CC')]
    
    def clean(self):
        """ validate unique project name """
        if self.cleaned_data.has_key('name') and self.cleaned_data.has_key('code'):
            name, code  = [self.cleaned_data['name'], self.cleaned_data['code']]
            if not code and Project.objects.filter(name = name).count() > 0:
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
        form.fields[self._pk_field.name] = Field(initial = pk_value,
            required=False, widget=HiddenInput)
        if (form.fields).has_key('invoice_terms'):
            form.fields['invoice_terms'] = forms.ModelChoiceField(
                    InvoiceTerms.objects.all().order_by('id'), empty_label = "select")
        BaseFormSet.add_fields(self, form, index)

    def clean(self):
        """ overridden clean not prevent form unique field checking
            and to change start date and end date format """
        pass

#class ProjectGroupForm(forms.ModelForm):
#    '''
#        form representing a project group
#    '''
#
#    unassigned_projects = forms.CharField(widget=
#                        forms.widgets.SelectMultiple(), required=False)
#    child_projects = forms.CharField(widget=
#                        forms.widgets.SelectMultiple(), required=False)
#
#    class Meta:
#        model = Project
#        fields = ['name', 'apex_body_owner', 'project_type']
#
#    def __init__(self, *args, **kwargs):
#        super(ProjectGroupForm, self).__init__(*args, **kwargs)
#        project_group = kwargs['instance']
#        project_group_id = project.pk if project_group else ''
#        self.fields['unassigned_projects'].widget.choices = get_values(
#                            Project.objects.filter(parent__isnull = True))
#
#        self.fields['child_projects'].widget.choices = get_values(
#                            Project.objects.filter(parent = project_group_id))
#
#    def save(self, commit = True):
#        project_group = super(ProjectGroupForm, self).save(commit = False)
#        if commit:
#            project_group.approval_type = Project.approval_choices[1][0]
#            project_group.save()
#            project_group2 = Project.objects.get(name = project_group.name)
#            project_group2.parent_id = project_group2.id
#            project_group2.save()
#            child_projects =  eval(self.cleaned_data['child_projects'])
#            for project in child_projects:
#                assigned_project = Project.objects.get(pk = project)
#                assigned_project.parent_id = project_group.pk
#                assigned_project.save()
#            deselected_project = Project.objects.filter(parent
#                = project_group.pk).exclude(pk__in = child_projects)
#            for project in deselected_project:
#                project.parent = None
#                project.save()
#        return project_group2


class BusinessUnitForm(forms.ModelForm):
    class Meta:
        model = BusinessUnit

class ProjectGroupForm(forms.ModelForm):
    def save(self, commit = True):
        project_group = super(ProjectGroupForm, self).save(commit = False)
        project_group.approval_type = Project.EXTERNAL
        project_group.is_project_group = True
        if commit:
            project_group.save()
        return project_group

    class Meta:
        model = Project
        fields = ('name', )

class ProjectInitiationRequestForm(forms.ModelForm):
    approval_type = forms.CharField(widget
        = forms.RadioSelect(choices = approval_choices,
        renderer = HorizRadioRenderer), label = _('Project Category'))
    
    is_approvedby = forms.CharField(widget
        = forms.RadioSelect(choices = approve_or_not,
        renderer = HorizRadioRenderer), label = _('Approval Category'), required = False)
    
    planned_effort =  forms.DecimalField(label = _('Estimated Effort(man-days)'),required=False)
    
    project_no = forms.IntegerField(label=_('Project Id'), required = False)
    rejection_reason = forms.CharField(max_length = 150,widget=forms.Textarea, label = _('Rejection Reason'), required = False)
    ex_approval = forms.BooleanField( required = False)
    estimation_no = forms.CharField(max_length = 500, required = False)
    proposal_name = forms.CharField(max_length = 500, required = False, label = _('Proposal Name/ID'))

    
    class Meta:
        model = Project
        fields = ('name', 'approval_type', 'project_type', 'planned_effort',
                   'objective', 'business_unit', 'requested_by', 'approved_by','delivery_centre',
                   'project_no', 'objective', 'other_project_type', 'is_approvedby', 
                'customer','apex_body_owner','owner','project_owner','rejection_reason','estimation_no','proposal_name')

    def __init__(self, *args, **kwargs):
        """
            Overriden init method to have add project related data to fields
        """
        user = kwargs.pop('user', None)
        super(self.__class__, self).__init__(*args, **kwargs)
        project = kwargs.pop('instance', None)
        self.fields['business_unit'].queryset =  BusinessUnit.objects.exclude(type__name = 'Customer').exclude(name = '5G-CG').exclude(name = '5G-PCG').exclude(name = '5G-PDG').exclude(name = '5G-PRG').exclude(name = '5G-PSG')

        self.fields['delivery_centre'].queryset =BusinessUnit.objects.exclude(type__name = 'Customer').exclude(name = '5g India').exclude(name = '5g Canada').exclude(name = '5g Europe')

        self.fields['approved_by'].queryset = User.objects.filter(
                                        groups__name = 'Corporate Admin', is_active = True)
        
        self.fields['owner'].queryset = User.objects.filter(
                groups__name__icontains = 'Manager', is_active = True)
        self.fields['apex_body_owner'].queryset = User.objects.filter(
                groups__name__icontains = 'Corporate Admin', is_active = True)
        self.fields['project_owner'].queryset = User.objects.filter(
                groups__name__icontains = 'Project Owner', is_active = True)
        self.fields['customer'].queryset = BusinessUnit.objects.filter(type__name = 'Customer')
        if project:
            self.fields['requested_by'].queryset = User.objects.filter(pk
                                                     = project.requested_by_id)
        else:
            #self.fields['project_no'].initial = Project.objects.aggregate(
                                #Max('project_no'))['project_no__max']+1
            self.fields['requested_by'].queryset = User.objects.filter(
                                                                pk = user.pk)

    def save(self, schedules, is_approved,ex_approval, commit = True ):
        """
            Overriden save method to save virtual field
            which are not displayed to user
        """
                
        project = super(ProjectInitiationRequestForm, self).save(commit = False)
        project.schedules = schedules
        project.is_approved = is_approved
        project.ex_approval = ex_approval
        project.owner = project.requested_by
        project.short_name = project.name
        project.estimation_no = project.estimation_no
        project.proposal_name = project.proposal_name
        if is_approved:
            project.apex_body_owner = project.approved_by
            is_active  = True
            self.fields['project_no'].initial = Project.objects.aggregate(
                                Max('project_no'))['project_no__max']+1
            
        if commit:
            project.save()
        return project

class ProjectSchedulesRequestForm(forms.ModelForm):

    expected_start_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    expected_end_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    initiation_request_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, label = _('Requested On'))

    approved_date = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, label = _('Approved Date'))
    
    
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
        self.fields['approved_date'].initial = today
        
        if schedules:
            schedules.planned_start_date = schedules.expected_start_date
            schedules.planned_end_date = schedules.expected_end_date
            schedules.approved_date =  self.fields['approved_date'].initial          
            if not schedules.initiation_request_date:
                self.fields['initiation_request_date'].initial = today
                              
        else:
            self.fields['initiation_request_date'].initial = today        
