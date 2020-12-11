# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import TreasuryPositionAutocomplete, SygmaAutocomplete

urlpatterns = [

  url(
    r'^treasuryPosition-autocomplete/$',
    TreasuryPositionAutocomplete.as_view(),
    name='treasuryPosition-autocomplete',
    ),

  url(
    r'^sygma-autocomplete/$',
    SygmaAutocomplete.as_view(),
    name='sygma-autocomplete',
    ),
]

  
  