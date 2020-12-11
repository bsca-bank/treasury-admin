from dal import autocomplete, forward
from django import forms

#
from django.contrib.admin.helpers import ActionForm
from .sca.models import Meeting, MeetingItem, MeetingDoc


import re

class UpdateDateActionForm(ActionForm):
  date = forms.DateField(widget=forms.SelectDateWidget)
  
class UpdateTextActionForm(ActionForm):
  text = forms.IntegerField()  


class MeetingForm(forms.ModelForm):

    class Meta:
      model = Meeting
      fields = ('__all__')
      widgets = {
            'name_fr': forms.Textarea(attrs={'rows':3, 'cols':45}),
            'name_cn': forms.Textarea(attrs={'rows':3, 'cols':45}),
            'obs': forms.Textarea(attrs={'rows':3, 'cols':45})
      } 

class MeetingItemForm(forms.ModelForm):

    class Meta:
      model = MeetingItem
      fields = ('__all__')
      widgets = {
            'ref_no': forms.Textarea(attrs={'rows':1, 'cols':3}),
            'name_fr': forms.Textarea(attrs={'rows':3, 'cols':45}),
            'name_cn': forms.Textarea(attrs={'rows':3, 'cols':45}),
            'obs': forms.Textarea(attrs={'rows':3, 'cols':45})
      } 

class MeetingDocForm(forms.ModelForm):

    class Meta:
      model = MeetingDoc
      fields = ('__all__')
      widgets = {
        #
        'name_fr': forms.Textarea(attrs={'rows':2, 'cols':30}),
        'name_cn': forms.Textarea(attrs={'rows':2, 'cols':30}),
        'obs': forms.Textarea(attrs={'rows':2, 'cols':45})

      } 

class MeetingDocShortForm(forms.ModelForm):

    class Meta:
      model = MeetingDoc
      fields = ('__all__')
      widgets = {
        #
        'name_fr': forms.Textarea(attrs={'rows':4, 'cols':30}),
        'name_cn': forms.Textarea(attrs={'rows':4, 'cols':30}),

      } 