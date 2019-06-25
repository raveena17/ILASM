"""
    Forms for customers.
"""
from django import forms
from django.contrib.auth.models import User

from project_management.business_unit.models import BusinessUnit, BusinessUnitType
from project_management.business_unit.forms import BusinessUnitForm
from project_management.users.models import UserProfile

import datetime

class CustomerForm(forms.ModelForm):
    """
        Form representing customer.
    """
    def save(self, address, commit=True):
        customer = super(CustomerForm, self).save(commit = False)
        customer.address = address
        customer.type = BusinessUnitType.objects.get(name = 'Customer')
        if commit:
            customer.save()
        return customer

    class Meta:
        model = BusinessUnit
        exclude = ('cancel', 'address', 'type')

class CustomerContactProfileForm(forms.ModelForm):
    """
        Form representing customer contact profile.
    """
    business_unit = forms.ModelChoiceField(queryset
        = BusinessUnit.objects.filter(type__name = 'Customer'),
        label = 'Customer')

#    def __init__(self, *args, **kwargs):
#        super(self.__class__, self).__init__(*args, **kwargs)
#        customer_profile = getattr(self, 'instance', None)
#        if customer_profile:
#            self.fields['business_unit'].initial = customer_profile.business_unit.all()[0].pk

    def save(self, address, contact, commit=True):
        contact_profile = super(CustomerContactProfileForm, self).save(commit=False)
        contact_profile.address_contact = address
        contact_profile.user = contact
        contact_profile.type = 'CC'
        if commit:
            contact_profile.save()
            contact_profile.business_unit.clear()
            contact_profile.business_unit.add(self.cleaned_data['business_unit'])
            print contact_profile.business_unit.all()
        return contact_profile

    class Meta:
        model = UserProfile
        fields = ('salutation', 'designation', 'business_unit', 'phone_office',
            'phone_office_extension', 'phone_mobile')

class CustomerContactForm(forms.ModelForm):
    """
        Form representing customer contact.
    """
    
    def save(self, commit=True):
        user = super(CustomerContactForm, self).save(commit = False)
        user.username = self.generate_username(user.first_name)
        user.is_active = False
        if commit:
            user.save()
        return user

    def generate_username(self, first_name):
        username = first_name[:14] + str(datetime.datetime.now())[:16]
        if User.objects.filter(username = username).count() > 0:
            username = first_name[:11] + str(datetime.datetime.now())[:19]
        return username

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        

class ClientForm(forms.ModelForm):
    """
        form which represents the business unit.
    """
    name = forms.CharField(label='Client Company Name')
    firstname = forms.CharField(label='Client Contact FirstName')
    lastname =  forms.CharField(label='Client Contact LastName', required = False)
    
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = BusinessUnitType.objects.filter(name
                                                                = 'Customer')
        self.fields['related_to'].queryset = BusinessUnit.objects.exclude(type__name = 'Customer')
    def save(self, address, commit = True):
        business_unit = super(ClientForm, self).save(commit = False)
        business_unit.address = address
        
        if commit:
            business_unit.save()
        return business_unit

    class Meta:
        model = BusinessUnit
        exclude = ('cancel', 'address',  'customer_code', 'is_active')        
