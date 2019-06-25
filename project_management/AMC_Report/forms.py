from django import forms

from project_management.AMC_Report.models import *



class NumberInput(forms.NumberInput):

    input_type = 'number'


class AMCForm(forms.ModelForm):
    """
        form which represents the business unit.
    """

    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(self.__class__, self).__init__(*args, **kwargs)
    
    def save(self, address, commit=True):
        AMC_Report = super(AMCForm, self).save(commit=False)
        
        if commit:
          today = datetime.date.today()
          self.instance.amc_created_date = today
          AMC_Report.save()
        return AMC_Report

    class UploadFileForm(forms.Form):
        file = forms.FileField()

    

    class Meta:
            model = ReportAMC1
            exclude = ('is_active','amc_created_date',)
            widgets = {
                'frequency': NumberInput()
            }



class AMCHistoryForm(forms.ModelForm):

   
    def save(self, commit=True):
        Amc_history_form = super(AMCHistoryForm, self).save(commit=commit)        
        return Amc_history_form

    class Meta:
        model = AmcHistory
        exclude = ('amc_created_date','amc_renewal_date','amc_id')

