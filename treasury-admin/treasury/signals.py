# -*- coding: utf-8 -*-
from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save, pre_delete
#
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
#
from cashflow.models import CashFlowDetail
from util.workflow.models import DocTraceLog
#
from .models import FX,MM,FI,FXCli


@receiver(post_save, sender=FX)
def create_fxDoubleCashFlow(sender, instance, created, **kwargs):
    #
    print ("DEBUG: create_fxDoubleCashFlow triggered")
    #
    ctype = ContentType.objects.get_for_model(instance)
    obj = CashFlowDetail.objects.filter(
        object_id=instance.pk,
        content_type=ctype
    )
    #
    if not obj and instance.ctrl_cf:
        # Create cash outflow
        cf_nature = 1
        #
        obj_out = CashFlowDetail.objects.get_or_create(
            object_id=instance.pk,
            content_type=ctype,
            type_product=instance.type_product,
            ref_id=instance.ref_id,
            date_val=instance.date_val,
            chk_verify=True,
            #
            nature=cf_nature,
            corresp=instance.corresp_out,
            account=instance.account_out,
            montant=instance.montant_out,
        )
        # Create cash inflow
        cf_nature = 0
        #
        obj_in = CashFlowDetail.objects.get_or_create(
            object_id=instance.pk,
            content_type=ctype,
            type_product=instance.type_product,
            ref_id=instance.ref_id,
            date_val=instance.date_val,
            chk_verify=True,
            #
            nature=cf_nature,
            corresp=instance.corresp_in,
            account=instance.account_in,
            montant=instance.montant_in,
        )
    elif obj:
        if instance.ctrl_cf:
            # update cash_outflow
            cf_nature=1
            #
            obj_out=CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = cf_nature,
            )
            #
            obj_out.update(
                ref_id = instance.ref_id,
                type_product = instance.type_product,
                corresp = instance.corresp_out,
                account = instance.account_out,                
                montant = instance.montant_out,
                date_val = instance.date_val,
            )
            # update cash_inflow
            cf_nature=0
            #
            obj_in=CashFlowDetail.objects.filter(
                object_id = instance.pk,
                content_type = ctype,
                nature = cf_nature,
            )
            #
            obj_in.update(
                ref_id = instance.ref_id,
                type_product = instance.type_product,
                corresp = instance.corresp_in,
                account = instance.account_in,                
                montant = instance.montant_in,
                date_val = instance.date_val,
            )
        else:
            # si ctrl_cf are reversed, then delete cashflow
            CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk).delete()    

@receiver(pre_delete, sender=FX)    
def delete_fxDoubleCashFlow(sender, instance,**kwargs):
    print ("DEBUG: delete_fxDoubleCashFlow")         
    ctype = ContentType.objects.get_for_model(instance)
    CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk).delete()            

@receiver(post_save, sender=MM)
@receiver(post_save, sender=FI)
def delete_cashFlow(sender, instance, created, **kwargs):
    print ("DEBUG: delete_cashFlow triggered")
    ctype = ContentType.objects.get_for_model(instance)
    obj = CashFlowDetail.objects.filter(
        object_id=instance.pk,
        content_type=ctype
    )
    if obj and not instance.ctrl_cf:
        CashFlowDetail.objects.filter(content_type=ctype, object_id=instance.pk).delete()       


@receiver(post_save, sender=FX)
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
        print ("DEBUG: Log obj created" + str(obj))
    
    #link log to parent
    docTraceLog = DocTraceLog.objects.get(content_type=ctype, object_id=instance.pk)
    obj_parent = FX.objects.filter(id=instance.pk)
    obj_parent.update(
        docTraceLog = docTraceLog
    )
    print ("DEBUG: Log obj linked" + str(obj_parent))

@receiver(post_save, sender=MM)
def create_mmTracingLog(sender, instance, **kwargs):
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
        print ("DEBUG: Log obj created" + str(obj))
    
    #link log to parent
    docTraceLog = DocTraceLog.objects.get(content_type=ctype, object_id=instance.pk)
    obj_parent = MM.objects.filter(id=instance.pk)
    obj_parent.update(
        docTraceLog = docTraceLog
    )
    print ("DEBUG: Log obj linked" + str(obj_parent))


@receiver(post_save, sender=FI)
def create_fiTracingLog(sender, instance, **kwargs):
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
        print ("DEBUG: Log obj created" + str(obj))
    
    #link log to parent
    docTraceLog = DocTraceLog.objects.get(content_type=ctype, object_id=instance.pk)
    obj_parent = FI.objects.filter(id=instance.pk)
    obj_parent.update(
        docTraceLog = docTraceLog
    )
    print ("DEBUG: Log obj linked" + str(obj_parent))


@receiver(post_save, sender=FXCli)
def create_fxcliTracingLog(sender, instance, **kwargs):
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
        print ("DEBUG: Log obj created" + str(obj))
    
    #link log to parent
    docTraceLog = DocTraceLog.objects.get(content_type=ctype, object_id=instance.pk)
    obj_parent = FXCli.objects.filter(id=instance.pk)
    obj_parent.update(
        docTraceLog = docTraceLog
    )
    print ("DEBUG: Log obj linked" + str(obj_parent))