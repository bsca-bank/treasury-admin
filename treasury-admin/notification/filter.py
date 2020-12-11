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

class ClientFilter(InputFilter):
    title = _("Client Code")
    parameter_name = 'client'
  
    def queryset(self, request, queryset):
        if self.value() is not None:
            client = self.value()
            return queryset.filter(Q(client__ref_id=client)) 


class BatchNoFilter(InputFilter):
    title = _("Email Reference")
    parameter_name = 'batch_no'
  
    def queryset(self, request, queryset):
        if self.value() is not None:
            batch_no = self.value()
            return queryset.filter(Q(batch_no=batch_no)|Q(exp_no=batch_no)|Q(send_no=batch_no)) 