# -*- coding: utf-8 -*-
from datetime import date, timedelta
#
from django import forms
from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.contenttypes.admin import GenericTabularInline
from django.db.models.functions import Trunc
from django.db.models import Count, Min, Max, Sum, DateField
#
from import_export.admin import ImportExportModelAdmin
#
from tiers.corresp.models import *
from tiers.corresp.models import AccountCorresp
#
from .resource import *
from .forms import *
from .models import *

def get_next_in_date_hierarchy(request, date_hierarchy):
	if date_hierarchy + '__day' in request.GET:
		return 'day'
	if date_hierarchy + '__month' in request.GET:
		return 'day'
	if date_hierarchy + '__year' in request.GET:
		return 'month'
	return 'month'
	
class CashFlowDetailAdmin(ImportExportModelAdmin):
	
	resource_class = CashFlowDetailRsrc
	form = CashFlowDetailForm
	
	inlines = []	
	
	#alter change_list view to enhanced view
	#change_list_template = 'admin/cashflow/change_list.html'     

	list_display = ('id','nature','content_type','date_val','jour_restant','object_id','ref_id','category','account','montant','chk_verify','chk_pay')    
	list_filter = [
		#limit the list_filter choices to the users.
		'nature',
	    'chk_verify','chk_pay',
		('content_type', admin.RelatedOnlyFieldListFilter),
		('corresp', admin.RelatedOnlyFieldListFilter),
		('account', admin.RelatedOnlyFieldListFilter),
	]
	search_fields = ['ref_id',]
	date_hierarchy = 'date_val' 

	def get_form(self, request, obj=None, **kwargs):
		# just save obj reference for future processing in Inline
		request._obj_ = obj
		#print(request._obj_)
		return super(CashFlowDetailAdmin, self).get_form(request, obj, **kwargs)

	def get_readonly_fields(self, request, obj=None):

		def is_dmf(user):
			return user.groups.filter(name='DMF').exists()
			
		fields_dmf = ['nature','corresp','date_val','corresp','account','chk_verify','chk_pay',] 

		self.readonly_fields = ['content_type','object_id',]
		fields_excl = []
		readonly_fields = []
		if obj:
			readonly_fields = list(set([f.name for f in obj._meta.fields]))
			if request.user.is_superuser:
				readonly_fields = ['content_type','object_id',]
			elif is_dmf(request.user):
				fields_excl = fields_dmf 
		else:
			readonly_fields = ['content_type','object_id',]

		#print(fields_excl) 
		#remove readonly lock accoring to department
		for field in fields_excl:
			if field in readonly_fields:
				readonly_fields.remove(field)
				
		#print(readonly_fields)
		#add additional constrain
		if obj and obj.chk_pay:

			readonly_fields = readonly_fields + fields_dmf
			if 'chk_pay' in readonly_fields:
				readonly_fields.remove('chk_pay')

		self.readonly_fields = self.readonly_fields + readonly_fields 

		return self.readonly_fields  

	#actions
	#----------------------------------------------------------------------
	def chk_verify(self, modeladmin, request, queryset):
		#select = request.POST.getlist(admin.ACTION_CHECKBOX_NAME)
		#ct = ContentType.objects.get_for_model(queryset.model)
		statut = queryset.values_list('chk_verify', flat=True)
		if not statut[0]:
			queryset.update(chk_verify=False)
		else:
			queryset.update(chk_verify=True)
		#modeladmin.message_user(request, ("Successfully updated statut for %d rows") % (queryset.count(),), messages.SUCCESS)
	chk_verify.short_description = "Check/Uncheck Verify" 	
	
	def export_csv(self,modeladmin, request, queryset):
		import csv
		from django.http import HttpResponse
		from django.utils.encoding import smart_str
		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename=CashFlowCtrl.csv'
		writer = csv.writer(response, csv.excel)
		response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
		writer.writerow([
			smart_str(u"id"),
			smart_str(u"nature"),
			smart_str(u"content_type"),
			smart_str(u"date_val"),
			smart_str(u"jour_restant"),
			smart_str(u"object_id"),
			smart_str(u"ref_id"),            
			smart_str(u"category"),
			smart_str(u"corresp"),
			smart_str(u"account"),
			smart_str(u"montant"),
			smart_str(u"chk_verify"),
			smart_str(u"chk_pay"),
		])
		for obj in queryset:
			writer.writerow([
				smart_str(obj.pk),
				smart_str(obj.get_nature_display()),
				smart_str(obj.content_type.model),
				smart_str(obj.date_val),
				smart_str(obj.jour_restant()),
				smart_str(obj.object_id),
				smart_str(obj.ref_id),            
				smart_str(obj.category),
				smart_str(obj.corresp),
				smart_str(obj.account.ccy),
				smart_str(obj.montant),
				smart_str(obj.chk_verify),
				smart_str(obj.chk_pay),
			])

		return response

	export_csv.short_description = u"Export CSV"    

	actions = [chk_verify, export_csv]    

# Register your models here.
admin.site.register(CashFlowDetail, CashFlowDetailAdmin)
