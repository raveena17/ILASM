from django import forms
from .models import Reimbursement_new, BudgetType, User, Allowance,ReimbursementType, ReimbursementStatus
from project_management.users.models import UserProfile
from project_management.client_visit_report.models import ClientVisitReport
from django.forms import widgets, BaseInlineFormSet
from django.forms.models import inlineformset_factory

DATE_INPUT_FORMAT = '%m-%d-%Y'
DATE_FIELD_ATTR = {'class': 'vDateField'}


class Filter(forms.Form):

	status = forms.ModelChoiceField(queryset=ReimbursementStatus.objects.all(), required=False)
	def __init__(self, *args, **kwargs):
		
		super(Filter, self).__init__(*args, **kwargs)


class ReimbursementModelForm(forms.ModelForm):
 
	name = forms.ModelChoiceField(queryset=User.objects.filter(is_active=1))
	status = forms.ModelChoiceField(queryset=ReimbursementStatus.objects.all(), required=False)
	# bill_location = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
	# type = forms.ModelChoiceField(queryset=ReimbursementType.objects.all())
	client_visit_report = forms.CharField(widget=forms.HiddenInput(), label='', required=False)

	def __init__(self,user, *args, **kwargs):
		row = kwargs.pop('row')

		super(ReimbursementModelForm, self).__init__(*args, **kwargs)

		self.fields['total_amount'].widget.attrs['readonly'] = 'readonly'
		self.fields['special_approval'].widget.attrs['readonly'] = True		
		self.fields['status'].empty_label = None
		# self.fields['bill_location'].required = False
		self.fields['notes'].required = False
		# self.fields['bill_location'].label = "Bills"
		reporting_senior_name = UserProfile.objects.get(user=user).reporting_senior_name
		# import pdb;pdb.set_trace()
		if not self.instance.id:
			self.initial['name'] = user
			self.initial['status'] = ReimbursementStatus.objects.get(status='Pending').id
			if row == None:
				self.fields['approver'].queryset = User.objects.filter(groups__name='Manager', is_active=True).exclude(username=user.username)
				reporting_senior_name = UserProfile.objects.get(user=user).reporting_senior_name
				self.initial['approver'] = reporting_senior_name.id
				self.initial['type'] = ReimbursementType.objects.get(id=1)
			else:
				self.initial['type'] = ReimbursementType.objects.get(id=1)
		else:
			self.fields['approver'].queryset = User.objects.filter(id=self.instance.approver.id)
			# self.initial['name'] = self.instance.name
			self.fields['name'].initial = self.instance.name
			self.initial['approver'] = self.instance.approver
			reimbursement = Reimbursement_new.objects.get(id=self.instance.id)
			self.initial['approver'] = self.instance.approver
			if self.instance.name.id == user.id:
				if self.instance.status.status == 'Pending':
					# if row == 'Add Row':
					self.initial['name'] = self.instance.name
					# self.fields['name'].initial = self.instance.name
					self.fields['approver'].queryset = User.objects.filter(groups__name='Manager', is_active=True).exclude(username=user.username)
					self.fields['status'].disabled = True
				else:
					self.fields['approver'].disabled = True
					self.fields['status'].disabled = True
					self.fields['type'].disabled = True

			elif self.instance.approver.id == user.id:
				if user.groups.filter(name__in=['Corporate Admin']).exists() :
					if self.instance.status.status == 'Approved':
						self.fields['status'].queryset = ReimbursementStatus.objects.filter(status__in=['Approved', 'Verified'])
					if self.instance.status.status == 'Verified':
						self.fields['status'].queryset = ReimbursementStatus.objects.filter(status__in=['Processed', 'Verified'])
					if self.instance.status.status in ['Approved', 'Verified']:
						self.fields['approver'].disabled = False
						self.fields['status'].disabled = False
						self.fields['type'].disabled = True
						self.fields['special_approval'].disabled = True
					else:
						self.fields['approver'].disabled = True
						self.fields['status'].disabled = True
						self.fields['type'].disabled = True
						self.fields['special_approval'].disabled = True
				else:
					self.fields['approver'].disabled = True
					self.fields['status'].disabled = True
					self.fields['type'].disabled = True
					self.fields['special_approval'].disabled = True
			else:
				if self.instance.status.status == 'Approved':
					self.fields['status'].queryset = ReimbursementStatus.objects.filter(status__in=['Approved', 'Verified'])
				if self.instance.status.status == 'Verified':
					self.fields['status'].queryset = ReimbursementStatus.objects.filter(status__in=['Processed', 'Verified'])
				if self.instance.status.status in ['Approved', 'Verified']:
					self.fields['status'].disabled = False
					self.fields['type'].disabled = True
					self.fields['special_approval'].disabled = True
				else:
					self.fields['approver'].disabled = True
					self.fields['status'].disabled = True
					self.fields['type'].disabled = True
					self.fields['special_approval'].disabled = True
					

	class Meta:

		model = Reimbursement_new
		exclude = ('created_on', 'details','approved_on', 'processed_on')
		widgets = {
	        'notes':forms.Textarea(attrs={'rows':4, 'cols':24}),
	        'total_amount':forms.NumberInput(attrs={'placeholder':0}),
	        # 'bill_location':forms.FileInput(attrs={'required':False}),
	        }  



