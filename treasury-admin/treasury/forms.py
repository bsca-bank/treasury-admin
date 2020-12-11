from dal import autocomplete,forward
from django import forms
#
from django.contrib.admin.helpers import ActionForm
from .models import *


from .models import *

class MMForm(forms.ModelForm):

  class Meta:
    model = MM
    fields = ('__all__')
    widgets = {
      
      'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                      forward=(
                                          forward.Const('treasury','app_label'),
                                          forward.Const('mm','model'),
                                          )),

      'docTraceLog': autocomplete.ModelSelect2(url='docTraceLog-autocomplete',
                                          forward=(
                                            forward.Field('id','object_id'),
                                            forward.Const('treasury','app_label'),
                                            forward.Const('mm','model'),
                                            )),

      'corresp': autocomplete.ModelSelect2(url='corresp-autocomplete'),
        
      'account': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                           forward=['corresp'])
    }  
    
class FXForm(forms.ModelForm):

  class Meta:
    model = MM
    fields = ('__all__')
    widgets = {

      'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                      forward=(
                                          forward.Const('treasury','app_label'),
                                          forward.Const('fx','model'),
                                          )),

      'client': autocomplete.ModelSelect2(url='client-autocomplete'),   

      'corresp_in': autocomplete.ModelSelect2(url='corresp-autocomplete'),

      'corresp_out': autocomplete.ModelSelect2(url='corresp-autocomplete'),  

      'account_in': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                              forward=(forward.Field('corresp_in', 'corresp'),)),

      'account_out': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                               forward=(forward.Field('corresp_out', 'corresp'),)),

      'docTraceLog': autocomplete.ModelSelect2(url='docTraceLog-autocomplete',
                                          forward=(
                                            forward.Field('id','object_id'),
                                            forward.Const('treasury','app_label'),
                                            forward.Const('fx','model'),
                                            )),                                 
    }  
    
class FXCliForm(forms.ModelForm):

    class Meta:
      model = FXCli
      fields = ('__all__')
      widgets = {
        
        'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                        forward=(
                                            forward.Const('treasury','app_label'),
                                            forward.Const('fxcli','model'),
                                            )),

        'client': autocomplete.ModelSelect2(url='client-autocomplete'),    


        'corresp_in': autocomplete.ModelSelect2(url='corresp-autocomplete'),
        
        'corresp_out': autocomplete.ModelSelect2(url='corresp-autocomplete'),  

        'account_in': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                                forward=(forward.Field('corresp_in', 'corresp'),)),
        
        'account_out': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                                 forward=(forward.Field('corresp_out', 'corresp'),)),

        'docTraceLog': autocomplete.ModelSelect2(url='docTraceLog-autocomplete',
                                            forward=(
                                              forward.Field('id','object_id'),
                                              forward.Const('treasury','app_label'),
                                              forward.Const('fxcli','model'),
                                              )),                                                        
      }  


    
class FIForm(forms.ModelForm):

  class Meta:
    model = FI
    fields = ('__all__')
    widgets = {

      'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                      forward=(
                                          forward.Const('treasury','app_label'),
                                          forward.Const('fi','model'),
                                          )),

       'client': autocomplete.ModelSelect2(url='client-autocomplete'),    

      'docTraceLog': autocomplete.ModelSelect2(url='docTraceLog-autocomplete',
                                          forward=(
                                            forward.Field('id','object_id'),
                                            forward.Const('treasury','app_label'),
                                            forward.Const('fi','model'),
                                            )),                                 
    }  