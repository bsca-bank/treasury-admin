# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#
from datetime import date
#
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.exceptions import ValidationError
#
from django_pandas.managers import DataFrameManager
#
from util.fx.models import Ccy, CcyPair
from util.catalog.models import CatalogTypeProduct
#
from tiers.depo.models import Depo
from tiers.cpty.models import Cpty
from tiers.client.models import ClientCtrl

'''
FXTicket Base-Model
'''
class FXTicket(models.Model):

    ctrl_cf = models.BooleanField(default=True, 
                                verbose_name="Genr Cashflow",
                                help_text="Check if genrerate cashflow")  

    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.SET_NULL, 
                                    blank=True, null=True,
                                    related_name = '%(app_label)s_%(class)s_type_product')  
    #
    #Basic Trading information
    ref_id = models.CharField(max_length=50, null=True, blank=True)  

    #oper = models.ForeignKey(User, on_delete=models.CASCADE,
    #                        related_name='%(app_label)s_%(class)s_oper')  

    client = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL,
                               blank=True, null=True,
                               related_name ='%(app_label)s_%(class)s_client',
                               verbose_name="Client",                             
                               help_text="Tapez le code client ici Amplitude")    

    cpty = models.ForeignKey(Cpty, on_delete=models.SET_NULL,
                             blank=True, null=True,
                             related_name = '%(app_label)s_%(class)s_cpty',
                             verbose_name="Counterparty",                             
                             help_text="Tapez code client ici")    
   
    date_trd = models.DateField(verbose_name="Trading Date")
    date_val = models.DateField(verbose_name="Value Date")
    date_end = models.DateField(verbose_name="Settlement Date",
                                blank=True, null=True,)

    chk_end = models.BooleanField(default=False, 
                                  verbose_name="Chk End",
                                  help_text="Check if fully settled")    

    ccy_pair = models.ForeignKey(CcyPair, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_ccy_pair', 
                                verbose_name="Currency Pair")
    
    fx_rate = models.DecimalField(default=1, max_digits=8, decimal_places=4)	

    ccy_in = models.ForeignKey(Ccy, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='%(app_label)s_%(class)s_ccy_in', 
                               verbose_name="Receving Ccy")

    ccy_out = models.ForeignKey(Ccy, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_ccy_out', 
                                verbose_name="Paying Ccy")
    
    montant_in = models.DecimalField(default=0, max_digits=18, decimal_places=2, 
                                     verbose_name="Receving Value")	                              

    montant_out = models.DecimalField(default=0, max_digits=18, decimal_places=2, 
                                      verbose_name="Paying Value")  

    class Meta:
        abstract = True

    #calculat the residual days
    def jour_restant(self):
        if self.date_val >= date.today(): 
            delta = self.date_val - date.today()
            outset = str(delta.days) + " jours" 
        else:
            outset = None    
        return outset     

