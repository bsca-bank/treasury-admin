from dal import autocomplete
from .models import ClientCtrl, ClientFileStorage

class ClientCtrlAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return ClientCtrl.objects.none()
        qs = ClientCtrl.objects.all()
        #key

        if self.q:
            qs = qs.filter(ref_id__istartswith=self.q)
        return qs


class ClientFileStorageAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return ClientFileStorage.objects.none()
        qs = ClientFileStorage.objects.all()
        #key
        client = self.forwarded.get('client', None)

        if client:
            qs = qs.filter(clientCtrl=client)
        return qs