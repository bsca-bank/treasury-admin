# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

#
import datetime
from datetime import date, timedelta
from django.utils import timezone

import os
import decimal
#
from django_pandas.managers import DataFrameManager
#
from tiers.corresp.models import Corresp, AccountCorresp
from tiers.client.models import ClientCtrl, ClientFileStorage
#
from util.fx.models import Ccy
from util.workflow.models import Statut, DocTraceLog
from util.workflow.abstracts import MixinFourEyesChecking
#
from settlement.sygma.models import SygmaCtrl 
from settlement.models import TreasuryPosition
#
from util.catalog.models import *
from cashflow.models import CashFlowDetail

#choose email Template
from notification.models import EmailCtrl

class DomDossier(models.Model):      
    
    oper_input = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_oper_input',  
                                    verbose_name="Agent")
                                   
    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, 
                                blank=True, null=True,
                                related_name='%(app_label)s_%(class)s_statut',)
    
    code_banque = models.CharField(max_length=6, verbose_name="Code Banque") 

    #from util.catalog.models import *
    client = models.ForeignKey(ClientCtrl, on_delete=models.CASCADE, 
                        help_text="Tapez le code client ici")

    nomenc_lv0 = models.ForeignKey(CatalogTypeCommercial,on_delete=models.CASCADE,
                            limit_choices_to={'level':0})

    #
    ccy	= models.ForeignKey(Ccy, on_delete=models.CASCADE,
                            related_name='%(app_label)s_%(class)s_ccy',
                            verbose_name="Ccy Devise")
    
    montant = models.DecimalField(max_digits=18, decimal_places=2,
                                verbose_name="Montant FX",
                                help_text="Montant devise de la déclaration") 	

    #
    ccy_lc = models.ForeignKey(Ccy, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                related_name='%(app_label)s_%(class)s_ccy_lc',
                                verbose_name="Ccy Locale")   

    montant_lc = models.DecimalField(max_digits=18, decimal_places=0,
                                blank=True, null=True,
                                verbose_name="Montant Local",
                                help_text="Montant équivalent en F.CFA") 

    fx_rate = models.DecimalField(max_digits=8, decimal_places=3,
                                blank=True, null=True,
                                verbose_name="Taux de convertion",
                                help_text="Taux de changes Fixing ECB") 
    #
    ref_di = models.CharField(max_length=50, unique=True,
                            verbose_name="Réf décl",
                            help_text="Réf de déclaration distribuée par MINFI/GUOT ou Banque Centrale")

    date_di = models.DateField(verbose_name="Date de Déclaration")   

    date_ref = models.DateField(blank=True, null=True,
                                verbose_name="Date de validation",
                                help_text="Date validation de déclaration")   

    objects = DataFrameManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
    
        ''' On save, update timestamps '''
        if self.montant and self.montant_lc:
            try:
                self.fx_rate = round(self.montant_lc / self.montant, 3)
            except:
                self.fx_rate = 0

        elif self.ccy.iso == 'EUR':
            self.fx_rate = 655.957
            self.montant_lc = round(float(self.montant)*655.957, 0)

        return super(DomDossier, self).save(*args, **kwargs)

    @property
    def ref_dom(self):
  
        outset = str(self.statut) + " | Validation en attente"
        
        if self.date_ref:
            
            code_niu = str(self.client.niu)
            code_banque = str(self.code_banque)
            code_oper = str(self.nomenc_lv0.code_oper)
            code_nomenc_lv0 = str(self.nomenc_lv0.code_nature)        
            num = str(self.pk).zfill(5)
            
            str_month = self.date_ref.strftime('%m') 
            str_year = self.date_ref.strftime('%Y') 

            str_01 = code_niu + '-' + code_banque + '-' + code_oper + '-' + num + '-' + code_nomenc_lv0 
            str_02 = str_month + '-' + str_year
            str_ccy = str(self.ccy)

            outset = str_01 + '-' + str_02 + '-' + str_ccy

        return outset 

#create your models here.
class DomDossierMultiAbstract(models.Model):  

    class Meta:
        abstract = True

