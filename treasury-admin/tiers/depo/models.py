# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
#
from django_pandas.managers import DataFrameManager

from util.catalog.models import CatalogTypeTiers
#
from tiers.models import Tiers
from tiers.account.models import Account

class Depo(Tiers):
        
    swift = models.CharField(max_length=50, null=True, blank=True)
    
    #override
    content_type = ContentType.objects.get_by_natural_key(app_label='tiers', model='Depo')  
    type_tiers = models.ForeignKey(CatalogTypeTiers,
                                   models.SET_NULL, 
                                   limit_choices_to={'content_type': content_type.id},                                                                           
                                   blank=True, null=True)      
    
    class Meta:
        managed = True
        db_table = 'third_depo'
        verbose_name = "Ctrl Depository" 
        verbose_name_plural = "Ctrl Depository"           
    def __str__(self):
        return u"%s" %(self.alias)

class AccountDepo(Account): 
    #
    depo = models.ForeignKey(Depo, on_delete=models.CASCADE)  
    objects = DataFrameManager()    
    
    class Meta:
        managed = True
        db_table = 'third_depo_acc'
        unique_together = (('depo','alias'),)
  
    def __str__(self):
        return u"%s" %(self.alias)