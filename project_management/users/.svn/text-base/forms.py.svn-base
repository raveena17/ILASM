"""
    Forms required by the user application.
"""
import os
from django.conf import settings
from django import forms
from django.contrib.auth.models import User, Group
from django.forms.forms import BoundField
from django.db.models import Max

from project_management.users.models import UserProfile, DocumentCheckList
from project_management.projects.models import ProjectRole
from project_management.business_unit.models import BusinessUnit


DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class':'vDateField'}

class UserProfileForm(forms.ModelForm):
    """
        Form which represents User profile models
    """
    date_of_birth = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    date_of_joining = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    passport_validity = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    date_of_confirmation = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    date_of_resignation = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    date_of_relieving = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    users_image = forms.ImageField(required = False)
    reporting_senior_name = forms.ModelChoiceField(queryset =  User.objects.filter(groups__name__icontains = 'Manager', is_active = True))


    def __init__(self, *args, **kwargs):
        """
            Overriden to remove Customer types in type
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        profile = kwargs.pop('instance', None)

        self.fields['type'].choices = UserProfile.EMPLOYEE_TYPES
        self.fields['business_unit'].queryset = BusinessUnit.objects.exclude(
                                                    type__name = 'Customer')
        self.fields['document_check_list'].queryset = DocumentCheckList.objects.all()

        self.destPath = settings.MEDIA_ROOT

    def save(self, user, address_contact, address_permanent, commit = True):
        """
            overriden to assign forign key fields
        """

        user_profile = super(UserProfileForm, self).save(commit = False)
        user_profile.user = user
        user_profile.address_contact = address_contact
        user_profile.address_permanent = address_permanent

        if user_profile.pk == None:
            user_profile.customer_code = '5GI'
            user_profile.reporting_senior =  user_profile.reporting_senior_name.username
            for business in self.cleaned_data['business_unit']:
                if str(business).startswith('5G Canada'):
                    auto_code = UserProfile.objects.filter(code__startswith='5GA')
                    if auto_code:
                        auto_code = UserProfile.objects.filter(code__startswith='5GA').order_by('-code')
                        codeDigits = auto_code[0].code.lstrip('5GA')
                        codeValue = int(codeDigits) + 1
                        if len(str(codeValue)) == 1:
                            user_profile.code = '5GA00' + str(codeValue)
                        elif len(str(codeValue)) == 2:
                            user_profile.code = '5GA0' + str(codeValue)
                        else:
                            user_profile.code = '5GA' + str(codeValue)
                    else:
                        user_profile.code = '5GA001'
                elif str(business).startswith('5G Europe'):
                    auto_code = UserProfile.objects.filter(code__startswith='5GE')
                    if auto_code:
                        auto_code = UserProfile.objects.filter(code__startswith='5GE').order_by('-code')
                        codeDigits = auto_code[0].code.lstrip('5GE')
                        codeValue = int(codeDigits) + 1
                        if len(str(codeValue)) == 1:
                            user_profile.code = '5GE00' + str(codeValue)
                        elif len(str(codeValue)) == 2:
                            user_profile.code = '5GE0' + str(codeValue)
                        else:
                            user_profile.code = '5GE' + str(codeValue)
                    else:
                        user_profile.code = '5GE001'
                elif str(business).startswith('5G India') or str(business).startswith('5G-CG') or str(business).startswith('5G-PCG') or str(business).startswith('5G-PDG') or str(business).startswith('5G-PRG') or str(business).startswith('5G-PSG') :

                    if self.cleaned_data['type'] == 'E':
                        auto_code = UserProfile.objects.filter(code__startswith='E')
                        if auto_code:
                            auto_code = UserProfile.objects.filter(code__startswith='E').order_by('-code')
                            codeDigits = auto_code[0].code.lstrip('E')
                            codeValue = int(codeDigits) + 1
                            if codeDigits.startswith('00'):
                                user_profile.code = 'E00' + str(codeValue)
                            elif codeDigits.startswith('0'):
                                user_profile.code = 'E0' + str(codeValue)
                            else:
                                user_profile.code = 'E' + str(codeValue)
                        else:
                            user_profile.code = 'E001'
                    elif self.cleaned_data['type'] == 'C':
                        auto_code = UserProfile.objects.filter(code__startswith='C')
                        if auto_code:
                            auto_code = UserProfile.objects.filter(code__startswith='C').order_by('-code')
                            codeDigits = auto_code[0].code.lstrip('C')
                            codeValue = int(codeDigits) + 1
                            if codeDigits.startswith('00'):
                                user_profile.code = 'C00' + str(codeValue)
                            elif codeDigits.startswith('0'):
                                user_profile.code = 'C0' + str(codeValue)
                            else:
                                user_profile.code = 'C' + str(codeValue)
                        else:
                            user_profile.code = 'C001'
                    elif self.cleaned_data['type'] == 'T':
                        auto_code = UserProfile.objects.filter(code__startswith='5GTR')
                        if auto_code:                           
                            auto_code = UserProfile.objects.filter(code__startswith='5GTR').order_by('-code')
                            codeDigits = auto_code[0].code.lstrip('5GTR')
                            codeValue = int(codeDigits) + 1
                            if len(str(codeValue)) == 1:
                                user_profile.code = '5GTR00' + str(codeValue)
                            elif len(str(codeValue)) == 2:
                                user_profile.code = '5GTR0' + str(codeValue)
                            else:
                                user_profile.code = '5GTR' + str(codeValue)
                        else:
                            user_profile.code = '5GTR001'

                    elif self.cleaned_data['type'] == 'TP':
                        auto_code = UserProfile.objects.filter(code__startswith='5GTP')
                        if auto_code:
                            auto_code = UserProfile.objects.filter(code__startswith='5GTP').order_by('-code')
                            codeDigits = auto_code[0].code.lstrip('5GTP')
                            codeValue = int(codeDigits) + 1
                            if len(str(codeValue)) == 1:
                                user_profile.code = '5GTP00' + str(codeValue)
                            elif len(str(codeValue)) == 2:
                                user_profile.code = '5GTP0' + str(codeValue)
                            else:
                                user_profile.code = '5GTP' + str(codeValue)
                        else:
                            user_profile.code = '5GTP001'

        if user_profile.pk != None:
            user_profile_img_check = UserProfile.objects.filter(pk = user_profile.pk)
            if len(user_profile_img_check) > 0:
                user_profile_img_check = user_profile_img_check[0]
            if user_profile_img_check.users_image != user_profile.users_image:
                user_profile.users_image = str(user_profile.user_id) + '_' + str(user_profile.user) + '.jpg'
                filename = str(self.cleaned_data['users_image'])
                fileType = filename[filename.rindex('.'):len(filename)]
                if not os.path.exists(self.destPath + '/user_images/'):
                    os.mkdir(self.destPath + '/user_images/')
                currentdir = self.destPath + '/user_images'

                fd = open('%s/%s' % (currentdir, user_profile.users_image), 'wb+')
                for chunk in self.cleaned_data['users_image'].chunks():
                    fd.write(chunk)
                fd.close()


        if commit == True:
            user_profile.save()
            print user_profile.reporting_senior
            user_profile.business_unit.clear()
            for each in self.cleaned_data['business_unit']:
                user_profile.business_unit.add(each)

            for each in self.cleaned_data['document_check_list']:
                user_profile.document_check_list.add(each)

        return user_profile

    class Meta:
        """
            Describes the configuration for the form.
        """
        model = UserProfile
        exclude = ('user', 'address_contact', 'address_permanent', 'is_confirmed')



class UserForm(forms.ModelForm):
    """
        Form which represents auth user
    """
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    def __init__(self, *args, **kwargs):
        """
            Overriden init method to remove the help text in username
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    def save(self, commit = True):
        """
            Overriden save method to add groups
        """
        user = super(UserForm, self).save(commit = False)
        user.set_unusable_password()
        if commit == True:
            user.save()
            user.groups.clear()
            for group in self.cleaned_data['groups']:
                user.groups.add(group)
        return user

    def __init__(self, *args, **kwargs):
        """
            Overriden init method to give Group queryset
        """
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['groups'].queryset = Group.objects.exclude(pk__in
            = [ role.group.pk for role in ProjectRole.objects.all()])

    class Meta:
        """
            Describes the configuration for the form.
        """
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'groups')

