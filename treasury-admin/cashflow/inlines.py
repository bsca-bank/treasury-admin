# -*- coding: utf-8 -*-
#
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from .models import *
from .forms import *
#
class CashFlowDetailInline(GenericTabularInline):
    model = CashFlowDetail
    form = CashFlowDetailForm
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    #
    fieldsets = (
        (None, {
            'fields': ('id','nature','date_val','montant','corresp','account','chk_verify','date_pay','chk_pay') #,
            }),  
    )
    readonly_fields = ('id','nature','date_val','montant','corresp','account','chk_verify','date_pay','chk_pay')
    #readonly_fields = ('id','nature','date_val','montant','corresp','account','chk_verify')
    show_change_link = True
    can_delete = False

class CashFlowDetailEditableInline(GenericTabularInline):
    model = CashFlowDetail
    form = CashFlowDetailForm
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    #
    fieldsets = (
        (None, {
            'fields': ('id','nature','date_val','montant','corresp','account','chk_verify','date_pay','ref_swift','chk_pay') #,
            }),  
    )
    readonly_fields = ('id',)
    #readonly_fields = ('id','nature','date_val','montant','corresp','account','chk_verify')
    show_change_link = True
    can_delete = False


class CashFlowDetailInfoPlusInline(GenericTabularInline):
    model = CashFlowDetail
    form = CashFlowDetailForm
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    #
    fieldsets = (
        (None, {
            'fields': ('id','nature','date_val','category','montant','corresp','account','chk_verify','date_pay','chk_pay') #,
            }),  
    )
    readonly_fields = ('id','nature','date_val','category','montant','corresp','account','chk_verify','date_pay','chk_pay')
    show_change_link = True
    can_delete = False