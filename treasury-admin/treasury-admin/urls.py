# -*- coding: utf-8 -*-
"""DMFSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
#
from django.conf import settings
#from django.conf.urls import include, url
from django.conf.urls.static import static
from django.urls import include, path  # For django versions from 2.0 and up
#
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [
    #special url-resolver for django-smart-selects
    path(r'admin/', admin.site.urls),
    #
    #path(r'^$',TemplateView.as_view(template_name="index.html")),
    #
    path(r'settlement/', include('settlement.urls')),
    path(r'notification/', include('notification.urls')),
    path(r'transfert/', include('transfert.urls')),
    path(r'tiers/', include('tiers.urls')),
    path(r'util/', include('util.urls')),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#if settings.DEBUG:
#    import debug_toolbar
#    urlpatterns = [
#        path('__debug__/', include(debug_toolbar.urls)),
#
#    ] + urlpatterns


