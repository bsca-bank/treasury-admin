# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
import datetime, decimal
from datetime import date, timedelta
#
from django.db import models
from django.db.models import Sum, Max, Min
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.template.defaultfilters import truncatechars
#
from django_pandas.managers import DataFrameManager
#
from tiers.corresp.models import Corresp, AccountCorresp
from tiers.client.models import ClientCtrl, ClientFileStorage
#
from util.fx.models import Ccy
from util.fileStorage.models import *
from util.workflow.models import *
from util.workflow.abstracts import MixinFourEyesChecking, MixinDocTracingLog
from util.catalog.models import CatalogTypeCommercial
from util.catalog.models import *
from util.workflow.models import Statut
#
from interface.models import *
#
from .abstracts import *
from .func import pct_dossier, pct_dom_dossier_multi
from django.contrib import admin
#
from django.contrib.humanize.templatetags.humanize import intcomma
from notification.models import EmailTemplate

def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.dossier.pk
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)  


class TrfDossierCtrl(TrfDossierBase, 
                    MixinFourEyesChecking, 
                    MixinTreasuryCtrl, 
                    MixinSettlementCtrl,
                    MixinDocTracingLog,
                    MixinNotify,
                    MixinLABFT):

    dossier_dom = models.ForeignKey('DomDossierCtrl', on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_dossierDom',  
                                verbose_name="Dossier de Domiciliation")

    dossier_dom_m2m = models.ManyToManyField('DomDossierCtrl', through='DomDossierMulti',
                                related_name='%(app_label)s_%(class)s_dossier_dom_m2m',  
                                verbose_name="Dossier de Domiciliation M2M")

    bkdopi = models.OneToOneField('TrfDossierExec', on_delete=models.SET_NULL, 
                               blank=True, null=True,
                               related_name='%(app_label)s_%(class)s_bkdopi',
                               help_text="Amplitude Record Reference")

    msg_payment = models.ForeignKey(SygmaCtrl, on_delete=models.SET_NULL, 
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_msg_payment',  
                                verbose_name="Payment Message")   

    dossier_couvr = models.ForeignKey('TrfDossierCouvr', on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_dossierCouvr',  
                                verbose_name="Couvr BEAC")

    dossier_rtroc = models.ForeignKey('TrfDossierCouvr', on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_dossierRtroc',  
                                    verbose_name="Rtroc BEAC")


    chk_recu = models.BooleanField(default=False, 
                                   verbose_name="Exéc",
                                   help_text="Check saisie d'Exécution")
    

    #add other data manager
    objects = DataFrameManager()

    @property
    def date_ap(self):
        
        if self.date_val:        
            date_val = self.date_val
            c_oper = self.nomenc_lv0.code_oper
            c_nature = self.nomenc_lv0.code_nature
            
            #90 days for import goods
            if c_oper == "M" and c_nature == "B":
                date_ap = date_val + timedelta(days=90)
                return date_ap
            #30days for import service
            elif c_oper == "M" and c_nature == "S":
                date_ap = date_val + timedelta(days=30)
                return date_ap
            #15days for export
            elif c_oper == "X":
                date_ap = date_val + timedelta(days=15)
                return date_ap
            else:
                return None
        else:
            return None
            
    #calculat the residual days
    def nb_jours(self):
        
        nb_days = None

        if self.date_val and self.time_verify:        
            delta = self.date_val - self.time_verify.date()
            nb_days = delta.days
        elif self.time_approv:
            delta = date.today() - self.time_approv.date()
            nb_days = delta.days
        else:
            nb_days = "-"
        
        outset = nb_days

        return outset 

    def save(self, *args, **kwargs):

        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        #
        if self.montant_lc and not self.fx_rate:
            self.fx_rate = self.montant_lc/self.montant

        return super(TrfDossierCtrl, self).save(*args, **kwargs)

    #common cleaning rules
    def clean(self):
        
        #validation level
        if self.chk_verify:

            if not self.nomenc_lv0 or not self.nomenc_lv1:     
                raise ValidationError("Nomenclature Niveau 0 et 1 requis")
        
        #approvral level
        if self.chk_approv:

            if not self.corresp:
                raise ValidationError("Correspondant requise")     
            #
            if self.type_fund == 3 and not self.client.chk_actif:
                if not self.chk_exec:
                    raise ValidationError("Validation de directeur DMF requis")     

        #check if nomenc need a dom dossier
        if self.nomenc_lv0 and not self.dossier_dom:
            if self.nomenc_lv0.chk_dom:
                raise ValidationError("Dossier de domiciliation requis!")



    #model configuration
    class Meta:
        managed = True
        db_table = 'trf_dossier_ctrl'  
        verbose_name = 'TRF/RPT/VIR/CREDOC Reception'
        verbose_name_plural = 'TRF/RPT/VIR/CREDOC Reception'  

    #show up settings
    def __str__(self):
        return u" %s | %s | %s" %(self.type_product.code_product, self.id, self.bkdopi)
