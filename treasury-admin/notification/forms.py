from dal import autocomplete, forward
from django import forms
#
from django.contrib.admin.helpers import ActionForm
from django.forms.models import BaseInlineFormSet

#
from .models import EmailCtrl, EmailTemplate


class EmailForm(forms.ModelForm):

    class Meta:
      model = EmailCtrl
      fields = ('__all__')
      widgets = {
            'cc_email': forms.Textarea(attrs={'rows':3, 'cols':85}),
            'subject': forms.Textarea(attrs={'rows':2, 'cols':85}),
            'body': forms.Textarea(attrs={'rows':10, 'cols':85}),
      } 


class EmailTemplateForm(forms.ModelForm):

    class Meta:
      model = EmailTemplate
      fields = ('__all__')
      widgets = {
            'cc_email': forms.Textarea(attrs={'rows':3, 'cols':85}),
            'subject': forms.Textarea(attrs={'rows':2, 'cols':85}),
            'body': forms.Textarea(attrs={'rows':10, 'cols':85}),

            'content_type': autocomplete.ModelSelect2(url='contentType-autocomplete'),     
      } 