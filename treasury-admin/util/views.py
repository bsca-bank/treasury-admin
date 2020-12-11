from dal import autocomplete
#
from django.db.models import Q
#
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
#
from .catalog.models import CatalogTypeCommercial,CatalogTypeFile,CatalogTypeProduct,CatalogTypeTiers
from .workflow.models import Statut, DocTraceLog
from .fx.models import Ccy


class DocTraceLogAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      return DocTraceLog.objects.none()

    qs = DocTraceLog.objects.all()

    object_id = self.forwarded.get('object_id', None)
    app_label = self.forwarded.get('app_label', None)
    model = self.forwarded.get('model', None)

    ctype = ContentType.objects.get_by_natural_key(
      app_label=app_label, model=model)

    c_ctype = Q(content_type=ctype)
    c_id = Q(content_type=object_id)

    # print(ctype)
    # key
    if self.q:
        qs = qs.filter(object_id__contains=self.q)
    else:
        qs = qs.filter(c_ctype, c_id)
    return qs


class CcyAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      return Ccy.objects.none()

    qs = Ccy.objects.all()

    iso = self.forwarded.get('iso', None)
    include = self.forwarded.get('include', False)
    
    c_iso = Q(iso__in=iso)

    if self.q:
      c_query = Q(iso__istartswith=self.q)
      qs = qs.filter(c_query)
    else:
      if include: 
          qs = qs.filter(c_iso)
      else:
          qs = qs.filter().exclude(c_iso)
    return qs

class UserAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      return User.objects.none()

    qs = User.objects.all()

    request_user = self.forwarded.get('request_user', None)

    user_groups = self.request.user.groups.values_list('id')
    crews = User.objects.filter(groups__id__in=user_groups)
    c_group = Q(id__in=crews)

    if request_user and not self.request.user.is_superuser:
      c_query = Q(id=self.request.user.id)
      qs = qs.filter(c_query)
    elif self.q and not self.request.user.is_superuser:
      c_query = Q(username__istartswith=self.q)
      qs = qs.filter(c_query + c_group)
    else:
      c_query = Q(username__istartswith=self.q)
      qs = qs.filter(c_query)
    
    return qs

class ContentTypeAutocomplete(autocomplete.Select2QuerySetView):
  # def get_model_id(self, instance):
  #      ctype = ContentType.objects.get_for_model(instance)
  #      return ctype.id
  #ctype = ContentType.objects.get_by_natural_key(app_label='transfert', model='')
  #ctype = ContentType.objects.get_for_model(instance)

  def get_queryset(self):
    if not self.request.user.is_authenticated:
      return ContentType.objects.none()
    qs = ContentType.objects.all()

    # key
    if self.q:
      qs = qs.filter(model__contains=self.q)
    return qs

class StatutAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):

    if not self.request.user.is_authenticated:
      return Statut.objects.none()
    qs = Statut.objects.all()

    app_label = self.forwarded.get('app_label', None)
    model = self.forwarded.get('model', None)
    
    ctype = self.forwarded.get('ctype', None)
    
    if not ctype:
      ctype = ContentType.objects.get_by_natural_key(
        app_label=app_label, model=model)

    c_ctype = Q(content_type=ctype)

    # print(ctype)
    # key
    if self.q:
        qs = qs.filter(model__contains=self.q)
    else:
        qs = qs.filter(c_ctype)
    return qs

class CatalogTypeCommercialAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):

    if not self.request.user.is_authenticated:
      return CatalogTypeCommercial.objects.none()

    qs = CatalogTypeCommercial.objects.all()
    #key
    turple = self.forwarded.get('turple', False)
    #
    include = self.forwarded.get('include', True)
    nature = self.forwarded.get('nature', '')
    level = self.forwarded.get('level', 99)
    parent_type = self.forwarded.get('parent_type', None)
  
    if not turple:
      c_nature = Q(nature__contains=nature)
    else:
      c_nature = Q(nature__in=nature)

    c_level = Q(level__lt=level)
    c_parent = Q(parent_type=parent_type)

    if self.q:
      qs = qs.filter(nature__istartswith=self.q)
    else:
      if include:
        qs = qs.filter(c_nature, c_level, c_parent)
      else:
        qs = qs.filter(c_level, c_parent).exclude(c_nature)
    return qs

class CatalogTypeFileAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):

    if not self.request.user.is_authenticated:
      return CatalogTypeFile.objects.none()

    qs = CatalogTypeFile.objects.all()

    ctype = self.forwarded.get('content_type', None)

    c_ctype = Q(content_type=ctype)

    if self.q:
      qs = qs.filter(category_l1__istartswith=self.q)
    else:
      qs = qs.filter(c_ctype)
    return qs

class CatalogTypeProductAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):

    if not self.request.user.is_authenticated:
      return CatalogTypeProduct.objects.none()

    qs = CatalogTypeProduct.objects.all()

    app_label = self.forwarded.get('app_label', None)
    model = self.forwarded.get('model', None)
    ctype = ContentType.objects.get_by_natural_key(
      app_label=app_label, model=model)
    c_ctype = Q(content_type=ctype)
    print("DEBUG: Ctype = " + str(ctype))
    #child_ctype = self.forwarded.get('child_ctype', None)
    
    if self.q:
        qs = qs.filter(category_l2__istartswith=self.q)
    else:
        qs = qs.filter(c_ctype)
    return qs

class CatalogTypeTiersAutocomplete(autocomplete.Select2QuerySetView):

  def get_queryset(self):

    if not self.request.user.is_authenticated:
      return CatalogTypeTiers.objects.none()

    qs = CatalogTypeTiers.objects.all()

    app_label = self.forwarded.get('app_label', None)
    model = self.forwarded.get('model', None)
    ctype = ContentType.objects.get_by_natural_key(
      app_label=app_label, model=model)
    c_ctype = Q(content_type=ctype)
    print("DEBUG: Ctype = " + str(ctype))
    #child_ctype = self.forwarded.get('child_ctype', None)
    
    if self.q:
        qs = qs.filter(category_l2__istartswith=self.q)
    else:
        qs = qs.filter(c_ctype)
    return qs

