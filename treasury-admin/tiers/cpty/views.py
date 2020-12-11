from dal import autocomplete
from .models import Cpty


class CptyAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return Cpty.objects.none()
        qs = Cpty.objects.all()
        #key
        type_tiers = self.forwarded.get('type_tiers', None)
        
        if type_tiers:
            qs = qs.filter(type_tiers=type_tiers)
        if self.q:
            qs = qs.filter(swift__istartswith=self.q)
        return qs