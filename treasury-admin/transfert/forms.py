from dal import autocomplete, forward
from django import forms

#
from django.contrib.admin.helpers import ActionForm
from .models import *
from .proxys import *

import re

class UpdateDateActionForm(ActionForm):
  date = forms.DateField(widget=forms.SelectDateWidget)
  
class UpdateTextActionForm(ActionForm):
  text = forms.IntegerField()  

class DomDossierCtrlForm(forms.ModelForm):

    #use regex to clean DI reference
    def clean_ref_di(self):
        ref_di = self.cleaned_data['ref_di']
        nomenc = self.cleaned_data['nomenc_lv0']
        if nomenc == 35 and not re.match('[A-Z][A-Z][A-Z]?\-\d',ref_di):
            raise forms.ValidationError("Saisie REF_DI commence par 'DI-','TI-' ou 'ASI-'")
        if nomenc == 35 and len(ref_di) > 11:
            raise forms.ValidationError("Saisie REF_DI en 11 caractère MAX")
        return ref_di

    class Meta:
      model = DomDossierCtrl
      fields = ('__all__')
      widgets = {

        'statut': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(
                                              forward.Const('transfert','app_label'),
                                              forward.Const('DomDossierCtrl','model'),
                                              )),

        'nomenc_lv0': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                      forward=(
                                          forward.Const(['Import','Export'],'nature'),
                                          forward.Const(True,'include'),
                                          forward.Const(True,'turple'),
                                        )),   

        'client': autocomplete.ModelSelect2(url='client-autocomplete'),

        'ccy': autocomplete.ModelSelect2(url='ccy-autocomplete',
                                        forward=(
                                          forward.Const(['EUR','USD','CNY',],'iso'),  
                                          forward.Const(True, 'include'), 
                                        )),     

        'ccy_lc': autocomplete.ModelSelect2(url='ccy-autocomplete',
                                    forward=(
                                        forward.Const(['XAF',], 'iso'),  
                                        forward.Const(True, 'include'), 
                                    )), 

        'oper_verify': autocomplete.ModelSelect2(url='user-autocomplete'),
        
        'oper_approv': autocomplete.ModelSelect2(url='user-autocomplete'),


      } 

class TrfDossierExecForm(forms.ModelForm):

    class Meta:
      model = TrfDossierExec
      fields = ('__all__')
      widgets = {

        'trfDossier': autocomplete.ModelSelect2(url='dossier_ctrl-autocomplete'),

      } 

class TrfDossierCtrlForm(forms.ModelForm):

    def clean_cpty(self):
        cpty = self.cleaned_data['cpty']
        if not cpty:
            raise forms.ValidationError("Saisie Contrepartie, c'est le bénéficiaire pour TRF/VIR et donneur d'ordre pour RPT")
        return self.cleaned_data['cpty']

    class Meta:
      model = TrfDossierCtrl
      fields = ('__all__')
      widgets = {

        'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                        forward=(
                                            forward.Const('transfert','app_label'),
                                            forward.Const('TrfDossierCtrl','model'),
                                            )),

        'client': autocomplete.ModelSelect2(url='client-autocomplete'),        


        'ccy': autocomplete.ModelSelect2(url='ccy-autocomplete',
                                        forward=(
                                          forward.Const(['XAF',], 'iso'),  
                                          forward.Const(False, 'include'), 
                                        )),     

        'dossier_dom': autocomplete.ModelSelect2(url='dossier_dom-autocomplete',
                                                forward=(
                                                  forward.Field('client', 'client'),  
                                                  forward.Field('nomenc_lv0', 'nomenc_lv0'),
                                                )),

        'dossier_couvr': autocomplete.ModelSelect2(url='dossier_couvr-autocomplete'),  

        'dossier_rtroc': autocomplete.ModelSelect2(url='dossier_couvr-autocomplete'),   

        'docTraceLog': autocomplete.ModelSelect2(url='docTraceLog-autocomplete',
                                            forward=(
                                              forward.Field('id','object_id'),
                                              forward.Const('transfert','app_label'),
                                              forward.Const('TrfDossierCtrl','model'),
                                              )),

        'statut': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(
                                              forward.Const('transfert','app_label'),
                                              forward.Const('TrfDossierCtrl','model'),
                                              )),

        'nomenc_lv0': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                      forward=(
                                          forward.Const(['Export','F.CFA'],'nature'),
                                          forward.Const(False,'include'),
                                          forward.Const(True,'turple'),
                                        )),       

        'nomenc_lv1': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                                forward=(forward.Field('nomenc_lv0', 'parent_type'),)), 

        'corresp': autocomplete.ModelSelect2(url='corresp-autocomplete'),
        'account': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                              forward=['corresp']),

        'oper_input': autocomplete.ModelSelect2(url='user-autocomplete'),

        'oper_verify': autocomplete.ModelSelect2(url='user-autocomplete'),
        
        'oper_approv': autocomplete.ModelSelect2(url='user-autocomplete'),

        'bkdopi': autocomplete.ModelSelect2(url='bkdopi-autocomplete'),   
      } 

