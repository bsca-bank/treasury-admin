from .models import *
#from import_export.admin import ImportExportModelAdmin
from datetime import date


#class TrfDossierReceptionProxy(TrfDossierCtrl):

#    class Meta:
#        proxy = True
#        verbose_name = "TRF Dossier Reception" 
#        verbose_name_plural = "TRF Dossier Reception" 

class TrfDossierCtrlProxy(TrfDossierCtrl):

    #calculat the residual days
    def nb_jours(self):

        if self.chk_pay and self.date_val:
            delta = self.date_val - self.time_verify.date()
            nb_days = delta.days
            print (delta)
            
        elif self.chk_approv and self.time_approv:
            delta = date.today() - self.time_approv.date()
            nb_days = delta.days

        else:
            nb_days = None

        if nb_days:
            outset = str(nb_days) + " jc"
        else:
            outset = "-"

        return outset 

    #common cleaning rules
    def clean(self):
        
        #validation level
        if self.chk_verify:

            if not self.nomenc_lv0 or not self.nomenc_lv1:     
                raise ValidationError("Nomenclature Niveau 0 et 1 requis")
                #check if nomenc need a dom dossier

            if self.nomenc_lv0 and not self.dossier_dom:
                if self.nomenc_lv0.chk_dom:
                    raise ValidationError("Dossier de domiciliation requis!")

        #approvral level
        if self.chk_approv:

            if not self.corresp:
                raise ValidationError("Correspondant requise")     
            #
            if self.type_fund == 3 and not self.client.chk_actif:
                if not self.chk_exec:
                    raise ValidationError("Validation de directeur requis")   

            if not self.account.ccy == self.ccy:
                raise ValidationError("La monnaie du compte ne correpond pas à la monnaie de l'opération") 

        if self.chk_exec:

            if not self.chk_approv:
                raise ValidationError("Chk_apporv requis!")      
        
        #pay level
        if self.chk_pay:

            if not self.chk_exec:     
                raise ValidationError("Cochez chk_exec!")

    class Meta:
        proxy = True
        verbose_name = "TRF Dossier Ctrl." 
        verbose_name_plural = "TRF Dossier Ctrl."  
 
class RptDossierCtrlProxy(TrfDossierCtrl):

    @property
    def num_dom(self):
        # extend scope of variable
        num_dom= DomDossierMulti.objects.filter(dossier_trf=self.id).count()
        return num_dom    

    class Meta:
        proxy = True
        verbose_name = "RPT Dossier Ctrl." 
        verbose_name_plural = "RPT Dossier Ctrl."  

class CredocDossierCtrlProxy(TrfDossierCtrl):

    #calculat the residual days
    def nb_jours(self):

        if self.chk_pay and self.date_val:
            delta = self.date_val - self.time_verify.date()
            nb_days = delta.days
            print (delta)
            
        elif self.chk_approv and self.time_approv:
            delta = date.today() - self.time_approv.date()
            nb_days = delta.days

        else:
            nb_days = None

        if nb_days:
            outset = str(nb_days) + " jc"
        else:
            outset = "-"

        return outset 

    #common cleaning rules
    def clean(self):
        
        #validation level
        if self.chk_verify:

            if not self.nomenc_lv0 or not self.nomenc_lv1:     
                raise ValidationError("Nomenclature Niveau 0 et 1 requis")
                #check if nomenc need a dom dossier

            if self.nomenc_lv0 and not self.dossier_dom:
                if self.nomenc_lv0.chk_dom:
                    raise ValidationError("Dossier de domiciliation requis!")

        #approvral level
        if self.chk_approv:

            if not self.corresp:
                raise ValidationError("Correspondant requise")     
            #
            if self.type_fund == 3 and not self.client.chk_actif:
                if not self.chk_exec:
                    raise ValidationError("Validation de directeur requis")   

            if not self.account.ccy == self.ccy:
                raise ValidationError("La monnaie du compte ne correpond pas à la monnaie de l'opération") 

        if self.chk_exec:

            if not self.chk_approv:
                raise ValidationError("Chk_apporv requis!")      
        
        #pay level
        if self.chk_pay:

            if not self.chk_exec:     
                raise ValidationError("Cochez chk_exec!")

    class Meta:
        proxy = True
        verbose_name = "CREDOC Dossier Ctrl." 
        verbose_name_plural = "CREDOC Dossier Ctrl." 



class VirDossierCtrlProxy(TrfDossierCtrl):

    class Meta:
        proxy = True
        verbose_name = "VIR Dossier Ctrl." 
        verbose_name_plural = "VIR Dossier Ctrl."  

class TrfDossierCouvrProxy(TrfDossierCouvr):

    class Meta:
        proxy = True
        verbose_name = "BEAC COUVR Ctrl." 
        verbose_name_plural = "BEAC COUVR Ctrl." 

class RptDossierRtrocProxy(TrfDossierCouvr):

    class Meta:
        proxy = True
        verbose_name = "BEAC RTROC Ctrl." 
        verbose_name_plural = "BEAC RTROC Ctrl." 