
import datetime

from django.contrib.contenttypes.models import ContentType

from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete, m2m_changed
from django.utils import timezone

from cashflow.models import CashFlowDetail
from util.workflow.models import Workflow, Statut
from util.workflow.models import DocTraceLog
from notification.models import EmailCtrl
#
from .models import *
from .proxys import *

from settlement.sygma.models import SygmaCtrl

@receiver(post_save, sender=DomDossierCtrl)
@receiver(post_save, sender=TrfDossierCtrlProxy)
@receiver(post_save, sender=RptDossierCtrlProxy)
@receiver(post_save, sender=VirDossierCtrlProxy)
@receiver(post_save, sender=CredocDossierCtrlProxy)
def create_trfTracingLog(sender, instance, **kwargs):
    #print ("DEBUG: create_trfSingleCashFlow has been triggered")         
    #print ("DEBUG: " + str(instance.time_approv.date()))
    #
    ctype = ContentType.objects.get_for_model(instance)
    obj = DocTraceLog.objects.filter(object_id = instance.pk, content_type = ctype)
  
    if not obj:
        obj = DocTraceLog.objects.get_or_create(
                content_type = ctype,
                object_id = instance.pk,
                chk_create = True,
                time_create = timezone.now(),
                obs = "Création Automatique " + str(timezone.now())
        )
        #print ("DEBUG: Log obj created" + str(obj))
    
    #link log to parent
    docTraceLog = DocTraceLog.objects.get(content_type=ctype, object_id=instance.pk)
    obj_parent = sender.objects.filter(id=instance.pk)
    obj_parent.update(
        docTraceLog = docTraceLog
    )
    #print ("DEBUG: Log obj linked" + str(obj_parent))

@receiver(post_save, sender=TrfDossierCtrlProxy)
@receiver(post_save, sender=VirDossierCtrlProxy)
@receiver(post_save, sender=CredocDossierCtrlProxy)
def create_trfSingleCashFlow(sender, instance, **kwargs):
    #print ("DEBUG: create_trfSingleCashFlow has been triggered")         
    #print ("DEBUG: " + str(instance.time_approv.date()))
    #
    ctype = ContentType.objects.get_for_model(instance)
    obj = CashFlowDetail.objects.filter(object_id = instance.pk, content_type = ctype)
    
    cf_nature = 1 #cashOutflow
    if sender == RptDossierCtrlProxy:
        cf_nature = 0 #cashInflow
  
    if not instance.chk_pay and instance.time_approv:
        date_val = instance.time_approv.date()
        #very strange, should convert date to string
        str_date_val = date_val.strftime('%Y-%m-%d')
        str_date_pay = None
    else:
        str_date_val = instance.date_val
        str_date_pay = instance.date_val
    
    if not obj and instance.chk_approv:

        obj = CashFlowDetail.objects.get_or_create(
            nature = cf_nature,
            content_type = ctype,
            object_id = instance.pk,
            type_product = instance.type_product,
            #
            corresp = instance.corresp,
            account = instance.account,
            montant = instance.montant,
            chk_verify = instance.chk_approv,
            chk_pay = instance.chk_pay,
            date_val = str_date_val,
            date_pay = str_date_pay
        )
        print ("DEBUG: Cashflow obj created" + str(obj))

    elif obj and instance.chk_approv:
        if instance.chk_pay:
            obj.update(
                nature = cf_nature,
                content_type = ctype,
                object_id = instance.pk,
                type_product = instance.type_product,
                corresp = instance.corresp,
                account = instance.account,
                montant = instance.montant,
                chk_verify = instance.chk_approv,
                chk_pay = instance.chk_pay,
                date_val = str_date_val,
                date_pay = str_date_val
            )
            print ("DEBUG: Cashflow obj updated" + str(obj))
    else:
        CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk).delete() 


