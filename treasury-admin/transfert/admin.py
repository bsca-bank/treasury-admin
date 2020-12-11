# -*- coding: utf-8 -*-
from django.contrib import admin

from django.contrib.admin.views.main import ChangeList
from django.contrib.contenttypes.models import ContentType
#
from django.utils.html import format_html
from django.urls import path, reverse
from django.conf.urls import url
#
from django.http import HttpResponseRedirect
from django.template import Context, Template
from django.template.response import TemplateResponse
#

from util.catalog.models import CatalogTypeProduct
from util.admin import DocTraceLogGenericInline 
from treasury.inlines import FXCliInline
from cashflow.inlines import CashFlowDetailInline
from notification.inlines import EmailCtrlInline
#
from django.utils import timezone
#choose email Template
from django.http import HttpResponseRedirect
from django.template import Context, Template
from django.template.response import TemplateResponse
#
from django.urls import include, path   
#
from notification.models import EmailTemplate, EmailCtrl
from notification.inlines import EmailCtrlInline
from django.shortcuts import render
from django.template.loader import render_to_string
import datetime, time
#
from .resource import *
from .forms import *
from .inlines import *
from .signals import *
from .admin_base import *    
from .filter import *
from .proxys import *



'''
Transfert Entrant Control Administration
'''
class TrfDossierCtrlAdmin(TrfDossierCtrlAdminBase):

    #change_list_template = 'custom/change_list_with_mail_button.html'  
            
    form = TrfDossierCtrlForm
    
    inlines = [ClientFileStorageGenericInline, EmailCtrlInline]

    list_display = ('id','get_agent','client','get_benef','ccy','montant','time_recv','nb_jours','type_dcc','chk_verify','statut','chk_notify','template_key',)

    list_filter = [
        DirectClientFilter, 
        ('type_product',admin.RelatedOnlyFieldListFilter),
        ('ccy', admin.RelatedOnlyFieldListFilter),
        'chk_recv',
        'chk_dcc',
        'chk_verify',
        'chk_notify',
        'template_key',
    ]

    date_hierarchy = 'created'

    search_fields = ['id','bkdopi__ref_id','oper_input__last_name','client__ref_id','client__alias','client__fullname','montant']
    
    fieldsets = (  

        ('Reception', {
            'fields': (
                'type_product','client','cpty','ccy','montant','obs',#'chk_notify','batch_no','message','template_key'
            ) 
        }), 
        ('Contrôle LAB-FT', {
            'fields': (
                'chk_dcc','type_dcc','obs_dcc',#'chk_notify','batch_no','message','template_key'
            ) 
        }), 

        ('Suivi de traitement', {
            'fields': (
                ('created','oper_input'),
                ('time_recv','oper_recv'),
                ('time_dcc','oper_dcc'),
                ('time_verify','oper_verify'),
                ('time_approv','oper_approv'),
                'type_fund',
                'dossier_couvr','dossier_rtroc',
                'ref_exec','date_val','ref_swift',
            ) 
        }), 

    )

    def get_readonly_fields(self, request, obj=None):

        self.readonly_fields = [
            'created','time_recv','time_verify','time_approv','oper_dcc','time_dcc',
            'oper_input','oper_recv','oper_verify','oper_approv',
            'type_product','type_fund','dossier_couvr','dossier_rtroc',
            'ref_exec','date_val','ref_swift',
            'chk_notify','batch_no','message',]
        return self.readonly_fields

    #authorization filter
    def get_queryset(self, request):
        #TrfDossierCtrlAdminBase, self
        qs = super(TrfDossierCtrlAdminBase, self).get_queryset(request)

        def has_global_view(user):
            #group can see all transactions
            return user.groups.filter(name='ctrl_has_global_view').exists()

        def has_grp_view(user):
            #group can see transactions of the same group
            return user.groups.filter(name='ctrl_has_grp_view').exists()

        #if has controler priority
        if request.user.is_superuser or has_global_view(request.user) :
            return qs
        elif has_grp_view(request.user):
            user_groups = request.user.groups.values_list('id')
            crews = User.objects.filter(groups__id__in = user_groups)
            return qs.filter(oper_input__in=crews) 
        else:
            return qs.filter(oper_input=request.user)  
    
    def save_model(self, request, obj, form, change):

        if not obj.type_product_id:
            obj.type_product_id = 5 #transfert
        
        if not obj.oper_input_id:
            obj.oper_input_id = request.user.id

        #controle DCC
        if obj.chk_dcc and not obj.oper_dcc_id:
            obj.oper_dcc_id = request.user.id

        obj.save()

# Register your models here.
admin.site.register(TrfDossierCtrl, TrfDossierCtrlAdmin)