class TrfDossierCtrlProxyForm(forms.ModelForm):
  
    def clean_nomenc_lv0(self):
        nomenc_lv0 = self.cleaned_data['nomenc_lv0']
        chk_recv = self.cleaned_data['chk_recv']
        if nomenc_lv0 and not chk_recv:
            raise forms.ValidationError("chk_recv requis")
        return nomenc_lv0

    def clean_type_fund(self):
        type_fund = self.cleaned_data['type_fund']
        chk_verify = self.cleaned_data['chk_verify']
        chk_fund = self.cleaned_data['chk_fund']
        #
        if type_fund and not chk_verify:
            raise forms.ValidationError("chk_verify requis")
        if type_fund and not chk_fund:
            raise forms.ValidationError("chk_fund requis")
        return type_fund

    def clean_bkdopi(self):
        #
        chk_exec = self.cleaned_data['chk_exec']
        ref_exec = self.cleaned_data['ref_exec']
        bkdopi = self.cleaned_data['bkdopi']
        if ref_exec:
            is_ref_exec = (len(ref_exec) > 0)
        else:
            is_ref_exec = None   
        #
        if chk_exec and is_ref_exec:
             if not bkdopi:
                raise forms.ValidationError("Saisie Bkodopi!")
        return bkdopi

    class Meta:
      model = TrfDossierCtrlProxy
      fields = ('__all__')
      widgets = TrfDossierCtrlForm.Meta.widgets.copy()
      widgets.update({

        'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                        forward=(
                                            forward.Const('transfert','app_label'),
                                            forward.Const('TrfDossierCtrlProxy','model'),
                                            )),
      })

class RptDossierCtrlForm(TrfDossierCtrlForm):

    #use regex to clean DI reference
    def clean_ref_swift(self):
        ref_swift = self.cleaned_data['ref_swift']
        if not ref_swift:
            raise forms.ValidationError("Saisie ref_swift dans le message swift")
        return ref_swift

    def clean_bkdopi(self):
        #
        chk_exec = self.cleaned_data['chk_exec']
        ref_exec = self.cleaned_data['ref_exec']
        bkdopi = self.cleaned_data['bkdopi']
        if ref_exec:
            is_ref_exec = (len(ref_exec) > 0)
        else:
            is_ref_exec = None   
        #
        if chk_exec and is_ref_exec:
             if not bkdopi:
                raise forms.ValidationError("Saisie Bkodopi!")
        return bkdopi


    class Meta(TrfDossierCtrlForm.Meta):
      model = RptDossierCtrlProxy
      fields = ('__all__')
      widgets = TrfDossierCtrlForm.Meta.widgets.copy()
      widgets.update({

        'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                        forward=(
                                            forward.Const('transfert','app_label'),
                                            forward.Const('RptDossierCtrlProxy','model'),
                                            )),

        'nomenc_lv0': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                    forward=(
                                        forward.Const(['Import','F.CFA'],'nature'),
                                        forward.Const(False,'include'),
                                        forward.Const(True,'turple'),
                                        )),       
      })

