from django import forms

class ImportForm(forms.Form):
    docfile = forms.FileField(
        label='Select a google file to import',
        help_text='xml'
    )
