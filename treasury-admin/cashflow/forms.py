
from dal import autocomplete, forward
from django import forms
#
from .models import *

class CashFlowDetailForm(forms.ModelForm):

  class Meta:
        
    model = CashFlowDetail
    fields = ('__all__')
    widgets = {
      'account': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                           forward=['corresp']),
      
      'sygmaCtrl': autocomplete.ModelSelect2(url='sygma-autocomplete',
                                             forward=(forward.Field('date_pay', 'date_val'),)),  
 }
