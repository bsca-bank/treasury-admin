from dal import autocomplete, forward
from django import forms
#
from django.contrib.admin.helpers import ActionForm
from django.forms.models import BaseInlineFormSet

from .models import Tiers
from .client.models import ClientCtrl, ClientFileStorage
from .corresp.models import Corresp



class ClientCtrlForm(forms.ModelForm):
  
    class Meta:
      model = ClientCtrl
      fields = ('__all__')
      widgets = {
     
        'type_client': autocomplete.ModelSelect2(url='catalogTypeTiers-autocomplete',
                                            forward=(
                                              forward.Const('tiers','app_label'),
                                              forward.Const('ClientCtrl','model'),
                                              )),

        'oper': autocomplete.ModelSelect2(url='user-autocomplete',
                                          forward=(forward.Const(True,'request_user'),
                                          )),
      } 

class CorrespForm(forms.ModelForm):

  class Meta:
    model = Corresp
    fields = ('__all__')
    widgets = {
      'clientCtrl': autocomplete.ModelSelect2(url='client-autocomplete'),     
    }  

class TiersForm(forms.ModelForm):

  class Meta:
    model = Tiers
    fields = ('__all__')
    widgets = {
      'clientCtrl': autocomplete.ModelSelect2(url='client-autocomplete'),     
    }  

class ClientFileStorageForm(forms.ModelForm):

  class Meta:
    model = ClientFileStorage
    fields = ('__all__')  
    widgets = {
        'type_file': autocomplete.ModelSelect2(url='catalogTypeFile-autocomplete',
                                        forward=(forward.Field('content_type','content_type'),  
                                        )),     
    }  

class ClientFileStorageGenericInlineForm(forms.ModelForm):
  class Meta:
    model = ClientFileStorage
    fields = ('__all__')
    widgets = {
        'type_file': autocomplete.ModelSelect2(url='catalogTypeFile-autocomplete',
                                  forward=(forward.Field('content_type','content_type'),  
                                  )),     
    }  