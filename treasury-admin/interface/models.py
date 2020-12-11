# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
#
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

#

import decimal

#
from django.core.files.storage import FileSystemStorage
from django_pandas.managers import DataFrameManager

import os

## Create your models here.

class ApTB(models.Model):

  #statut
  date_rpt = models.DateField(db_column='DRT')   
  date_cpt = models.DateField(db_column='DCO')  
  date_val = models.DateField(db_column='DVA')   
  cha_lv2 = models.CharField(db_column='CHA2',max_length = 200)
  cha_lv3 = models.CharField(db_column='CHA3',max_length = 200) 
  code_client = models.CharField(db_column='CLI',max_length=6, blank=True, null=True)
  ccy_code = models.CharField(db_column='DEV',max_length=3)
  acc = models.CharField(db_column='NCP',max_length=11)
  solde_t0 = models.DecimalField(db_column='SHI',max_digits=18, decimal_places=2) 
  mvmt_dr = models.DecimalField(db_column='MVTD',max_digits=18, decimal_places=2)  
  mvmt_cr = models.DecimalField(db_column='MVTC',max_digits=18, decimal_places=2)  
  solde_t1 = models.DecimalField(db_column='SDE',max_digits=18, decimal_places=2)  
  ctrl = models.DecimalField(db_column='CTRL',max_digits=18, decimal_places=2)  
  timestamp = models.CharField(db_column='TIMESTAMP',max_length=12)
  ##Foreign Keys
  objects = DataFrameManager()    

  def __str__(self):
    return u"%s | %s" %(self.date_rpt, self.acc)

  class Meta:
    managed = True
    db_table = 'ap_tb'
    verbose_name = "Interface Amplitude Trial Balance (TB)" 
    verbose_name_plural = "Interface Amplitude Trial Balance (TB)" 
    #
    unique_together = (('date_rpt','acc','ccy_code',))


class ApBkcom(models.Model):

  #statut
  entity = models.CharField(db_column='AGE',max_length=5, blank=True, null=True)      
  date_val = models.DateField(db_column='DATE_VAL', blank=True, null=True)   
  date_cr = models.DateField(db_column='DATE_CR', blank=True, null=True)  
  date_dr = models.DateField(db_column='DATE_DR', blank=True, null=True)  
  code_client = models.CharField(db_column='CLI',max_length=6, blank=True, null=True)
  acc = models.CharField(db_column='ACC',max_length=6)
  acc_txt = models.CharField(db_column='ACC_TXT',max_length=100, blank=True, null=True)
  ccy_code = models.CharField(db_column='CCY_CODE',max_length=3)
  montant = models.DecimalField(db_column='AMT',max_digits=18, decimal_places=2)  
  timestamp = models.CharField(db_column='TIMESTAMP',max_length=12)


  ##Foreign Keys
  objects = DataFrameManager()    

  def __str__(self):
    return u"%s | %s" %(self.date_val, self.code_client,)

  class Meta:
    managed = True
    db_table = 'ap_bkcom'
    verbose_name = "Interface Amplitude A/C Balance (BKCOM)" 
    verbose_name_plural = "Interface Amplitude A/C Balance (BKCOM)" 
    #
    unique_together = (('date_val','code_client','entity','acc','ccy_code',))