# Create your models here.
class TrfDossierBase(models.Model):
  
    #from util.catalog.models import *
    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.CASCADE, 
                                    related_name='%(app_label)s_%(class)s_type_product', 
                                    verbose_name="Type de produit")   

    
    #
    created = models.DateTimeField(editable=False, verbose_name="Time Input", 
                                    help_text="Heure de Saisie")

    oper_input = models.ForeignKey(User, on_delete=models.CASCADE,
                                    related_name='%(app_label)s_%(class)s_oper_input',  
                                    verbose_name="Oper Input")

    nomenc_lv0 = models.ForeignKey(CatalogTypeCommercial, 
                            limit_choices_to={'level':0},
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='%(app_label)s_%(class)s_nomenc_lv0',)

    nomenc_lv1 = models.ForeignKey(CatalogTypeCommercial, 
                            limit_choices_to={'level':1},
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='%(app_label)s_%(class)s_nomenc_lv1',)
    ##Basic information
    client = models.ForeignKey(ClientCtrl, on_delete=models.CASCADE, 
                               help_text="Tapez le code client ici")
    #
    ccy	= models.ForeignKey(Ccy, on_delete=models.CASCADE,
                            related_name='%(app_label)s_%(class)s_ccy',
                            verbose_name="Ccy")
    
    montant = models.DecimalField(max_digits=18, decimal_places=2,
                                verbose_name="Montant",
                                help_text="Montant devise du paiement") 	    
    #------------------
    ccy_lc = models.ForeignKey(Ccy, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                related_name='%(app_label)s_%(class)s_ccy_lc',
                                verbose_name="Ccy Locale")   

    montant_lc = models.DecimalField(max_digits=18, decimal_places=0,
                                blank=True, null=True,
                                verbose_name="Montant Local",
                                help_text="Montant équivalent en F.CFA") 

    fx_rate = models.DecimalField(max_digits=8, decimal_places=3,
                                blank=True, null=True,
                                verbose_name="Taux de convertion",
                                help_text="Taux de changes Fixing ECB") 
    #statut
    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, 
                               blank=True, null=True,
                               related_name='%(app_label)s_%(class)s_statut',)

    cpty = models.CharField(max_length=100, 
                            verbose_name="Contrepartie", 
                            help_text="Bénéficiaire pour TRF/Donneur d'ordre pour RPT")

    ref_id = models.CharField(default=None, max_length=20, 
                              null=True, blank=True)

    ref_inv = models.TextField(null=True, blank=True, 
                                verbose_name="Réf. des factures",
                                help_text="Remplissez toutes no. de factures s'il y en a plusieur et les séparez par ';' ")    
    #
    objects = DataFrameManager()

    class Meta:
      abstract = True

# Create your models here.
class MixinTreasuryCtrl(models.Model):
    #
    NATURE_CHOICES = (
        (1, '\COUVR'), 
        (2, '\ENVLP'),
        (3, '\FPROP'),        
    )
    
    #FX CONFIRMATION
    chk_fund = models.BooleanField(default=False, verbose_name="Chk Fund_Type",
                                help_text="Cochez en après la selection du type fund")

    
    type_fund =  models.IntegerField(choices=NATURE_CHOICES, blank=True, null=True,
                                    verbose_name="TFund",
                                    help_text="Source de fond à utiliser")    

    oper_fund = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_oper_fund',  
                                verbose_name="Agent de Validation du Fond")                                
    #    
    corresp = models.ForeignKey(Corresp, on_delete=models.SET_NULL, 
                                blank=True, null=True,
                                verbose_name="Correspondant")

    account = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                blank=True, null=True,
                                verbose_name="Account")
    class Meta:
        abstract = True


    def save(self, *args, **kwargs):
        
        ''' On save, update timestamps '''
        if not self.chk_fund:
            self.oper_fund = None

        return super(MixinTreasuryCtrl, self).save(*args, **kwargs)


