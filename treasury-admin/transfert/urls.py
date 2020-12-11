# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import DomDossierAutocomplete, DossierCtrlAutocomplete, BkdopiAutocomplete, TrfDossierCouvrAutocomplete

urlpatterns = [

  url(
    r'^bkdopi-autocomplete/$',
    BkdopiAutocomplete.as_view(),
    name='bkdopi-autocomplete',
    ),
  url(
    r'^dossier_dom-autocomplete/$',
    DomDossierAutocomplete.as_view(),
    name='dossier_dom-autocomplete',
    ),
  url(
    r'^dossier_couvr-autocomplete/$',
    TrfDossierCouvrAutocomplete.as_view(),
    name='dossier_couvr-autocomplete',
    ),
  url(
    r'^dossier_ctrl-autocomplete/$',
    DossierCtrlAutocomplete.as_view(),
    name='dossier_ctrl-autocomplete',
    ),
]



  
  