# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
#
from tiers.client.models import ClientFileStorage
from tiers.inlines import ClientFileStorageInline, ClientFileStorageGenericInline
from cashflow.inlines import CashFlowDetailInline, CashFlowDetailEditableInline
from util.catalog.models import CatalogTypeProduct
#
from .models import *
from .forms import *
from .inlines import CollateralInline

class MMAdmin(admin.ModelAdmin):

  form = MMForm 
  inlines = [CollateralInline, CashFlowDetailEditableInline, ClientFileStorageGenericInline] #

  list_display = ('id','type_product','cpty','date_val','date_end','jour_restant','ccy','nominal','taux','chk_end',)
  list_filter = [
    ('type_product', admin.RelatedOnlyFieldListFilter),    
    'chk_end',
  ]

  #search_fields = ['counterparty','ref_id','nominal']
  search_fields = ['nominal',]
  date_hierarchy = 'date_val' 

  fieldsets = (      
    ('Négociation', {
      'fields': (
                 'type_product',
                 #'client',
                 'cpty',
                 'ccy',
                 'nominal',
                 'date_trd',
                 'date_val',
                 'date_end',
                 'taux',
                 'repayment',
                 'chk_verify',
                 'oper_verify',
                 'time_verify'
                 ) 
      }), 
    ('Approbation', {
      #'classes': ('collapse', 'open'),
      'fields': ('chk_approv',
                 'corresp',
                 'account',
                 'ctrl_cf',
                 'oper_approv',
                 'time_approv',
                 #'cliFile',
                 ),
      }),       
     ('Follow-ups', {
      #'classes': ('collapse', 'open'),
      'fields': (
                'docTraceLog',
                'chk_end',
                 ),
      }),   
  )

  def get_readonly_fields(self, request, obj=None):
    #if not request.user.is_superuser:
    self.readonly_fields = ['oper_verify','time_verify','oper_approv','time_approv'] #  
    return self.readonly_fields 

  def get_form(self, request, obj=None, **kwargs):
      # just save obj reference for future processing in Inline
      request._obj_ = obj
      #print(request._obj_)
      return super(MMAdmin, self).get_form(request, obj, **kwargs)

  def save_model(self, request, obj, form, change):
      #update oper_verify
      if not obj.oper_verify and obj.chk_verify:  
          obj.oper_verify = request.user 

      if not obj.oper_approv and obj.chk_approv: 
          #if not obj.oper_verify == request.user:
          obj.oper_approv = request.user
      
      obj.save()

  def save_formset(self, request, form, formset, change):
      if formset.model != ClientFileStorage:
          return super(MMAdmin, self).save_formset(request, form, formset, change)
      #pass parent value to child 
      instances = formset.save(commit=False)
      for instance in instances:
          if not instance.pk and request.user.is_authenticated:
              #
              parent_id = instance.object_id
              parent_obj = FX.objects.get(pk=parent_id)
              #
              instance.oper = request.user
              instance.client = parent_obj.client
          instance.save()
      formset.save_m2m()

  #actions
  #----------------------------------------------------------------------
  def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str
    import datetime
    today = datetime.date.today().strftime("%Y%m%d") 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=" + today + '_MoneyMarket.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
      smart_str(u"id"),
      smart_str(u"type_product"),
      smart_str(u"date_val"),
      smart_str(u"date_end"),
      smart_str(u"cpty"),
      smart_str(u"ccy_in"),
      smart_str(u"nominal"),
      smart_str(u"taux"),
      smart_str(u"repayment"),
      smart_str(u"chk_end"),

    ])
    for obj in queryset:
      writer.writerow([
        smart_str(obj.id),
        smart_str(obj.type_product),
        smart_str(obj.date_val),
        smart_str(obj.date_end),
        smart_str(obj.cpty),
        smart_str(obj.ccy),
        smart_str(obj.nominal),                
        smart_str(obj.taux),
        smart_str(obj.repayment),   
        smart_str(obj.chk_end),          
      ])
    return response
  export_csv.short_description = u"Export CSV"    


  def chk_end(modeladmin, request, queryset):
    statut = queryset.values_list('chk_end', flat=True)
    #date = request.POST['date']
    if not statut[0]:
      queryset.update(chk_end=True)
    else:
      queryset.update(chk_end=False)
    #modeladmin.message_user(request, ("Successfully updated statut for %d rows") % (queryset.count(),), messages.SUCCESS)
  chk_end.short_description = "Check/Uncheck End" 

  actions = [export_csv, chk_end]    