@receiver(post_save, sender=RptDossierCtrlProxy)
def create_rptDoubleCashFlow(sender, instance, **kwargs):
    #print ("DEBUG: create_trfSingleCashFlow has been triggered")         
    #print ("DEBUG: " + str(instance.time_approv.date()))
    #
    ctype = ContentType.objects.get_for_model(instance)
    #obj = CashFlowDetail.objects.filter(object_id = instance.pk, content_type = ctype)
    
    if not instance.chk_pay and instance.time_approv:
        date_val = instance.time_approv.date()
        #very strange, should convert date to string
        str_date_val = date_val.strftime('%Y-%m-%d')
        str_date_pay = None
    else:
        str_date_val = instance.date_val
        str_date_pay = instance.date_val
    
    '''
    Cashflow Incoming= (incoming, principal)
    ----------------------------------------
    ''' 
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 0, #cash_inflow
    )
    if not obj:
        if instance.chk_pay:
            #create cash inflow
            cf_nature = 0 #cashInflow
            obj = CashFlowDetail.objects.get_or_create(
                nature = cf_nature,
                content_type = ctype,
                object_id = instance.pk,
                type_product = instance.type_product,
                category = "CF_IN",
                #
                corresp = instance.corresp,
                account = instance.account,
                montant = instance.montant,
                chk_verify = instance.chk_pay,
                chk_pay = instance.chk_pay,
                date_val = str_date_val,
                date_pay = str_date_pay
            )    
    elif not instance.chk_pay:
        CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk).delete() 

    '''
    Cashflow retrocession = (outcoming, principal)
    ----------------------------------------
    ''' 
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 1, #cash_outflow
    )
    if not obj:
        if instance.chk_pay and instance.ctrl_cf and not instance.dossier_rtroc:
            #create retrocession
            cf_nature = 1 #cashOutflow
            montant = round(float(instance.montant)*0.7,2)
            obj = CashFlowDetail.objects.get_or_create(
                nature = cf_nature,
                content_type = ctype,
                object_id = instance.pk,
                type_product = instance.type_product,
                category = "CF_RTROC",
                #
                corresp = instance.corresp,
                account = instance.account,
                montant = montant,
                chk_verify = instance.chk_pay,
                chk_pay = False,
                date_val = str_date_val,
                #date_pay = str_date_pay
            )
    elif not instance.chk_pay or not instance.ctrl_cf or instance.dossier_rtroc:
        CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, category="CF_RTROC").delete() 

## Create your models here.
@receiver(post_save, sender=TrfDossierCouvrProxy) 
def update_trfDossierCouvrCF(sender, instance, created,**kwargs):

    ctype = ContentType.objects.get_for_model(instance)

    '''
    Cashflow F.CFA = (outcoming, principal)
    ----------------------------------------
    '''
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 1, #cash_outflow
        category = "CTVAL FCFA",
    )
    if not obj:     
        v_chk_pay = instance.chk_pay
        v_date_pay = instance.date_val
        if instance.chk_verify and instance.date_trd and not instance.chk_approv:
            obj = CashFlowDetail.objects.get_or_create(
                object_id = instance.pk,
                content_type = ctype,
                nature = 1, #cash_outflow
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "CTVAL FCFA",
                corresp = instance.corresp_out,
                account = instance.account_out,                
                montant = instance.montant_out,
                date_val = instance.date_val,
                date_pay = v_date_pay, 
                chk_verify = True,
                chk_pay = v_chk_pay,
                sygmaCtrl = instance.msg_payment,  
            )           
    else:   
        #update CF
        if instance.chk_pay and instance.date_val:
            obj_out = CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = 1, #cash_outflow
                category = "CTVAL FCFA",
            )
            obj_out.update(
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "CTVAL FCFA",
                corresp = instance.corresp_out,
                account = instance.account_out, 
                montant = instance.montant_out, 
                date_val = instance.date_val,
                date_pay = instance.date_val, 
                chk_verify = True,
                chk_pay = True,
                sygmaCtrl = instance.msg_payment,          
            ) 
        #delete CF
        elif not instance.chk_verify:
            #here we delete commission cash flow as well
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 1).delete()

        elif instance.chk_approv and not instance.chk_couvr:
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 1).delete()

        else:
            return 0

    '''
    Cashflow FX = (incoming prefinance)
    ----------------------------------------
    '''            
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 0, #cash_inflow
        category = "COUVR FX",
    )
    if not obj: 
        v_chk_couvr = instance.chk_couvr
        v_date_couvr = instance.date_couvr
        if instance.chk_verify and instance.date_trd and not instance.chk_approv:
            obj = CashFlowDetail.objects.get_or_create(
                object_id = instance.pk,
                content_type = ctype,
                nature = 0, #cash_inflow
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "COUVR FX",
                corresp = instance.corresp_in,
                account = instance.account_in, 
                montant = instance.montant_in,
                date_val = instance.date_val,
                date_pay = v_date_couvr,   
                chk_verify = v_chk_couvr,
                chk_pay = v_chk_couvr,   
                ref_swift = instance.ref_swift,   
            )
    else:
        #update
        if instance.chk_couvr and instance.date_couvr:          
            obj_in = CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = 0, #cash_inflow
                category = "COUVR FX",
            )
            obj_in.update(
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "COUVR FX",
                corresp = instance.corresp_in,
                account = instance.account_in,                
                montant = instance.montant_in, 
                date_val = instance.date_val,
                date_pay = instance.date_couvr,                        
                chk_verify = True,
                chk_pay = True,   
                ref_swift = instance.ref_swift,               
            )
        elif not instance.chk_verify:
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 0).delete()

        elif instance.chk_approv and not instance.chk_couvr:
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 0).delete()
    
        else:
            return 0

    '''
    Cashflow F.CFA = (outcoming, Commission)
    ----------------------------------------
    '''
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 1, #cash_outflow
        category = "COMM F.CFA",
    )
    if not obj: 
        v_chk_pay = instance.chk_commission
        v_date_pay = instance.date_commission    
        if instance.chk_verify and instance.date_trd and not instance.chk_approv:
            obj = CashFlowDetail.objects.get_or_create(
                object_id = instance.pk,
                content_type = ctype,
                nature = 1, #cash_outflow
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "COMM F.CFA",
                corresp = instance.corresp_out,
                account = instance.account_out,                
                montant = instance.montant_commission,
                date_val = instance.date_val,
                date_pay = v_date_pay,
                chk_verify = True,
                chk_pay = v_chk_pay,
                sygmaCtrl = instance.msg_commission,    
            )           
    else:   
        #update CF
        if instance.chk_commission and instance.date_commission:
            obj_out = CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = 1, #cash_outflow
                category = "COMM F.CFA",
            )
            obj_out.update(
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "COMM F.CFA",
                corresp = instance.corresp_out,
                account = instance.account_out, 
                montant = instance.montant_commission, 
                date_val = instance.date_val,
                date_pay = instance.date_commission, 
                chk_verify = True,
                chk_pay = True,
                sygmaCtrl = instance.msg_commission,           
            ) 
        #delete CF
        elif not instance.chk_verify:
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 1, category = "COMM F.CFA",).delete()

        else:
            return 0

