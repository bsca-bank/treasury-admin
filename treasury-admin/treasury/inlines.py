# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericStackedInline
#
from django.db.models import Q
#
from .models import FXCli, Collateral
from .forms import FXCliForm

class FXCliInline(GenericStackedInline):
    model = FXCli
    form = FXCliForm
    fieldsets = (
        (None, {
            'fields': ('nature','ccy_pair','fx_rate','fee_rate', 
                'date_trd','date_val',
                'oper_verify','chk_verify','time_verify')
            }),  
    )
    readonly_fields = ['oper_verify','time_verify']
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    max_num=1
    show_change_link = True 
    can_delete = True   
    classes = ['collapse']

    #limit inline formfield
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        field = super(FXCliInline, self).formfield_for_foreignkey( \
            db_field, request, **kwargs)
        
        if db_field.name == 'ccy_pair':
            #print(request._obj_.ccy)
            if request._obj_:
                q_ccy1 = Q(ccy1=request._obj_.ccy)
                q_ccy2 = Q(ccy2=request._obj_.ccy)
                field.queryset = field.queryset.filter(q_ccy1|q_ccy2)
            else:
                field.queryset = field.queryset.none()
        return field


class CollateralInline(admin.TabularInline):
    model = Collateral
    fieldsets = (
        (None, {
            'fields': ('id','mm','fi','decot_pct','decote_montant','couvr_pct','dom_pct','dom_pct_montant_lc')
            }),  
    )
    readonly_fields = ['id','decote_montant','couvr_pct','dom_pct']
    extra = 0
    show_change_link = True 
    can_delete = True   
    #classes = ['collapse']