# Register your models here.
admin.site.register(MM, MMAdmin)

class FIAdmin(admin.ModelAdmin,):

  form = FIForm 
  inlines = [CashFlowDetailEditableInline, ClientFileStorageGenericInline] #    

  list_display = ('id','folio','type_product','ref_id','ccy','nominal','price_pct','date_val','taux','date_end','jour_restant','chk_end')
  list_filter = [
    ('type_product', admin.RelatedOnlyFieldListFilter),
    'folio',
    'chk_end',
    'ccy'
  ]
  search_fields = ['ref_id']
  date_hierarchy = 'date_val' 

  fieldsets = (      
    ('Négociation', {
      'fields': (
                 'type_product',
                 'folio',
                 'ref_id',
                 'client',
                 'depo',
                 'ccy',
                 'unit',
                 ('nominal','coupon_couru'),
                 ('price','price_pct'),
                 'daycount',
                 'date_val',
                 'date_end',
                 'taux',
                 'fee',
                 'obs',
                 'chk_verify',
                 'oper_verify',
                 'time_verify'
                 ) 
      }), 
    ('Approbation', {
      #'classes': ('collapse', 'open'),
      'fields': (
                 'date_trd',
                 'chk_approv',
                 'corresp',
                 'account',
                 #'ctrl_cf',
                 'oper_approv',
                 'time_approv',
                 #'cliFile',
                 ),
      }),
     ('Follow-ups', {
      #'classes': ('collapse', 'open'),
      'fields': (
                'docTraceLog',
                'chk_end',
                 ),
      }),
  )

  def get_readonly_fields(self, request, obj=None):
    #if not request.user.is_superuser:
    self.readonly_fields = ['oper_verify','time_verify','oper_approv','time_approv'] #

    return self.readonly_fields 

  def get_form(self, request, obj=None, **kwargs):
      # just save obj reference for future processing in Inline
      request._obj_ = obj
      #print(request._obj_)
      return super(FIAdmin, self).get_form(request, obj, **kwargs)

  def save_model(self, request, obj, form, change):
      #update oper_verify
      if not obj.oper_verify and obj.chk_verify:  
          obj.oper_verify = request.user 

      if not obj.oper_approv and obj.chk_approv: 
          #if not obj.oper_verify == request.user:
          obj.oper_approv = request.user

      obj.save()
  
  def save_formset(self, request, form, formset, change):
      if formset.model != ClientFileStorage:
          return super(FIAdmin, self).save_formset(request, form, formset, change)
      #pass parent value to child 
      instances = formset.save(commit=False)
      for instance in instances:
          if not instance.pk and request.user.is_authenticated:
              #
              parent_id = instance.object_id
              parent_obj = FX.objects.get(pk=parent_id)
              #
              instance.oper = request.user
              instance.client = parent_obj.client
          instance.save()
      formset.save_m2m()

  #actions
  #----------------------------------------------------------------------
  def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str
    import datetime
    today = datetime.date.today().strftime("%Y%m%d") 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=" + today + '_FixedIncome.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
      smart_str(u"id"),  
      smart_str(u"folio"),
      smart_str(u"ref_id"),
      smart_str(u"type_product"),
      smart_str(u"date_val"),
      smart_str(u"face_val"),
      smart_str(u"price"),
      smart_str(u"coupon_couru"),
      smart_str(u"price_pct"),
      smart_str(u"ccy"),
      smart_str(u"taux"),
      smart_str(u"date_end"),
      smart_str(u"fee"), 
      smart_str(u"chk_end"),                  
    ])
    for obj in queryset:
      writer.writerow([
        smart_str(obj.id),        
        smart_str(obj.get_folio_display()),
        smart_str(obj.ref_id),
        smart_str(obj.type_product),
        smart_str(obj.date_val),       
        smart_str(obj.nominal),
        smart_str(obj.price),
        smart_str(obj.coupon_couru),
        smart_str(obj.price_pct),
        smart_str(obj.ccy),              
        smart_str(obj.taux),
        smart_str(obj.date_end), 
        smart_str(obj.fee),  
        smart_str(obj.chk_end),  
      ])
    return response

  export_csv.short_description = u"Export CSV"    

  def chk_end(modeladmin, request, queryset):
    statut = queryset.values_list('chk_end', flat=True)
    #date = request.POST['date']
    if not statut[0]:
      queryset.update(chk_end=True)
    else:
      queryset.update(chk_end=False)
    #modeladmin.message_user(request, ("Successfully updated statut for %d rows") % (queryset.count(),), messages.SUCCESS)
  chk_end.short_description = "Check/Uncheck End" 

  actions = [export_csv, chk_end]