'''
TRF/RPT Execution Ctrl.
'''
class TrfDossierExecAdmin(TrfDossierExecAdminBase):
# Register your models here.
    #----------------------------------------------------------------------
    list_display = ('ref_id','date_exec_d','get_oper_input',
                    'trfDossier_link',
                    'client_link', 's_donneur',
                    #'get_trf_nomenc',
                    #'dossier_dom_link',
                    'ccy_code','montant','fx_rate','ctrl'
                    ) 
    list_filter = ['ctrl','nature', 'ccy_code',]

    date_hierarchy = 'date_exec_d' 

    #set fieldsets
    #----------------------------------------------------------------------
    fieldsets = (
        ('Etat du dossier', {
            #'classes': ('collapse', 'open'),
            'fields': ('statut_sys','ref_id','date_val','date_exec',
                    'trfDossier','ctrl')
            }),           
        ("Etat d'Exécution", {
            'fields': ('agenceID','operType',  
                       'donneur','accDonneur','benef','accBenef',
                       'ccy_code','montant','montant_xaf','fxRate',
                       'invoice','feeType','motif','uti')
            }),
    )
    def get_readonly_fields(self, request, obj=None):
    
        self.readonly_fields = ['statut_sys','ref_id',
                                'operType','agenceID', 
                                'invoice','date_val','date_exec',
                                'donneur','accDonneur','benef','accBenef',
                                'ccy_code','montant','montant_xaf','fxRate',
                                'feeType','motif','uti',]
        
        return self.readonly_fields
    
    #system status filter
    #----------------------------------------------------------------------
    def get_queryset(self, request):
        qs = super(TrfDossierExecAdmin, self).get_queryset(request)
        return qs.filter(statut_sys='FO').exclude(ref_id__istartswith='RPT') 

admin.site.register(TrfDossierExec, TrfDossierExecAdmin)

class RptDossierExecAdmin(TrfDossierExecAdminBase):

    #----------------------------------------------------------------------
    list_display = ('id','ref_id','date_exec_d','get_oper_input',
                    'trfDossier_link',
                    'client_link','s_benef',
                    #'get_trf_nomenc',
                    #'dossier_dom_link',
                    'ccy_code','montant','fx_rate','ctrl'
                    ) 
    list_filter = ['ctrl','nature','ccy_code',]
    
    date_hierarchy = 'date_exec_d'
    #set fieldsets
    #----------------------------------------------------------------------
    fieldsets = (
        ('Etat du dossier', {
            #'classes': ('collapse', 'open'),
            'fields': ('statut_sys','ref_id','date_val','date_exec',
                    'trfDossier','trfDossierCouvr','ctrl')
            }),           
        ("Etat d'Exécution", {
            'fields': ('agenceID','operType',  
                       'donneur','accDonneur','benef','accBenef',
                       'ccy_code','montant','montant_xaf','fxRate',
                       'invoice','feeType','motif','uti')
            }),
    )
    def get_readonly_fields(self, request, obj=None):
    
        self.readonly_fields = ['statut_sys','ref_id',
                                'operType','agenceID', 
                                'invoice','date_val','date_exec',
                                'donneur','accDonneur','benef','accBenef',
                                'ccy_code','montant','montant_xaf','fxRate',
                                'feeType','motif','uti','trfDossierCouvr']
        
        return self.readonly_fields
    #system status filter
    #----------------------------------------------------------------------
    def get_queryset(self, request):
        qs = super(RptDossierExecAdmin, self).get_queryset(request)
        return qs.filter(statut_sys='FO').exclude(ref_id__istartswith='TRF') 

admin.site.register(RptDossierExec, RptDossierExecAdmin)