'''
FiTicket Base-Model
'''
class FiTicket(models.Model):

    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.SET_NULL, 
                                    blank=True, null=True,
                                    related_name = '%(app_label)s_%(class)s_type_product')  

    ctrl_cf = models.BooleanField(default=True, 
                                verbose_name="Genr Cashflow",
                                help_text="Check if genrerate cashflow")  
                                
    #oper = models.ForeignKey(User, on_delete=models.CASCADE,
    #                        related_name='%(app_label)s_%(class)s_oper')  

    emetteur = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL,
                               blank=True, null=True,
                               related_name ='%(app_label)s_%(class)s_emetteur',
                               verbose_name="Emetteur",                             
                               help_text="Tapez le code client ici Amplitude")    

    depo = models.ForeignKey(Depo, on_delete=models.SET_NULL,
                            blank=True, null=True,
                            related_name = '%(app_label)s_%(class)s_depo',
                            verbose_name="Depository",
                            help_text="Tapez le code client ici Amplitude")

    client = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL,
                               blank=True, null=True,
                               related_name ='%(app_label)s_%(class)s_client',
                               verbose_name="Client",                             
                               help_text="Tapez le code client ici Amplitude")    

    ref_id = models.CharField(max_length=50)

    ccy	= models.ForeignKey(Ccy, on_delete=models.CASCADE,
                            related_name = '%(app_label)s_%(class)s_ccy')
    
    nominal = models.DecimalField(max_digits=18, decimal_places=2)	

    coupon_couru = models.DecimalField(max_digits=18, decimal_places=2, help_text="Coupon couru à l'acquisition")

    price = models.DecimalField(max_digits=18, decimal_places=2, help_text="Prix d'Aquisition")

    price_pct = models.DecimalField(max_digits=7, decimal_places=4, help_text="Prix d'Aquisition en %")


    fee = models.DecimalField(max_digits=18, decimal_places=2, 
                                blank=True, null=True,
                                help_text="-/+ frais/revenu totaux d'acquisition")

    date_trd = models.DateField(verbose_name="Trading Date")
    date_val = models.DateField(verbose_name="Value Date")
    date_end = models.DateField(verbose_name="Maturity Date")

    chk_end = models.BooleanField(default=False, 
                                  verbose_name="Chk End",
                                  help_text="Check if fully settled")    

    #
    NATURE_CHOICES = (
        (0, 'ACT/360'),        
        (1, 'ACT/ACT'),        
    )
    daycount = models.IntegerField(choices=NATURE_CHOICES, default=0)     

    unit = models.DecimalField(max_digits=18, decimal_places=0, help_text='Nominal par unité')	

    taux = models.DecimalField(max_digits=8, decimal_places=4, help_text='Coupon Rate')  

    class Meta:
        abstract = True

    #calculat the residual days
    def jour_restant(self):
        if self.date_end >= date.today(): 
            delta = self.date_end - date.today()
            outset = str(delta.days) + " jours" 
        else:
            outset = None    
        return outset     

    def clean(self):

        if self.price and self.price_pct and self.nominal:
            try:
                price_calc = self.price_pct/100*self.nominal
            except:
                price_calc = 0

            if abs(self.price - price_calc) >= 1000  :
                raise ValidationError("le prix d'acquisition n'est pas cohéhent avec le prix saisi en % ")


'''
FiTicket Base-Model
'''
class MmTicket(models.Model):

    ctrl_cf = models.BooleanField(default=True, 
                                verbose_name="Genr Cashflow",
                                help_text="Check if genrerate cashflow")  
                                
    #oper = models.ForeignKey(User, on_delete=models.CASCADE,
    #                        related_name='%(app_label)s_%(class)s_oper')  

    cpty = models.ForeignKey(Cpty, on_delete=models.SET_NULL,
                             blank=True, null=True,
                             related_name = '%(app_label)s_%(class)s_cpty',
                             verbose_name="Counterparty",                             
                             help_text="Tapez code client ici")    

    client = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL,
                               blank=True, null=True,
                               related_name ='%(app_label)s_%(class)s_client',
                               verbose_name="Client",                             
                               help_text="Tapez le code client ici Amplitude")    

    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.SET_NULL, 
                                    blank=True, null=True,
                                    related_name = '%(app_label)s_%(class)s_type_product')  

    ccy	= models.ForeignKey(Ccy, on_delete=models.CASCADE,
                            related_name = '%(app_label)s_%(class)s_ccy')

    nominal = models.DecimalField(max_digits=18, decimal_places=2)	

    date_trd = models.DateField(verbose_name="Trading Date")
    date_val = models.DateField(verbose_name="Value Date")
    date_end = models.DateField(verbose_name="Maturity Date")
    #
    chk_end = models.BooleanField(default=False, 
                                  verbose_name="Chk End",
                                  help_text="Check if fully settled")    

    daycount = models.CharField(max_length=12)     

    taux = models.DecimalField(max_digits=8, decimal_places=4)  

    taux_fx = models.FloatField(default=1, 
                                blank=True, null=True, 
                                verbose_name="Taux de change") 

    repayment = models.DecimalField(max_digits=18, decimal_places=2)
    #
    class Meta:
        abstract = True

    #calculat the residual days
    def jour_restant(self):
        if self.date_end >= date.today(): 
            delta = self.date_end - date.today()
            outset = str(delta.days) + " jours" 
        else:
            outset = None    
        return outset     


# Create your models here.
class MixinFolioCtrl(models.Model):
    
    NATURE_CHOICES = (
        (1, '\PROP'), 
        (2, '\CLI'),
        (3, '\COLT')
    )
    folio =  models.IntegerField(choices=NATURE_CHOICES, default=1,
                                verbose_name="Folio",
                                help_text="Portefeuille du titre")    
    #   
    class Meta:
        abstract = True