class VirDossierCtrlForm(TrfDossierCtrlForm):
    #use regex to clean DI reference
    def clean_msg_payment(self):
        date_val = self.cleaned_data['date_val']
        if date_val and not self.cleaned_data['msg_payment']:
            raise forms.ValidationError("Saisie msg_payment")
        return self.cleaned_data['msg_payment']

    class Meta(TrfDossierCtrlForm.Meta):
      model = VirDossierCtrlProxy
      fields = ('__all__')
      widgets = TrfDossierCtrlForm.Meta.widgets.copy()
      widgets.update({

          'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                            forward=(
                                                forward.Const('transfert','app_label'),
                                                forward.Const('VirDossierCtrlProxy','model'),
                                                )),

          'ccy': autocomplete.ModelSelect2(url='ccy-autocomplete',
                                        forward=(
                                          forward.Const(['XAF',], 'iso'),  
                                          forward.Const(True, 'include'), 
                                        )), 
          'nomenc_lv0': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                        forward=(
                                          forward.Const('F.CFA','nature'),
                                          forward.Const(True,'include'),
                                          )),  
          'msg_payment': autocomplete.ModelSelect2(url='sygma-autocomplete',
                                          forward=(forward.Field('date_val', 'date_val'),)),           
      })

class CredocDossierCtrlForm(TrfDossierCtrlForm):

    #use regex to clean DI reference
    def clean_type_product(self):
        type_product = self.cleaned_data['type_product']
        if not type_product:
            raise forms.ValidationError("Saisie type_product est obligatoire'")
        return type_product

    class Meta(TrfDossierCtrlForm.Meta):
      model = CredocDossierCtrlProxy
      fields = ('__all__')
      widgets = TrfDossierCtrlForm.Meta.widgets.copy()
      widgets.update({
        
          'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                            forward=(
                                              forward.Const('transfert','app_label'),
                                              forward.Const('CredocDossierCtrlProxy','model'),
                                              )),

          'nomenc_lv0': autocomplete.ModelSelect2(url='catalogTypeCommercial-autocomplete',
                                        forward=(
                                          forward.Const(['Export','Import'],'nature'),
                                          forward.Const(True,'include'),
                                          forward.Const(True,'turple'),
                                          )),              
      })

class TrfDossierCouvrForm(forms.ModelForm):

    #use regex to clean DI reference
    def clean_ref_id(self):
        ref_id = self.cleaned_data['ref_id']
        if not re.match('[0-9][0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]\-[CE]', ref_id):
            raise forms.ValidationError("Saisie REF_ID commence par 'AAAA-####-C ou E'")
        if len(ref_id) > 11:
            raise forms.ValidationError("Saisie REF_ID en 11 caractère MAX")
        return ref_id

    #use regex to clean DI reference
    def clean_client(self):
        client = self.cleaned_data['client']
        if client is None:
            raise forms.ValidationError("Information de Client requis!")
        return client

    class Meta:
      model = TrfDossierCouvrProxy
      fields = ('__all__')
      widgets = {

        'statut': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(
                                              forward.Const('transfert','app_label'),
                                              forward.Const('TrfDossierCouvrProxy','model'),
                                              )),

        'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                          forward=(
                                            forward.Const('transfert','app_label'),
                                            forward.Const('TrfDossierCouvrProxy','model'),
                                            )),

        'client': autocomplete.ModelSelect2(url='client-autocomplete'),

        'corresp_in': autocomplete.ModelSelect2(url='corresp-autocomplete'),
        
        'corresp_out': autocomplete.ModelSelect2(url='corresp-autocomplete'),

        'account_in': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                                forward=(forward.Field('corresp_in', 'corresp'),)),
        
        'account_out': autocomplete.ModelSelect2(url='accountCorresp-autocomplete',
                                                forward=(forward.Field('corresp_out', 'corresp'),)), 
        

        'msg_payment': autocomplete.ModelSelect2(url='sygma-autocomplete',
                                                forward=(forward.Field('date_val', 'date_val'),
                                                        )), 

        'msg_commission': autocomplete.ModelSelect2(url='sygma-autocomplete',
                                                forward=(forward.Field('date_commission', 'date_val'),
                                                         )), 
      }  

