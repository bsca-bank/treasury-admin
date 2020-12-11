# -*- coding: utf-8 -*-
#native libs
from datetime import date, timedelta
from django.contrib import admin
from django.db.models import Q
#3rd-party libs
from import_export.admin import ImportExportModelAdmin
#native modules
from .models import *
from .forms import *
from .forms import *
from .sygma.models import *
#related apps
from cashflow.models import *
from cashflow.forms import *
#
from util.catalog.models import CatalogTypeProduct
from .calc import calc_cash_position #, calc_cash_position_detail


class CashflowDetailInline(admin.TabularInline):
    model = CashFlowDetail
    form = CashFlowDetailForm
    extra = 0    
    fieldsets = (
        (None, {
            'fields': ('id','nature','content_type','ref_id','date_val','montant','ref_swift','chk_verify','chk_pay')
            }),  
    )
    readonly_fields = ('id','nature','content_type','ref_id','date_val','montant','ref_swift')
    show_change_link = True
    can_delete = False

    def has_add_permission(self, request):
        return False 

class TreasuryPositionAdmin(ImportExportModelAdmin):

    form = TreasuryPositionForm

    #alter change_list view to enhanced view
    change_list_template = 'custom/change_list.html'  

    #inlines = []

    list_display = ('id','oper_input','nature','date_val','corresp','account','montant_op','montant','time_verify')    
    list_filter = [
        #limit the list_filter choices to the users.
        ('corresp', admin.RelatedOnlyFieldListFilter),
        ('account__ccy', admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ['corresp',]
    date_hierarchy = 'date_val' 

    fieldsets = (      
        ('Saisie des informations', {
            'fields': ('type_product',\
                'date_val','corresp','account','montant_op','montant',
                'chk_verify','oper_verify','time_verify') #
            }), 
        ('Validation des informaton', {
            'fields': ('chk_approv','oper_approv','time_approv') #
            }),        
    )
    def get_readonly_fields(self, request, obj=None):
        
        self.readonly_fields = ['type_product','time_verify','time_approv','oper_verify','oper_approv'] 
        
        if not request.user.is_superuser:
            self.readonly_fields = self.readonly_fields + ['oper_input']

        return self.readonly_fields    

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(TreasuryPositionAdmin, self).get_form(request, obj, **kwargs)

    def changelist_view(self, request, extra_context=None):

        #récupération des données
        #-------------------------------------------------------
        first_date = date(2018,12,31)

        c_ts = Q(date_val__gt=first_date)
        c_cp = Q(corresp__chk_active=True)
        c_ac = Q(account__chk_active=True)
        c_valid = Q(chk_pay=0,chk_verify=1) 

        qs_ts = TreasuryPosition.objects.filter(c_ts,c_cp,c_ac).values("id","nature","date_val","corresp","account","montant_op","montant")
        qs_cf = CashFlowDetail.objects.filter(c_ts,c_cp,c_ac,c_valid)
    
        tb_ts = qs_ts.to_dataframe(coerce_float=True)
        tb_cf = qs_cf.to_dataframe(coerce_float=True)          
       
        #out_path = 'C://github//temp//' + 'tb_ts.csv'
        #tb_ts.to_csv(out_path, sep="|", na_rep='', encoding='utf-8')    
    
        #out_path = 'C://github//temp//' + 'tb_cf.csv'
        #tb_cf.to_csv(out_path, sep="|", na_rep='', encoding='utf-8')          
       
        cash_html = calc_cash_position(tb_ts, tb_cf)
        #cash_detail_html = calc_cash_position_detail(tb_ts, tb_cf)
        def is_dmf(user):
            return user.groups.filter(name='DMF').exists()
        
        #récupération des données
        #-------------------------------------------------------     
        extra_context = {
            "cash_html": cash_html,
            #"cash_detail_html": cash_detail_html,
            "is_dmf_user": is_dmf(request.user)            
        }
        return super(TreasuryPositionAdmin, self).changelist_view(request, extra_context=extra_context) 

    def save_model(self, request, obj, form, change):
        #same person is authorized to input and verify this ticket
        if not obj.oper_input:
            obj.oper_input = request.user

        if not obj.oper_verify and obj.chk_verify:   
            obj.oper_verify = request.user

        if not obj.oper_approv and obj.chk_approv: 
            #if not obj.oper_verify == request.user:
            obj.oper_approv = request.user
            #else:
            #    obj.oper_approv = False

        if not obj.type_product:
            ctype = ContentType.objects.get_for_model(obj, for_concrete_model=True)
            obj.type_product = CatalogTypeProduct.objects.get(content_type=ctype)

        if not obj.nature:
            obj.nature = obj.corresp.type_tiers.category_l1

        obj.save()

    #authorization filter
    def get_queryset(self, request):

        def is_dmf(user):
            return user.groups.filter(name='DMF').exists()

        def has_grp_view(user):
            return user.groups.filter(name='ctrl_has_grp_view').exists()
        
        qs = super(TreasuryPositionAdmin, self).get_queryset(request)

        #if has controler priority
        if is_dmf(request.user):
            return qs

        elif has_grp_view(request.user):
            user_groups = request.user.groups.values_list('id')
            crews = User.objects.filter(groups__id__in = user_groups)
            return qs.filter(oper_input__in=crews) 
        return qs.filter(oper_input=request.user)  

    #actions
    #----------------------------------------------------------------------
    def export_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=LoroCorresp.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"id"),
            smart_str(u"date_val"),
            smart_str(u"corresp"),
            smart_str(u"type_tiers"),                        
            smart_str(u"account"), 
            smart_str(u"ccy"),   
            smart_str(u"montant_op"),
            smart_str(u"montant"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.date_val), 
                smart_str(obj.corresp),
                smart_str(obj.corresp.type_tiers), 
                smart_str(obj.account),
                smart_str(obj.account.ccy),
                smart_str(obj.montant_op),
                smart_str(obj.montant),
            ])
        return response

    export_csv.short_description = u"Export CSV"    

    actions = [export_csv ]    