class ApBkmvt(models.Model):

  #statut
  statut = models.CharField(db_column='ETA', max_length=2)
  entity = models.CharField(db_column='AGE',max_length=5, blank=True, null=True)      
  date_val = models.DateField(db_column='DVA')      
  date_trd = models.DateField(db_column='DSAI', blank=True, null=True) 
  time_trd = models.TimeField(db_column='HSAI', blank=True, null=True)
  code_client = models.CharField(db_column='CLI',max_length=6)
  alias = models.CharField(db_column='NOMP',max_length=200)  
  acc = models.CharField(db_column='NCP',max_length=11)    
  #
  nature = models.CharField(db_column='NAT',max_length=6)      
  direction = models.CharField(db_column='SEN', max_length=1)
  
  #
  ccy_code1 = models.CharField(db_column='DEVC',max_length=3, blank=True, null=True)
  montant1 = models.DecimalField(db_column='MHTT',max_digits=18, decimal_places=2)  

  ccy_code2 = models.CharField(db_column='DEVA', max_length=3, blank=True, null=True)
  montant2 = models.DecimalField(db_column='MNAT', max_digits=18, decimal_places=2)  
  
  fx_rate = models.DecimalField(db_column='TCAI2', max_digits=18, decimal_places=8)	

  ctrl = models.BooleanField(db_column='CTRL', default=False)
  
  timestamp = models.CharField(db_column='TIMESTAMP', max_length=12)


  ##Foreign Keys
  objects = DataFrameManager()    

  def __str__(self):
    return u"%s | %s | %s" %(self.date_val, self.nature, self.code_client, )

  class Meta:
    managed = True
    db_table = 'ap_bkmvt'
    verbose_name = "Interface Amplitude Fx Retail (BKMVT)" 
    verbose_name_plural = "Interface Amplitude Fx Retail (BKMVT)" 



class ApBkdopi(models.Model):

  #statut
  nature = models.CharField(db_column='NATURE', max_length=3)  
  agenceID = models.CharField(db_column='AGENCE_ID', max_length=5, blank=True, null=True) 
  ref_id = models.CharField(db_column='REF_ID', max_length=11)  
  statut_sys = models.CharField(db_column='STATUT_SYS', max_length=2)
  ccy_code = models.CharField(db_column='CCY_CODE', max_length=3)   
  operType = models.CharField(db_column='OTRF', max_length=1, blank=True, null=True)
  #
  donneur = models.CharField(db_column='DONNEUR', max_length=200, blank=True, null=True)  
  accDonneur = models.CharField(db_column='NCPDO', max_length=11, blank=True, null=True)  
  benef= models.CharField(db_column='BENEF', max_length=200, blank=True, null=True) 
  accBenef = models.CharField(db_column='NCPBF', max_length=11, blank=True, null=True)
  #
  montant = models.DecimalField(db_column='MONTANT', max_digits=18, decimal_places=2)  
  montant_xaf = models.DecimalField(db_column='MONTANT_XAF', max_digits=18, decimal_places=0)
  #
  fxRate = models.DecimalField(db_column='FX_RATE', max_digits=12, decimal_places=7, blank=True, null=True)  
  date_val = models.CharField(db_column='DATE_VAL', max_length=8)  
  date_exec = models.CharField(db_column='DATE_EXEC', max_length=8, blank=True, null=True)  
  #
  invoice = models.CharField(db_column='INV', max_length=200, blank=True, null=True)  

  feeType = models.CharField(db_column='FEE_TYPE', max_length=3, blank=True, null=True)
  motif = models.TextField(db_column='MOTIF',null=True, blank=True)

  uti = models.CharField(db_column='UTI', max_length=5, blank=True, null=True)  

  timestamp = models.CharField(db_column='TIMESTAMP', max_length=12)

  objects = DataFrameManager()    

  def __str__(self):
    return u"%s | %s" %(self.statut_sys, self.ref_id,)

  class Meta:
    managed = True
    db_table = 'ap_bkdopi'
    unique_together = (('ref_id', 'statut_sys',),)
    verbose_name = "Interface Amplitude TRF/RPT (BKDOPI)" 
    verbose_name_plural = "Interface Amplitude TRF/RPT (BKDOPI)" 

class ApBkcli(models.Model):

  ref_id = models.CharField(max_length=6, unique=True)
  fullname = models.CharField(max_length=100, null=True, blank=True)

  chk_actif = models.BooleanField(default=False,
                                  verbose_name="Chk Actif", 
                                  help_text="Cochez si la client normal")     

  date_profil = models.DateField(null=True, blank=True, verbose_name="Date de Création")   
  date_val = models.DateField(null=True, blank=True, verbose_name="Date de Modification")   

  class Meta:
    managed = True
    db_table = 'ap_bkcli'
    ordering = ('ref_id',)

    verbose_name = "Interface Amplitude client (BKCLI)"
    verbose_name_plural = "Interface Amplitude client (BKCLI)"        

  def __str__(self):
    return u"%s | %s" %(self.ref_id, self.fullname)
