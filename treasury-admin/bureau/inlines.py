# -*- coding: utf-8 -*-

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
#
# Create your tests here.
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from django.contrib.contenttypes.models import ContentType
#
from .gestion.models import InternalFileFolder, InternalFileStorage
from .sca.models import MeetingItem, MeetingDoc

from .forms import MeetingItemForm, MeetingDocForm, MeetingDocShortForm

class InternalFileStorageInline(admin.TabularInline):
    model = InternalFileStorage
    #form = ClientFileStorageForm
    #formset = ClientFileStorageFormSet
    extra = 0
    fk_name= 'file_folder'
    fieldsets = (
        (None, {
            'fields': ('id','ref_id','file_name','group_oper','type_file','file','modified',) #,
            }),  
    )
    readonly_fields = ('id','ref_id','file_name','group_oper','type_file','file','modified',) #'change_link',
    show_change_link = True
    can_delete = True


class MeetingItemInline(admin.TabularInline):
    #TRF/RPT may be linked to a Rtroc Ticket ()
    model = MeetingItem
    form = MeetingItemForm
    extra = 0
    sortable_field_name = "order_no"
    fieldsets = (
        (None, {
            'fields': ('id','meeting','nature','order_no','ref_no','name_fr','name_cn','obs')
            }),  
    )
    readonly_fields = ('id','meeting',) #'nature','order_no','name_fr','name_cn')
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request):
        return True  

class MeetingDocInline(admin.TabularInline):
    model = MeetingDoc
    form = MeetingDocForm
    extra = 0
    sortable_field_name = "modified"
    fieldsets = (
        (None, {
            'fields': ('id','modified','nature','name_fr','file_fr','name_cn','file_cn','obs')
            }),  
    )
    readonly_fields = ('id','meeting','modified') #'nature','order_no','name_fr','name_cn')
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request):
        return True  

    #limit inline formfield
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        field = super(MeetingDocInline, self).formfield_for_foreignkey( \
            db_field, request, **kwargs)
        if db_field.name == 'nature':
            ctype = ContentType.objects.get_for_model(MeetingDoc, for_concrete_model=True)
            field.queryset = field.queryset.filter(content_type=ctype)
        return field


class MeetingDocShortInline(admin.TabularInline):
    model = MeetingDoc
    form = MeetingDocShortForm
    extra = 0
    sortable_field_name = "modified"
    fieldsets = (
        (None, {
            'fields': ('id','nature','name_fr','name_cn','file_fr')
            }),  
    )
    readonly_fields = ('id','meeting') 
    show_change_link = True
    can_delete = True

    def has_add_permission(self, request):
        return True  

    #limit inline formfield
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        field = super(MeetingDocShortInline, self).formfield_for_foreignkey( \
            db_field, request, **kwargs)
        
        if db_field.name == 'nature':
            ctype = ContentType.objects.get_for_model(MeetingDoc, for_concrete_model=True)
            field.queryset = field.queryset.filter(content_type=ctype)
        return field

        