'''
Transfert Sortant Control Administration
'''
class TrfDossierCtrlProxyAdmin(TrfDossierCtrlAdminBase):
                
    form = TrfDossierCtrlProxyForm
    
    #attach inline model
    inlines = [SingleDomDossierInline, FXCliInline, CashFlowDetailInline, ClientFileStorageGenericInline]

    list_display = ('id','statut','client_link','get_benef','ccy','montant','type_fund','dossier_couvr','bkdopi','nb_jours','chk_verify','chk_approv','chk_pay')

    list_filter = [
        DirectClientFilter, 
        'type_fund',
        'chk_verify',
        'chk_approv',
        'chk_pay',
        ('statut',admin.RelatedOnlyFieldListFilter),
        ('nomenc_lv0',admin.RelatedOnlyFieldListFilter),
        ('corresp',admin.RelatedOnlyFieldListFilter),        
        ('ccy', admin.RelatedOnlyFieldListFilter),
    ]

    search_fields = ['id','bkdopi__ref_id','oper_input__last_name','client__ref_id','client__alias','client__fullname','montant']
    
    date_hierarchy = 'time_verify' 

    fieldsets = (      
        ('Reception', {
            'fields': ('type_product','client','cpty','montant','ccy',
                        ('created','oper_input'),
                        ('time_recv','oper_recv'),
                        ('time_dcc','oper_dcc'),
                        ('time_verify','oper_verify'),
                        ('time_approv','oper_approv'),) 
            }), 
        ('Front Office', {
            'fields': ( 'chk_recv','nomenc_lv0','nomenc_lv1','dossier_dom',
                        'ref_inv','docTraceLog','statut',
                        ('ccy_lc','montant_lc','fx_rate')) 
            }), 
        ('Contrôle de Dossier', {
            #'classes': ('collapse', 'open'),
            'fields': ('chk_dcc','type_dcc','obs_dcc','chk_verify','obs','dossier_couvr','nb_jours')
            }),
        ('Contrôle de Trésorerie', {
            #'classes': ('collapse', 'open'),
            'fields': (('chk_fund','oper_fund'),'type_fund','chk_approv','corresp','account','dossier_rtroc',)
            }),
        ("Contrôle d'Exécution", {
            #'classes': ('collapse', 'open'),
            'fields': ('chk_exec','ref_exec','bkdopi','chk_pay','date_val','ref_swift',),
            }),        
    )

    def export_rpt_DFX2201(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today + '_rpt_DFX2201.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"ref_ordre"),       
            smart_str(u"date_ordre"),
            smart_str(u"date_pay"),
            smart_str(u"ref_swift"),
            smart_str(u"donneur"),
            smart_str(u"benef"),
            smart_str(u"object"),
            smart_str(u"ref_dom"),
            smart_str(u"corresp"),
            smart_str(u"devise"),
            smart_str(u"montant"),
            #
            smart_str(u"statut"),
            smart_str(u"dossier_couvr"),
            smart_str(u"dossier_rtroc"),
            smart_str(u"nature"),
            smart_str(u"oper_input"),
            smart_str(u"chk_verify"),
            smart_str(u"time_verify"),
            smart_str(u"chk_approv"),
            smart_str(u"time_approv"),  
            smart_str(u"nb_jours"),
            smart_str(u"bkdopi"),
        ])
        for obj in queryset:

            str_ref_ordre = obj.pk

            #
            if obj.time_verify:
                str_date_ordre = obj.time_verify.date()
            else:
                str_date_ordre ="N/A"
            
            #date_val
            if obj.time_approv:
                str_date_val = obj.time_approv.date()
            else:
                str_date_val ="N/A"
    
            #
            if not obj.ref_swift:
                if obj.bkdopi:
                    str_ref_swift = obj.bkdopi.ref_id
                else:
                    str_ref_swift = "N/A"
            else:
                str_ref_swift = obj.ref_swift

            str_donneur = obj.client.fullname
            str_benef = obj.cpty

            #
            if obj.nomenc_lv1:
                str_object = obj.nomenc_lv1.alias
            else:
                str_object ="N/A"

            #ref_dom
            if obj.dossier_dom:
                str_ref_dom = obj.dossier_dom.ref_di
            else:
                str_ref_dom ="N/A"

            #corresp
            if obj.corresp:
                str_corresp = obj.corresp.swift
            else:
                str_corresp ="N/A"

            str_ccy = obj.ccy
            str_montant = obj.montant
            #
            str_nature = obj.nomenc_lv0
            str_oper_input = obj.oper_input
            str_nb_jours = ""
            str_dossier_couvr = obj.dossier_couvr
            str_dossier_rtroc = obj.dossier_rtroc
            str_statut = obj.statut
            str_chk_verify = obj.chk_verify
            str_chk_approv = obj.chk_approv
            str_time_verify = obj.time_verify
            str_time_approv = obj.time_approv
            str_bkdopi = obj.bkdopi

            writer.writerow([
                str_ref_ordre,
                str_date_ordre,
                str_date_val,
                str_ref_swift,
                str_donneur,
                str_benef,
                str_object,
                str_ref_dom,
                str_corresp,
                str_ccy,
                str_montant,
                #``
                str_statut,
                str_dossier_couvr,
                str_dossier_rtroc,
                str_nature,
                str_oper_input,
                str_chk_verify,
                str_chk_approv,
                str_time_verify,
                str_time_approv,
                str_nb_jours,
                str_bkdopi
                         ]) # 

        return response

    export_rpt_DFX2201.short_description = u"Export DFX2201 Report"    

    actions = [export_rpt_DFX2201]

# Register your models here.
admin.site.register(TrfDossierCtrlProxy, TrfDossierCtrlProxyAdmin)


