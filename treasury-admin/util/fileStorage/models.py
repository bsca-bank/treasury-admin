# encoding: UTF-8
from __future__ import unicode_literals

from django.db import models

#library
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta
#
from django.core.exceptions import ValidationError

from django.utils import timezone
import os
#
from util.catalog.models import CatalogTypeFile


def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.pk,
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)  


## Create your models here.
class FileStorage(models.Model):
  object_id    = models.PositiveIntegerField()
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  of           = GenericForeignKey('content_type', 'object_id')    
  #
  file_name = models.CharField(max_length=50)    
  #
  created     = models.DateTimeField(editable=False)
  modified    = models.DateTimeField()
  #
  oper = models.ForeignKey(User, on_delete=models.CASCADE,
                          related_name='%(app_label)s_%(class)s_oper')       
  #link
  group_oper = models.ForeignKey(Group, on_delete=models.SET_NULL, 
                          blank=True, null=True, 
                          related_name='%(app_label)s_%(class)s_group_oper',
                          verbose_name="group_oper",
                          help_text='Group propriétaire')
  #
  type_file = models.ForeignKey(CatalogTypeFile, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                verbose_name="type_file",
                                help_text='Type du document')   
 
  file = models.FileField(upload_to=upload_path_handler)
  #
  class Meta:
    abstract = True
  
  def save(self, *args, **kwargs):
      ''' On save, update timestamps '''
      if not self.id:
          self.created = timezone.now()
      self.modified = timezone.now()
      return super(FileStorage, self).save(*args, **kwargs)



class FileStorageFolder(models.Model):
  object_id    = models.PositiveIntegerField()
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  of           = GenericForeignKey('content_type', 'object_id')    
  #
  folder_name = models.CharField(max_length=50)    

  created     = models.DateTimeField(editable=False)
  modified    = models.DateTimeField()

  oper = models.ForeignKey(User, on_delete=models.CASCADE,
                          related_name='%(app_label)s_%(class)s_oper',
                          verbose_name="Oper")       
 
  group_oper = models.ForeignKey(Group, on_delete=models.SET_NULL, 
                          blank=True, null=True, 
                          related_name='%(app_label)s_%(class)s_group_oper',
                          verbose_name="group_oper",
                          help_text='Group propriétaire')

  type_folder = models.ForeignKey(CatalogTypeFile, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_type_file',)  
  #
  obs = models.TextField(max_length=200, null=True, blank=True)
  #
  class Meta:
    abstract = True
  
  def save(self, *args, **kwargs):
      ''' On save, update timestamps '''
      if not self.id:
          self.created = timezone.now()
      self.modified = timezone.now()
      return super(FileStorageFolder, self).save(*args, **kwargs)