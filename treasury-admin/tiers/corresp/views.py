from dal import autocomplete
#
from django.db.models import Q
#
from .models import Corresp, AccountCorresp

class CorrespAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Corresp.objects.none()

        c_active=Q(chk_active=True)

        qs = Corresp.objects.all().filter(swift__isnull=False)

        if self.q:
            c_alias=Q(alias__istartswith=self.q)
            qs = qs.filter(c_active, c_alias)
            
        return qs.filter(c_active)    

class AccountCorrespAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return AccountCorresp.objects.none()
        
        qs = AccountCorresp.objects.all()
        #key
        corresp = self.forwarded.get('corresp', None)

        c_corresp = Q(corresp=corresp)      
        c_active = Q(chk_active=True)             
        
        if corresp:
            qs = qs.filter(c_corresp & c_active)
        if self.q:
            c_alias=Q(alias__istartswith=self.q)
            qs = qs.filter(c_active, c_alias)
        return qs