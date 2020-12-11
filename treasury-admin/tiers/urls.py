# -*- coding: utf-8 -*-
from django.conf.urls import url

from .client.views import ClientCtrlAutocomplete, ClientFileStorageAutocomplete
from .corresp.views import CorrespAutocomplete, AccountCorrespAutocomplete

urlpatterns = [
  url(
    r'^client-autocomplete/$',
    ClientCtrlAutocomplete.as_view(),
    name='client-autocomplete',
    ),
  url(
    r'^clientFile-autocomplete/$',
    ClientFileStorageAutocomplete.as_view(),
    name='clientFile-autocomplete',
    ),
  url(
    r'^corresp-autocomplete/$',
    CorrespAutocomplete.as_view(),
    name='corresp-autocomplete',
    ),
  url(
    r'^accountCorresp-autocomplete/$',
    AccountCorrespAutocomplete.as_view(),
    name='accountCorresp-autocomplete',
    ),
]

  
  