## Create your models here.
@receiver(post_save, sender=RptDossierRtrocProxy) 
def update_rptDossierRtrocCF(sender, instance, created,**kwargs):

    ctype = ContentType.objects.get_for_model(instance)

    '''
    Cashflow Creation
    ----------------------------------------
    '''
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 1, #cash_outflow
    )
    if not obj:     
        v_chk_pay = instance.chk_pay
        v_date_pay = instance.date_val
        #generate cashflow as soon as RPT confirmed
        if instance.chk_verify and instance.date_trd:
            obj = CashFlowDetail.objects.get_or_create(
                object_id = instance.pk,
                content_type = ctype,
                nature = 1, #cash_outflow
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "RTROC FX",
                corresp = instance.corresp_out,
                account = instance.account_out,                
                montant = instance.montant_out,
                date_val = instance.date_trd,
                date_pay = v_date_pay, 
                chk_verify = True,
                chk_pay = v_chk_pay,
                ref_swift = instance.ref_swift,   
            )           
    else:   
        #update CF
        if instance.chk_pay and instance.date_val:
            obj_out = CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = 1, #cash_outflow
                category = "RTROC FX",
            )
            obj_out.update(
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "RTROC FX",
                corresp = instance.corresp_out,
                account = instance.account_out, 
                montant = instance.montant_out, 
                date_val = instance.date_trd,
                date_pay = instance.date_val, 
                chk_verify = True,
                chk_pay = True,
                ref_swift = instance.ref_swift,          
            ) 
        #delete CF
        elif not instance.chk_verify:
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 1).delete()
        else:
            return 0
             
          
    obj = CashFlowDetail.objects.filter(
        object_id = instance.pk,
        content_type = ctype,
        nature = 0, #cash_outflow
    )
    if not obj: 
        v_chk_couvr = instance.chk_couvr
        v_date_couvr = instance.date_couvr
        if instance.chk_verify and instance.date_trd:
            obj = CashFlowDetail.objects.get_or_create(
                object_id = instance.pk,
                content_type = ctype,
                nature = 0, #cash_inflow
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "CTVAL FCFA",
                corresp = instance.corresp_in,
                account = instance.account_in, 
                montant = instance.montant_in,
                date_val = instance.date_trd,
                date_pay = v_date_couvr,
                chk_verify = True,
                chk_pay = v_chk_couvr,   
                sygmaCtrl = instance.msg_payment, 
            )
    else:
        #update
        if instance.chk_couvr and instance.date_couvr:          
            obj_in = CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = 0, #cash_inflow
                category = "CTVAL FCFA",
            )
            obj_in.update(
                type_product = instance.type_product,
                ref_id = instance.ref_id,
                category = "CTVAL FCFA",
                corresp = instance.corresp_in,
                account = instance.account_in,                
                montant = instance.montant_in, 
                date_val = instance.date_trd,
                date_pay = instance.date_couvr,                        
                chk_verify = True,
                chk_pay = True,   
                sygmaCtrl = instance.msg_payment,                
            )
        elif not instance.chk_verify:
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk, nature = 0).delete()             
        else:
            return 0

