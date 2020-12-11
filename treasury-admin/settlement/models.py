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
from util.workflow.abstracts import MixinFourEyesChecking
#
from .abstracts import MT950
import os

## Create your models here.
class TreasuryPosition(MT950, MixinFourEyesChecking):

    class Meta:
        managed = True
        db_table = 'tresor_loro_corresp'
        ordering = ('-date_val',)
        unique_together = (('date_val','corresp','account'),)
        
        verbose_name = 'Contrôle de la solde de trésorerie'
        verbose_name_plural = 'Contrôle de la solde de trésorerie'  

    def __str__(self):
        return u"%s | %s | %s" %(self.date_val, self.corresp, self.account)
