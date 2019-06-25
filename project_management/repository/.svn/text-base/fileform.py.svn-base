"""
    file forms for Repository
"""
from django import forms

class FileUploadForm(forms.Form):
    """ form to upload the file in repository """
    fileUploaded = forms.FileField()

    def clean_image(self):
        return self.cleaned_data['fileUploaded']
