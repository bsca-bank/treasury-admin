# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from tiers.client.models import ClientCtrl

from util.catalog.models import CatalogTypeTiers

class Tiers(models.Model):
  
  alias = models.CharField(max_length=50)
  
  type_tiers = models.ForeignKey(CatalogTypeTiers,
                                  models.SET_NULL, 
                                  #limit_choices_to={'content_type': contenttype.id},                                                                           
                                  blank=True, null=True)  
  
  clientCtrl = models.ForeignKey(ClientCtrl, 
                                 models.SET_NULL, 
                                 ##limit_choices_to={'content_type': contenttype.id},                                         
                                 blank=True, null=True,)   
                                 #
  #structure
  #-----------------------------------------------------------------
 
  def __str__(self):
    return u"%s" %(self.clientCtrl)
  
  class Meta:
    abstract = True