'''
Transfert Sortant Control Administration
'''
class RptDossierCtrlProxyAdmin(TrfDossierCtrlAdminBase):

    form = RptDossierCtrlForm

    inlines = [MultiDomDossierInline, FXCliInline, CashFlowDetailInfoPlusInline, ClientFileStorageGenericInline]

    list_display = ('id','chk_pay','date_val','client',
                    'ccy','montant','nomenc_lv0','chk_verify','num_dom','chk_exec','bkdopi','dossier_rtroc',)

    list_filter = [
        DirectClientFilter, 
        'chk_verify',
        'chk_approv',
        'chk_pay',
        ('statut',admin.RelatedOnlyFieldListFilter),
        ('nomenc_lv0',admin.RelatedOnlyFieldListFilter),
        ('corresp',admin.RelatedOnlyFieldListFilter),        
        ('ccy', admin.RelatedOnlyFieldListFilter),
    ]

    search_fields = ['id','bkdopi__ref_id','oper_input__last_name','client__ref_id','client__alias','client__fullname','montant']
    date_hierarchy = 'date_val' 

    fieldsets = ( 
            ("Contrôle Back-Office", {
                'fields': ('type_product',
                    'date_val','corresp','account',
                    'client','cpty','montant','ccy','chk_pay','ref_swift','oper_input','docTraceLog'),
                }),
            ("Contrôle Domiciliation", {
                'fields': ('nomenc_lv0','nomenc_lv1','dossier_dom',
                    'chk_verify','oper_verify','time_verify','obs')
                }),   
            ("Contrôle Trésorier", {
                #'classes': ('collapse', 'open'),
                'fields': ('statut','dossier_couvr','dossier_rtroc','chk_fund','ctrl_cf','chk_approv','oper_approv','time_approv')
                }), 
            ("Contrôle d'Encaissment", {
                #'classes': ('collapse', 'open'),
                'fields': ('chk_dcc','type_dcc','obs_dcc','chk_exec','ref_exec','bkdopi','ccy_lc','montant_lc','fx_rate',),
                }),        
        )
      
    def export_rpt_DFX1100(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today + '_rpt_DFX2201.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"ref_ordre"),
            smart_str(u"date_val"),
            #
            smart_str(u"ref_swift"),       
            smart_str(u"mt"),
            smart_str(u"corresp_name"),
            smart_str(u"corresp_swift"),
            smart_str(u"client"),
            smart_str(u"devise"),
            smart_str(u"montant"),
            smart_str(u"type_rpt"),
            smart_str(u"object"),
            smart_str(u"cpty"),
            smart_str(u"dossier_rtroc"),
        ])
        for obj in queryset:
            str_ref_ordre = obj.pk
            str_date_val= obj.date_val
            str_ref_swift = obj.ref_swift
            str_mt = "103"
            str_client = obj.client.fullname
            str_cpty = obj.cpty
            #
            if obj.nomenc_lv0:
                str_object = obj.nomenc_lv0.alias
            else:
                str_object ="N/A"
            #corresp
            if obj.corresp:
                str_corresp_name = obj.corresp.alias
                str_corresp_swift = obj.corresp.swift
            else:
                str_corresp_name = "N/A"
                str_corresp_swift = "N/A"

            str_ccy = obj.ccy
            str_montant = obj.montant
            #
            str_type = "RETROCEDABLE"
            str_dossier_rtroc = obj.dossier_rtroc

            writer.writerow([
                str_ref_ordre,
                str_date_val,
                #
                str_ref_swift,
                str_mt,
                str_corresp_name,
                str_corresp_swift,
                str_client,
                str_ccy,
                str_montant,
                str_type,
                str_object,
                str_cpty,
                str_dossier_rtroc
            ]) # 

        return response

    export_rpt_DFX1100.short_description = u"Export DFX1100 Report"    

    actions = [export_rpt_DFX1100]


# Register your models here.
admin.site.register(RptDossierCtrlProxy, RptDossierCtrlProxyAdmin)

'''
Transfert F.CFA Control Administration
'''
class VirDossierCtrlProxyAdmin(TrfDossierCtrlAdminBase):
    
    form = VirDossierCtrlForm

    inlines = [CashFlowDetailInline, ClientFileStorageGenericInline] 

    list_display = ('id','get_oper_input','client_link',
                    'ccy','montant','statut','chk_approv','chk_pay','time_approv','msg_payment')

    list_filter = [
        DirectClientFilter, 
        'chk_verify',
        'chk_approv',
        'chk_pay',
        ('statut',admin.RelatedOnlyFieldListFilter),
        ('nomenc_lv0',admin.RelatedOnlyFieldListFilter),
        ('corresp',admin.RelatedOnlyFieldListFilter),        
        ('ccy', admin.RelatedOnlyFieldListFilter),
    ]

    search_fields = ['id','bkdopi__ref_id','oper_input__last_name','client__ref_id','client__alias','client__fullname','montant']
    date_hierarchy = 'time_approv' 

    fieldsets = (      
            ('Front Office', {
                'fields': ('type_product','oper_input',
                'client','cpty','montant','ccy','nomenc_lv0','nomenc_lv1','docTraceLog') 
                }), 
            ('Contrôle de Trésorerie', {
                #'classes': ('collapse', 'open'),
                'fields': ('statut','obs','oper_approv',
                        'corresp','account','chk_approv','time_approv'),
                }),
            ('Contrôle de Settlement', {
                #'classes': ('collapse', 'open'),
                'fields': ('chk_pay','date_val','ref_swift','msg_payment'),
                }),
    )

# Register your models here.
admin.site.register(VirDossierCtrlProxy, VirDossierCtrlProxyAdmin)