#update sygma
@receiver(post_save, sender=TrfDossierCouvrProxy) 
@receiver(post_save, sender=RptDossierRtrocProxy) 
def update_sygma(sender, instance, created,**kwargs):
    if instance.msg_payment:
        try:
            obj_pay = SygmaCtrl.objects.filter(
                id = instance.msg_payment.id,
            )
            obj_pay.update(
                link_id = instance.ref_id,
                ctrl = True       
            ) 
        except:
            pass
            #print("DEBUG: Msg sygma du paiement introuvable")

    if instance.msg_commission:
        try:
            obj_comm = SygmaCtrl.objects.filter(
                id = instance.msg_commission.id,
            )
            obj_comm.update(
                link_id = instance.ref_id,
                ctrl = True       
            ) 
        except:
            pass
            #print("DEBUG: Msg sygma du commssion introuvable")

    return 0

#update sygma
@receiver(post_save, sender=VirDossierCtrlProxy) 
def update_msg_payment(sender, instance, created,**kwargs):

    #print("update_msg_payment triggered")

    if instance.msg_payment:
        
        try:
            obj_pay = SygmaCtrl.objects.filter(
                id = instance.msg_payment.id,
            )
            obj_pay.update(
                link_id = "VIR/" + str(instance.id),
                ctrl = True       
            ) 
            #print("DEBUG: Msg sygma updated")
            return 0
        except:
            pass
            #print("DEBUG: Msg sygma du paiement introuvable")

    return 0 

#Workflow pour la couverture et la retrocession 
@receiver(pre_save, sender=RptDossierRtrocProxy) 
@receiver(pre_save, sender=TrfDossierCouvrProxy) 
def update_TrfDossierCouvrWFStatus(sender, instance, *args,**kwargs):

    ctype = ContentType.objects.get_for_model(instance, for_concrete_model=False)

    if not instance.statut:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=None, chk_switch=None,)
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_verify == " + str(instance.chk_verify))
            pass

    if instance.chk_verify:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=instance.statut, chk_switch='chk_verify')
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_verify == " + str(instance.chk_verify))
            pass
    else:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_fnl=instance.statut, chk_switch='chk_verify')
            instance.statut = workflow.s_init
        except:
            #print("DEBUG: chk_verify == " + str(instance.chk_verify))
            pass

    if instance.chk_approv:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=instance.statut, chk_switch='chk_approv')
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_approv == " + str(instance.chk_approv))
            pass
    else:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_fnl=instance.statut, chk_switch='chk_approv')
            instance.statut = workflow.s_init
        except:
            #print("DEBUG: chk_approv == " + str(instance.chk_approv))
            pass

    if instance.chk_pay:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=instance.statut, chk_switch='chk_pay')
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_pay == " + str(instance.chk_pay))
            pass
    else:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_fnl=instance.statut, chk_switch='chk_pay')
            instance.statut = workflow.s_init
        except:
            #print("DEBUG: chk_pay == " + str(instance.chk_pay))
            pass

    if instance.chk_couvr:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=instance.statut, chk_switch='chk_couvr')
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_couvr == " + str(instance.chk_pay))
            pass
    else:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_fnl=instance.statut, chk_switch='chk_couvr')
            instance.statut = workflow.s_init
        except:
            #print("DEBUG: chk_couvr == " + str(instance.chk_pay))
            pass
    #
    ctype = ContentType.objects.get_for_model(TrfDossierCtrl, for_concrete_model=True)
    ack_statut = Statut.objects.get(content_type=ctype, statut='/ACK BEAC')
    nck_statut = Statut.objects.get(content_type=ctype, statut='/REJET')
    couvr_statut = Statut.objects.get(content_type=ctype, statut='/COUVR BEAC')


    #update child ticket
    if instance.chk_pay and not instance.chk_couvr:
        try:
            obj = TrfDossierCtrl.objects.filter(dossier_couvr = instance.pk,).update(statut=ack_statut)
        except:
            obj = None

    elif instance.chk_couvr:
        try:
            obj = TrfDossierCtrl.objects.filter(dossier_couvr = instance.pk,).update(statut=couvr_statut)
        except:
            obj = None
    #rejet
    elif (instance.chk_verify and instance.chk_approv) and not (instance.chk_pay and instance.chk_couvr):
        try:
            obj = TrfDossierCtrl.objects.filter(dossier_couvr = instance.pk,).update(statut=nck_statut)
        except:
            obj = None

    return 0