class Reimbursement_form(forms.Form):

	report = forms.ModelChoiceField(queryset=ClientVisitReport.objects.none(), required=False)

	def __init__(self, *args, **kwargs):
		
		super(Reimbursement_form, self).__init__(*args, **kwargs)

class ClientVisitReport_Form(forms.Form):

	prepared_by = forms.CharField(required=False)
	client_name = forms.CharField(required=False)
	visit_location = forms.CharField(required=False)
	from_date = forms.CharField(required=False)
	to_date = forms.CharField(required=False)
	status = forms.CharField(required=False)

	def __init__(self, *args, **kwargs):

		super(ClientVisitReport_Form, self).__init__(*args, **kwargs)
		self.fields['prepared_by'].widget.attrs['readonly'] = 'readonly'
		self.fields['client_name'].widget.attrs['readonly'] = 'readonly'
		self.fields['visit_location'].widget.attrs['readonly'] = 'readonly'
		self.fields['from_date'].widget.attrs['readonly'] = 'readonly'
		self.fields['to_date'].widget.attrs['readonly'] = 'readonly'
		self.fields['status'].widget.attrs['readonly'] = 'readonly'
		self.fields['status'].widget.attrs['class'] = 'status'
		self.fields['status'].widget.attrs['id'] = 'cvr_status'

class AllowanceForm(forms.ModelForm):

    reimbursement = forms.ModelChoiceField(queryset=BudgetType.objects.all())
    bill_location = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), label='Upload Bill')
    # import pdb;pdb.set_trace()
    # budget = forms.NumberInput(attrs={'disabled':True})
    # reimbursement_type = forms.ModelChoiceField(queryset=ReimbursementType.objects.all(), initial=0)

    class Meta:
        model = Allowance
        fields = "__all__"
        widgets = {
            'date' : forms.TextInput(attrs={'class':'datepicker'}),
            'expenditure':forms.NumberInput(attrs={'class': 'expenditure', 'rows':3, 'cols':25}),
            'description':forms.Textarea(attrs={'rows':1, 'cols':25, 'class':'description','required':False}),
            'category':forms.Select(attrs={'class':'category','rows':1, 'cols':10}),
            'budget':forms.NumberInput(attrs={'class':'budget', 'disabled':True, 'required':False}),
            'bill_availability':forms.CheckboxInput(attrs={'class':'bill_availability'}),
            'bill_location':forms.FileInput(attrs={'class':'upload_bill'}),
            }

class BaseFormSet(BaseInlineFormSet):

    def __init__(self, user, *args, **kwargs):
		super(BaseFormSet, self).__init__(*args, **kwargs)

		# self.fields['bill_availability'].label = "Bills"

		for form in self.forms:
			form.fields['description'].required = False
			form.fields['bill_location'].required = False
		if self.instance.id:
			if self.instance.name.id == user.id:
				if self.instance.status.status != 'Pending':
					self.disable_field()
			elif self.instance.approver.id == user.id:
				if user.groups.filter(name__in=['Corporate Admin']).exists() :
					self.disable_field()
					for form in self.forms:
						if self.instance.status.status in ['Approved']:
							form.fields['bill_checking'].disabled = False
						else:
							form.fields['bill_checking'].disabled = True

				else:
					self.disable_field()
					for form in self.forms:
						form.fields['bill_checking'].disabled = True
			else:
				self.disable_field()
				for form in self.forms:
					if self.instance.status.status in ['Approved']:
						form.fields['bill_checking'].disabled = False
					else:
						form.fields['bill_checking'].disabled = True
			
			# reimbursement = Reimbursement.objects.get(id=self.instance.id)
			# if reimbursement.name == user:
			# 	if reimbursement.status.status != 'Pending':
			# 		self.disable_field()
			# else:
			# 	self.disable_field()            

    def disable_field(self):
        for form in self.forms:
			form.fields['date'].disabled = True
			form.fields['category'].disabled = True
			form.fields['expenditure'].disabled = True
			form.fields['description'].disabled = True
			form.fields['bill_availability'].disabled = True
			# form.fields['bill_availability'].disabled = True		



allowanceInlineFormSet = inlineformset_factory(Reimbursement_new, Allowance, formset=BaseFormSet, form=AllowanceForm, extra=1)

        