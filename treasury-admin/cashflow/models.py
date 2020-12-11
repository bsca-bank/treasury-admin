# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from datetime import date, timedelta
#
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ValidationError
#
from django_pandas.managers import DataFrameManager
#
from util.fx.models import Ccy, CcyPair
from util.catalog.models import CatalogTypeFile, CatalogTypeProduct
from settlement.models import TreasuryPosition
from settlement.sygma.models import SygmaCtrl
from tiers.corresp.models import Corresp, AccountCorresp 


## Create your models here.
class CashFlowDetail(models.Model):

    object_id    = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    of           = GenericForeignKey('content_type', 'object_id')    

    NATURE_CHOICES = (
        (0, 'CF_InFlow'),        
        (1, 'CF_OutFlow'),        
    )

    nature =  models.IntegerField(choices=NATURE_CHOICES, default=1)     

    #from util.catalog.models import *
    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.SET_NULL, 
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_type_product')  

    #identifier: commission, principal, couverture etc....
    category = models.CharField(max_length=20, null=True, blank=True)
    #
    date_val = models.DateField(null=True, blank=True)
    corresp = models.ForeignKey(Corresp, on_delete=models.CASCADE)
    #
    account = models.ForeignKey(AccountCorresp, on_delete=models.CASCADE)

    montant = models.FloatField(null=True, blank=True)  

    chk_verify = models.BooleanField(default=False)

    ref_id = models.CharField(max_length=50, null=True, blank=True)   

    chk_pay = models.BooleanField(default=False)
    
    date_pay = models.DateField(null=True, blank=True)

    ref_swift = models.CharField(max_length=50, null=True, blank=True,
                            verbose_name="Réf. Payment",
                            help_text="Référence Swift/Sygma")

    sygmaCtrl = models.ForeignKey(SygmaCtrl, on_delete=models.SET_NULL, 
                                  null=True, blank=True)

    obs = models.TextField(null=True, blank=True)   

    objects = DataFrameManager()

    #calculat the residual days
    def jour_restant(self):
        
        if self.date_val: 
            end_date = self.date_val 

            if self.chk_verify and not self.chk_pay:  
                
                delta = end_date - date.today()

                if delta.days <=0: 
                    outset = str('O/N')
                if delta.days >0 and delta.days <=3: 
                    outset = str('3D')
                if delta.days >3 and delta.days <=7: 
                    outset = str('7D')  
                if delta.days >7 and delta.days <=30: 
                    outset = str('1M')
                if delta.days >30 and delta.days <=90: 
                    outset = str('3M')                      
                if delta.days >90 and delta.days <=180: 
                    outset = str('6M')    
                if delta.days >180 and delta.days <=270: 
                    outset = str('9M')
                if delta.days >270 and delta.days <=360: 
                    outset = str('1Yr')                                           
                if delta.days >360: 
                    outset = str('1Yr+')   
                #outset = str(delta.days)   
            else:
                outset = "-"
        else:
            outset = "-"   

        return outset 

    def __str__(self):
        return u"%s | %s | %s " %(self.date_val, self.content_type, self.object_id)	

    class Meta:
        managed = True
        db_table = 'cashflow_detail'
        ordering = ('-date_val','content_type','object_id')