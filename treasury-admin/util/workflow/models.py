from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

# Create from 
class Statut(models.Model):
  statut = models.CharField(max_length=50)
  content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
  obs= models.TextField(null=True, blank=True)
  
  #statut
  def __str__(self):
    return u"%s" %(self.statut)

  class Meta:
    managed = True
    db_table = 'util_wf_statut'
    verbose_name = "Workflow Status" 
    verbose_name_plural = "Workflow Status"


# Create from 
class Workflow(models.Model):

  content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
  
  s_init = models.ForeignKey(Statut, on_delete=models.SET_NULL,
                            null=True, blank=True,
                            related_name='%(app_label)s_%(class)s_init',                            
                            verbose_name="Statut Initial")
  
  chk_switch = models.CharField(max_length=15, null=True, blank=True) 

  s_fnl = models.ForeignKey(Statut, on_delete=models.CASCADE,
                            related_name='%(app_label)s_%(class)s_fnl',
                            verbose_name="Statut Final")

  obs= models.CharField(max_length=15, null=True, blank=True)
  
  #statut
  def __str__(self):
    return u"%s | %s | %s" %(self.content_type, self.s_init, self.chk_switch)

  class Meta:
    managed = True
    db_table = 'util_wf'
    unique_together = (('content_type','s_init','chk_switch'),)
    verbose_name = "Workflow" 
    verbose_name_plural = "Workflow"

# Create from 
class DocTraceLog(models.Model):
  #
  object_id    = models.PositiveIntegerField()
  content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
  of           = GenericForeignKey('content_type', 'object_id')    
  #
  chk_create = models.BooleanField(default=False, 
                              verbose_name="Chk Create",
                              help_text="Create Tracing Log")

  time_create = models.DateTimeField(null=True, 
                                  blank=True,editable=False,
                                  help_text="Time Creation")

  obs = models.TextField(max_length=1000, null=True, blank=True) 

  #statut
  def __str__(self):
    return u"%s | %s | %s" %(self.pk, self.content_type, self.object_id)

  class Meta:
    managed = True
    db_table = 'util_doc_trace_log'

  def save(self, *args, **kwargs):
    
      ''' On save, update timestamps '''
      if self.chk_create and not self.time_create:
          self.time_create = timezone.now()
      elif not self.chk_create:
        self.time_create = None

      return super(DocTraceLog, self).save(*args, **kwargs)


# Create from 
class DocTraceLogDetail(models.Model):

  docTraceLog = models.ForeignKey(DocTraceLog, 
                                related_name='%(app_label)s_%(class)s_docTraceLog', 
                                on_delete=models.CASCADE)

  obs = models.CharField(max_length=15, null=True, blank=True) 

  #agent1
  chk_exp = models.BooleanField(default=False, 
                                  verbose_name="Chk Expédition",
                                  help_text="Sending Agent")

  oper_exp = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='%(app_label)s_%(class)s_exp')

  time_exp = models.DateTimeField(null=True, blank=True,editable=False,
                                  help_text="Heure Expédition")
  #agent2
  chk_recv = models.BooleanField(default=False, 
                                verbose_name="Chk Réception",
                                help_text="Receiving Agent")

  oper_recv = models.ForeignKey(User, on_delete=models.SET_NULL,
                                  null=True, blank=True,
                                  related_name='%(app_label)s_%(class)s_recv')

  time_recv = models.DateTimeField(null=True, blank=True,editable=False,
                                  help_text="Heure Réception")


  def clean(self):
      #nomencature are forced when for all new transfert waiting
      if self.chk_recv and not self.chk_exp:
          raise ValidationError("La personnel qui envoie le dossier doit cochez en premier")
 
  #statut
  def __str__(self):
    return u"%s | %s " %(self.docTraceLog, self.pk)

  class Meta:
    managed = True
    db_table = 'util_doc_trace_log_detail'

  def save(self, *args, **kwargs):
      
      ''' On save, update timestamps '''
      if self.chk_exp and not self.time_exp:
          self.time_exp = timezone.now()
      elif not self.chk_exp and not self.oper_exp:
        self.time_exp = None
      
      if self.chk_recv and not self.time_recv:
        self.time_recv = timezone.now()
      elif not self.chk_recv and not self.oper_recv:
        self.time_recv = None
        
      return super(DocTraceLogDetail, self).save(*args, **kwargs)
