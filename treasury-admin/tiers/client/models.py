# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.db import models
#
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from datetime import date
#
from interface.models import ApBkcli
#
#from util.fx.models import *
from util.catalog.models import CatalogTypeTiers, CatalogTypeFile
from util.fileStorage.models import FileStorage


class ClientCtrl(ApBkcli):

    #structure
    #-----------------------------------------------------------------
    alias = models.CharField(max_length=15,                              
                             verbose_name="Sigle", null=True, blank=True)    
    
    #only allow unique principal agent
    oper = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)  

    #contenttype = ContentType.objects.get_by_natural_key(app_label='tiers', model='ClientCtrl')
    type_client = models.ForeignKey(CatalogTypeTiers, on_delete=models.SET_NULL,                                      
                                    related_name= '%(app_label)s_%(class)s_type_client', 
                                    default=7,
                                    blank=True, null=True)        
    #
    obs = models.TextField(null=True, blank=True)       
    
    #demande BEAC 2019.JUL pour la prefinancement
    niu = models.CharField(max_length=50,
                            verbose_name="NIU", help_text="NIU ou autre numéro d'identification de l'établissement",
                            null=True, blank=True)

   
    email = models.CharField(default=None, max_length=100, 
                            verbose_name="Email", help_text="Addresse Mail Electronique",
                            null=True, blank=True)                         
    #--------------------------------------------------------
    chk_corresp = models.BooleanField(default=False,
                                    verbose_name="Treasury Unit")   
    chk_cpty = models.BooleanField(default=False,
                                    verbose_name="Counterparty")   
    chk_depo = models.BooleanField(default=False,
                                    verbose_name="Depository")       
  
    def __str__(self):
        if self.alias:
            short_alias = self.alias[0:10]
            return u"%s | %s | %s" %(self.ref_id, self.type_client, short_alias)
        else:
            return u"%s | %s | %s" %(self.ref_id, self.type_client, "#N/A")

    class Meta:
        managed = True
        db_table = 'third_client_ctrl'
        verbose_name = "Ctrl Client" 
        verbose_name_plural = "Ctrl Client"          
        ordering = ('ref_id',)

def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.clientCtrl.pk
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)  

class ClientFileStorage(FileStorage):
    #link
    client = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL,
    blank=True, null=True)
    #    
    def __str__(self):
        return u"%s | %s | %s " %(self.type_file, self.client, self.id)
    
    class Meta:
        managed = True
        db_table = 'third_client_file' 
        verbose_name = "Client file storage" 
        verbose_name_plural = "Client file storage"    
        ordering = ('client','type_file','-id')   