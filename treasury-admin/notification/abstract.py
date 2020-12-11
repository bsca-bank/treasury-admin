# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from django.db import models

from django.contrib.contenttypes.models import ContentType
# Create your models here.

from django import template
from django.conf import settings
from django.core.mail import send_mail, EmailMultiAlternatives
from django.db import models
from django.template import Context


def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.pk,
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)  

class Email(models.Model):
    """
    Email templates get stored in database so that admins can
    change emails on the fly
    """
    from_email = models.CharField(max_length=255, blank=True, null=True)
    to_email = models.CharField(max_length=255, blank=True, null=True)
    cc_email = models.TextField(blank=True, null=True)
    
    subject = models.TextField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    
    class Meta:
        abstract = True