class RptDossierRtrocForm(TrfDossierCouvrForm):

    #use regex to clean DI reference
    def clean_ref_id(self):
        ref_id = self.cleaned_data['ref_id']
        if not re.match('[0-9][0-9][0-9][0-9]\-[0-9][0-9][0-9][0-9]\-R', ref_id):
            raise forms.ValidationError("Saisie REF_ID commence par 'AAAA-####-R'")
        if len(ref_id) > 11:
            raise forms.ValidationError("Saisie REF_ID en 11 caractère MAX")
        return ref_id

    class Meta:
      model = RptDossierRtrocProxy
      fields = ('__all__')
      widgets = TrfDossierCouvrForm.Meta.widgets.copy()
      widgets.update({ 
        
        'statut': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(
                                              forward.Const('transfert','app_label'),
                                              forward.Const('RptDossierRtrocProxy','model'),
                                              )),

        'type_product': autocomplete.ModelSelect2(url='catalogTypeProduct-autocomplete',
                                          forward=(
                                            forward.Const('transfert','app_label'),
                                            forward.Const('RptDossierRtrocProxy','model'),
                                            )),

        'msg_payment': autocomplete.ModelSelect2(url='sygma-autocomplete',
                                                forward=(forward.Field('date_couvr', 'date_val'),
                                                        )),      
      })  
  
 
class DomDossierMultiForm(forms.ModelForm):

    class Meta:
      model = DomDossierMulti
      fields = ('__all__')
      widgets = {

        'statut': autocomplete.ModelSelect2(url='statut-autocomplete',
                                            forward=(
                                              forward.Const('transfert','app_label'),
                                              forward.Const('DomDossierMulti','model'),
                                              )),

        'dossier_dom': autocomplete.ModelSelect2(url='dossier_dom-autocomplete'),
                                                # forward=(
                                                #   forward.Field('_obj_.client', 'client'),  
                                                #   forward.Field('_obj_.nomenc_lv0', 'nomenc_lv0'),
                                                # )),
      } 

class AdminObjectActionForm(forms.ModelForm):

    def do_object_action(self):
        raise NotImplementedError('do_object_action has not been implemented')
        # obj.action_method(self.cleaned_data)
        # if commit:
        #     obj.save()
        # return obj
    def save(self, commit=True):

        try:
            if hasattr(self, 'do_object_action_callable'):
                self.do_object_action_callable(self.instance, self)
            else:
                self.do_object_action()
        except Exception as e:
            self.add_error(None, str(e))
            raise
        return self.instance


class ActionBaseForm(forms.Form):
    obs = forms.CharField(required=False, widget = forms.Textarea,)
    send_email = forms.BooleanField(required=False,)
    
    @property
    def email_subject_template(self):
      raise NotImplementedError()
    
    def email_body_template(self):
      raise NotImplementedError()

    def save(self, dossier, user):
      try:
        dossier, action = self.form_action(dossier, user)
      except:
        return -1
    
      if self.cleaned_data.get('send_email',False):
        print("Sending Email")

      return dossier, action

class CustomActionForm(ActionBaseForm):

  code_cli = forms.IntegerField(required=True, help_text='Code Client')
  email_body_template = 'email/account/apure.txt'
  field_order = (
    'code_cli',
    'obs',
    'send_email',
  )
  def form_action(self, dossier, user):
    return 1

