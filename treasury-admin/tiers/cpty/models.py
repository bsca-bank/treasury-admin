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


class Cpty(Tiers):
        
    swift = models.CharField(max_length=50, null=True, blank=True)
    
    #override
    content_type = ContentType.objects.get_by_natural_key(app_label='tiers', model='Cpty')  
    type_tiers = models.ForeignKey(CatalogTypeTiers,
                                   models.SET_NULL, 
                                   limit_choices_to={'content_type': content_type.id},                                                                           
                                   blank=True, null=True)      
    
    
    class Meta:
        managed = True
        db_table = 'third_cpty'
        verbose_name = "Ctrl Counterparty" 
        verbose_name_plural = "Ctrl Counterparty"   
        
    def __str__(self):
        return u"%s" %(self.alias)