'''
CREDOC Control Administration
'''
class CredocDossierCtrlProxyAdmin(TrfDossierCtrlAdminBase):
                
    form = CredocDossierCtrlForm

    #attach inline model
    inlines = [SingleDomDossierInline, FXCliInline, CashFlowDetailInline, ClientFileStorageGenericInline]

    list_display = ('id','get_oper_input','client_link','get_benef','ccy','montant','statut','dossier_couvr','chk_verify','chk_approv','ref_exec','chk_pay',)
    
    list_filter = [
        DirectClientFilter, 
        'chk_verify',
        'chk_approv',
        'chk_pay',
        ('statut',admin.RelatedOnlyFieldListFilter),
        ('nomenc_lv0',admin.RelatedOnlyFieldListFilter),
        ('corresp',admin.RelatedOnlyFieldListFilter),        
        ('ccy', admin.RelatedOnlyFieldListFilter),
    ]

    search_fields = ['id','bkdopi__ref_id','oper_input__last_name','client__ref_id','client__alias','client__fullname','montant','ref_exec']
    date_hierarchy = 'time_verify' 

    fieldsets = (      
        ('Front Office', {
            'fields': ('type_product','oper_input',
            'client','cpty','montant','ccy','nomenc_lv0','nomenc_lv1',
            'ref_inv','docTraceLog','statut','dossier_dom',
            ('ccy_lc','montant_lc','fx_rate'), 
            ) 
            }), 
        ('Contrôle de Dossier', {
            #'classes': ('collapse', 'open'),
            'fields': ('chk_dcc','type_dcc','obs_dcc','chk_verify','oper_verify','time_verify','obs','dossier_couvr',)
            }),
        ('Contrôle de Trésorerie', {
            #'classes': ('collapse', 'open'),
            'fields': (('chk_fund','oper_fund'),'type_fund','chk_approv','corresp','account','dossier_rtroc',)
            }),

        ("Contrôle d'Exécution", {
            #'classes': ('collapse', 'open'),
            'fields': ('chk_exec','ref_exec','bkdopi','chk_pay','date_val','ref_swift',),
            }),        
    )

    def get_readonly_fields(self, request, obj=None):

        readonly_fields = [ 'oper_input','oper_verify','oper_approv','chk_dcc','type_dcc','obs_dcc',
                            'time_verify','time_approv','nb_jours','created']
        
        if request.user.is_superuser:
            readonly_fields = ['oper_verify','time_verify','oper_approv','time_approv','nb_jours','created','chk_dcc','type_dcc','obs_dcc',]

        fields_excl = []

        if obj:
            readonly_all_fields = list(set([f.name for f in obj._meta.fields]))
        else:
            readonly_all_fields = readonly_fields

        #remove readonly lock accoring to department
        for field in fields_excl:
            if field in readonly_fields:
                readonly_fields.remove(field)

        self.readonly_fields = readonly_fields

        return self.readonly_fields  

# Register your models here.
admin.site.register(CredocDossierCtrlProxy, CredocDossierCtrlProxyAdmin)


'''
Import/Export Domiciliation Ctrl
'''
class DomDossierCtrlAdmin(DomDossierCtrlAdminBase):

    inlines = [MultiDomDossierInline, ClientFileStorageGenericInline] 
    #
    list_display = ('id','statut','get_ref_decl','get_oper_input','client_link','ccy','montant','num_verify',
                    'chk_notify','chk_verify','chk_approv') #'num_verify','approv_pct','exec_pct', #'jc_restant'

    list_filter = [
        DirectClientFilter,
        DirectRefDIFilter,
        'chk_notify',
        'chk_verify',
        ('statut', admin.RelatedOnlyFieldListFilter),
        ('nomenc_lv0', admin.RelatedOnlyFieldListFilter),
        ]

    search_fields = ['ref_di','oper_input__last_name','client__fullname','client__ref_id','client__alias',]

    date_hierarchy = 'date_di' 

    fieldsets = (      
        ('Contrôle de Information de base', {
            'fields': ('oper_input','ref_dom','client','nomenc_lv0',
                        'ccy','montant','ref_di','date_di','statut','obs','docTraceLog',
                        ('ccy_lc','montant_lc','fx_rate'),'chk_notify','batch_no','message', 
                    )
            }), 
        ("Contrôle de Domiciliation", {
            #'classes': ('collapse', 'open'),
            'fields': ('chk_verify','date_ref','oper_verify','time_verify'),
            }),
        ("Contrôle d'Apurement (Réservé au BO)", {
            #'classes': ('collapse', 'open'),
            'fields': ('chk_approv','oper_approv','time_approv'),
            }),
    )

    def get_readonly_fields(self, request, obj=None):
 
        self.readonly_fields = ['ref_dom','type_product','oper_input','oper_verify','oper_approv',
        'time_approv','time_verify','fx_rate','chk_notify','batch_no','message',]

        return self.readonly_fields  

# Register your models here.
admin.site.register(DomDossierCtrl, DomDossierCtrlAdmin)

