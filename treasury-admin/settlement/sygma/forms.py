
from dal import autocomplete
from django import forms
#
from .models import SygmaCtrl

class SygmaForm(forms.ModelForm):

  class Meta:
    model = SygmaCtrl
    fields = ('__all__')
    widgets = {
      'corresp': autocomplete.ModelSelect2(url='corresp-autocomplete',
                                           forward=['nature']),      
      'account': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                           forward=['corresp'])
    }
