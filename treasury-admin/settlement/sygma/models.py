# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

#
##import tiers.agence.models 
from interface.sygma.models import Sygma
from tiers.client.models import ClientCtrl

class SygmaCtrl(Sygma):    

  clientCtrl = models.ForeignKey(ClientCtrl, models.SET_NULL, blank=True, null=True) 
  #
  ctrl = models.BooleanField(db_column='CTRL', default=False)
  #
  class Meta:
    managed = True
    db_table = 'tresor_sygma_ctrl'
    verbose_name = 'Contrôle de SYGMA'
    verbose_name_plural = 'Contrôle de SYGMA'

  def __str__(self):
    return u"%s" %(self.ref_id)
  
  def check_settlement(self, ctrl):
    self.ctrl = ctrl
    self.save