#
class DomDossierCtrl(DomDossier, 
                    MixinFourEyesChecking, 
                    MixinApureCtrl,
                    MixinDocTracingLog,
                    MixinNotify):  

    def clean(self):

        #check if nomenc need a dom dossier
        if self.chk_verify and not self.date_ref:
            self.chk_verify = False
            raise ValidationError("La saisie de date de validation est obligasoire!")

        if self.client:
                        
            if not self.client.niu:
                raise ValidationError("La saisie de 'NIU/Identification d'établissement' dans ClientCtrl est obligasoire! Mettez 'N/A' si non applicable")

            if not self.client.alias:
                raise ValidationError("La saisie de 'sigle' dans ClientCtrl est obligasoire!")

            if not self.client.type_client:
                raise ValidationError("La saisie de 'type_client' dans ClientCtrl est obligasoire!")

            if not self.client.oper:
                raise ValidationError("La saisie de 'oper' dans ClientCtrl est obligasoire!")

            if not self.client.email:
                raise ValidationError("La saisie de 'email' dans ClientCtrl est obligasoire!")

        if not self.montant_lc or self.montant_lc == 0:
            raise ValidationError("Montant local est obligatoire!")

    @property
    def num_verify(self):
        # extend scope of variable
        num_dossier = TrfDossierCtrl.objects.filter(dossier_dom_m2m__id__exact=self.id, chk_verify=True).count()
        return num_dossier    

    @property
    def num_exec(self):
        # extend scope of variable
        num_dossier = TrfDossierCtrl.objects.filter(dossier_dom_m2m__id__exact=self.id, chk_exec=True).count()
        return num_dossier    

    @property
    def verify_pct(self):
        # get all entries for the given cart
        entries = TrfDossierCtrl.objects.filter(dossier_dom_m2m__id__exact=self.id, chk_verify=True)
        return pct_dossier(self, entries)
    @property
    def approv_pct(self):
        # get all entries for the given cart
        entries =TrfDossierCtrl.objects.filter(dossier_dom_m2m__id__exact=self.id, chk_approv=True)
        return pct_dossier(self, entries)
    @property
    def exec_pct(self):
        # get all entries for the given cart
        entries = TrfDossierCtrl.objects.filter(dossier_dom_m2m__id__exact=self.id, chk_pay=True)
        return pct_dossier(self, entries)
    @property
    def apure_pct(self):
        # #get all entries for the given cart
        # entries = TrfDossierCtrl.objects.filter(dossier_dom_m2m__id__exact=self.id, dossier_dom_m2m__id__exact=True)
        # return pct_dossier(self, entries)
        return 0

    class Meta:
        managed = True
        db_table = 'dom_dossier_ctrl'   
        verbose_name = "DOM Dossier Ctrl."
        verbose_name_plural = "DOM Dossier Ctrl." 
        
    def __str__(self):
        return u"%s | %s | %s" %(self.statut, self.id, self.ref_di)
#
class TrfDossierExec(ApBkdopi):

    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, 
                               blank=True, null=True,
                               related_name='%(app_label)s_%(class)s_statut')    
    #dossier
    trfDossier = models.OneToOneField('TrfDossierCtrl', 
                                    on_delete=models.SET_NULL, 
                                    blank=True, null=True,
                                    related_name='%(app_label)s_%(class)s_trfDossier')
    #
    trfDossierCouvr = models.ForeignKey('TrfDossierCouvr', 
                                    on_delete=models.SET_NULL, 
                                    blank=True, null=True,
                                    related_name='%(app_label)s_%(class)s_trfDossierCouvr')

    #
    date_val_d = models.DateField(blank=True, null=True)  
    date_exec_d = models.DateField(blank=True, null=True)  

    ctrl = models.BooleanField(db_column='CTRL', default=False,
                               verbose_name="ctrl",
                               help_text="Check rapprochement")

    objects = DataFrameManager()    

    def __str__(self):
        return u"%s" %(self.ref_id)

    def s_donneur(self):
        return truncatechars(self.donneur,15)

    def s_benef(self):
        return truncatechars(self.benef,15)
   
    def fx_rate(self):
        try:
            return "%.3f" % self.fxRate
        except:
            return "Err"

    class Meta:
        managed = True
        db_table = 'trf_dossier_exec'
        verbose_name = 'TRF BO Manager'
        verbose_name_plural = 'TRF BO Manager' 

