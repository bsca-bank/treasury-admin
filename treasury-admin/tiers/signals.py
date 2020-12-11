
from django.dispatch import Signal
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, m2m_changed
#
from datetime import date
from decimal import Decimal

#
from .client.models import ClientCtrl
from .corresp.models import Corresp
from .cpty.models import Cpty
from .depo.models import Depo



@receiver(post_save, sender=ClientCtrl)
def create_TiersCtrl(sender, instance, **kwargs):

    print ("DEBUG: ClientCtrl post_save has been triggered")      

    #create corresp
    if instance.chk_corresp == True:
        obj = Corresp.objects.filter(
                    clientCtrl_id = instance.pk
                )
        if not obj:
            #cash_flow has not been created
            obj = Corresp.objects.get_or_create(			
                            alias = instance.alias,
                            clientCtrl_id = instance.pk,
                        )
        print ("DEBUG: Corresp updated") 

    #create cpty
    if instance.chk_cpty == True:
        obj = Cpty.objects.filter(
                    clientCtrl_id = instance.pk
                )
        if not obj:
            #cash_flow has not been created
            obj = Cpty.objects.get_or_create(			
                            alias = instance.alias,
                        clientCtrl_id = instance.pk,
                        )
        print ("DEBUG: Cpty updated")   		

    #create depo
    if instance.chk_depo == True:
        obj = Depo.objects.filter(
                    clientCtrl_id = instance.pk
                )
        if not obj:
            #cash_flow has not been created
            obj = Depo.objects.get_or_create(			
                            alias = instance.alias,
                        clientCtrl_id = instance.pk,
                        )
        print ("DEBUG: Depo updated") 	


    else:
        #msg = TiersCtrl.objects.filter(clientCtrl_id=instance.pk).delete() 
        pass

@receiver(pre_delete, sender=ClientCtrl)
def delete_TiersCtrl(sender, instance, **kwargs):
    print ("DEBUG: ClientCtrl pre_delete triggered")         
    pass
