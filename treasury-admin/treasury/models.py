# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
#
from django_pandas.managers import DataFrameManager
#
from tiers.corresp.models import Corresp, AccountCorresp 
from tiers.client.models import ClientCtrl, ClientFileStorage
from tiers.cpty.models import Cpty

from util.fx.models import Ccy, CcyPair
from util.workflow.abstracts import MixinFourEyesChecking, MixinDocTracingLog
#
from .abstracts import *

## Create your models here.

class MM(MmTicket, MixinFourEyesChecking, MixinDocTracingLog): 

    corresp = models.ForeignKey(Corresp, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                related_name = '%(app_label)s_%(class)s_corresp',
                                verbose_name="Correpondant Bank") 
    
    account = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                blank=True, null=True,
                                related_name = '%(app_label)s_%(class)s_ac',
                                verbose_name="Correpondant A/C.")  

    ccy_in = models.ForeignKey(Ccy, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='%(app_label)s_%(class)s_ccy_in', 
                               verbose_name="Receving Ccy")

    ccy_out = models.ForeignKey(Ccy, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_ccy_out', 
                                verbose_name="Paying Ccy")

    #
    collateral = models.ManyToManyField('FI', through='Collateral',
                                related_name='%(app_label)s_%(class)s_collateral',  
                                verbose_name="collateral")

    def __str__(self):
        return u"%s | %s | %s" %(self.id, self.type_product, self.date_val) 

    class Meta:
        managed = True
        db_table = 'tresor_mm_mgr'
        verbose_name = 'MM Manager'
        verbose_name_plural = 'MM Manager'


class FI(FiTicket, MixinFolioCtrl, MixinFourEyesChecking, MixinDocTracingLog):  

    corresp = models.ForeignKey(Corresp, on_delete=models.SET_NULL,
                                blank=True, null=True,
                                related_name = '%(app_label)s_%(class)s_corresp',
                                verbose_name="Correpondant Bank") 
    
    account = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                blank=True, null=True,
                                related_name = '%(app_label)s_%(class)s_ac',
                                verbose_name="Correpondant A/C.")  

    def __str__(self):
        return u"%s | %s | %s" %(self.id, self.type_product, self.ref_id) 

    class Meta:
        managed = True
        db_table = 'tresor_fi_mgr'
        ordering = ('-date_val',)
        verbose_name = 'FI Manager'
        verbose_name_plural = 'FI Manager'

'''
FX Trading: Spot/Forward and Brokerage Deals
'''
class FX(FXTicket, MixinFourEyesChecking, MixinDocTracingLog): 
    #
    corresp_in = models.ForeignKey(Corresp, on_delete=models.SET_NULL, 
                                   blank=True, null=True, 
                                   related_name='%(app_label)s_%(class)s_corresp_in',
                                   verbose_name="Receving Bank")
    
    account_in = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                   blank=True, null=True, 
                                   related_name='%(app_label)s_%(class)s_ac_in',
                                   verbose_name="Receving a/c")
    #
    corresp_out = models.ForeignKey(Corresp, on_delete=models.SET_NULL, 
                                    blank=True, null=True, 
                                    related_name='%(app_label)s_%(class)s_corresp_out',
                                    verbose_name="Paying Bank")
    
    account_out = models.ForeignKey(AccountCorresp, on_delete=models.SET_NULL, 
                                    blank=True, null=True, 
                                    related_name='%(app_label)s_%(class)s_ac_out',
                                    verbose_name="Paying a/c")        

    class Meta:
        managed = True
        db_table = 'tresor_fx_mgr'
        ordering = ('-date_val',)
        verbose_name = 'FX Manager'
        verbose_name_plural = 'FX Manager'

    def __str__(self):
        return u"%s|%s %s" %(self.id, self.type_product, self.date_val) 

'''
Buying/Selling FX between bank a/c and client a/c
'''
class FXCli(FXTicket, MixinFourEyesChecking, MixinDocTracingLog):
    #generic link to other moodel
    object_id    = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    of           = GenericForeignKey('content_type', 'object_id')    
  
    NATURE_CHOICES = (
        (0, '/FX'),        
        (1, '/FEE'),        
    )
    nature =  models.IntegerField(choices=NATURE_CHOICES,
                                  default=1)    
  
    fee_rate = models.FloatField(default=0, verbose_name="Fee Rate(HT)",
                                help_text="Taux de commission(ex. 2,0% = 0.02)")
  #
    montant_tva =  models.IntegerField(null=True, blank=True, verbose_name="TVA(XAF)")


    ###to_delte
    chk_ok = models.BooleanField(default=False, verbose_name="Chk OK"
                                 ,help_text="Cochez si le taux fx a été approuvé")

    class Meta:
        managed = True
        db_table = 'tresor_fx_cli' 
        verbose_name = 'FX CLI Manager'
        verbose_name_plural = 'FX CLI Manager'



#Create your models here.
class Collateral(models.Model):  
    
    #dossier
    fi = models.ForeignKey('FI', on_delete=models.CASCADE, 
                                    related_name='%(app_label)s_%(class)s_fi',
                                    verbose_name="Fixed Income")
    #domiciliation
    mm = models.ForeignKey('MM', on_delete=models.CASCADE,
                                related_name='%(app_label)s_%(class)s_mm',  
                                verbose_name="Money Market")

    decot_pct = models.DecimalField(max_digits=7, decimal_places=4,
                            verbose_name="Decot",
                            help_text="Taux de Decot") 

    dom_pct = models.DecimalField(max_digits=7, decimal_places=4,
                                blank=True, null=True,
                                verbose_name="Pct Titre",
                                help_text="Pourcentage de Nantissement") 	

    dom_pct_montant_lc = models.DecimalField(max_digits=18, decimal_places=0,
                                verbose_name="dom_pct_montant_lc",
                                help_text="Montant équivalent en F.CFA") 

    obs = models.TextField(max_length=1000, null=True, blank=True,
                            default="",)
    
    #Addtional Information for filtering
    #------------------------------------------------------------------------------------------------
    def __str__(self):
        return u"%s| %s | %s" %(self.id, self.fi, self.dom_pct) 

    #calculat the residual days
    @property
    def decote_montant(self):
        if self.decot_pct and self.dom_pct_montant_lc:
            outset = round((1-float(self.decot_pct))*float(self.dom_pct_montant_lc),0)
        else:
            outset = "#Err"
        return outset      

    @property
    def couvr_pct(self):
        if self.decote_montant and self.mm.nominal:
            #outset = round((1-float(self.decot_pct))*float(self.mm.dom_pct_montant_lc),0)
            outset = round(float(self.decote_montant) / float(self.mm.nominal),4)
        else:
            outset = "#Err"
        return outset    


    def save(self, *args, **kwargs):
        if self.dom_pct_montant_lc:
            if self.fi.nominal:
                self.dom_pct = round(float(self.dom_pct_montant_lc)/float(self.fi.nominal),4)
            else:
               self.dom_pct = 1 

        elif not self.dom_pct and not self.dom_pct_montant_lc:
            self.dom_pct = 1
            if self.fi.nominal:
                self.dom_pct_montant_lc = self.fi.nominal

        return super(Collateral, self).save(*args, **kwargs)
    
    class Meta:
        managed = True
        db_table = 'tresor_collateral'   
        verbose_name = "Collateral Manager"
        verbose_name_plural = "Collateral Manager" 
        unique_together = ('mm','fi')
