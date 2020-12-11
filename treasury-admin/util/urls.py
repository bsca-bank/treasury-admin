# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import CcyAutocomplete, UserAutocomplete, ContentTypeAutocomplete, \
                    StatutAutocomplete, CatalogTypeCommercialAutocomplete, \
                    CatalogTypeFileAutocomplete, CatalogTypeProductAutocomplete, \
                    DocTraceLogAutocomplete, CatalogTypeTiersAutocomplete

urlpatterns = [
  url(
    r'^ccy-autocomplete/$',
    CcyAutocomplete.as_view(),
    name='ccy-autocomplete',
    ),
  url(
    r'^user-autocomplete/$',
    UserAutocomplete.as_view(),
    name='user-autocomplete',
    ),    
  url(
    r'^contentType-autocomplete/$',
    ContentTypeAutocomplete.as_view(),
    name='contentType-autocomplete',
    ),
  url(
    r'^statut-autocomplete/$',
    StatutAutocomplete.as_view(),
    name='statut-autocomplete',
    ),
  url(
    r'^catalogTypeCommercial-autocomplete/$',
    CatalogTypeCommercialAutocomplete.as_view(),
    name='catalogTypeCommercial-autocomplete',
    ),
  url(
    r'^catalogTypeFile-autocomplete/$',
    CatalogTypeFileAutocomplete.as_view(),
    name='catalogTypeFile-autocomplete',
    ),
  url(
    r'^catalogTypeProduct-autocomplete/$',
    CatalogTypeProductAutocomplete.as_view(),
    name='catalogTypeProduct-autocomplete',
    ),
  url(
    r'^catalogTypeTiers-autocomplete/$',
    CatalogTypeTiersAutocomplete.as_view(),
    name='catalogTypeTiers-autocomplete',
    ),
  url(
    r'^docTraceLog-autocomplete/$',
    DocTraceLogAutocomplete.as_view(),
    name='docTraceLog-autocomplete',
    ),
]

  
  