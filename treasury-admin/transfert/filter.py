from datetime import datetime
from django.db.models import Q
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datetime import date, timedelta


class InputFilter(admin.SimpleListFilter):
   
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the "all" option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice


class DirectClientFilter(InputFilter):
    title = _("Client Code")
    parameter_name = 'client'
  
    def queryset(self, request, queryset):
        if self.value() is not None:
            client = self.value()
            return queryset.filter(Q(client__ref_id=client)) 

class DirectRefDIFilter(InputFilter):
    title = _("Référence DI")
    parameter_name = 'ref_di'
    def queryset(self, request, queryset):
        if self.value() is not None:
            ref = self.value()
            return queryset.filter(Q(ref_di__contains=ref)) 

class TrfDossierClientFilter(InputFilter):
    title = _("Client Code")
    parameter_name = 'client'
    def queryset(self, request, queryset):
        if self.value() is not None:
            client = self.value()
            return queryset.filter(Q(dossier_trf__client__ref_id=client)) 

class DomDossierRefDIFilter(InputFilter):
    title = _("Référence DI")
    parameter_name = 'ref_di'
    def queryset(self, request, queryset):
        if self.value() is not None:
            ref = self.value()
            return queryset.filter(Q(dossier_dom__ref_di__contains=ref)) 


class OverdueFilter(admin.SimpleListFilter):
   
    title = _("Ctrl. d'Apurement")
    parameter_name = 'date_ap'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return (
            ('expire',_("Dossier Expiré")),
            ('live',_("Dossier Non-Expiré")),
            ('vide',_("Date d'Ap Vide")),
            )
    def queryset(self, request, queryset):
        if self.value() == 'live':
            return queryset.filter(date_ap__gte=date.today())
        elif self.value() == 'expire':
            return queryset.filter(date_ap__lt=date.today())
        elif self.value() == 'vide':
            return queryset.filter(date_ap__isnull=True)
        else:
            return queryset
