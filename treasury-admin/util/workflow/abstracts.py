from __future__ import unicode_literals

from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.db import models
#
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from .models import DocTraceLog

#
from django.utils import timezone

class MixinDocTracingLog(models.Model):

    docTraceLog = models.OneToOneField(DocTraceLog, 
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_docTraceLog', 
                                    on_delete=models.SET_NULL)
    class Meta:
        abstract = True

# Create from 
class MixinFourEyesChecking(models.Model):

    #agent1
    chk_verify = models.BooleanField(default=False, 
                                   verbose_name="Verf",
                                   help_text="1st Agent")

    oper_verify = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_verify')

    time_verify = models.DateTimeField(null=True, blank=True,editable=False,
                                    help_text="Time Verify")
    #agent2
    chk_approv = models.BooleanField(default=False, 
                                  verbose_name="Appv",
                                  help_text="2nd Agent")

    oper_approv = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_approv')

    time_approv = models.DateTimeField(null=True, blank=True,editable=False,
                                    help_text="Time Approv")
  
    obs = models.TextField(max_length=1000, null=True, blank=True) 
    
    class Meta:
      abstract = True


    def save(self, *args, **kwargs):
        
        ''' On save, update timestamps '''
        if self.chk_verify and not self.time_verify:
            self.time_verify = timezone.now()
        elif not self.chk_verify:
          self.oper_verify = None
          self.time_verify = None

        if self.chk_approv and not self.time_approv:
          self.time_approv = timezone.now()
        elif not self.chk_approv:
            self.oper_approv = None
            self.time_approv = None

        return super(MixinFourEyesChecking, self).save(*args, **kwargs)

