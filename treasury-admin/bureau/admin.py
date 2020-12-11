# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib import messages
from django.db.models.signals import pre_save

import datetime
from django.utils import timezone

from .gestion.models import *
from .sca.models import *
from .inlines import InternalFileStorageInline, MeetingItemInline, MeetingDocInline,MeetingDocShortInline
from .forms import *
#

#@admin.site.unregister(InternalFileFolder)
class InternalFileFolderAdmin(admin.ModelAdmin):
    #attach inline model
    inlines = [InternalFileStorageInline] 

    list_display = ('id','ref_id','folder_name','type_folder','group_oper','created','modified') 
    
    list_filter = [
        #limit the list_filter choices to the users.

        ('oper', admin.RelatedOnlyFieldListFilter),
        ('group_oper', admin.RelatedOnlyFieldListFilter),
        ] 
    date_hierarchy = 'created'

    def save_formset(self, request, form, formset, change):
        if formset.model != InternalFileStorage:
            return super(InternalFileFolderAdmin, self).save_formset(request, form, formset, change)
        
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                #
                parent_ctype = ContentType.objects.get_for_model(instance)
                parent_id = instance.id
                #parent_obj = ClientCtrl.objects.get(pk=parent_id)
                instance.oper = request.user
                instance.object_id = parent_id
                instance.content_type = parent_ctype
            instance.save()
        formset.save_m2m()

    def save_model(self, request, obj, form, change):
        if obj and obj.group_oper:
            ctype = ContentType.objects.get_for_model(Group, for_concrete_model=True)
        else:
            ctype = ContentType.objects.get_for_model(User, for_concrete_model=True)        
        #check status
        if not obj.object_id:
            if obj.group_oper: 
               obj.object_id = obj.group_oper.id
               obj.content_type_id = ctype.id
            else:
                obj.object_id = request.user.id
                obj.content_type_id = ctype.id        
        
        if not obj.oper_id:
            obj.oper_id = request.user.id
        
        obj.save()
            
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['object_id','content_type','oper','created','modified'] #
        return self.readonly_fields    
#Register your models here.
admin.site.register(InternalFileFolder, InternalFileFolderAdmin)


#@admin.site.unregister(InternalFileStorage)
class InternalFileStorageAdmin(admin.ModelAdmin):

    list_display = ('id','date_recu','ref_id','group_oper','file_folder','file','modified','date_val','chk_verify','chk_approv',)   
    
    list_filter = [
        #limit the list_filter choices to the users.
        'chk_verify','chk_approv',
        ('oper', admin.RelatedOnlyFieldListFilter),
        ('group_oper', admin.RelatedOnlyFieldListFilter),
        ] 
    
    #search_fields = ['demandeur_last_name',]
    date_hierarchy = 'date_recu' 
    
    fieldsets = (      
            ('Information de Base', {
                'fields': ('date_recu','file_name','ref_id','group_oper','oper','file_folder','file','created','modified',
                'group_disrib',
                'obs',
                'date_val',) 
                }), 
            ("Contrôle de Traitement", {
                'classes': ('collapse', 'open'),
                'fields': ('chk_verify','oper_verify','time_verify','chk_approv','oper_approv','time_approv'),
                }),
        )

    def get_changeform_initial_data(self, request):
        return {'oper': request.user}     

    def save_model(self, request, obj, form, change):
        if obj and obj.group_oper:
            ctype = ContentType.objects.get_for_model(Group, for_concrete_model=True)
        else:
            ctype = ContentType.objects.get_for_model(User, for_concrete_model=True)        
        #check status
        if not obj.object_id:
            if obj.group_oper: 
               obj.object_id = obj.group_oper.id
               obj.content_type_id = ctype.id
            else:
                obj.object_id = request.user.id
                obj.content_type_id = ctype.id        
        
        if not obj.date_val: 
            obj.chk_verify = True
            obj.chk_approv = True

        if not obj.oper_id:
            obj.oper_id = request.user.id
        
        if not obj.oper_verify and obj.chk_verify: 
            obj.oper_verify = request.user 

        if not obj.oper_approv and obj.chk_approv: 
            obj.oper_approv = request.user

        obj.save()
    
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['object_id','content_type','oper','created','modified','time_verify','time_approv'] #
        return self.readonly_fields    

# Register your models here.
admin.site.register(InternalFileStorage, InternalFileStorageAdmin)


#
class MeetingTypeAdmin(admin.ModelAdmin):
 
    list_display = ('id','level','nature','type_session','name_fr','name_cn','alias','parent_type',)   
    
    list_filter = [
        #limit the list_filter choices to the users.
        'nature', #admin.RelatedOnlyFieldListFilter),
        'type_session',
        ] 
    
    search_fields = ['alias',]

admin.site.register(MeetingType, MeetingTypeAdmin)

class MeetingItemTypeAdmin(admin.ModelAdmin):
 
    list_display = ('id','level','nature','name_fr','name_cn','item_key','parent_type',)   

    list_filter = [
        #limit the list_filter choices to the users.
        'nature', #admin.RelatedOnlyFieldListFilter),
        'item_key', #admin.RelatedOnlyFieldListFilter),
        ] 

    search_fields = ['item_key',]

admin.site.register(MeetingItemType, MeetingItemTypeAdmin)


class MeetingUserTypeAdmin(admin.ModelAdmin):

    list_display = ('id','nature','name_fr','name_cn','alias','parent_type')   

    list_filter = [
        #limit the list_filter choices to the users.
        'nature', #admin.RelatedOnlyFieldListFilter),
        'alias', #admin.RelatedOnlyFieldListFilter),
        ] 
    
    search_fields = ['alias',]

