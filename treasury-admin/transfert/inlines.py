# -*- coding: utf-8 -*-
from django.contrib import admin
from django.db.models import Q

#
from .models import *
from .proxys import *
from .forms import *
    
class TrfDossierExecInline(admin.TabularInline):
    
    model = TrfDossierExec
    extra = 0    
    sortable_field_name = "ref_id"
    fieldsets = (
        (None, {
            'fields': ('ref_id','donneur','date_exec','statut_sys','ccy_code','montant','montant_xaf')
            }),  
    )
    show_change_link = True
    readonly_fields = ('ref_id','donneur','date_exec','statut_sys','ccy_code','montant','montant_xaf')
    can_delete = False  

class TrfDossierCtrlProxyInline(admin.TabularInline):
    model = TrfDossierCtrlProxy
    fk_name = 'dossier_couvr'
    form = TrfDossierCtrlForm
    extra = 0
    sortable_field_name = "id"
    fieldsets = (
        (None, {
            'fields': ('id','statut','client','ccy','montant','type_fund','chk_verify','chk_approv','chk_pay','bkdopi')
            }),  
    )
    readonly_fields = ('id','statut','client','ccy','montant','type_fund','chk_verify','chk_approv','chk_pay','bkdopi')
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request):
        return False  

class TrfDossierCtrlInline(admin.TabularInline):
    #TRF/RPT may be linked to a Rtroc Ticket ()
    model = TrfDossierCtrl
    fk_name = 'dossier_rtroc'
    form = TrfDossierCtrlForm
    extra = 0
    sortable_field_name = "id"
    fieldsets = (
        (None, {
            'fields': ('id','statut','client','ccy','montant','type_fund','chk_verify','chk_approv','chk_pay','bkdopi')
            }),  
    )
    readonly_fields = ('id','statut','client','ccy','montant','type_fund','chk_verify','chk_approv','chk_pay','bkdopi')
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request):
        return False  

class SingleDomDossierInline(admin.TabularInline):
    model = DomDossierMulti
    form = DomDossierMultiForm
    show_change_link = True
    #
    extra = 0

    fieldsets = (
        (None, {
            'fields': ('id','statut','dossier_trf','dossier_dom','dom_pct','dom_pct_montant_lc','dom_ccy','dom_montant','dom_montant_lc','jc_restant',) #'apure_pct','apure_ccy','apure_montant',
            }),  
    )
    readonly_fields = ('id','statut','date_ap','jc_restant','dom_montant','dom_ccy','dom_montant_lc',) #'apure_pct','apure_ccy','apure_montant',

    def has_add_permission(self, request):
        return True

    # def formfield_for_foreignkey(self, db_field, request, **kwargs):

    #     field = super().formfield_for_foreignkey(db_field, request, **kwargs)

    #     if db_field.name == 'client':
    #         try:
    #             if request._obj_.client:
    #                 # setting the user from the request object
    #                 kwargs['initial'] = request._obj_.client
    #                 # making the field readonly
    #                 kwargs['disabled'] = True
    #                 q_client = Q(apbkcli_ptr=request._obj_.client.id)
    #                 field.queryset = field.queryset.filter(q_client)
    #             else:
    #                 field.queryset = field.queryset.none()
    #         except:
    #             pass

    #         return field

    #     if db_field.name == 'nomenc_lv0':
    #         try:
    #             if request._obj_.nomenc_lv0:
    #                 # setting the user from the request object
    #                 kwargs['initial'] = request._obj_.nomenc_lv0
    #                 # making the field readonly
    #                 kwargs['disabled'] = True
    #                 q_nomenc_lv0 = Q(id=request._obj_.nomenc_lv0.id)
    #                 field.queryset = field.queryset.filter(q_nomenc_lv0)
    #             else:
    #                 field.queryset = field.queryset.none()
    #         except:
    #             pass
            
    #         return field

    #     if db_field.name == 'dossier_dom':
    #         try:    
    #             if request._obj_:
    #                 q_client = Q(client=request._obj_.client)
    #                 q_nomenc_lv0 = Q(nomenc_lv0=request._obj_.nomenc_lv0)
    #                 field.queryset = field.queryset.filter(q_client|q_nomenc_lv0)
    #             else:
    #                 field.queryset = field.queryset.none()
    #         except:
    #             pass
            
    #         return field

class MultiDomDossierInline(SingleDomDossierInline):

    def has_add_permission(self, request):
        return True

class ApureDomDossierInline(SingleDomDossierInline):

    def has_add_permission(self, request):
        return False