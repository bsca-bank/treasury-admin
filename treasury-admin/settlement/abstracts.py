# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
from django.db import models

#
from django.contrib.auth.models import User
#
#import tiers.agence.models 
from util.workflow.models import *
from tiers.corresp.models import *
#
from util.catalog.models import CatalogTypeProduct
import os

## Create your models here.
class MT950(models.Model):

    type_product = models.ForeignKey(CatalogTypeProduct, 
                                    on_delete=models.SET_NULL,
                                    #limit_choices_to={'category_l1':'Transfert'}, 
                                    blank=True, null=True)   

    oper_input = models.ForeignKey(User, on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='%(app_label)s_%(class)s_oper_input',  
                            verbose_name="Oper Input")
    #
    nature =  models.CharField(max_length=50, blank=True, null=True)
    
    date_val = models.DateField('DATE_VAL')
    
    corresp = models.ForeignKey(Corresp, on_delete=models.CASCADE)

    account = models.ForeignKey(AccountCorresp, on_delete=models.CASCADE)

    montant_op = models.DecimalField(default=0, max_digits=18, decimal_places=2,
                                     verbose_name="Opening Balance", 
                                     help_text="Solde d'Ouverture",
                                     blank=True, null=True) 
    
    montant = models.DecimalField(default=0, max_digits=18, decimal_places=2,
                                  verbose_name="Closing Balance", 
                                  help_text="Solde de Clôture"
                                  )
    #
    objects = DataFrameManager()

    class Meta:
        abstract = True