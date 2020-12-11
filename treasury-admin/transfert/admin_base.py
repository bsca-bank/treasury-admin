# -*- coding: utf-8 -*-

from datetime import date, timedelta
from django.contrib import admin
#reverse link
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db.models import Q
#
from import_export.admin import ImportMixin
from django_extensions.admin import ForeignKeyAutocompleteAdmin
#
from treasury.models import FXCli
from util.workflow.models import Statut

from cashflow.inlines import CashFlowDetailInline, CashFlowDetailInfoPlusInline
from treasury.inlines import FXCliInline
from tiers.inlines import ClientFileStorageInline, ClientFileStorageGenericInline
#
#choose email Template
from django.http import HttpResponseRedirect
from django.template import Context, Template
from django.template.response import TemplateResponse
#
from django.urls import include, path   
#
from notification.models import EmailTemplate,EmailCtrl
from django.shortcuts import render
from django.template.loader import render_to_string
import datetime, time
#
from .resource import *
from .forms import *
from .signals import *
from .inlines import *
from .filter import *
#
class TrfDossierExecAdminBase(ForeignKeyAutocompleteAdmin): 
    form = TrfDossierExecForm
    #

    inlines = [CashFlowDetailInline, ClientFileStorageGenericInline]

    #resource_class = TrfDossierExecRsrc
    
    search_fields = ['id','ref_id','donneur','benef', \
        'trfDossier__oper_input__last_name', \
        'trfDossier__client__ref_id','trfDossier__client__alias','trfDossier__client__fullname',
        'montant']
    #
    def trfDossier_link(self,TrfDossierExec):
        url=''
        if not TrfDossierExec.trfDossier:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            if TrfDossierExec.nature == 'TRF':
                url = reverse("admin:transfert_trfdossierctrlproxy_change", args=[TrfDossierExec.trfDossier.id])
            if TrfDossierExec.nature == 'RPT':
                url = reverse("admin:transfert_rptdossierctrlproxy_change", args=[TrfDossierExec.trfDossier.id])
            link='<a href="%s">%s</a>'%(url,TrfDossierExec.trfDossier.id)
            return mark_safe(link)
    trfDossier_link.short_description = "TRFCTRL"
      
    def client_link(self,TrfDossierExec):
        url=''
        if not TrfDossierExec.trfDossier:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:tiers_clientctrl_change", args=[TrfDossierExec.trfDossier.client.id])
            link='<a href="%s">%s</a>'%(url,TrfDossierExec.trfDossier.client.ref_id)
            return mark_safe(link)
    client_link.short_description = "Client"

    def dossier_dom_link(self, TrfDossierExec):
        url=''
        if not TrfDossierExec.trfDossier:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            raw_id = TrfDossierExec.trfDossier.id
            trfDossier = TrfDossierCtrl.objects.filter(pk=raw_id)
            #print(trfDossier.id)
            if trfDossier:
                link_id = trfDossier.values_list('dossier_dom', flat=True)[0]
                ref_id = link_id or ''           
                #print(link_id)
            url = reverse("admin:transfert_domdossierctrl_change", args=[link_id])
            link='<a href="%s">%s</a>'%(url,ref_id)
            return mark_safe(link)
    dossier_dom_link.short_description = "DOM"

    def get_dom_dossier(self, obj):
        if obj.trfDossier:
            return obj.trfDossier.dossier_dom
        else:
            return None
    get_dom_dossier.short_description = "Dom"

    def get_oper_input(self, obj):
        if obj.trfDossier:
            first_name = obj.trfDossier.oper_input.first_name[0:1]
            last_name = obj.trfDossier.oper_input.last_name[0:6]
            return str(first_name + '.' + last_name)
        else:
            return None
    get_oper_input.short_description = "Agent"

    def get_trf_nomenc(self, obj):
        if obj.trfDossier:
            return obj.trfDossier.nomenc_lv0.nature
        else:
            return None
    get_trf_nomenc.short_description = "Nomenc"

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(TrfDossierExecAdminBase, self).get_form(request, obj, **kwargs)

    #authorization filter
    def get_queryset(self, request):

        def is_dmf(user):
            return user.groups.filter(name='DMF').exists()
        def has_grp_view(user):
            return user.groups.filter(name='ctrl_has_grp_view').exists()
        #need to modify when copy-paste
        qs = super(TrfDossierExecAdminBase, self).get_queryset(request)

        #if has controler priority
        if is_dmf(request.user):
            return qs
        elif has_grp_view(request.user):
            user_groups = request.user.groups.values_list('id')
            crews = User.objects.filter(groups__id__in = user_groups)
            return qs.exclude(trfDossier__isnull=True) \
                .filter(trfDossier__oper_input__in=crews) 
        return qs.exclude(trfDossier__isnull=True) \
            .filter(trfDossier__oper_input=request.user)  
    #actions
    #----------------------------------------------------------------------
    def get_actions(self, request):
        actions = super(TrfDossierExecAdminBase, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions    

    def chk_ctrl(modeladmin, request, queryset):
        ctrl = queryset.values_list('ctrl', flat=True)
        #date = request.POST['date']
        if request.user.is_superuser:
            if not ctrl[0]:
                queryset.update(ctrl=True)
            else:
                queryset.update(ctrl=False)
        #modeladmin.message_user(request, ("Successfully updated statut for %d rows") % (queryset.count(),), messages.SUCCESS)
    chk_ctrl.short_description = "Check/Uncheck Ctrl" 

    def export_csv(self, request, queryset): #modeladmin, 
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=Bkdopi.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"id"),
            smart_str(u"nature"),
            smart_str(u"statut_exec"),
            smart_str(u"ref_id"),
            smart_str(u"donneur"),
            smart_str(u"accDonneur"),
            smart_str(u"benef"),
            smart_str(u"accBenef"),            
            smart_str(u"date_exec"),
            smart_str(u"ccy_code"),
            smart_str(u"montant"),
            smart_str(u"fxRate"),
            smart_str(u"montant_xaf"),
            #
            smart_str(u"agent"),
            smart_str(u"client"),
            smart_str(u"chk_fund"),
            smart_str(u"statut"),
            smart_str(u"nomenc_lv0"),  
            smart_str(u"nomenc_lv1"),  
            #
            smart_str(u"trfDossierCouvr"),
            smart_str(u"dateCouvr"),
        ])
        
        for obj in queryset:

            basic_data = [
                smart_str(obj.pk),
                smart_str(obj.nature),
                smart_str(obj.statut_sys),
                smart_str(obj.ref_id),
                smart_str(obj.donneur),
                smart_str(obj.accDonneur),
                smart_str(obj.benef),
                smart_str(obj.accBenef),
                smart_str(obj.date_exec),
                smart_str(obj.ccy_code),                
                smart_str(obj.montant),
                smart_str(obj.fxRate),
                smart_str(obj.montant_xaf),
            ]
            #-------------------------------------------------------------------------
            if obj.trfDossier:
                trfDossier = [
                    obj.trfDossier.oper_input,
                    obj.trfDossier.client,
                    obj.trfDossier.chk_fund,
                    obj.trfDossier.statut,
                    obj.trfDossier.nomenc_lv0,
                    obj.trfDossier.nomenc_lv1,                    
                              ]
            else:
                trfDossier = ["","","","","","",] 
            #-------------------------------------------------------------------------
            if obj.trfDossierCouvr:
                trfDossierCouvr = [
                    smart_str(obj.trfDossierCouvr.ref_id),
                    smart_str(obj.trfDossierCouvr.date_couvr)
            ]
            else:
                trfDossierCouvr = ["","",]         
            
            writer.writerow(basic_data + trfDossier + trfDossierCouvr) # 
              
        return response
    export_csv.short_description = u"Export CSV"    

    actions = [export_csv, chk_ctrl]    

