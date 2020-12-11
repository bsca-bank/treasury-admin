# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
#
from django_pandas.managers import DataFrameManager

from util.fx.models import Ccy


class Account(models.Model):
    #basic
    alias = models.CharField(max_length=50)
    account = models.CharField(max_length=50, null=True, blank=True)
    ccy = models.ForeignKey(Ccy, on_delete=models.CASCADE)
    #descriptive
    fullname = models.CharField(max_length=100, null=True, blank=True)
    obs = models.CharField(max_length=100,null=True, blank=True)
    #ctrl
    chk_active = models.BooleanField(default=True)             
    #    
    objects = DataFrameManager()         
   
    class Meta:
        abstract = True