'''
Approvisionnement BEAC ctrl.
'''
class TrfDossierCouvrProxyAdmin(TrfDossierCouvrAdminBase):

    inlines = [CashFlowDetailInfoPlusInline, TrfDossierCtrlProxyInline, ClientFileStorageGenericInline]

    form = TrfDossierCouvrForm

    list_display = ('id','get_oper_input','chk_approv','statut','ref_id','ccy_in','montant_in','num_doc','nb_jours','chk_notify','chk_verify','chk_acc','chk_pay','chk_couvr','date_couvr','chk_commission')

    list_filter = [
        #limit the list_filter choices to the users.
        DirectClientFilter,
        ('type_product', admin.RelatedOnlyFieldListFilter),
        ('statut', admin.RelatedOnlyFieldListFilter),
        'chk_notify',
        'chk_verify',
        'chk_acc',
        'chk_pay',
        'chk_couvr',
        'chk_commission',
        'chk_approv'
    ]    
    search_fields = ['ref_id','montant_in',]

    date_hierarchy = 'time_verify' 

   #set fieldsets
    fieldsets = ( 
        ('Ticket de Couverture', {
            'fields': (
                'type_product', 
                'statut',
                'date_trd',
                'ref_id',
                'client',
                'ccy_out',
                ('corresp_out','account_out','montant_out'),
                'ccy_in',
                ('corresp_in','account_in','montant_in'),
                'oper_input',
                'chk_verify',   
                ('oper_verify','time_verify'),'nb_jours',
                #
                #'chk_notify','batch_no','message',
                #
                'chk_acc','date_acc','ref_acc','obs',
            )
            }),
        ("Info. de Compensation", {
            'fields': (
                'chk_pay',('date_val', 'montant_payment','ref_sygma','msg_payment'),
                'chk_couvr',('date_couvr','montant_couvr','ref_swift'),  
                'chk_commission',('date_commission','montant_commission','msg_commission'),  
                'chk_approv',
                'oper_approv','time_approv',   
                ),
            }),       
    )  

    def get_queryset(self, request):
        #
        qs = super(TrfDossierCouvrProxyAdmin, self).get_queryset(request)
        ctype = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        type_product = CatalogTypeProduct.objects.filter(content_type=ctype).values_list('id')
        #print(filter_id)
        qs = qs.filter(type_product__in=type_product)  
        return qs  

    def get_changeform_initial_data(self, request):
        return {
                'corresp_out': 3,    #BEAC
                'account_out': 5,    #XAF Account
                'ccy_out': 5,        #XAF
                }  
   
# Register your models here.
admin.site.register(TrfDossierCouvrProxy, TrfDossierCouvrProxyAdmin)


'''
Approvisionnement BEAC ctrl.
'''
class RptDossierRtrocProxyAdmin(TrfDossierCouvrAdminBase):

    inlines = [CashFlowDetailInfoPlusInline, TrfDossierCtrlInline, ClientFileStorageGenericInline, ]

    form = RptDossierRtrocForm

    list_display = ('id','ref_id','chk_approv','date_trd','statut','ccy_out','montant_out','ccy_in','montant_in','num_doc','chk_pay','date_val','chk_couvr','date_couvr',)

    list_filter = [
        #limit the list_filter choices to the users.
        ('statut', admin.RelatedOnlyFieldListFilter),
        'chk_pay',
        'chk_couvr',
        'chk_approv'
    ]    
    search_fields = ['ref_id','montant_out',]
    date_hierarchy = 'date_trd' 

    #set fieldsets
    fieldsets = ( 
        ('Ticket de Rétrocession', {
            'fields': (
                'type_product', 
                'statut',
                'ref_id',
                'ccy_out',
                ('corresp_out','account_out','montant_out'),
                'ccy_in',
                ('corresp_in','account_in','montant_in'),
                'date_trd',
                'oper_input',
                'obs',
                'chk_verify',   
                'oper_verify','time_verify',
            )
            }),
        ("Info. de Compensation", {
            'fields': (
                'chk_pay',('date_val', 'montant_payment','ref_swift'),
                'chk_couvr',('date_couvr','montant_couvr','ref_sygma','msg_payment'),  
                'chk_approv',
                'oper_approv','time_approv',   
                ),
            }),       
    )  

    def get_changeform_initial_data(self, request):
        return {'corresp_in': 3,    #BEAC
                'account_in': 5,    #XAF Account
                'ccy_in': 5,        #XAF
                }  

    #authorization filter
    def get_queryset(self, request):
        #
        qs = super(RptDossierRtrocProxyAdmin, self).get_queryset(request)
        ctype = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        type_product = CatalogTypeProduct.objects.get(content_type=ctype)
        qs = qs.filter(type_product=type_product.id)  
        return qs  

    def export_csv_eod(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today +"_"+ str(request.user) + '.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

        writer.writerow([
            smart_str(u"id"),
            smart_str(u"oper_input"),
            smart_str(u"date_emis"),
            smart_str(u"nb_jours"),
            smart_str(u"statut"),
            smart_str(u"ref_id"),
            smart_str(u"client"),
            smart_str(u"montant_in"),   
            smart_str(u"ccy_in"),
            smart_str(u"montant_out"),
            smart_str(u"ccy_out"),
            smart_str(u"date_trd"),
            smart_str(u"date_acc"),
            smart_str(u"date_pay"),   
            smart_str(u"date_couvr"),  
            smart_str(u"date_commission"),   
            smart_str(u"time_approv"),  
            smart_str(u"obs"), 
        ])
        
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.oper_input),
                smart_str(obj.time_verify.date()),
                smart_str(""),
                smart_str(obj.statut),
                smart_str(obj.ref_id),
                smart_str(""),
                smart_str(obj.montant_in),
                smart_str(obj.ccy_in),
                smart_str(obj.montant_out),
                smart_str(obj.ccy_out),
                smart_str(obj.date_trd),
                smart_str(obj.date_acc),
                smart_str(obj.date_val),
                smart_str(obj.date_couvr),            
                smart_str(obj.date_commission),
                smart_str(obj.time_approv),
                smart_str(obj.obs),
            ])
        return response
    export_csv_eod.short_description = u"Export Rapport CSV"    

    actions = [export_csv_eod ]


