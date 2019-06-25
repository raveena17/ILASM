from django import forms


class Password_reset_form(forms.Form):

    old_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'your old Password',  'class' : 'span'}))
    new_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'New Password',  'class' : 'span'}))
    confirm_password = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'type':'password', 'placeholder':'Confirm New Password',  'class' : 'span'}))