# Create your models here.
class MixinSettlementCtrl(models.Model):

    chk_exec = models.BooleanField(default=False, 
                                   verbose_name="Exéc",
                                   help_text="Check saisie d'Exécution")
    
    ref_exec = models.CharField(max_length=50, 
                                null=True, blank=True, 
                                verbose_name="Réf. Exécution",
                                help_text="ex: TRF/RPTXXXXXXX")  

    date_val = models.DateField(null=True, blank=True,
                                verbose_name="Value Date",
                                help_text="Value date d'Exécution")

    chk_pay = models.BooleanField(default=False, 
                                  verbose_name="Cosp",
                                  help_text="Check paiement du Correspondant")

    ref_swift = models.CharField(max_length=50, 
                                null=True, blank=True, 
                                verbose_name="Référence du paiement (Sygma/Swift etc.)") 

    ctrl_cf = models.BooleanField(default=True, 
                                verbose_name="Genr Cashflow",
                                help_text="Check if genrerate cashflow")  

    class Meta:
        abstract = True

# Create your models here.
class MixinApureCtrl(models.Model):

    # Ctrl
    '''
        1. We keep using the same 'status' field;
        2. We add additional fields to handle apurement check flow;
        3. 
    '''
    chk_apure = models.BooleanField(default=False, verbose_name="Chk Apure",
                                help_text="Validation d'apurement")

    oper_ap = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_oper_ap',  
                                verbose_name="Agent de Validation")
    
    date_ap = models.DateField(blank=True, null=True,
                            verbose_name="Date Limite",
                            help_text="Date limite pour l'apurement") 

    time_ap = models.DateTimeField(null=True, blank=True,editable=False,
                                    help_text="Time Approv")

    class Meta:
        abstract = True

    ''' On save, update timestamps '''
    def save(self, *args, **kwargs):
        if self.chk_apure and not self.time_ap:
            self.time_ap = timezone.now()
        return super(MixinApureCtrl, self).save(*args, **kwargs)

# Create your models here.
class MixinNotify(models.Model):

    # Ctrl
    '''
        1. We keep using the same 'status' field;
        2. We add additional fields to handle apurement check flow;
        3. 
    '''
    #recv
    chk_recv = models.BooleanField(default=False, 
                                   verbose_name="Recv",
                                   help_text="Check Reception")

    oper_recv = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_recv')

    time_recv = models.DateTimeField(null=True, blank=True,editable=False,
                                    help_text="Time Receive")

    chk_notify = models.BooleanField(default=False, verbose_name="NTFY",
                                help_text="Check Notification")

    batch_no = models.CharField(max_length=19, blank=True, null=True, verbose_name="Batch NO.")
    #
    message = models.ForeignKey(EmailCtrl, on_delete=models.SET_NULL,
                            blank=True, null=True,
                            related_name='%(app_label)s_%(class)s_message')

    template_key = models.CharField(max_length=255, blank=True, null=True, verbose_name="Email Template")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.chk_recv and not self.time_recv:
            self.time_recv = timezone.now()
        elif not self.chk_recv:
          self.oper_recv = None
          self.time_recv = None

        return super(MixinNotify, self).save(*args, **kwargs)


# Create your models here.
class MixinLABFT(models.Model):

    # Ctrl
    '''
    '''
    NATURE_CHOICES = (
        (None, '\ATTN'),
        (0, '\REJET'), 
        (1, '\ACK'),     
     )
    
    #FX CONFIRMATION
    type_dcc =  models.IntegerField(choices=NATURE_CHOICES, blank=True, null=True,
                                     verbose_name="Type DCC",
                                     help_text="Avis de DCC sur l'EXAMEN LAB-FT")    

    chk_dcc = models.BooleanField(default=False, 
                                verbose_name="Chk DCC",
                                help_text="Check LAB-FT")

    oper_dcc = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_dcc')

    time_dcc = models.DateTimeField(null=True, blank=True,editable=False,
                                    help_text="Time Chk DCC")

    obs_dcc = models.TextField(max_length=1000, null=True, blank=True,
                                default="",help_text="Observation DCC")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if self.chk_dcc and not self.time_dcc:
            self.time_dcc = timezone.now()
        elif not self.chk_dcc: 
            self.type_dcc = None
            self.oper_dcc = None
            self.time_dcc = None

        return super(MixinLABFT, self).save(*args, **kwargs)