# Register your models here.
admin.site.register(RptDossierRtrocProxy, RptDossierRtrocProxyAdmin)


class DomDossierMultiAdmin(DomDossierMultiAdminBase):

    inlines = [EmailCtrlInline]

    form = DomDossierMultiForm

    list_display = ('id','statut','client_link','ref_di','get_type_product','payment_link','ref_exec',
                    'dom_pct','apure_pct','jc_restant','date_ap','chk_notify','template_key')

    search_fields = ['dossier_trf','dossier_dom']
    
    date_hierarchy = 'date_val' 

    list_filter = [
        OverdueFilter,
        TrfDossierClientFilter,
        DomDossierRefDIFilter,
        'dossier_dom__nomenc_lv0__nature',
        'chk_notify',
        'template_key',
        ('statut', admin.RelatedOnlyFieldListFilter),
    ]
    fieldsets = (      
        ("Contrôle d'Apurement", {
            #'classes': ('collapse', 'open'),
            'fields': ('id',
                'nomenc_lv0',
                'dossier_trf',
                'dossier_dom','dom_pct','apure_pct',
                ('dom_ccy','dom_montant','dom_montant_lc'),
                ('apure_ccy','apure_montant','apure_montant_lc'),
                ),
            }),  
            ("Contrôle d'Apurement", {
            #'classes': ('collapse', 'open'),
            'fields': ('date_verify','date_val','date_ap',
                'jc_restant',
                #
                #'chk_email',
                #'sending_user',
                'chk_notify',
                'batch_no',
                'template_key', 
                #
                'statut',
                'obs',
                'chk_apure',
                'oper_ap',
                'time_ap',
                ),
            }),  

    )
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['id','oper_ap','time_ap',
                                'date_ap','jc_restant','date_verify','date_val',
                                'dom_ccy','dom_montant','dom_montant_lc',
                                'apure_ccy','apure_montant','apure_montant_lc','apure_pct',
                                #
                                #'chk_email',
                                #'sending_user',
                                'chk_notify',
                                'batch_no',
                                'template_key', 
        ] #'apure_pct',
        return self.readonly_fields  
    
    #----------------------------------------------------------------------
    def get_queryset(self, request):
        qs = super(DomDossierMultiAdmin, self).get_queryset(request)
        #return qs
        return qs.exclude(dossier_trf__chk_pay=False) 

    def save_model(self, request, obj, form, change):

        if obj.chk_apure and not obj.oper_ap:
            obj.oper_ap = request.user
        obj.save()

    #--------------------------------------
    def export_csv(modeladmin, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today + '_apure_Monthly.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            #
            smart_str(u"id"),
            smart_str(u"statut"), 
            smart_str(u"code_client"),
            smart_str(u"client"),  
            smart_str(u'nomenc'),
            smart_str(u"date_ap"),
            smart_str(u"jc_restant"),
            #payment info
            smart_str(u'dossier_trf'),             
            smart_str(u"date_pay"),
            smart_str(u"ap_ccy"),
            smart_str(u"ap_montant"),
            smart_str(u"ap_montant_lc"),
            smart_str(u"ap_pct"),
            #supplementary info
            smart_str(u"couvr_beac"),
            smart_str(u"retro_beac"), 
            #dom info
            smart_str(u"dom_ref"),
            smart_str(u'dom_ref_di'),
            smart_str(u"dom_date_di"),
            smart_str(u"dom_date_verify"),  
            smart_str(u"dom_ccy"),
            smart_str(u"dom_montant"),
            smart_str(u"dom_montant_lc"),
            smart_str(u"dom_num_dossier"),
            smart_str(u"dom_approv_pct"),
            smart_str(u"dom_ap_pct"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.statut), 
                smart_str(obj.dossier_dom.client.ref_id),
                smart_str(obj.dossier_dom.client.fullname),
                smart_str(obj.nomenc_lv0),
                smart_str(obj.date_ap),
                smart_str(obj.jc_restant),
                #payment info
                smart_str(obj.dossier_trf),                
                smart_str(obj.date_val), 
                smart_str(obj.apure_ccy),
                smart_str(obj.apure_montant),
                smart_str(obj.apure_montant_lc),
                smart_str(obj.apure_pct),
                #supplementary info
                smart_str(obj.dossier_trf.dossier_couvr),
                smart_str(obj.dossier_trf.dossier_rtroc),
                #dom info
                smart_str(obj.dossier_dom.ref_dom),
                smart_str(obj.dossier_dom.ref_di),
                smart_str(obj.dossier_dom.date_di),
                smart_str(obj.dossier_dom.date_ref),  
                smart_str(obj.dom_ccy),
                smart_str(obj.dom_montant),
                smart_str(obj.dom_montant_lc),
                smart_str(obj.dossier_dom.num_exec),
                smart_str(obj.dossier_dom.approv_pct),
                smart_str(obj.dossier_dom.apure_pct),
            ])
        return response

    export_csv.short_description = u"Export CSV"  

    #--------------------------------------
    class email_template_form(forms.forms.Form):    
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)    

        ctype = ContentType.objects.get_for_model(DomDossierMulti, for_concrete_model=True)    
        email_template = forms.ModelChoiceField(
            EmailTemplate.objects.filter(
                chk_approv=True,
                content_type=ctype)
                )

    def genr_email(modeladmin, request, queryset):  
        
        batch_no = 'GENR_' + datetime.date.today().strftime("%Y%m%d") + time.strftime("%H%M%S", time.localtime())        

        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Generate Email Interface File Cancelled')    
            return  

        elif 'email_template' in request.POST:    
            form = modeladmin.email_template_form(request.POST) 

            if form.is_valid():      
                email_template = form.cleaned_data['email_template']
                ctype = ContentType.objects.get_for_model(DomDossierMulti, for_concrete_model=True)
                ctype_email = ContentType.objects.get_for_model(EmailCtrl, for_concrete_model=True)
                statut = Statut.objects.get(content_type=ctype_email, statut='/ATTN')

                #action section      
                for case in queryset:        
                    #create email records
                    obj, created = EmailCtrl.objects.get_or_create(
                        object_id = case.id,
                        content_type = ctype,
                        template = email_template,
                    )
                    obj.statut = statut
                    obj.client = case.dossier_trf.client     
                    obj.to_email = case.dossier_trf.client.email
                    obj.from_email = email_template.from_email
                    obj.cc_email = email_template.cc_email 
                    #
                    if obj.subject == 1:
                        obj.subject = email_template.subject
                    else:
                        template = Template(email_template.subject)
                        context = Context({"cli_code": case.dossier_trf.client.ref_id})
                        obj.subject = template.render(context)
                    #
                    obj.chk_verify = True
                    obj.oper_verify = request.user
                    obj.time_verify = timezone.now()
                    obj.batch_no = batch_no
                                                
                    body = render_to_string('notification/'+ email_template.template_key + '.html',
                        {   
                            "type_operation": email_template.type_operation,
                            "type_action": email_template.type_action,
                            "nomenc": case.dossier_trf.nomenc_lv0,
                            "ref_exec": case.dossier_trf.bkdopi,
                            "ccy": case.dossier_trf.ccy.iso,
                            "montant": case.dossier_trf.montant, 
                            "date_val": case.dossier_trf.date_val,
                            "ref_di": case.dossier_dom.ref_di,
                            "cli_fullname": case.dossier_trf.client.fullname,
                            "cli_code": case.dossier_trf.client.ref_id,
                            "date_notif": timezone.now().date,
                            "dom_id":case.dossier_dom.id,
                            "trf_id":case.dossier_trf.id,
                            "obs":case.obs
                        })
                    obj.body = body
                    obj.save()

                #update information in model tickets
                queryset.update(chk_notify=True, batch_no=batch_no, message=obj, template_key=email_template.template_key)

                modeladmin.message_user(request, "<Batch #%s> %s Successfully generated please check file." %(batch_no, queryset.count()))    
                #url = reverse('/', kwargs={'batch_no': batch_no})
                #return HttpResponseRedirect(url)
                return HttpResponseRedirect('/admin/notification/emailctrl/?batch_no=%s' % batch_no)
            else:      
                messages.warning(request, u"Please choose email template")      
                form = None   

        if not form:    
            form  = modeladmin.email_template_form(
                initial={'_selected_action': 
                queryset.values_list('id',flat=True)
                #request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                })  

            return render(request,'custom//batch_update.html',
                {   'objs': queryset, 
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'genr_email', 
                    'title': u'Generate email interface file',
                    'batch_no': batch_no
                })

    genr_email.short_description = u'Genr Email'
    
    actions = [export_csv, genr_email]

# Register your models here.
admin.site.register(DomDossierMulti, DomDossierMultiAdmin)
