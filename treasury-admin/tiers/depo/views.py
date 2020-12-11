from dal import autocomplete
from .models import Depo, AccountDepo


class DepoAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return Depo.objects.none()
        qs = Depo.objects.all()
        #key
        type_tiers = self.forwarded.get('type_tiers', None)
        
        if type_tiers:
            qs = qs.filter(type_tiers=type_tiers)
        if self.q:
            qs = qs.filter(swift__istartswith=self.q)
        return qs

class AccountDepoAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return AccountDepo.objects.none()
        qs = AccountDepo.objects.all()
        #key
        corresp = self.forwarded.get('corresp', None)

        if corresp:
            qs = qs.filter(corresp=corresp)
            
        if self.q:
            qs = qs.filter(alias__istartswith=self.q)

        return qs