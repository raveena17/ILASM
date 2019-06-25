"""
    Business Unit forms
"""
from django import forms

from project_management.business_unit.models import BusinessUnit, \
                                                BusinessUnitType

class BusinessUnitForm(forms.ModelForm):
    """
        form which represents the business unit.
    """
    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = BusinessUnitType.objects.exclude(name
                                                                = 'Customer')

    def save(self, address, commit = True):
        business_unit = super(BusinessUnitForm, self).save(commit = False)
        business_unit.address = address
        business_unit.related_to = BusinessUnit.objects.get(pk = '1')
        if commit:
            business_unit.save()
        return business_unit

    class Meta:
        model = BusinessUnit
        exclude = ('cancel', 'address', 'related_to', 'customer_code', 'firstname', 'lastname', 'contact_email', 'is_active')