class MyProfileForm(forms.ModelForm):
    """
        Form which represents my profile
    """
    date_of_birth = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    passport_validity = forms.DateField(input_formats = [DATE_INPUT_FORMAT],
        required = False, widget = forms.TextInput(attrs = DATE_FIELD_ATTR))

    class Meta:
        """
            Describes the configuration for the form.
        """
        model = UserProfile
        exclude = ('date_of_joining', 'user', 'business_unit',
            'address_contact', 'address_permanent', 'salutation',
            'code', 'type', 'designation', 'gender','confirmation_status','is_confirmed', 'date_of_confirmation', 'probation_end_date',
            'probation_period', 'document_check_list','date_of_resignation', 'date_of_relieving', 'document_check_list_others', 'division', 'comments')

    def save(self, address_contact, address_permanent, commit = True):
        """
            overriden to assign forign key fields
        """
        user_profile = super(MyProfileForm, self).save(commit = False)
        user_profile.address_contact = address_contact
        user_profile.address_permanent = address_permanent

        if commit == True:
            user_profile.save()
        return user_profile

__init__temp = BoundField.__init__

def __my_init__(self, form, field, name):
    """
        add '*' to all manadatory field.
    """
    __init__temp(self, form, field, name)
    if self.field.required:
        self.label += '*'
BoundField.__init__ = __my_init__
