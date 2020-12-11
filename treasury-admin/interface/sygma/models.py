# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#

class ClearingMessage(models.Model):

    CF_CHOICES = (
        (0, 'N/A'),        
        (1, 'CF_InFlow'),
        (2, 'CF_OutFlow'),        
    ) 
    cf = models.IntegerField(choices=CF_CHOICES, default=0)
    #
    date_val = models.DateField()     
    ref_id = models.CharField(max_length=50)     
    type_msg = models.CharField(max_length=3)  
    statut_msg = models.CharField(max_length=5, blank=True, null=True)     
    codtype = models.CharField(max_length=13, blank=True, null=True)      
    ccy = models.CharField(max_length=3, blank=True, null=True)  
    montant = models.DecimalField(max_digits=18, decimal_places=0, blank=True, null=True)  
    expd = models.CharField(max_length=12)
    dest = models.CharField(max_length=12)
    info = models.TextField(max_length=255, blank=True, null=True) 
    #derived
    #
    link_id = models.CharField(max_length=12, blank=True, null=True)

    class Meta:
        abstract = True


class Sygma(ClearingMessage):    
    #
    donneur = models.CharField(max_length=50, blank=True, null=True)
    benef = models.CharField(max_length=50, blank=True, null=True)
    #    
    cmpt_expd = models.CharField(max_length=12, blank=True, null=True)  
    corr_expd = models.CharField(max_length=12, blank=True, null=True)          
    cmpt_dest = models.CharField(max_length=12, blank=True, null=True)  
    corr_dest = models.CharField(max_length=12, blank=True, null=True)
    #
    charge_type = models.CharField(max_length=3, blank=True, null=True)
    #
    obs = models.TextField(blank=True, null=True)
    #
    timestamp = models.CharField(db_column='timestamp', max_length=12, blank=True, null=True)
        
    class Meta:
        managed = True
        db_table = 'sygma'
        verbose_name = 'Interface SYGMA'
        verbose_name_plural = 'Interface SYGMA'
        
    def __str__(self):
        return u"%s | %s" %(self.date_val, self.id,)