# Register your models here.
admin.site.register(FI, FIAdmin)

class FXAdmin(admin.ModelAdmin):

  form = FXForm 
  inlines = [CashFlowDetailInline, ClientFileStorageGenericInline] #

  list_display = ('id','chk_end','cpty','type_product','date_val','ccy_pair','fx_rate', #'counterparty',
                  'corresp_in','ccy_in','montant_in',
                  'corresp_out','ccy_out','montant_out')
  
  list_filter = [('type_product', admin.RelatedOnlyFieldListFilter),
                 'chk_end',
                 ('ccy_pair', admin.RelatedOnlyFieldListFilter),
                 ('cpty', admin.RelatedOnlyFieldListFilter),
                 ]
  search_fields = ['montant_in','montant_out',]
  date_hierarchy = 'date_val' 
  
  fieldsets = (      
    ('Négociation', {
      'fields': (
                 'type_product',
                 'cpty',
                 'ccy_pair',
                 'date_trd',
                 'date_val',
                 'fx_rate',
                 ('ccy_out','montant_out'),
                 ('ccy_in','montant_in'),
                 'chk_verify',
                 'oper_verify',
                 'time_verify',
                 #'cliFile',
                 ) 
      }), 
    ('Approbation', {
      #'classes': ('collapse', 'open'),
      'fields': (
                 'chk_approv',
                 'ctrl_cf',
                 ('corresp_in','account_in'),
                 ('corresp_out','account_out'),
                 'oper_approv',
                 'time_approv',
                 ),
      }),  
     ('Follow-ups', {
      #'classes': ('collapse', 'open'),
      'fields': (
                'docTraceLog',
                'chk_end','date_end',
                 ),
      }), 
  )

  def get_readonly_fields(self, request, obj=None):
    #if not request.user.is_superuser:
    self.readonly_fields = ['oper_verify','time_verify','oper_approv','time_approv'] #
  
    return self.readonly_fields 

  def get_form(self, request, obj=None, **kwargs):
    # just save obj reference for future processing in Inline
    request._obj_ = obj
    #print(request._obj_)
    return super(FXAdmin, self).get_form(request, obj, **kwargs)

  def save_model(self, request, obj, form, change):
      #update oper_verify
      if not obj.oper_verify and obj.chk_verify:  
          obj.oper_verify = request.user 

      if not obj.oper_approv and obj.chk_approv: 
          #if not obj.oper_verify == request.user:
          obj.oper_approv = request.user
      
      obj.save()

  def save_formset(self, request, form, formset, change):
      if formset.model != ClientFileStorage:
          return super(FXAdmin, self).save_formset(request, form, formset, change)
      #pass parent value to child 
      instances = formset.save(commit=False)
      for instance in instances:
          if not instance.pk and request.user.is_authenticated:
              #
              parent_id = instance.object_id
              parent_obj = FX.objects.get(pk=parent_id)
              #
              instance.oper = request.user
              instance.client = parent_obj.client
          instance.save()
      formset.save_m2m()

  #actions
  #----------------------------------------------------------------------
  def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str
    import datetime
    today = datetime.date.today().strftime("%Y%m%d") 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=" + today + '_Forex.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
      smart_str(u"id"),
      smart_str(u"type_product"),      
      smart_str(u"cpty"),        
      smart_str(u"date_val"),
      smart_str(u"ccy_pair"),
      smart_str(u"fx_rate"),
      smart_str(u"ccy_in"),            
      smart_str(u"montant_in"),
      smart_str(u"ccy_out"),            
      smart_str(u"montant_out"),
    ])
    for obj in queryset:
      writer.writerow([
        smart_str(obj.pk),
        smart_str(obj.type_product),        
        smart_str(obj.cpty), 
        smart_str(obj.date_val),
        smart_str(obj.ccy_pair),
        smart_str(obj.fx_rate),
        smart_str(obj.ccy_in),
        smart_str(obj.montant_in),
        smart_str(obj.ccy_out),
        smart_str(obj.montant_out),
      ])
    return response

  export_csv.short_description = u"Export CSV"  
  
  def chk_end(modeladmin, request, queryset):
    statut = queryset.values_list('chk_end', flat=True)
    #date = request.POST['date']
    if not statut[0]:
      queryset.update(chk_end=True)
    else:
      queryset.update(chk_end=False)
    #modeladmin.message_user(request, ("Successfully updated statut for %d rows") % (queryset.count(),), messages.SUCCESS)
  chk_end.short_description = "Check/Uncheck End" 

  actions = [export_csv, chk_end]
