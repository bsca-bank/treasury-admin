from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
#
from .fx.models import *
from .workflow.models import *
from .catalog.models import *
from .fileStorage.models import *

from .forms import WorkflowForm, StatutForm, CatalogTypeCommercialForm,CatalogTypeProductForm

# from .related_admin.models import *


#
class DocTraceLogDetailAdmin(admin.ModelAdmin):
    list_display = ('id','chk_exp','oper_exp','time_exp','chk_recv','oper_recv','time_recv')

    def save_model(self, request, obj, form, change):    
        
        if not obj.oper_exp and obj.chk_exp:
            obj.oper_exp = request.user
       
        #update oper_verify
        if not obj.oper_recv and obj.chk_recv:  
                obj.oper_recv = request.user 

        obj.save()

    def get_readonly_fields(self, request, obj=None):

        self.readonly_fields = ['time_exp','oper_exp','time_recv','oper_recv',]

        if obj and not request.user.is_superuser:
            readonly_fields = []
            
            if obj.chk_exp :
                readonly_fields = readonly_fields + ['chk_exp',]
            if obj.chk_recv :
                readonly_fields = readonly_fields + ['chk_recv',]

            self.readonly_fields = self.readonly_fields + readonly_fields 

        return self.readonly_fields  

# Register your models here.
admin.site.register(DocTraceLogDetail, DocTraceLogDetailAdmin)


class DocTraceLogDetailInline(admin.TabularInline):
    
    model = DocTraceLogDetail
    extra = 0    
    sortable_field_name = "ref_id"
    fieldsets = (
        (None, {
            'fields': ('id','obs','chk_exp','oper_exp','time_exp','chk_recv','oper_recv','time_recv')
            }),  
    )

    show_change_link = True
    can_delete = False

    #def has_change_permission(self, request, obj=None,):
    #    return False

    def get_readonly_fields(self, request, obj=None):

        if not request.user.is_superuser:
            self.readonly_fields = ['time_exp','oper_exp','time_recv','oper_recv',]
        else:
            self.readonly_fields = ['time_exp','time_recv',]

        return self.readonly_fields
        
class DocTraceLogAdmin(admin.ModelAdmin):
    
    inlines = [DocTraceLogDetailInline]
    list_display = ('id','content_type','object_id','time_create')

    list_filter = [
        ('content_type',admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ['object_id']
    date_hierarchy = 'time_create' 
    
    fieldsets = (
        (None, {
            'fields': ('obs','time_create',)
            }),  
    )
    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['time_create']
        return self.readonly_fields  

    def save_formset(self, request, form, formset, change):
        if formset.model not in [DocTraceLogDetail]:
            return super(DocTraceLogAdmin, self).save_formset(request, form, formset, change)
        
        #pass parent value to child at inception
        instances = formset.save(commit=False)
        for instance in instances:
            
            if request.user.is_authenticated:
                if not instance.oper_exp and instance.chk_exp:
                    if not instance.time_exp:
                        instance.oper_exp = request.user

                if not instance.oper_recv and instance.chk_recv:
                    if not instance.time_recv:
                        instance.oper_recv = request.user

            instance.save()
        formset.save_m2m()


# Register your models here.
admin.site.register(DocTraceLog, DocTraceLogAdmin)

#from django.urls import resolve
class DocTraceLogGenericInline(GenericTabularInline):
    model = DocTraceLog
    #form = ClientFileStorageGenericInlineForm
    #formset = ClientFileStorageGenericFormSet
    extra = 1
    max_num = 1
    ct_field_name = 'content_type'
    id_field_name = 'object_id'
    fieldsets = (
        (None, {
            'fields': ('id','chk_create','time_create','obs') #,
            }),  
    )
    readonly_fields = ('id','time_create','obs') #'change_link',
    show_change_link = True
    can_delete = True

    #limit inline formfield
    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        
        field = super(DocTraceLogGenericInline, self).formfield_for_foreignkey( \
            db_field, request, **kwargs)
        if db_field.name == 'content_type':
            if request._obj_ is not None:
                ctype = ContentType.objects.get_for_model(request._obj_, for_concrete_model=True)
                field.queryset = field.queryset.filter(content_type=ctype)
            else:
                field.queryset = field.queryset.none()
        return field

class CcyPairAdmin(admin.ModelAdmin):
    list_display = ('id','alias','ccy1','ccy2','desc')
    list_filter = ['ccy1','ccy2',]
# Register your models here.
admin.site.register(CcyPair, CcyPairAdmin)

class StatutAdmin(admin.ModelAdmin):
    
    form = StatutForm

    list_display = ('id','content_type','statut','obs')
    list_filter = [
        'statut',
        ('content_type',admin.RelatedOnlyFieldListFilter),
        ]
    search_fields = ['statut']

# Register your models here.
admin.site.register(Statut, StatutAdmin)

class WorkflowAdmin(admin.ModelAdmin):
    
    form = WorkflowForm

    list_display = ('id','content_type','s_init','chk_switch','s_fnl','obs')

    list_filter = [
        ('content_type',admin.RelatedOnlyFieldListFilter),
        ]
    search_fields = ['chk_switch']

# Register your models here.
admin.site.register(Workflow, WorkflowAdmin)

class CatalogTypeCommercialAdmin(admin.ModelAdmin):

    form = CatalogTypeCommercialForm
    list_display = ('id','level','id_AP','nature','alias','parent_type','chk_dom','jour_dom','code_oper','code_nature')
    list_filter = [
        'level','nature',
    ]
# Register your models here.
admin.site.register(CatalogTypeCommercial, CatalogTypeCommercialAdmin)

class CatalogTypeFileAdmin(admin.ModelAdmin):
    list_display = ('id','category_l1','category_l2','content_type', )

    list_filter = [
        ('content_type',admin.RelatedOnlyFieldListFilter),
    ]
# Register your models here.
admin.site.register(CatalogTypeFile, CatalogTypeFileAdmin)

class CatalogTypeTiersAdmin(admin.ModelAdmin):
    list_display = ('id','content_type','category_l1','category_l2',)
    list_filter = [
        'category_l1',
        ('content_type',admin.RelatedOnlyFieldListFilter),
    ]
# Register your models here.
admin.site.register(CatalogTypeTiers, CatalogTypeTiersAdmin)

class CatalogTypeActivityAdmin(admin.ModelAdmin):
    list_display = ('id','category_l1','alias')
    list_filter = [
        'category_l1',
    ]
# Register your models here.
admin.site.register(CatalogTypeActivity, CatalogTypeActivityAdmin)

class CatalogTypeProductAdmin(admin.ModelAdmin):
        
    form = CatalogTypeProductForm

    list_display = ('id','code_product','category_l1','category_l2','category_act','content_type','child_type')
    list_filter = [
        ('content_type',admin.RelatedOnlyFieldListFilter),
    ]
# Register your models here.
admin.site.register(CatalogTypeProduct, CatalogTypeProductAdmin)