# Create your models here.
class TrfDossierCouvrBase(models.Model):

    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.CASCADE,
                                     related_name='%(app_label)s_%(class)s_type_product')
                                     
    #statut
    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, 
                               blank=True, null=True,
                               related_name='%(app_label)s_%(class)s_statut')

    #basic information
    #----------------------------------------------
    ref_id = models.CharField(max_length=20, null=True, blank=True)
    
    #
    client = models.ForeignKey(ClientCtrl, on_delete=models.CASCADE,
                        blank=True, null=True, 
                        help_text="Tapez le code client ici")
    #
    ccy_out = models.ForeignKey(Ccy, on_delete=models.CASCADE,
                                related_name='%(app_label)s_%(class)s_ccy_pay')

    corresp_out = models.ForeignKey(Corresp, on_delete=models.CASCADE,
                                    related_name='%(app_label)s_%(class)s_corresp_pay')

    account_out = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                    blank=True, null=True, 
                                    related_name='%(app_label)s_%(class)s_account_pay')  

    montant_out = models.DecimalField(max_digits=18, decimal_places=2) 
    #
    ccy_in = models.ForeignKey(Ccy, on_delete=models.CASCADE,
                               related_name='%(app_label)s_%(class)s_ccy_couvr')

    corresp_in = models.ForeignKey(Corresp, on_delete=models.CASCADE,
                                   related_name='%(app_label)s_%(class)s_corresp_couvr') 

    account_in = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                   blank=True, null=True, 
                                   related_name='%(app_label)s_%(class)s_account_couvr')  

    montant_in = models.DecimalField(max_digits=18, decimal_places=2)  


    #BEAC repond
    #----------------------------------------------
    #
    chk_acc = models.BooleanField(default=False, verbose_name="REP", 
                                help_text="Check d'Accept/Rejet BEAC",)
    
    date_acc = models.DateField(null=True, blank=True, verbose_name="Date de Réponse", 
                                help_text="Date d'Accept/Rejet BEAC")
    
    ref_acc = models.CharField(max_length=50, 
                                null=True, blank=True, 
                                verbose_name="Msg d'Accept/Rejet BEAC") 

    chk_pay = models.BooleanField(default=False, verbose_name="PAY", 
                                help_text="Check Flux Sortant",)
    
    date_val = models.DateField(null=True, blank=True, verbose_name="Date Pay", 
                                help_text="Date du flux Sortant")
    
    montant_payment = models.DecimalField(max_digits=18, decimal_places=2, 
                                          blank=True, null=True,
                                          verbose_name="Montant Sortant",
                                          help_text="Montant du flux Sortant")  
    
    msg_payment = models.ForeignKey(SygmaCtrl, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_msg_payment',
                                    verbose_name="Msg Sygma",help_text="Msg Sygma de la contrevaleur")  

    chk_couvr = models.BooleanField(default=False,  
                                    verbose_name="COUVR", 
                                    help_text="Check Flux Entrant",)
    
    date_couvr = models.DateField(null=True, blank=True, 
                                verbose_name="Date Couvr", 
                                help_text="Date du flux Entrant")  

    montant_couvr = models.DecimalField(max_digits=18, decimal_places=2, 
                                        blank=True, null=True, 
                                        verbose_name="Montant Entrant",
                                        help_text="Montant du flux Entrant")  

    ref_swift = models.CharField(max_length=50, 
                                null=True, blank=True, 
                                verbose_name="Réf. Swift MT950") 

    ref_sygma = models.CharField(max_length=50, 
                                null=True, blank=True, 
                                verbose_name="Réf. Sygma MT950/MT940") 


    #comission
    date_commission = models.DateField(null=True, blank=True) 
    
    chk_commission = models.BooleanField(default=False,
                                        verbose_name="FEE",
                                        help_text="Check paiement de commission")  
    
    montant_commission = models.DecimalField(max_digits=18, decimal_places=0, 
                                             blank=True, null=True)  
                                             
    msg_commission = models.ForeignKey(SygmaCtrl, on_delete=models.SET_NULL,
                                       null=True, blank=True,
                                       related_name='%(app_label)s_%(class)s_msg_commission',
                                       verbose_name="Msg Commission",
                                       help_text="Msg Sygma de la commission")  
    #
    oper_input = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_oper_input',  
                                    verbose_name="Agent")

    date_trd = models.DateField() 
    
    year_trd = models.IntegerField() 

    objects = DataFrameManager()    

    def __str__(self):
        return u"%s | %s" %(self.statut, self.ref_id)

    class Meta:
        abstract = True 
