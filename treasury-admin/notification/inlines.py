# -*- coding: utf-8 -*-
#
from django.contrib.contenttypes.admin import GenericTabularInline, GenericStackedInline
from .models import *
from .forms import *
#
class EmailCtrlInline(GenericTabularInline):
    model = EmailCtrl
    #form = CashFlowDetailForm
    extra = 0
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    #
    fieldsets = (
        (None, {
            'fields': ('id','time_approv','statut','client','to_email','template','batch_no','chk_approv') #,
            }),  
    )
    readonly_fields = ('id','time_approv','statut','client','to_email','template','batch_no','chk_approv')
    show_change_link = True
    can_delete = False
    