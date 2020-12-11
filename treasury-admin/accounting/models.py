# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import decimal
import os
#
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
#
from django.core.files.storage import FileSystemStorage
from django_pandas.managers import DataFrameManager
#
from interface.models import *
from tiers.client.models import ClientCtrl
# Create your models here.


class TrialBalance(ApTB):

  clientCtrl = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL, 
                                 null=True)
  ##Foreign Keys
  objects = DataFrameManager()    

  def __str__(self):
    return u"%s | %s" %(self.date_rpt, self.acc)

  class Meta:
    managed = True
    db_table = 'acc_tb'
    verbose_name = "Contrtôle de TB" 
    verbose_name_plural = "Contrtôle de TB" 
    
    