# Register your models here.
admin.site.register(FX, FXAdmin)

class FXCliAdmin(admin.ModelAdmin):

  form = FXCliForm 

  inlines = [ClientFileStorageGenericInline] #

  list_display = ('id','object_id','client',
                  'nature','date_trd','date_val','fx_rate','fee_rate',)
  
  list_filter = ['nature',
                 'chk_end',
                 ('type_product', admin.RelatedOnlyFieldListFilter),
                 ('ccy_pair', admin.RelatedOnlyFieldListFilter),
                 ]
  
  search_fields = ['montant_in','montant_out',]
  date_hierarchy = 'date_val' 

  fieldsets = (      
    ('Négociation', {
      'fields': (
                 #'ctrl_cf',
                 'type_product',
                 'content_type','object_id',
                 'client',
                 'ccy_pair',
                 'date_trd',
                 'date_val',
                 'nature',
                 'fx_rate','fee_rate',
                 ('ccy_out','montant_out'),
                 ('ccy_in','montant_in'),
                 'chk_verify',
                 'oper_verify',
                 'time_verify',
                 ) 
      }), 
    ('Approbation', {
      #'classes': ('collapse', 'open'),
      'fields': (
                'chk_approv',
                'montant_tva',
                'oper_approv',
                'time_approv',
                ),
      }), 
     ('Follow-ups', {
      #'classes': ('collapse', 'open'),
      'fields': (
                'docTraceLog',
                'chk_end','date_end',
                 ),
      }),   
  )

  def get_readonly_fields(self, request, obj=None):
    if not request.user.is_superuser:
      self.readonly_fields = ['type_product','content_type','object_id', 
                            'oper_verify','time_verify','oper_approv','time_approv'] #
    else:
      self.readonly_fields = ['oper_verify','time_verify','oper_approv','time_approv'] #


    return self.readonly_fields 

  def get_form(self, request, obj=None, **kwargs):
    # just save obj reference for future processing in Inline
    request._obj_ = obj
    #print(request._obj_)
    return super(FXCliAdmin, self).get_form(request, obj, **kwargs)  

  def save_model(self, request, obj, form, change):

      if obj and obj.client:
          ctype = ContentType.objects.get_for_model(ClientCtrl, for_concrete_model=True)
      else:
          ctype = ContentType.objects.get_for_model(User, for_concrete_model=True)        
      #check status
      if not obj.object_id:
          if obj.client: 
              obj.object_id = obj.client.id
              obj.content_type_id = ctype.id
          else:
              obj.object_id = request.user.id
              obj.content_type_id = ctype.id        
      #
      if not obj.type_product:
        ctype = ContentType.objects.get_for_model(obj, for_concrete_model=False)
        obj.type_product = CatalogTypeProduct.objects.get(content_type=ctype)

      #update oper_verify
      if not obj.oper_verify and obj.chk_verify:  
          obj.oper_verify = request.user 

      if not obj.oper_approv and obj.chk_approv: 
          #if not obj.oper_verify == request.user:
          obj.oper_approv = request.user
      
      #if obj.chk_verify and obj.montant_out >= 0:
      #  if obj.nature:
      #    ct_value = float(obj.nature)*round(float(obj.montant_out) * (1 + float(obj.fee_rate)) * float(obj.fx_rate),0)
      #  else:
      #    ct_value = round(float(obj.montant_out) * float(obj.fx_rate),0)
      #
      #    obj.date_pay = obj.date_val
      #    obj.chk_pay = True        
  
      #  tva = float(obj.nature)*round(ct_value * 0.189,0)
      #
      #  obj.montant_in = ct_value
      #  obj.montant_tva = tva

      obj.save()    

  def save_formset(self, request, form, formset, change):
      if formset.model != ClientFileStorage:
          return super(FXCliAdmin, self).save_formset(request, form, formset, change)
      #pass parent value to child 
      instances = formset.save(commit=False)
      for instance in instances:
          if not instance.pk and request.user.is_authenticated:
              #
              parent_id = instance.object_id
              parent_obj = FXCli.objects.get(pk=parent_id)
              #
              instance.oper = request.user
              instance.client = parent_obj.client
          instance.save()
      formset.save_m2m()
  
  #actions
  #----------------------------------------------------------------------
  def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str
    import datetime
    today = datetime.date.today().strftime("%Y%m%d") 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = "attachment; filename=" + today + '_ForexClient.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
      smart_str(u"id"),
      smart_str(u"type_product"),      
      smart_str(u"client"),        
      smart_str(u"date_val"),
      smart_str(u"ccy_pair"),
      smart_str(u"fx_rate"),
      smart_str(u"ccy_in"),            
      smart_str(u"montant_in"),
      smart_str(u"ccy_out"),            
      smart_str(u"montant_out"),
    ])
    for obj in queryset:
      writer.writerow([
        smart_str(obj.pk),
        smart_str(obj.type_product),        
        smart_str(obj.client), 
        smart_str(obj.date_val),
        smart_str(obj.ccy_pair),
        smart_str(obj.fx_rate),
        smart_str(obj.ccy_in),
        smart_str(obj.montant_in),
        smart_str(obj.ccy_out),
        smart_str(obj.montant_out),
      ])
    return response

  export_csv.short_description = u"Export CSV"  
  
  
  def chk_end(modeladmin, request, queryset):
    statut = queryset.values_list('chk_end', flat=True)
    #date = request.POST['date']
    if not statut[0]:
      queryset.update(chk_end=True)
    else:
      queryset.update(chk_end=False)
    #modeladmin.message_user(request, ("Successfully updated statut for %d rows") % (queryset.count(),), messages.SUCCESS)
  chk_end.short_description = "Check/Uncheck End" 

  actions = [export_csv, chk_end]
# Register your models here.
admin.site.register(FXCli, FXCliAdmin)



class CollateralAdmin(admin.ModelAdmin):

    list_display = ('id','mm','fi','decot_pct','decote_montant','dom_pct','dom_pct_montant_lc')

    #search_fields = ['dossier_trf','dossier_dom']
    
    #date_hierarchy = 'date_val' 

    #list_filter = [
    #]
    fieldsets = (      
        ("Contrôle d'Apurement", {
            #'classes': ('collapse', 'open'),
            'fields': ('id',
                'mm',
                'fi',
                'decot_pct','decote_montant','dom_pct','dom_pct_montant_lc',
                'obs',
                ),
            }),  
    )
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['id','decote_montant',]
        return self.readonly_fields  
    
    #----------------------------------------------------------------------    
    #def save_model(self, request, obj, form, change):
      #obj.save()


# Register your models here.
admin.site.register(Collateral, CollateralAdmin)
