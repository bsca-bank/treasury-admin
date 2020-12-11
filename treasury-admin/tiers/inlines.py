# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
#
from django import forms

from .client.models import ClientFileStorage
from .corresp.models import *
from .cpty.models import *
from .depo.models import *

from .forms import *
#
from django_extensions.admin import ForeignKeyAutocompleteAdmin


#from django.urls import resolve
class ClientFileStorageGenericInline(GenericTabularInline):
    model = ClientFileStorage
    form = ClientFileStorageGenericInlineForm
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    fieldsets = (
        (None, {
            'fields': ('id','oper','type_file','file_name','file','modified',) #,
            }),  
    )
    readonly_fields = ('id','modified','oper')
    show_change_link = True
    can_delete = True
    extra = 0

    def has_add_permission(self, request):
        return True

    #limit inline formfield
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        field = super(ClientFileStorageGenericInline, self).formfield_for_foreignkey( \
            db_field, request, **kwargs)
        
        if db_field.name == 'type_file':
            if request._obj_ is not None:
                ctype = ContentType.objects.get_for_model(request._obj_, for_concrete_model=True)
                field.queryset = field.queryset.filter(content_type=ctype)
            else:
                field.queryset = field.queryset.none()
        return field

#from django.urls import resolve
class ClientFileStorageInline(admin.TabularInline):
    model = ClientFileStorage
    form = ClientFileStorageForm

    extra = 0
    fk_name= 'client'
    fieldsets = (
        (None, {
            'fields': ('id','type_file','file_name','file','modified',) #,
            }),  
    )
    readonly_fields = ('id','modified') #'change_link',
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request):
        return True


class AccounCorresptInline(admin.TabularInline):
    model = AccountCorresp
    extra = 0
    
class AccounDepotInline(admin.TabularInline):
    model = AccountDepo
    extra = 0