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
from tiers.client.models import ClientCtrl
from tiers.account.models import Account

import os
def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.dossier.pk
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename) 


class Corresp(Tiers):
        
    chk_active = models.BooleanField(default=False) 
    
    swift = models.CharField(max_length=50, null=True, blank=True)
    
    #override
    content_type = ContentType.objects.get_by_natural_key(app_label='tiers', model='Corresp')  
    type_tiers = models.ForeignKey(CatalogTypeTiers,
                                   on_delete=models.CASCADE,
                                   limit_choices_to={'content_type': content_type.id},                                                                           
                                   blank=True, null=True)      
    
    class Meta:
        managed = True
        db_table = 'third_corresp'
        verbose_name = "Ctrl Treasury Unit" 
        verbose_name_plural = "Ctrl Treasury Unit"   
        
    def __str__(self):
        return u"%s" %(self.alias)


class AccountCorresp(Account): 
    #
    corresp = models.ForeignKey(Corresp, on_delete=models.CASCADE)  
    objects = DataFrameManager()    
    
    class Meta:
        managed = True
        db_table = 'third_corresp_account'
        unique_together = (('corresp','alias'),)
  
    def __str__(self):
        return u"%s" %(self.alias)