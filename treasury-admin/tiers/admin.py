# -*- coding: utf-8 -*-


from django.contrib import admin
from django_extensions.admin import ForeignKeyAutocompleteAdmin

from util.workflow.models import Statut
#
from .client.models import *
from .corresp.models import *
from .cpty.models import *
from .depo.models import *
#
from .forms import ClientCtrlForm, ClientFileStorageForm, TiersForm, CorrespForm
from .inlines import *
from django.utils import timezone
from django.http import HttpResponseRedirect
from django.template import Template, Context
from django.template.response import TemplateResponse
#
    
class ClientFileStorageAdmin(admin.ModelAdmin):
    
    form = ClientFileStorageForm

    list_display = ('id','client','type_file','file_name','modified')    
    
    list_filter = [
        ('type_file',admin.RelatedOnlyFieldListFilter),
        ('content_type',admin.RelatedOnlyFieldListFilter),
    ]
    search_fields = ['client__ref_id',  
                     'client__alias',
                     'client__fullname',
                     ]
    fieldsets = (    
        ('Front Office', {
            'fields': ('content_type','object_id','oper','client','file_name','type_file','created','modified','file',) 
            }),           
    )

    def get_readonly_fields(self, request, obj=None): 
            
        readonly_fields = list(set([f.name for f in obj._meta.fields])) 
        
        def is_dmf(user):
            return user.groups.filter(name='DMF').exists()
        
        if is_dmf(request.user) or request.user.is_superuser:
            fields_excl = ['client','file','file_name','type_file',]
            for field in fields_excl:
                if field in readonly_fields:
                    readonly_fields.remove(field)

        self.readonly_fields = readonly_fields
        return self.readonly_fields  

    def get_changeform_initial_data(self, request):
        return {'oper': request.user}    

    #authorization filter
    def get_queryset(self, request):

        def is_dmf(user):
            return user.groups.filter(name='DMF').exists()

        def has_grp_view(user):
            return user.groups.filter(name='ctrl_has_grp_view').exists()
        qs = super(ClientFileStorageAdmin, self).get_queryset(request)

        #if has controler priority
        if is_dmf(request.user):
            return qs
        elif has_grp_view(request.user):
            user_groups = request.user.groups.values_list('id')
            crews = User.objects.filter(groups__id__in = user_groups)
            return qs.filter(oper__in=crews) 
        return qs.filter(oper=request.user)  

    def has_delete_permission(self, request, obj=None):

        if request.user.is_superuser:
            return True
        #if a file has already been uploaded then ordinary user can not delete record
        elif obj and obj.file: 
            return False

        return super(ClientFileStorageAdmin, self).has_delete_permission(request, obj=obj)  

# Register your models here.
admin.site.register(ClientFileStorage, ClientFileStorageAdmin)


#choose email Template
from notification.models import EmailTemplate,EmailCtrl
from django.shortcuts import render
from django.template.loader import render_to_string
import datetime, time