class RptDossierExec(TrfDossierExec):
    class Meta:
        proxy = True
        verbose_name = 'RPT BO Manager'
        verbose_name_plural = 'RPT BO Manager'  

#
class TrfDossierCouvr(TrfDossierCouvrBase, MixinFourEyesChecking, MixinNotify):

    chk_verify = models.BooleanField(default=False, 
                                  verbose_name="EMI",
                                  help_text="Cochez si dossier est emis à la BEAC")

    chk_approv = models.BooleanField(default=False, 
                                  verbose_name="FIN",
                                  help_text="Cochez si l'ensemble des transactions liée soient exécutées")

    def date_trans(self):
        if self.time_verify:
            return self.time_verify.date()
        else:
            return "-"

    #calculat the residual days
    def nb_jours(self):
        
        nb_days = None

        if self.time_verify:        
            delta1 = date.today() - self.time_verify.date()
            nb_days = delta1.days

            if self.date_couvr:
                delta2 = self.date_couvr - self.time_verify.date()
                nb_days = min(delta1.days, delta2.days)
        
            if (self.chk_verify and self.chk_approv) and not (self.chk_pay and self.chk_couvr):
                nb_days = None

        if nb_days:
            outset = str(nb_days) + " jc"
        else:
            outset = "-"

        return outset 


    def num_doc(self):
        # extend scope of variable
        try:
            num_dossier_couvr = TrfDossierCtrl.objects.filter(dossier_couvr=self.id).count()
        except:
            num_dossier_couvr = 0
        try:
            num_dossier_rtroc = TrfDossierCtrl.objects.filter(dossier_rtroc=self.id).count()
        except:
            num_dossier_rtroc = 0

        return str(num_dossier_couvr + num_dossier_rtroc )

    def clean(self):

        if self.chk_verify and not self.chk_approv:
            try:
                num_dossier_couvr = TrfDossierCtrl.objects.filter(dossier_couvr=self.id).count()
            except:
                num_dossier_couvr = 0
            try:
                num_dossier_rtroc = TrfDossierCtrl.objects.filter(dossier_rtroc=self.id).count()
            except:
                num_dossier_rtroc = 0

            if num_dossier_couvr + num_dossier_rtroc == 0: 
                raise ValidationError("Complétez les transactions sous-jascent dans le panier")

            dossiers = TrfDossierCtrl.objects.filter(dossier_couvr=self.id)
            for obj in dossiers:
                if not obj.type_fund and not self.chk_couvr:
                    raise ValidationError("Complétez le type de tresorerie (type_fund) dans le ticket de transfert %s" %(obj.id))


        elif not self.chk_verify:

            if self.chk_pay or self.chk_couvr:
                raise ValidationError("Cochez le check verify d'abord")
                
        if self.chk_pay:
            if not self.date_val:     
                raise ValidationError("La date valeur est obligatoire")

        if self.chk_couvr:
            if not self.date_couvr:     
                raise ValidationError("La date de couverture est obligatoire")

        if self.chk_pay and self.chk_couvr:
            if not self.ref_swift:     
                raise ValidationError("Référence Swift est obligatoire")
            if not self.ref_sygma:     
                raise ValidationError("Référence Sygma est obligatoire")

        #force motif de rejet
        try:
            ctype = ContentType.objects.get_for_model(self, for_concrete_model=False)
            nck_statut = Statut.objects.get(content_type=ctype, statut='/NCK')
            if self.statut == nck_statut and not self.obs:
                raise ValidationError("Les informations liée au rejet est obligatoire")
        except:
            return 0
    class Meta:
        managed = True
        db_table = 'trf_dossier_couvr'
        unique_together = ('year_trd','ref_id',)
        verbose_name = 'BEAC RTROC/COUVR'
        verbose_name_plural = 'BEAC RTROC/COUVR'  

