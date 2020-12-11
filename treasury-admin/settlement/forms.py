
from dal import autocomplete
from django import forms

from .models import *

class TreasuryPositionForm(forms.ModelForm):

  class Meta:
    model = TreasuryPosition
    fields = ('__all__')
    widgets = {

      'corresp': autocomplete.ModelSelect2(url='corresp-autocomplete',
                                           forward=['nature']),   

      'account': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                           forward=['corresp'])
    }