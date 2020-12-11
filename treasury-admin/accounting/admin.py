# -*- coding: utf-8 -*-

from django.contrib import admin
#
from .models import *
#
#from import_export.admin import ImportExportModelAdmin
from datetime import date


class TrialBalanceAdmin(admin.ModelAdmin):

  #alter change_list view to enhanced view
  #change_list_template = 'admin/alco/change_list_loroCtrl.html'     

  #----------------------------------------------------------------------
  list_display = ('id',
                  'date_rpt',
                  'cha_lv2',
                  'cha_lv3',
                  'code_client',
                  'ccy_code',
                  'acc',
                  'solde_t0',
                  'mvmt_dr',
                  'mvmt_cr',
                  'solde_t1',
                  'ctrl')  

  list_filter = [
    'ccy_code','cha_lv2',
  ]

  search_fields = ['code_client','acc',]
  date_hierarchy = 'date_rpt' 

  def has_delete_permission(self, request, obj=None):
    if not request.user.is_superuser and obj:
        return False
    else:
      return True
    return super(TrialBalanceAdmin, self).has_delete_permission(request, obj=obj)         

  def get_actions(self, request):
    actions = super(TrialBalanceAdmin, self).get_actions(request)        
    if 'delete_selected' in actions:
      del actions['delete_selected']
    return actions
  
  #actions
  #----------------------------------------------------------------------
  def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str

    #SAVE XL files into Sql Server 
    today = date.today().strftime("%Y%m%d")     
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + today + '_TB_RPT.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
      smart_str(u"DATE_RPT"),
      smart_str(u"DATE_BAL"),
      smart_str(u"DATE_VAL"),
      smart_str(u"CODE_CLIENT"),
      smart_str(u"CHA_LV3"),
      smart_str(u"DEV"),
      smart_str(u"NCP"),    
      smart_str(u"SHI"), 
      smart_str(u"DR"),  
      smart_str(u"CR"),  
      smart_str(u"SDE"),
    ])
    for obj in queryset:
      writer.writerow([
        smart_str(obj.date_rpt),
        smart_str(obj.date_cpt),
        smart_str(obj.date_val), 
        smart_str(obj.code_client),
        smart_str(obj.cha_lv3[0:3]),
        smart_str(obj.ccy_code),
        smart_str(obj.acc),
        smart_str(obj.solde_t0),
        smart_str(obj.mvmt_dr),
        smart_str(obj.mvmt_cr),      
        smart_str(obj.solde_t1),      
  ])

    return response

  export_csv.short_description = u"Export CSV"    

  actions = [export_csv]      
  
# Register your models here.
admin.site.register(TrialBalance, TrialBalanceAdmin)