#Create your models here.
class DomDossierMulti(MixinApureCtrl, MixinNotify):  

    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, 
                                blank=True, null=True,
                                related_name='%(app_label)s_%(class)s_statut',)
    
    oper_input = models.ForeignKey(User, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_oper_input',  
                                verbose_name="Agent")
    #dossier
    dossier_trf = models.ForeignKey('TrfDossierCtrl', on_delete=models.CASCADE, 
                                    related_name='%(app_label)s_%(class)s_DomDossierMulti',
                                    verbose_name="Dossier de Paiement")
    #domiciliation
    dossier_dom = models.ForeignKey('DomDossierCtrl', on_delete=models.CASCADE,
                                related_name='%(app_label)s_%(class)s_DomDossierMulti',  
                                verbose_name="Dossier de Domiciliation")

    nomenc_lv0 = models.ForeignKey(CatalogTypeCommercial, 
                            limit_choices_to={'level':0},
                            on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='%(app_label)s_%(class)s_nomenc_lv0',)

    dom_pct = models.DecimalField(default=1, max_digits=7, decimal_places=4,
                                blank=True, null=True,
                                verbose_name="DOM Ratio",
                                help_text="Ratio de domiciliation") 	

    dom_pct_montant_lc = models.DecimalField(max_digits=18, decimal_places=0,
                                blank=True, null=True,
                                verbose_name="dom_pct_montant_lc",
                                help_text="Montant équivalent en F.CFA") 

    obs = models.TextField(max_length=1000, null=True, blank=True,
                            default="Nous n'avons pas reçu votre dossier d'apurement.",)
    
    date_verify = models.DateField(null=True, blank=True, editable=False,
                                    verbose_name="Date de Domiciliation",)   

    date_val = models.DateField(null=True, blank=True, editable=False,
                                    verbose_name="Date de Réglement",)  
    
    #Addtional Information for filtering
    #------------------------------------------------------------------------------------------------
    ref_exec = models.CharField(max_length=50, 
                                null=True, blank=True, 
                                verbose_name="REF_EXEC",
                                help_text="Réf d'Exécution") 
    #
    ref_di = models.CharField(max_length=50,verbose_name="REF_DI", blank=True, null=True,
                            help_text="Réf de déclaration distribuée par MINFI/GUOT ou Banque Centrale")

    #Save latest email sending information
    chk_email = models.BooleanField(default=False, verbose_name="Chk Sent Email")
    sending_user = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='%(app_label)s_%(class)s_sending_oper',
                                  verbose_name="Sending user") 
    
    def __str__(self):
        return u"%s| %s | (%s | %s)" %(self.id, self.statut, self.dossier_dom, self.dossier_trf) 

    def save(self, *args, **kwargs):
        ''' On save, update ref_trf & ref_dom '''
        if self.dossier_trf.ref_exec:
            self.ref_exec = self.dossier_trf.ref_exec
        #
        if self.dossier_dom.ref_di:
            self.ref_di = self.dossier_dom.ref_di
        #
        if self.dom_pct and not self.dom_pct_montant_lc:
            if self.dossier_trf.montant_lc:
                self.dom_pct_montant_lc = round(float(self.dom_pct)*float(self.dossier_trf.montant_lc),0)
            else:
                self.dom_pct_montant_lc = 0

        elif not self.dom_pct and self.dom_pct_montant_lc:
            if self.dossier_trf.montant_lc:
                self.dom_pct = round(float(self.dom_pct_montant_lc)/float(self.dossier_trf.montant_lc),4)
            else:
               self.dom_pct = 1 

        elif not self.dom_pct and not self.dom_pct_montant_lc:
            self.dom_pct = 1
            if self.dossier_trf.montant_lc:
                self.dom_pct_montant_lc = self.dossier_trf.montant_lc

        return super(DomDossierMulti, self).save(*args, **kwargs)
        
    @property
    def apure_ccy(self):
        return self.dossier_trf.ccy
    @property
    def apure_montant(self):
        outset = float(self.dossier_trf.montant) * float(self.dom_pct)
        return "%s%s" % (intcomma(int(outset)), ("%0.2f" % outset)[-3:])
    @property
    def apure_montant_lc(self):
        if self.dossier_trf.montant_lc:
            outset = float(self.dossier_trf.montant_lc) * float(self.dom_pct)
            return "%s" % (intcomma(int(outset)))
        else:
            outset = "N/A"
            return outset
    @property
    def dom_ccy(self):
        return self.dossier_dom.ccy
    @property
    def dom_montant(self):
        outset = self.dossier_dom.montant
        return "%s%s" % (intcomma(int(outset)), ("%0.2f" % outset)[-3:])
    @property
    def dom_montant_lc(self):
        outset = self.dossier_dom.montant_lc
        return "%s" % (intcomma(int(outset)))
    @property
    def dom_montant_lc(self):
        outset = self.dossier_dom.montant_lc
        return "%s" % (intcomma(int(outset)))
    @property
    def apure_pct(self):
        try:
            if self.dossier_dom.ccy == self.dossier_trf.ccy:
                outset = float(self.dossier_trf.montant)*float(self.dom_pct)/float(self.dossier_dom.montant)*100
            else:
                outset = float(self.dossier_trf.montant_lc)*float(self.dom_pct)/float(self.dossier_dom.montant_lc)*100
            
            return "%s" % ("%0.2f" % outset)
        
        except:
            return "#Err"
        
        #get all entries for the given cart
        #entries = DomDossierCtrl.objects.filter(id__exact=self.dossier_dom.id)
        #return pct_dom_dossier_multi(self, entries)
    
    #calculat the residual days
    @property
    def jc_restant(self):

        if self.dossier_trf.date_val:        
            date_val = self.dossier_trf.date_val
            c_oper = self.dossier_dom.nomenc_lv0.code_oper
            c_nature = self.dossier_dom.nomenc_lv0.code_nature
            
            #90 days for import goods
            if c_oper == "M" and c_nature == "B":
                date_ap = date_val + timedelta(days=90)
                delta = date_ap - date.today()
            #30days for import service
            elif c_oper == "M" and c_nature == "S":
                date_ap = date_val + timedelta(days=30)
                delta = date_ap - date.today()
            #15days for export
            elif c_oper == "X":
                date_ap = date_val + timedelta(days=15)
                delta = date_ap - date.today()
            else:
                return "-"

            if delta.days > 0:
                outset = str(delta.days) + " jc"
            else:
                outset = "Expiré"     
        else:
            outset = "-"

        return outset 
    
    def clean(self):

        if self.dossier_dom.ccy != self.dossier_trf.ccy:
            #check cross currency problem
            if not self.dossier_trf.montant_lc or self.dossier_trf.montant_lc == 0:
                raise ValidationError("Le montant local en F.CFA de ticket est obligatoire")  

        #check nomenc problem
        if self.dossier_dom.nomenc_lv0 != self.dossier_trf.nomenc_lv0:
            raise ValidationError("Nomenc lv0 ne correspond pas la nomenc_lv0 de dossier de domiciliation!")  
        
        if self.dom_pct and self.dom_pct <= 0:
            raise ValidationError("Dom pct est strictement supérieur à zéro!")

        if self.dossier_trf.chk_verify and self.dossier_dom and self.dom_pct:
            ccy_tag = 0
            domDossierMulti = DomDossierMulti.objects.filter(dossier_dom=self.dossier_dom)
            for obj in domDossierMulti:
                if obj.dossier_trf.ccy != obj.dossier_dom.ccy:
                    ccy_tag = 1

            if ccy_tag == 0: 
                dom_amt = self.dossier_dom.montant
                deal_amt = float(self.dossier_trf.montant) * float(self.dom_pct)

            else:              
                dom_amt = self.dossier_dom.montant_lc
                deal_amt = float(self.dossier_trf.montant_lc) * float(self.dom_pct)
            
            try:
                entries = DomDossierMulti.objects.filter( \
                    dossier_dom=self.dossier_dom,
                    dossier_trf__chk_verify=True,
                ).exclude(id = self.id)
                    
                montant_tot = 0
                # iterate through entries
                for entry in trf_entries:
                    
                    montant_dom_tot += dom_pct_montant_lc
                    if ccy_tag == 0:
                        montant_tot += montant
                    else:
                        if not entry.montant_lc or entry.montant_lc == 0:
                            montant_tot += montant_lc
                        else:
                            raise ValidationError("Montant local de ticket " + str(entry.id) + " requis")  
            except:
                montant_tot = 0
            
            #rapatriment
            if self.dossier_dom.nomenc_lv0.code_oper == "X":
                return 0
            else:
                print("DEBUG:"+ str(self.dossier_trf.type_product))
                if round(deal_amt + montant_tot,2) > round(dom_amt,2) + 1:
                    if not self.dossier_trf.chk_approv:
                        raise ValidationError("En ajoutant le Montant de deal le total des paiements dépasse le montant de domiciliation!") 
        return 0

    class Meta:
        managed = True
        db_table = 'dom_dossier_multi'   
        verbose_name = "DOM Dossier Apurement"
        verbose_name_plural = "DOM Dossier Apurement" 
        unique_together = ('dossier_dom','dossier_trf')