class TrfDossierCouvrAdminBase(admin.ModelAdmin):
    
    def get_oper_input(self, obj):
        if obj.oper_input:
            first_name = obj.oper_input.first_name[0:1]
            last_name = obj.oper_input.last_name[0:6]
            return str(first_name + '.' + last_name)
        else:
            return None
    get_oper_input.short_description = "Agent"

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        #print(request._obj_)
        return super(TrfDossierCouvrAdminBase, self).get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        
        # if not obj.type_product:
        #     ctype = ContentType.objects.get_for_model(obj, for_concrete_model=False)

        #     #chose main type product without child type
        #     q_parent_type = Q(content_type=ctype)
        #     q_child = Q(child_type__isnull=True)

        #     obj.type_product = CatalogTypeProduct.objects.get(q_parent_type, q_child)

        if not obj.date_trd:
            obj.date_trd = date.today()
            obj.year_trd = obj.date_trd.year

        if not obj.year_trd:
            obj.year_trd = obj.date_trd.year

        if not obj.oper_input:
            obj.oper_input = request.user
            
       #ctype = ContentType.objects.get_for_model(obj, for_concrete_model=False)

        #update oper_verify
        if obj.chk_verify:

            if not obj.oper_verify: 
                obj.oper_verify = request.user 

            if not obj.montant_payment:
                obj.montant_payment = obj.montant_out
           
            if not obj.montant_couvr:
                obj.montant_couvr = obj.montant_in
    
            if not obj.oper_approv:  
                obj.oper_approv = request.user 

        obj.save() 


    def save_formset(self, request, form, formset, change):
        if formset.model not in [ClientFileStorage]:
            return super(TrfDossierCouvrAdminBase, self).save_formset(request, form, formset, change)
        
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                if formset.model == ClientFileStorage:
                    instance.oper = request.user
                #
            instance.save()
        formset.save_m2m()

    def get_readonly_fields(self, request, obj=None): 

        readonly_fields = [ 'oper_input',
                            'oper_verify','time_verify',
                            'oper_approv','time_approv','nb_jours',]

        if request.user.is_superuser:
            readonly_fields = ['oper_verify','time_verify','oper_approv','time_approv','nb_jours',]

        self.readonly_fields = readonly_fields 

        return self.readonly_fields  

    #actions
    #----------------------------------------------------------------------
    def get_actions(self, request):
        actions = super(TrfDossierCouvrAdminBase, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions    

    def export_csv_eod(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today +"_"+ str(request.user) + '.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)

        writer.writerow([
            smart_str(u"id"),
            smart_str(u"oper_input"),
            smart_str(u"date_emis"),
            smart_str(u"nb_jours"),
            smart_str(u"statut"),
            smart_str(u"ref_id"),
            smart_str(u"client"),
            smart_str(u"corresp_in"),
            smart_str(u"account_in"), 
            smart_str(u"montant_in"),   
            smart_str(u"ccy_in"),
            smart_str(u"montant_out"),
            smart_str(u"ccy_out"),
            smart_str(u"date_trd"),
            smart_str(u"date_acc"),
            smart_str(u"date_pay"),   
            smart_str(u"date_couvr"),  
            smart_str(u"date_commission"),   
            smart_str(u"time_approv"),  
            smart_str(u"obs"),
        ])
        
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.oper_input),
                smart_str(obj.time_verify.date()),
                smart_str(""),
                smart_str(obj.statut),
                smart_str(obj.ref_id),
                smart_str(obj.client.fullname),
                smart_str(obj.corresp_in),
                smart_str(obj.account_in),
                smart_str(obj.montant_in),
                smart_str(obj.ccy_in),
                smart_str(obj.montant_out),
                smart_str(obj.ccy_out),
                smart_str(obj.date_trd),
                smart_str(obj.date_acc),
                smart_str(obj.date_val),
                smart_str(obj.date_couvr),            
                smart_str(obj.date_commission),
                smart_str(obj.time_approv),
                smart_str(obj.obs),
            ])
        return response
    export_csv_eod.short_description = u"Export Rapport CSV"    

    #
    class email_template_form(forms.forms.Form):    
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
        #
        ctype = ContentType.objects.get_for_model(TrfDossierCouvr, for_concrete_model=True)    
        email_template = forms.ModelChoiceField(
            EmailTemplate.objects.filter(
                chk_approv=True,
                content_type=ctype)
                )

    #generate email template
    def genr_email(modeladmin, request, queryset):  
        
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        batch_no = 'GENR_' + today + time.strftime("%H%M%S", time.localtime())        

        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Generate Email Interface File Cancelled')    
            return  

        elif 'email_template' in request.POST:    
            form = modeladmin.email_template_form(request.POST) 

            if form.is_valid():      
                email_template = form.cleaned_data['email_template']
                ctype = ContentType.objects.get_for_model(TrfDossierCouvr, for_concrete_model=True)
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
                    obj.client = case.client     
                    obj.to_email = case.client.email
                    obj.from_email = email_template.from_email
                    obj.cc_email = email_template.cc_email 
                    #
                    if obj.subject == 1:
                        obj.subject = email_template.subject
                    else:
                        template = Template(email_template.subject)
                        context = Context({"cli_code": case.client.ref_id})
                        obj.subject = template.render(context)
                    #
                    obj.chk_verify = True
                    obj.oper_verify = request.user
                    obj.time_verify = timezone.now()
                    obj.batch_no = batch_no

                    #
                    body = render_to_string('notification/'+ email_template.template_key + '.html',
                        {   
                            "type_operation": email_template.type_operation,
                            "type_action": email_template.type_action,
                            "ccy": case.ccy_in.iso,
                            "montant": case.montant_in, 
                            "date_val": case.date_val,
                            "cli_fullname": case.client.fullname,
                            "cli_code": case.client.ref_id,
                            "date_notif": timezone.now().date,
                            #"trf_id":case.id,
                            #"beac_id":beac_id,
                        })
                    obj.body = body
                    obj.save()

                #update link
                queryset.update(chk_notify=True, batch_no=batch_no, message=obj, template_key=email_template.template_key)
                #
                modeladmin.message_user(request, "<Batch #%s> %s Successfully generated please check file." %(batch_no, queryset.count()))    
                #url = reverse('/', kwargs={'batch_no': batch_no})
                #return HttpResponseRedirect(url)
                return HttpResponseRedirect('/admin/notification/emailctrl/?batch_no=%s' % batch_no)
            else:      
                messages.warning(request, u"Please choose email template")      
                form = None   

        if not form:    
            form  = modeladmin.email_template_form(
                initial={'_selected_action': 
                queryset.values_list('id',flat=True)
                #request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                })  

            return render(request,'custom//batch_update.html',
                {   'objs': queryset, 
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'genr_email', 
                    'title': u'Generate email interface file',
                    'batch_no': batch_no
                })

    genr_email.short_description = u'Genr Email'

    actions = [genr_email, export_csv_eod ]

class TrfDossierCtrlAdminBase(ForeignKeyAutocompleteAdmin):    
    
    def get_agent(self, obj):
        if obj.client.oper:
            first_name = obj.client.oper.first_name[0:1]
            last_name = obj.client.oper.last_name[0:6]
            return str(first_name + '.' + last_name)
        else:
            return "#N/A"
    get_agent.short_description = "Agent"
    #
    def get_benef(self, obj):
        if obj.cpty:
            benef = obj.cpty[0:10]
            return str(benef)
        else:
            return None
    get_benef.short_description = "Cpty"
    #
    def get_oper_input(self, obj):
        if obj.oper_input:
            first_name = obj.oper_input.first_name[0:1]
            last_name = obj.oper_input.last_name[0:6]
            return str(first_name + '.' + last_name)
        else:
            return None
    get_oper_input.short_description = "Agent"
    #
    def client_link(self,TrfDossierCtrl):
        url=''
        if not TrfDossierCtrl.client:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:tiers_clientctrl_change", args=[TrfDossierCtrl.client.id])
            link='<a href="%s">%s</a>'%(url,TrfDossierCtrl.client.ref_id)
            return mark_safe(link)
    client_link.short_description = "Client"
    #
    def dossier_dom_link(self, TrfDossierCtrl):
        url=''
        if not TrfDossierCtrl.dossier_dom:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:transfert_domdossierctrl_change", args=[TrfDossierCtrl.dossier_dom.id])
            link='<a href="%s">%s</a>'%(url,TrfDossierCtrl.dossier_dom.ref_di)
            return mark_safe(link)
    dossier_dom_link.short_description = "DOM"
    #
    def bkdopi_link(self, TrfDossierCtrl):
        url=''
        if not TrfDossierCtrl.bkdopi:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:transfert_trfdossierexec_change", args=[TrfDossierCtrl.bkdopi.id])
            link='<a href="%s">%s</a>'%(url,TrfDossierCtrl.bkdopi.ref_id)
            return mark_safe(link)
    bkdopi_link.short_description = "Bkdopi"

    def get_exec_pct(self, obj):
        if obj.dossier_dom:
            return str(obj.dossier_dom.exec_pct)
        else:
            return None
    get_exec_pct.short_description = "exec_pct"

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(TrfDossierCtrlAdminBase, self).get_form(request, obj, **kwargs)

    #authorization filter
    def get_queryset(self, request):
        #TrfDossierCtrlAdminBase, self
        qs = super(TrfDossierCtrlAdminBase, self).get_queryset(request)

        ctype = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        
        qs = qs.filter(type_product__content_type__id__exact=ctype.id)  

        def has_global_view(user):
            #group can see all transactions
            return user.groups.filter(name='ctrl_has_global_view').exists()

        def has_grp_view(user):
            #group can see transactions of the same group
            return user.groups.filter(name='ctrl_has_grp_view').exists()

        #if has controler priority
        if request.user.is_superuser or has_global_view(request.user) :
            return qs
        
        # elif has_grp_view(request.user):
        #     user_groups = request.user.groups.values_list('id')
        #     crews = User.objects.filter(groups__id__in = user_groups)
        #     return qs.filter(oper_input__in=crews) 
        else:
            q_nchk_approv = Q(chk_approv=False)
            q_nchk_pay = Q(chk_pay=False)
            return qs.filter(q_nchk_pay|q_nchk_pay)  

    def save_model(self, request, obj, form, change):

        if not obj.type_product_id:
            ctype = ContentType.objects.get_for_model(obj, for_concrete_model=False)    
            #chose main type product without child type
            q_parent_type = Q(content_type=ctype)
            q_child = Q(child_type__isnull=True)
            type_product = CatalogTypeProduct.objects.get(q_parent_type, q_child)

            obj.type_product_id = type_product.id
        
        if not obj.oper_input_id:
            obj.oper_input_id = request.user.id
        
        if not obj.oper_recv and obj.chk_recv:
            obj.oper_recv = request.user

        if not obj.oper_verify and obj.chk_verify:  
            obj.oper_verify = request.user 

        if not obj.oper_approv and obj.chk_approv: 
            obj.oper_approv = request.user
        
        if not obj.oper_fund and obj.chk_fund: 
            obj.oper_fund = request.user

        #update date_val automatically
        if obj.chk_pay and obj.date_val is None:    
            obj.date_val = date.today()  

        #update date_val automatically
        ctype = ContentType.objects.get_for_model(TrfDossierCtrl, for_concrete_model=True)
        statut = Statut.objects.get(content_type=ctype, statut='/ATTN')   
        if not obj.statut:    
            obj.statut = statut

        #update bkdopi, only allows one direction update
        if obj.bkdopi:    
            link_id = obj.pk 

            #check inconsistency,bkdopi is a query set not an object
            bkdopi = TrfDossierExec.objects.filter(pk=obj.bkdopi.id, statut_sys='FO')
            #print("DEBUG " + str(bkdopi))
            if bkdopi and bkdopi.values_list('trfDossier', flat=True)[0] != link_id:
                bkdopi.update(trfDossier_id = link_id) 
                bkdopi.update(ctrl = True)

        obj.save()

    def save_formset(self, request, form, formset, change):
        if formset.model not in [ClientFileStorage, FXCli, DomDossierMulti]:
            return super(TrfDossierCtrlAdminBase, self).save_formset(request, form, formset, change)
    
        #pass parent value to child 
        instances = formset.save(commit=False)
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                #
                if formset.model == FXCli:
                    parent_id = instance.object_id
                    parent_obj = TrfDossierCtrl.objects.get(pk=parent_id)
                    instance.client = parent_obj.client
                    instance.oper_verify = request.user
                    instance.ccy_out = parent_obj.ccy
                    instance.montant_out = parent_obj.montant 
                #
                if formset.model == ClientFileStorage:
                    instance.oper = request.user

            instance.save()
        formset.save_m2m()

    def get_readonly_fields(self, request, obj=None):

        readonly_fields = [ 'type_product',
                            'oper_input','oper_recv','oper_verify','oper_approv','oper_fund','type_dcc','chk_dcc','oper_dcc','time_dcc','obs_dcc',
                            'created','time_recv','time_verify','time_approv','nb_jours',]
        
        if request.user.is_superuser:
            readonly_fields = ['oper_input','oper_recv','oper_verify','oper_approv','oper_fund','type_dcc','chk_dcc','oper_dcc','time_dcc','obs_dcc',
                            'created','time_recv','time_verify','time_approv','nb_jours',]

        fields_excl = []

        if obj:
            readonly_all_fields = list(set([f.name for f in obj._meta.fields]))
        else:
            readonly_all_fields = readonly_fields

        #remove readonly lock accoring to department
        for field in fields_excl:
            if field in readonly_fields:
                readonly_fields.remove(field)

        self.readonly_fields = readonly_fields

        return self.readonly_fields  

    #actions
    #----------------------------------------------------------------------
    def get_actions(self, request):
        actions = super(TrfDossierCtrlAdminBase, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions    

    class email_template_form(forms.forms.Form):    
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput) 
        
        ctype = ContentType.objects.get_for_model(TrfDossierCtrl, for_concrete_model=True)       
        email_template = forms.ModelChoiceField(
            EmailTemplate.objects.filter(
                chk_approv=True,
                content_type=ctype)
                )

    #generate email template
    def genr_email(modeladmin, request, queryset):  
        
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        batch_no = 'GENR_' + today + time.strftime("%H%M%S", time.localtime())        

        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Generate Email Interface File Cancelled')    
            return  

        elif 'email_template' in request.POST:    
            form = modeladmin.email_template_form(request.POST) 

            if form.is_valid():      
                email_template = form.cleaned_data['email_template']
                ctype = ContentType.objects.get_for_model(TrfDossierCtrl, for_concrete_model=True)
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
                    obj.client = case.client     
                    obj.to_email = case.client.email
                    obj.from_email = email_template.from_email
                    obj.cc_email = email_template.cc_email 
                    #
                    if obj.subject == 1:
                        obj.subject = email_template.subject
                    else:
                        template = Template(email_template.subject)
                        context = Context({"cli_code": case.client.ref_id})
                        obj.subject = template.render(context)
                    #
                    obj.chk_verify = True
                    obj.oper_verify = request.user
                    obj.time_verify = timezone.now()
                    obj.batch_no = batch_no

                    if case.dossier_dom:
                        ref_dom = case.dossier_dom.id
                        ref_di = case.dossier_dom.ref_di
                    else:
                        ref_dom = None
                        ref_di = None

                    if case.bkdopi:
                        ref_exec = case.bkdopi
                    else:
                        ref_exec = None
                    
                    if case.dossier_couvr:
                        beac_id = case.dossier_couvr.ref_id
                    else:
                        beac_id = None

                    #
                    body = render_to_string('notification/'+ email_template.template_key + '.html',
                        {   
                            "type_operation": email_template.type_operation,
                            "type_action": email_template.type_action,
                            "nomenc": case.nomenc_lv0,
                            "ref_exec": ref_exec,
                            "ccy": case.ccy.iso,
                            "montant": case.montant, 
                            #"date_val": case.date_val,
                            "ref_di": ref_di,
                            "cli_fullname": case.client.fullname,
                            "cli_code": case.client.ref_id,
                            "date_notif": timezone.now().date,
                            "dom_id":ref_dom,
                            "trf_id":case.id,
                            "couvr_id":beac_id,
                            "obs": case.obs
                        })
                    obj.body = body
                    obj.save()

                #update link
                queryset.update(chk_notify=True, batch_no=batch_no, message=obj, template_key=email_template.template_key)
                #
                modeladmin.message_user(request, "<Batch #%s> %s Successfully generated please check file." %(batch_no, queryset.count()))    
                #url = reverse('/', kwargs={'batch_no': batch_no})
                #return HttpResponseRedirect(url)
                return HttpResponseRedirect('/admin/notification/emailctrl/?batch_no=%s' % batch_no)
            else:      
                messages.warning(request, u"Please choose email template")      
                form = None   

        if not form:    
            form  = modeladmin.email_template_form(
                initial={'_selected_action': 
                queryset.values_list('id',flat=True)
                #request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                })  

            return render(request,'custom//batch_update.html',
                {   'objs': queryset, 
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'genr_email', 
                    'title': u'Generate email interface file',
                    'batch_no': batch_no
                })

    genr_email.short_description = u'Genr Email'

    #
    def export_rpt_DFX2201(self, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today + '_rpt_DFX2201.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"ref_ordre"),       
            smart_str(u"date_ordre"),
            smart_str(u"date_val"),
            smart_str(u"ref_swift"),
            smart_str(u"donneur"),
            smart_str(u"benef"),
            smart_str(u"object"),
            smart_str(u"ref_dom"),
            smart_str(u"corresp"),
            smart_str(u"devise"),
            smart_str(u"montant"),
        ])
        for obj in queryset:

            str_ref_ordre = obj.pk

            #
            if obj.time_verify:
                str_date_ordre = obj.time_verify.date()
            else:
                str_date_ordre ="N/A"
            
            #date_val
            if obj.time_approv:
                str_date_val = obj.time_approv.date()
            else:
                str_date_val ="N/A"
    
            #
            str_ref_swift = obj.ref_swift
            str_donneur = obj.client.fullname
            str_benef = obj.cpty

            #
            if obj.nomenc_lv1:
                str_object = obj.nomenc_lv1.alias
            else:
                str_object ="N/A"

            #ref_dom
            if obj.dossier_dom:
                str_ref_dom = obj.dossier_dom.ref_di
            else:
                str_ref_dom ="N/A"

            #corresp
            if obj.corresp:
                str_corresp = obj.corresp.swift
            else:
                str_corresp ="N/A"

            str_ccy = obj.ccy
            str_montant = obj.montant

            writer.writerow([
                str_ref_ordre,
                str_date_ordre,
                str_date_val,
                str_ref_swift,
                str_donneur,
                str_benef,
                str_object,
                str_ref_dom,
                str_corresp,
                str_ccy,
                str_montant
                         ]) # 

        return response

    export_rpt_DFX2201.short_description = u"Export DFX2201 Report"    

    #--------------------------------------

    actions = [genr_email, export_rpt_DFX2201]

class DomDossierCtrlAdminBase(admin.ModelAdmin):
    #
    #action_form = UpdateTextActionForm  
    form = DomDossierCtrlForm
    #
    def get_ref_decl(self, obj):
        if obj.oper_input:
            ref_decl = obj.ref_di[0:10]
            return str(ref_decl)
        else:
            return None
    get_ref_decl.short_description = "ref_decl"

    def client_link(self, DomDossierCtrl):
        url=''
        if not DomDossierCtrl.client:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:tiers_clientctrl_change", args=[DomDossierCtrl.client.id])
            link='<a href="%s">%s</a>'%(url,DomDossierCtrl.client.ref_id)
            return mark_safe(link)
    client_link.short_description = "Client"
    #
    def get_oper_input(self, obj):
        if obj.oper_input:
            first_name = obj.oper_input.first_name[0:1]
            last_name = obj.oper_input.last_name[0:6]
            return str(first_name + '.' + last_name)
        else:
            return None
    get_oper_input.short_description = "Agent"
    #
    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(DomDossierCtrlAdminBase, self).get_form(request, obj, **kwargs)
    #
    def get_changeform_initial_data(self, request):
        return {
            'code_banque':30020,
            'oper_input':request.user,
        }
    #
    def save_model(self, request, obj, form, change):

        ctype = ContentType.objects.get_for_model(obj, for_concrete_model=True)
        
        #add code_bank
        if not obj.code_banque:
            obj.code_banque = 30020

        if not obj.chk_verify:
            obj.date_ref = None

        #chk users
        if not obj.oper_input: 
            obj.oper_input = request.user 
            
        if not obj.oper_verify and obj.chk_verify: 
            obj.oper_verify = request.user 

        if not obj.oper_approv and obj.chk_approv: 
            obj.oper_approv = request.user

        #update date_limite
        if obj.chk_verify:    
            link_id = obj.pk 
            #print("DEBUG Date_limit: " + str(link_id))
            #check inconsistency,TrfDossierExec is a query set not an object
            try:
                trdDossier = TrfDossierCtrl.objects.filter(dossier_dom=link_id, chk_pay=True)[0] 
                #\.order_by('date_val')
                date_val = trdDossier.date_val
                #end date + 6 month 
                end_date = date_val + timedelta(days=180)    
                #print("DEBUG Date_limit: " + str(end_date))
            except:
                print("Transfert non trouvé")

        obj.save()
    #
    def save_formset(self, request, form, formset, change):
        if formset.model not in [ClientFileStorage]:
            return super(DomDossierCtrlAdminBase, self).save_formset(request, form, formset, change)
        #pass parent value to child 
        instances = formset.save(commit=False)
        
        for instance in instances:
            if not instance.pk and request.user.is_authenticated:
                pass
            instance.save()
        formset.save_m2m()

    #actions
    #----------------------------------------------------------------------
    def get_actions(self, request):
        actions = super(DomDossierCtrlAdminBase, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions    

    def export_csv(modeladmin, request, queryset):
        import csv
        from django.http import HttpResponse
        from django.utils.encoding import smart_str
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = "attachment; filename=" + today + '_rpt_Monthly.csv'
        writer = csv.writer(response, csv.excel)
        response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
        writer.writerow([
            smart_str(u"id"),
            smart_str(u'nature'),
            smart_str(u"date_di"),
            smart_str(u'ref_di'),
            smart_str(u"statut"), 
            smart_str(u"code_client"),
            smart_str(u"client"),      
            smart_str(u"date_val"),
            smart_str(u"devise"),            
            smart_str(u"montant_decl"),
            smart_str(u"montant_pay"),
            smart_str(u"num_dossier"),
            smart_str(u"chk_verify"),
            smart_str(u"ref_dom"), 
            smart_str(u"approv_pct"),
            smart_str(u"exec_pct"),
        ])
        for obj in queryset:
            writer.writerow([
                smart_str(obj.pk),
                smart_str(obj.nomenc_lv0),
                smart_str(obj.date_di),
                smart_str(obj.ref_di),
                smart_str(obj.statut), 
                smart_str(obj.client.ref_id),
                smart_str(obj.client.fullname),
                smart_str(obj.time_verify.date()),
                smart_str(obj.ccy),
                smart_str(obj.montant),
                smart_str(""),
                smart_str(obj.num_exec),
                smart_str(obj.chk_verify),
                smart_str(obj.ref_dom),
                smart_str(obj.approv_pct),
                smart_str(obj.exec_pct),
            ])
        return response

    export_csv.short_description = u"Export CSV"  
    #
    class email_template_form(forms.forms.Form):    
        _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)

        ctype = ContentType.objects.get_for_model(DomDossierCtrl, for_concrete_model=True)        
        email_template = forms.ModelChoiceField(
            EmailTemplate.objects.filter(
                chk_approv=True,
                content_type=ctype)
                )
    #
    #generate email template
    def genr_email(modeladmin, request, queryset):  
        
        import datetime
        today = datetime.date.today().strftime("%Y%m%d") 
        batch_no = 'GENR_' + today + time.strftime("%H%M%S", time.localtime())        

        form = None

        if 'cancel' in request.POST:    
            modeladmin.message_user(request, u'Generate Email Interface File Cancelled')    
            return  

        elif 'email_template' in request.POST:    
            form = modeladmin.email_template_form(request.POST) 

            if form.is_valid():      
                email_template = form.cleaned_data['email_template']
                ctype = ContentType.objects.get_for_model(DomDossierCtrl, for_concrete_model=True)
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
                    obj.client = case.client     
                    obj.to_email = case.client.email
                    obj.from_email = email_template.from_email
                    obj.cc_email = email_template.cc_email 
                    #
                    if obj.subject == 1:
                        obj.subject = email_template.subject
                    else:
                        template = Template(email_template.subject)
                        context = Context({"cli_code": case.client.ref_id})
                        obj.subject = template.render(context)
                    #
                    obj.chk_verify = True
                    obj.oper_verify = request.user
                    obj.time_verify = timezone.now()
                    obj.batch_no = batch_no
                    #
                    body = render_to_string('notification/'+ email_template.template_key + '.html',
                        {   
                            "type_operation": email_template.type_operation,
                            "type_action": email_template.type_action,
                            "nomenc": case.nomenc_lv0,
                            "ccy": case.ccy.iso,
                            "montant": case.montant, 
                            "ref_di": case.ref_di,
                            "cli_fullname": case.client.fullname,
                            "cli_code": case.client.ref_id,
                            "date_notif": timezone.now().date,
                            "dom_id":case.ref_dom,
                        })
                    obj.body = body
                    obj.save()

                #update link
                queryset.update(chk_notify=True, batch_no=batch_no, message=obj, template_key=email_template.template_key)
                #
                modeladmin.message_user(request, "<Batch #%s> %s Successfully generated please check file." %(batch_no, queryset.count()))    
                #url = reverse('/', kwargs={'batch_no': batch_no})
                #return HttpResponseRedirect(url)
                return HttpResponseRedirect('/admin/notification/emailctrl/?batch_no=%s' % batch_no)
            else:      
                messages.warning(request, u"Please choose email template")      
                form = None   

        if not form:    
            form  = modeladmin.email_template_form(
                initial={'_selected_action': 
                queryset.values_list('id',flat=True)
                #request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
                })  

            return render(request,'custom//batch_update.html',
                {   'objs': queryset, 
                    'form': form, 
                    'path':request.get_full_path(), 
                    'action': 'genr_email', 
                    'title': u'Generate email interface file',
                    'batch_no': batch_no
                })

    genr_email.short_description = u'Genr Email'

    actions = [genr_email, export_csv]   

class DomDossierMultiAdminBase(admin.ModelAdmin):

    form = DomDossierMultiForm

    def client_link(self, obj):
        url=''
        if not obj.dossier_trf.client:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:tiers_clientctrl_change", args=[obj.dossier_trf.client.id])
            link='<a href="%s">%s | %s</a>'%(url,obj.dossier_trf.client.ref_id,obj.dossier_trf.client.alias)
            return mark_safe(link)
        client_link.short_description = "Client"

    def dossier_dom_link(self, obj):
        url=''
        if not obj.dossier_dom:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:transfert_domdossierctrl_change", args=[obj.dossier_dom.id])
            link='<a href="%s">%s <%s> | %s</a>'%(url, obj.dossier_dom.id, obj.dossier_dom.statut, 
                                                obj.dossier_dom.ref_di)
            return mark_safe(link)

    dossier_dom_link.short_description = "DOM"

    def payment_link(self, obj):
        url=''
        if not obj.dossier_trf:
            link='<a href="%s">%s</a>'%(url,'')
            return mark_safe(link) 
        else:
            url = reverse("admin:transfert_trfdossierctrlproxy_change", args=[obj.dossier_trf.id])
            link='<a href="%s">%s</a>'%(url, obj.dossier_trf.id)
            return mark_safe(link)
        payment_link.short_description = "Payment"

    def get_type_product(self, obj):
        if obj.dossier_trf:
            return str(obj.dossier_trf.type_product)
        else:
            return None
    get_type_product.short_description = "type_product"

    def get_bkdopi(self, obj):
        if obj.dossier_trf:
            return str(obj.dossier_trf.bkdopi)
        else:
            return None
    get_bkdopi.short_description = "bkdopi"

    def get_ref_swift(self, obj):
        if obj.dossier_trf:
            return str(obj.dossier_trf.ref_swift)
        else:
            return None
    get_ref_swift.short_description = "Ref.Swift"

    #authorization filter
    def get_queryset(self, request):
        #
        qs = super(DomDossierMultiAdminBase, self).get_queryset(request)
        #
        qs = qs.filter(dossier_dom__time_verify__isnull=False)

        def has_global_view(user):
            #group can see all transactions
            return user.groups.filter(name='ctrl_has_global_view').exists()

        def has_grp_view(user):
            #group can see transactions of the same group
            return user.groups.filter(name='ctrl_has_grp_view').exists()

        #if has controler priority
        if request.user.is_superuser or has_global_view(request.user) :
            return qs
        elif has_grp_view(request.user):
            user_groups = request.user.groups.values_list('id')
            crews = User.objects.filter(groups__id__in = user_groups)
            return qs.filter(oper_input__in=crews) 
        else:
            return qs.filter(oper_input=request.user)  

    #actions
    #----------------------------------------------------------------------
    def get_actions(self, request):
        actions = super(DomDossierMultiAdminBase, self).get_actions(request)
        if not request.user.is_superuser:        
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions    
