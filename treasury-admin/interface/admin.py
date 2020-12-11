# -*- coding: utf-8 -*-

from django.contrib import admin
#
from .models import *
from .sygma.models import Sygma
#
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from import_export.admin import ImportExportModelAdmin


class ApTBAdmin(ImportExportModelAdmin):

  #alter change_list view to enhanced view
  #change_list_template = 'admin/alco/change_list_loroCtrl.html'     

  #----------------------------------------------------------------------
  list_display = ('id',
                  'date_rpt',         
                  'date_cpt', 
                  'cha_lv2',
                  'code_client',
                  'ccy_code',
                  'acc',
                  'solde_t0',
                  'mvmt_dr',
                  'mvmt_cr',
                  'solde_t1',
                  'ctrl')  

  list_filter = [
    'cha_lv2','ccy_code',
  ]

  search_fields = ['code_client','acc',]
  date_hierarchy = 'date_rpt' 
  
# Register your models here.
admin.site.register(ApTB, ApTBAdmin)



class ApBkcomAdmin(admin.ModelAdmin):

  #alter change_list view to enhanced view
  #change_list_template = 'admin/alco/change_list_loroCtrl.html'     

  #----------------------------------------------------------------------
  list_display = ('id',
                  'date_val',
                  'entity',
                  'code_client',
                  'acc',
                  'acc_txt',
                  'ccy_code',
                  'montant',
                  'timestamp',
                  )  

  list_filter = [
    'ccy_code','entity',
  ]

  search_fields = ['code_client','date_val','acc','timestamp']
  date_hierarchy = 'date_val' 

# Register your models here.
admin.site.register(ApBkcom, ApBkcomAdmin)


class ApBkmvtAdmin(ImportExportModelAdmin):

  #alter change_list view to enhanced view
  #change_list_template = 'admin/alco/change_list_loroCtrl.html'     

  #----------------------------------------------------------------------
  list_display = ('id',
                  'statut',
                  'date_trd',
                  'entity',
                  'alias',
                  'acc',
                  'nature',
                  'ccy_code1',
                  'montant1',
                  'fx_rate',)  

  list_filter = [
    'entity','ccy_code1','nature',
  ]

  search_fields = ['code_client','date_trd',]
  date_hierarchy = 'date_trd' 

  #actions
  #----------------------------------------------------------------------
  def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str
    import datetime     
    today = datetime.date.today().strftime("%Y%m%d") 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=" + today + '_BKMVT.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
      smart_str(u"AGEE"),
      smart_str(u"DVA"),
      smart_str(u"DSAI"),
      smart_str(u"HSAI"),      
      smart_str(u"DEVA"), 
      smart_str(u"CLI"),
      smart_str(u"DEVC"),
      smart_str(u"NAT"),
      smart_str(u"NOMP"),
      smart_str(u"NCP"),
      smart_str(u"SEN"),            
      smart_str(u"MNAT"),
      smart_str(u"MHTT"),
      smart_str(u"TCAI2"),            
      smart_str(u"ETA"),      
    ])
    for obj in queryset:
      writer.writerow([
      smart_str(obj.entity),
      smart_str(obj.date_val),
      smart_str(obj.date_trd),
      smart_str(obj.time_trd),      
      smart_str(obj.ccy_code2), 
      smart_str(obj.code_client),
      smart_str(obj.ccy_code1), 
      smart_str(obj.nature),
      smart_str(obj.alias),
      smart_str(obj.acc),
      smart_str(obj.direction),            
      smart_str(obj.montant2),
      smart_str(obj.montant1),
      smart_str(obj.fx_rate),            
      smart_str(obj.statut),     
      ])
    return response

  export_csv.short_description = u"Export CSV"    

  actions = [export_csv]

  #system status filter
  #----------------------------------------------------------------------
  
  
  
  
  
# Register your models here.
admin.site.register(ApBkmvt, ApBkmvtAdmin)



class ApBkdopiAdmin(ImportExportModelAdmin):

  #alter change_list view to enhanced view
  #change_list_template = 'admin/alco/change_list_loroCtrl.html'     

  #----------------------------------------------------------------------
  list_display = ('id',
                  'ref_id',
                  'statut_sys',                  
                  'date_exec',  
                  'donneur','benef','ccy_code','montant','fxRate',)  

  list_filter = [
    'nature',
    'statut_sys',
    'ccy_code',
  ]

  search_fields = ['date_exec',
                   'ref_id',
                   'donneur',
                   'benef',
                   'montant',
                   'montant_xaf',
                   ]
  #date_hierarchy = 'date_trd' 

  #set fieldsets
  #----------------------------------------------------------------------
  fieldsets = (         
    ('Exécution', {
      'fields': (('statut_sys',),
                 'operType',
                 ('ref_id','agenceID',), 
                 ('invoice','date_val','date_exec'),
                 ('donneur','accDonneur'),('benef','accBenef'),
                 ('ccy_code','montant'),'montant_xaf','fxRate',
                 'feeType','motif', 'uti'
                 )
      }),
  )

# Register your models here.
admin.site.register(ApBkdopi, ApBkdopiAdmin)


class ApBkcliAdmin(ImportExportModelAdmin):
  
    list_display = ('id','ref_id','fullname','date_val','date_profil','chk_actif')    
    list_filter = ['chk_actif',]
    search_fields = ['ref_id','fullname',]
    date_hierarchy = 'date_profil' 
    
    #actions
    #----------------------------------------------------------------------
    def get_actions(self, request):
      actions = super(ApBkcliAdmin, self).get_actions(request)
      #if not request.user.is_superuser:        
      if 'delete_selected' in actions:
        del actions['delete_selected']
      return actions    
    
    def export_csv(modeladmin, request, queryset):
      import csv
      from django.http import HttpResponse
      from django.utils.encoding import smart_str
      import datetime     
      today = datetime.date.today().strftime("%Y%m%d") 
      response = HttpResponse(content_type='text/csv')
      response['Content-Disposition'] = "attachment; filename=" + today + '_BKCLI.csv'
      writer = csv.writer(response, csv.excel)
      response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
      writer.writerow([
        smart_str(u"ID"),
        smart_str(u"CODE_CLI"),
        smart_str(u"NAME_CLI"),   
        smart_str(u"DMO"),
        smart_str(u"DCR"),  
        smart_str(u"CHK_ACTIF"),  
      ])
      for obj in queryset:
        writer.writerow([
        smart_str(obj.id),
        smart_str(obj.ref_id),
        smart_str(obj.fullname),
        smart_str(obj.date_val), 
        smart_str(obj.date_profil),
        smart_str(obj.chk_actif),         
        ])
      return response
  
    export_csv.short_description = u"Export CSV"    
  
    actions = [export_csv]    
    
    
# Register your models here.
admin.site.register(ApBkcli, ApBkcliAdmin)


class SygmaAdmin(admin.ModelAdmin):
  list_display = ('id','type_msg','cf','date_val','ref_id','donneur','benef','ccy','montant','link_id',)
  list_filter = ['type_msg','cf','codtype','statut_msg']
  search_fields = ['ref_id','montant','donneur','link_id',]
  date_hierarchy = 'date_val' 

# Register your models here.
admin.site.register(Sygma, SygmaAdmin)