# Register your models here.
admin.site.register(TreasuryPosition, TreasuryPositionAdmin)


class SygmaCtrlAdmin(admin.ModelAdmin):
    
    list_display = ('id','type_msg','cf','statut_msg','corr_expd','corr_dest','date_val','ref_id','donneur','benef','ccy','montant','link_id','ctrl')
    list_filter = ['type_msg','cf','codtype','statut_msg']
    search_fields = ['ref_id','montant','donneur','link_id','corr_expd','corr_dest']
    date_hierarchy = 'date_val' 

    def chk_ctrl(modeladmin, request, queryset):
        statut = queryset.values_list('ctrl', flat=True)
        if not statut[0]:
            queryset.update(ctrl=True)
        else:
            queryset.update(ctrl=False)
    chk_ctrl.short_description = "Check/Uncheck Controle"

    def has_delete_permission(self, request, obj=None):
    
        if request.user.is_superuser and obj:
            return True
        else:
            return False

        return super(SygmaCtrlAdmin, self).has_delete_permission(request, obj=obj)         

    def get_actions(self, request):
        actions = super(SygmaCtrlAdmin, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    #actions
    #----------------------------------------------------------------------
    def export_csv(self,modeladmin, request, queryset):
        import csv
        import datetime
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        
        today = datetime.date.today().strftime("%Y%m%d") 
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=' + today + '_SygmaCtrl.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"id"),
            smart_str(u"type_msg"),
            smart_str(u"cashflow"),                        
            smart_str(u"statut_msg"), 
            smart_str(u"corr_expd"),   
            smart_str(u"corr_dest"),
            smart_str(u"date_val"), 
            smart_str(u"ref_id"),   
            smart_str(u"donneur"),
            smart_str(u"benef"), 
            smart_str(u"ccy"),   
            smart_str(u"montant"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.type_msg), 
                smart_str(obj.get_cf_display()), 
                smart_str(obj.statut_msg),
                smart_str(obj.corr_expd),
                smart_str(obj.corr_dest),
                smart_str(obj.date_val), 
                smart_str(obj.ref_id), 
                smart_str(obj.donneur),
                smart_str(obj.benef),
                smart_str(obj.ccy),  
                smart_str(obj.montant),  
            ])
        return response

    export_csv.short_description = u"Export CSV"    

    actions = [chk_ctrl,export_csv]    

# Register your models here.
admin.site.register(SygmaCtrl, SygmaCtrlAdmin)
