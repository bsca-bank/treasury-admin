from dal import autocomplete
from .models import DomDossierCtrl, TrfDossierCtrl, TrfDossierExec, TrfDossierCouvr
#
from django.db.models import Q


class DossierCtrlAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated == True:
      return TrfDossierCtrl.objects.none()
    qs = TrfDossierCtrl.objects.all()
    #key
    if self.q:
      qs = qs.filter(id__istartswith=self.q)
    return qs 


class BkdopiAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated == True:
      return TrfDossierExec.objects.none()
    qs = TrfDossierExec.objects.all()
    #key
    if self.q:
      qs = qs.filter(ref_id__istartswith=self.q, statut_sys='FO')
    return qs 

class DomDossierAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated == True:
      return DomDossierCtrl.objects.none()

    qs = DomDossierCtrl.objects.all()

    client = self.forwarded.get('client', None)
    nomenc_lv0 = self.forwarded.get('nomenc_lv0', None)
    
    c1 = Q(client=client)
    c2 = Q(nomenc_lv0=nomenc_lv0)
    print(c1,c2)
    if self.q:
      c3 = Q(ref_di__istartswith=self.q)
      qs = qs.filter(c3)
    else:
      qs = qs.filter(c1,c2)
    return qs 

class TrfDossierCouvrAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated == True:
      return TrfDossierCouvr.objects.none()
    qs = TrfDossierCouvr.objects.all()
    #key
    if self.q:
      qs = qs.filter(ref_id__istartswith=self.q)
    return qs 