class ClientCtrlAdmin(admin.ModelAdmin):
    
    form = ClientCtrlForm

    inlines = [
        #
        ClientFileStorageInline,
    ]

    list_display = ('id','ref_id','fullname','alias','oper','type_client','chk_actif',)    
    list_filter = [
        ('type_client',admin.RelatedOnlyFieldListFilter),
        ]
    search_fields = ['ref_id',  
                     'alias',
                     'fullname',
                     ]
    fieldsets = (    
        ('Front Office', {
            'fields': ('ref_id','type_client','fullname','alias','niu','email',
                        'oper','date_profil','date_val','chk_actif','obs') 
            }),           
        ('Profil Control', {
            'fields': ('chk_corresp',
                       'chk_cpty',
                       'chk_depo',) 
            }),           
    )

    def get_readonly_fields(self, request, obj=None):
        
        #readonly_fields = list(set([f.name for f in obj._meta.fields])) 
      
        if not request.user.is_superuser:
            self.readonly_fields = ['ref_id','fullname','chk_actif',]
        else:
            self.readonly_fields = []
        
        return self.readonly_fields 

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(ClientCtrlAdmin, self).get_form(request, obj, **kwargs)

    def save_formset(self, request, form, formset, change):
        if formset.model != ClientFileStorage:
            return super(ClientCtrlAdmin, self).save_formset(request, form, formset, change)
        
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                #
                parent_ctype = ContentType.objects.get_for_model(instance.client)
                parent_id = instance.client.id
                #parent_obj = ClientCtrl.objects.get(pk=parent_id)
                instance.oper = request.user
                instance.object_id = parent_id
                instance.content_type = parent_ctype
            instance.save()
        formset.save_m2m()

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return False
        else:
            return True
        return super(ClientCtrlAdmin, self).has_delete_permission(request, obj=obj)  

    def get_actions(self, request):
        actions = super(ClientCtrlAdmin, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions

    class email_template_form(forms.forms.Form):    
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)    
        email_template = forms.ModelChoiceField(EmailTemplate.objects.filter(chk_approv=True))


    def genr_email(modeladmin, request, queryset):  
        
        batch_no = 'GENR_' + datetime.date.today().strftime("%Y%m%d") + time.strftime("%H%M%S", time.localtime())        

        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Generate Email Interface File Cancelled')    
            return  

        elif 'email_template' in request.POST:    
            form = modeladmin.email_template_form(request.POST) 

            if form.is_valid():      
                email_template = form.cleaned_data['email_template']
                ctype = ContentType.objects.get_for_model(ClientCtrl, for_concrete_model=True)
                ctype_email = ContentType.objects.get_for_model(EmailCtrl, for_concrete_model=True)
                statut = Statut.objects.get(content_type=ctype_email, statut='/ATTN')

                #action section      
                for case in queryset:        
                    #create email records
                    obj, created = EmailCtrl.objects.get_or_create(
                        object_id = case.id,
                        content_type = ctype,
                        template = email_template,
                    )
                    obj.statut = statut
                    obj.client = case     
                    obj.to_email = case.email
                    obj.from_email = email_template.from_email
                    obj.cc_email = email_template.cc_email 
                    obj.subject = email_template.subject
                    #
                    obj.chk_verify = True
                    obj.oper_verify = request.user
                    obj.time_verify = timezone.now()
                    obj.batch_no = batch_no
                    
                    #text template
                    if email_template.template_type == 1:
                        body = email_template.body
                    elif email_template.template_type == 2: 
                        temp = Template(email_template.body)
                        context = Context({   
                                "cli_fullname": case.fullname,
                                "cli_code": case.ref_id,
                        })
                        body = str(temp.render(context))
                    else:
                        body = None
                
                    obj.body = body
                    obj.save()

                modeladmin.message_user(request, "<Batch #%s> %s Successfully generated please check file." %(batch_no, queryset.count()))    


                return HttpResponseRedirect('/admin/notification/emailctrl/?batch_no=%s' % batch_no)
            else:      
                messages.warning(request, u"Please choose email template")      
                form = None   

        if not form:    
            form  = modeladmin.email_template_form(initial={'_selected_action': 
                queryset.values_list('id',flat=True)}
                )  

            return render(request,'custom//batch_update.html',
                {   'objs': queryset, 
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'genr_email', 
                    'title': u'Generate email interface file',
                    'batch_no': batch_no
                })

    genr_email.short_description = u'Genr Email'
    actions = [genr_email]



# Register your models here.
admin.site.register(ClientCtrl, ClientCtrlAdmin)
    
class CorrespAdmin(admin.ModelAdmin):

    form = CorrespForm
    
    inlines = [ AccounCorresptInline, ]    
    list_display = ('id','chk_active','alias','type_tiers','clientCtrl','swift')    
    list_filter = ['type_tiers','chk_active',]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(CorrespAdmin, self).get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return False
        else:
            return True
        return super(CorrespAdmin, self).has_delete_permission(request, obj=obj)  

# Register your models here.
admin.site.register(Corresp, CorrespAdmin)


class CptyAdmin(admin.ModelAdmin):
    form = CorrespForm
       
    list_display = ('id','alias','type_tiers','clientCtrl','swift')    
    list_filter = ['type_tiers',]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(CptyAdmin, self).get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return False
        else:
            return True
        return super(CptyAdmin, self).has_delete_permission(request, obj=obj)  
# Register your models here.
admin.site.register(Cpty, CptyAdmin)
    
class DepoAdmin(admin.ModelAdmin):

    form = TiersForm
    
    inlines = [ AccounDepotInline, ]    
    list_display = ('id','alias','type_tiers','clientCtrl','swift')    
    list_filter = ['type_tiers',]

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(DepoAdmin, self).get_form(request, obj, **kwargs)

    def has_delete_permission(self, request, obj=None):
        if not request.user.is_superuser and obj:
            return False
        else:
            return True  
        return super(DepoAdmin, self).has_delete_permission(request, obj=obj)  
# Register your models here.
admin.site.register(Depo, DepoAdmin)