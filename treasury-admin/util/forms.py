from dal import autocomplete, forward
from django import forms
#
from django.contrib.admin.helpers import ActionForm
from .catalog.models import CatalogTypeCommercial, CatalogTypeProduct
from .workflow.models import Workflow, Statut


class DocTraceLogDetailForm(forms.ModelForm):
    class Meta:
      model = Statut
      fields = ('__all__')
      widgets = {
        'content_type': autocomplete.ModelSelect2(url='contentType-autocomplete'),
      } 

class StatutForm(forms.ModelForm):
    class Meta:
      model = Statut
      fields = ('__all__')
      widgets = {
        'content_type': autocomplete.ModelSelect2(url='contentType-autocomplete'),
      } 

class WorkflowForm(forms.ModelForm):
    class Meta:
      model = Workflow
      fields = ('__all__')
      widgets = {
        'content_type': autocomplete.ModelSelect2(url='contentType-autocomplete'),

        's_init': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(forward.Field('content_type','ctype',),
                                            )), 

        's_fnl': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(forward.Field('content_type','ctype',),
                                            )), 
      } 

class CatalogTypeProductForm(forms.ModelForm):
    class Meta:
      model = CatalogTypeProduct
      fields = ('__all__')
      widgets = {
        'content_type': autocomplete.ModelSelect2(url='contentType-autocomplete'),
      } 

class CatalogTypeCommercialForm(forms.ModelForm):
    class Meta:
      model = CatalogTypeCommercial
      fields = ('__all__')
      widgets = {
        'parent_type': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                                forward=(forward.Field('nature','nature'),
                                                         forward.Field('level', 'level'), 
                                                         )), 
      } 