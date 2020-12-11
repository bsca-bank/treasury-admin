# -*- coding: utf-8 -*-

from django.contrib import admin
from django import forms
from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render

import xlwt
import datetime, time

#
from .models import EmailCtrl, EmailTemplate
from .filter import ClientFilter, BatchNoFilter

from transfert.models import DomDossierMulti

from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from util.workflow.models import Statut
#
from .forms import EmailForm, EmailTemplateForm

class EmailTemplateAdmin(admin.ModelAdmin):

    form = EmailTemplateForm

    list_display = ['id','template_key','type_operation','type_action','template_type','chk_approv']

    list_filter = [
        'chk_approv',
        ('content_type',admin.RelatedOnlyFieldListFilter),
        'type_operation',#,admin.RelatedOnlyFieldListFilter),
        #('type_action',admin.RelatedOnlyFieldListFilter),
        #('template_type',admin.RelatedOnlyFieldListFilter),
        ]

    fieldsets = (      
        ("Template", {
            #'classes': ('collapse', 'open'),
            'fields': (
                'id',
                'content_type',
                'template_key',
                'type_operation','type_action',
                'from_email','to_email','cc_email',
                'subject_type',
                'subject',
                'body',
                'template_type',
                'int_template',
                'ext_template',
                ),
            }), 
        ("Contrôle de Template", {
            #'classes': ('collapse', 'open'),
            'fields': (
                'chk_approv','oper_approv','time_approv',
                ),
            }),     
    )

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['id','oper_verify','time_verify','oper_approv','time_approv']
        return self.readonly_fields  

# Register your models here.
admin.site.register(EmailTemplate, EmailTemplateAdmin)


class EmailCtrlAdmin(admin.ModelAdmin):

    form = EmailForm

    list_display = ['id','statut','client','object_id','template','chk_verify','time_verify','chk_approv','time_approv']

    date_hierarchy = 'time_approv'

    search_fields = ['batch_no','exp_no','send_no']
    
    list_filter = [
        BatchNoFilter,
        ClientFilter,
        ('content_type', admin.RelatedOnlyFieldListFilter),
        ('statut', admin.RelatedOnlyFieldListFilter),
        ('template', admin.RelatedOnlyFieldListFilter),
        ]

    fieldsets = (      
        ("Contexte de message", {
            #'classes': ('collapse', 'open'),
            'fields': (
                'batch_no',
                'content_type','object_id',
                'statut','client',
                'from_email','to_email','cc_email',
                'subject',
                'body',
                'template'
                ),
            }), 
        ("Contrôle Expédition", {
            #'classes': ('collapse', 'open'),
            'fields': (
                'chk_verify','oper_verify','time_verify',
                'exp_no',
                'chk_approv','oper_approv','time_approv',
                'send_no',
                'obs',
                ),
            }),     
    )

    def get_readonly_fields(self, request, obj=None):
        self.readonly_fields = ['batch_no','exp_no','send_no','content_type','object_id',
                                'oper_verify','time_verify','oper_approv','time_approv']
        return self.readonly_fields  

	#actions
	#----------------------------------------------------------------------

    class popup_confirm_form(forms.forms.Form):    
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)    

    def action_export_email(modeladmin, request, queryset):

        exp_no = 'EXP_' + datetime.date.today().strftime("%Y%m%d") + time.strftime("%H%M%S", time.localtime())
        
        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Generate Email Interface File Cancelled')    
            return  

        elif 'apply' in request.POST: 
            #
            response = HttpResponse(content_type='application/ms-excel')
            response['Content-Disposition'] = 'attachment; filename='+ exp_no +'_email.xls'

            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet(exp_no)

            # Sheet header, first row
            row_num = 0
            #
            font_style = xlwt.XFStyle()
            font_style.font.bold = False

            columns = ['to_email', 'cc_email', 'subject', 'body', ]
            for col_num in range(len(columns)):
                ws.write(row_num, col_num, columns[col_num], font_style)

            # Sheet body, remaining rows
            font_style = xlwt.XFStyle()
            rows = queryset.values_list('to_email', 'cc_email', 'subject', 'body')   
            for row in rows:
                row_num += 1
                for col_num in range(len(row)):
                    ws.write(row_num, col_num, row[col_num], font_style)

            wb.save(response)
            
            #update file
            queryset.update(exp_no=exp_no)
            modeladmin.message_user(request,('<Batch: %s> Interface file successfully generated, please check' % exp_no))
            return response
        
        elif 'return' in request.POST:
            return HttpResponseRedirect('/admin/notification/emailctrl/')
            
        if not form:    
            form  = modeladmin.popup_confirm_form(
                initial={'_selected_action': queryset.values_list('id',flat=True)}
                )  
            return render(request, 'custom/popup_confirm.html', 
                context={
                    'objs':queryset,
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'action_export_email',
                    'batch_no': exp_no
                })

    action_export_email.short_description = u"Export Email"    

    #
    def action_chk_approv(modeladmin, request, queryset):

        ctype = ContentType.objects.get_for_model(EmailCtrl, for_concrete_model=True)
        send_no = 'SENT_' + datetime.date.today().strftime("%Y%m%d") + time.strftime("%H%M%S", time.localtime()) 
        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Operation Cancelled')    
            return
         
        elif 'apply' in request.POST:
            #    
            approv_statut = Statut.objects.get(content_type=ctype, statut='/SENT')
            non_approv_statut = Statut.objects.get(content_type=ctype, statut='/ATTN')

            for obj in queryset:
                obj.chk_approv=True
                obj.oper_approv=request.user
                obj.time_approv=timezone.now()
                obj.statut=approv_statut
                obj.send_no=send_no
                obj.save()

            modeladmin.message_user(request, "<Batch #%s> %s email successfully sent." %(send_no, queryset.count()))    
            return HttpResponseRedirect('/admin/notification/emailctrl/?send_no=%s' % send_no)

        elif 'return' in request.POST:
            return HttpResponseRedirect('/admin/notification/emailctrl/')

        if not form:    
            form  = modeladmin.popup_confirm_form(
                initial={'_selected_action': queryset.values_list('id',flat=True)}
                ) 

            return render(request, 'custom/popup_confirm.html', 
                context={
                    'objs':queryset,
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'action_chk_approv',
                    'batch_no': send_no
                })
    
    action_chk_approv.short_description = "Send Email"

    actions = [action_export_email, action_chk_approv]

# Register your models here.
admin.site.register(EmailCtrl, EmailCtrlAdmin)