admin.site.register(MeetingUserType, MeetingUserTypeAdmin)


#Create your models here.
class MeetingAdmin(admin.ModelAdmin):

    form = MeetingForm

    inlines = [MeetingDocShortInline, MeetingItemInline]

    list_display = ('id','year','nature','date_val','order_no','name_fr','name_cn','acc_period','ref_meeting',)   

    list_filter = [
        #limit the list_filter choices to the users.
        'acc_period',
        'nature', #admin.RelatedOnlyFieldListFilter),
        ] 

    search_fields = ['ref_meeting','acc_period']
    date_hierarchy = 'date_val' 

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(MeetingAdmin, self).get_form(request, obj, **kwargs)


    def save_formset(self, request, form, formset, change):
        if formset.model not in [MeetingDoc, MeetingItem]:
            return super(MeetingAdmin, self).save_formset(request, form, formset, change)
        
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:

            if not instance.pk and request.user.is_authenticated:
                instance.oper = request.user

            if formset.model == MeetingItem:
                parent_id = instance.meeting.id
                parent_obj = Meeting.objects.get(pk=parent_id)
                instance.date_val = parent_obj.date_val

            instance.save()
        formset.save_m2m()

admin.site.register(Meeting, MeetingAdmin)

#Create your models here.
class MeetingItemAdmin(admin.ModelAdmin):

    form = MeetingItemForm

    inlines = [MeetingDocInline]

    list_display = ('id','year','date_val','meeting','order_no','ref_no','nature','name_cn','name_fr',)   

    list_filter = [
        #limit the list_filter choices to the users.
        'nature', #admin.RelatedOnlyFieldListFilter),
        'meeting', #admin.RelatedOnlyFieldListFilter),
        ] 
    
    search_fields = ['ref_item',]
    date_hierarchy = 'date_val' 

    def save_formset(self, request, form, formset, change):
        if formset.model != MeetingDoc:
            return super(MeetingItemAdmin, self).save_formset(request, form, formset, change)
        
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                #
                parent_ctype = ContentType.objects.get_for_model(instance)
                parent_id = instance.id
                #parent_obj = ClientCtrl.objects.get(pk=parent_id)
                instance.oper = request.user
                instance.modified = timezone.now()
            instance.save()
        formset.save_m2m()

    def get_actions(self, request):
        actions = super(MeetingItemAdmin, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions    

    def export_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=MeetingItems.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"id"),
            smart_str(u"date_val"),
            smart_str(u"meeting"),
            smart_str(u"order_no"),
            smart_str(u"ref_no"),          
            smart_str(u"nature"),
            smart_str(u"name_cn"),
            smart_str(u"name_fr"),
            smart_str(u"obs"),
		])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.meeting.date_val),
                smart_str(obj.meeting),
                smart_str(obj.order_no),
                smart_str(obj.ref_no),
                smart_str(obj.nature),
                smart_str(obj.name_cn),
                smart_str(obj.name_fr),
                smart_str(obj.obs),
            ])

        return response

    export_csv.short_description = u"Export CSV"    

    actions = [export_csv]    

admin.site.register(MeetingItem, MeetingItemAdmin)


class MeetingUserAdmin(admin.ModelAdmin):

    inlines = [MeetingDocInline]

    list_display = ('id','alias','gender','date_birth','nationality','no_passport','date_exp_passport','position')  

    list_filter = [
        'nature', #admin.RelatedOnlyFieldListFilter),
        'nationality',
        ] 

    search_fields = ['first_name','last_name','name_cn',]

    fieldsets = (      
            ('Information de Base', {
                'fields': ('nature','first_name','last_name','name_cn','alias','gender','date_birth','nationality','is_active', 
                ) 
                }), 
            ("Contrôle", {
                #'classes': ('collapse', 'open'),
                'fields': ('is_staff','position','no_passport','date_exp_passport','tel_fix','tel_mobile','email'),
                }),
        )

    def save_formset(self, request, form, formset, change):
        if formset.model != MeetingDoc:
            return super(MeetingUser, self).save_formset(request, form, formset, change)
        
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                #
                parent_ctype = ContentType.objects.get_for_model(instance)
                parent_id = instance.id
                #parent_obj = ClientCtrl.objects.get(pk=parent_id)
                instance.oper = request.user
            instance.save()
        formset.save_m2m()

    def get_actions(self, request):
        actions = super(MeetingUserAdmin, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    def export_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=MeetingUsers.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"first_name"),
            smart_str(u"last_name"),
            smart_str(u"name_cn"),         
            smart_str(u"gender"),
            smart_str(u"nationality"),
            smart_str(u"no_passport"),          
            smart_str(u"date_exp_passport"),
            smart_str(u"position"),
		])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.first_name),
                smart_str(obj.last_name),
                smart_str(obj.name_cn),
                smart_str(obj.get_gender_display()),
                smart_str(obj.nationality),
                smart_str(obj.no_passport),
                smart_str(obj.date_exp_passport),
                smart_str(obj.position),
            ])

        return response

    export_csv.short_description = u"Export CSV"    

    actions = [export_csv]    

admin.site.register(MeetingUser, MeetingUserAdmin)


class MeetingDocAdmin(admin.ModelAdmin):

    form = MeetingDocForm

    list_display = ('id','nature','meeting','meeting_item','file_fr','file_cn')   

    list_filter = [
        'nature',
        'meeting', #admin.RelatedOnlyFieldListFilter),
        'meeting_item', #admin.RelatedOnlyFieldListFilter),
        ] 

    def get_actions(self, request):
        actions = super(MeetingDocAdmin, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

admin.site.register(MeetingDoc, MeetingDocAdmin)