#Workflow pour la couverture et la retrocession 
@receiver(pre_save, sender=DomDossierCtrl) 
def update_DomDossierWFStatus(sender, instance, *args,**kwargs):

    ctype = ContentType.objects.get_for_model(instance, for_concrete_model=False)

    if not instance.statut:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=None, chk_switch=None,)
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_verify == " + str(instance.chk_verify))
            pass

    if instance.chk_verify:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=instance.statut, chk_switch='chk_verify')
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_verify == " + str(instance.chk_verify))
            pass
    else:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_fnl=instance.statut, chk_switch='chk_verify')
            instance.statut = workflow.s_init
        except:
            #print("DEBUG: chk_verify == " + str(instance.chk_verify))
            pass

    if instance.chk_approv:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_init=instance.statut, chk_switch='chk_approv')
            instance.statut = workflow.s_fnl
        except:
            #print("DEBUG: chk_approv == " + str(instance.chk_approv))
            pass
    else:
        try:
            workflow = Workflow.objects.get(content_type=ctype, s_fnl=instance.statut, chk_switch='chk_approv')
            instance.statut = workflow.s_init
        except:
            #print("DEBUG: chk_approv == " + str(instance.chk_approv))
            pass


## Create your models here.
@receiver(post_save, sender=TrfDossierCtrlProxy)
@receiver(post_save, sender=RptDossierCtrlProxy)
@receiver(post_save, sender=CredocDossierCtrlProxy)
def update_TRF_DomDossierMulti(sender, instance, created,**kwargs):

    if instance.dossier_dom:
        try:
            objs = DomDossierMulti.objects.filter(
                dossier_trf = instance,
            )
        except:
            objs = None

        ctype = ContentType.objects.get_for_model(DomDossierMulti, for_concrete_model=True)
        statut = Statut.objects.get(content_type=ctype, statut='/ATTN')   
        
        if not objs:     
            obj, created = DomDossierMulti.objects.get_or_create(
                dossier_trf = instance,
                dossier_dom = instance.dossier_dom,
                oper_input = instance.oper_input,
            )
            obj.dom_pct = 1
            obj.statut = statut
            obj.nomenc_lv0 = instance.nomenc_lv0
            obj.date_ap = instance.date_ap
            if instance.dossier_dom.time_verify:
                obj.date_verify = instance.dossier_dom.time_verify
            obj.save()
        else:
            for obj in objs:
                #print(obj)
                if not obj.statut:
                    obj.statut = statut
                #
                obj.ref_exec = instance.ref_exec
                obj.nomenc_lv0 = instance.nomenc_lv0
                obj.date_val = instance.date_val
                obj.date_ap = instance.date_ap
                if instance.dossier_dom.time_verify:
                    obj.date_verify = instance.dossier_dom.time_verify
                obj.save()               
    else:
        DomDossierMulti.objects.filter(dossier_trf=instance.pk).delete() 
    
    return 0 


## Create your models here.
@receiver(post_save, sender=DomDossierCtrl) 
def update_DOM_DomDossierMulti(sender, instance, created,**kwargs):

    if instance.date_ref:
        objs = DomDossierMulti.objects.filter(
            dossier_dom = instance.id,
        ).update(date_verify = instance.date_ref)
    
    return 0