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
from django.contrib.contenttypes.fields import GenericForeignKey

from tiers.client.models import ClientCtrl
from django_pandas.managers import DataFrameManager
from util.workflow.models import Statut
from util.workflow.abstracts import MixinFourEyesChecking
#
from util.catalog.models import *


from .abstract import Email

def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.pk,
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)  


class EmailTemplate(Email, MixinFourEyesChecking):
    #
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL,
                                    blank=True, null=True)

    # unique identifier of the email template
    template_key = models.CharField(max_length=255, unique=True)

    SUBJECT_TYPE_CHOICES = (
        (1, 'Text Subject'),        
        (2, 'Html Subject'),        
    )  
    #
    subject_type = models.IntegerField(choices=SUBJECT_TYPE_CHOICES, default=1)   

    TEMPLATE_TYPE_CHOICES = (
        (1, 'Text Template'),        
        (2, 'Html Template'), 
        (3, 'Ext. Template'),         
    )  
    #
    template_type = models.IntegerField(choices=TEMPLATE_TYPE_CHOICES, default=1)   
    #
    int_template = models.TextField(blank=True, null=True)
    ext_template = models.FileField(upload_to=upload_path_handler, blank=True, null=True)
    #
    type_operation = models.CharField(max_length=255, blank=True, null=True)
    type_action = models.CharField(max_length=255, blank=True, null=True)
    #
    def __str__(self):
        return "{} | {}".format(self.id, self.template_key)
    
    class Meta:
        managed = True
        db_table = 'email_template'
        verbose_name = "Email Template Mgr." 
        verbose_name_plural = "Email Template Mgr." 


class EmailCtrl(Email, MixinFourEyesChecking):

    object_id    = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    of           = GenericForeignKey('content_type', 'object_id')  
    #
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name='%(app_label)s_%(class)s_template',  
                                verbose_name="Email Template")

    #statut
    statut = models.ForeignKey(Statut, on_delete=models.SET_NULL, 
                               blank=True, null=True,
                               related_name='%(app_label)s_%(class)s_statut',
                               )

    ##Basic information
    client = models.ForeignKey(ClientCtrl, on_delete=models.SET_NULL,
                               blank=True, null=True, 
                               help_text="Tapez le code client ici")

    type_product = models.ForeignKey(CatalogTypeProduct, on_delete=models.SET_NULL,
                                     blank=True, null=True,
                                     related_name='%(app_label)s_%(class)s_type_product')

    batch_no = models.CharField(max_length=19, blank=True, null=True)
    #
    exp_no = models.CharField(max_length=19, blank=True, null=True)
    #
    send_no = models.CharField(max_length=19, blank=True, null=True)

    def get_rendered_template(self, tpl, context):
        return self.get_template(tpl).render(context)

    def get_template(self, tpl):
        return template.Template(tpl)

    def get_subject(self, subject, context):
        return subject or self.get_rendered_template(self.subject, context)

    def get_body(self, body, context):
        return body or self.get_rendered_template(self._get_body(), context)

    def get_sender(self):
        return self.from_email or settings.DEFAULT_FROM_EMAIL

    def get_recipient(self, emails, context):
        return emails or [self.get_rendered_template(self.to_email, context)]

    def __str__(self):
        return "<{}> {} | {}".format(self.id, self.statut, self.batch_no)
    
    #internal ucntions
    def _get_body(self):
        if self.EmailTemplate.template_type == 3:
            #read external file and return
            return 3  
        else:
            #read internal file and return
            return self.int_template


    objects = DataFrameManager()

    class Meta:
        managed = True
        db_table = 'email_ctrl'
        verbose_name = "Email Ctrl." 
        verbose_name_plural = "Email Ctrl." 

    # @staticmethod
    # def send(*args, **kwargs):
    #     EmailCtrl._send(*args, **kwargs)

    # @staticmethod
    # def _send(template_key, context, subject=None, body=None, sender=None,
    #           emails=None, bcc=None, attachments=None):

    #     mail_template = EmailTemplate.objects.get(template_key=template_key)
    #     context = Context(context)

    #     subject = mail_template.get_subject(subject, context)
    #     body = mail_template.get_body(body, context)
    #     sender = sender or mail_template.get_sender()
    #     emails = mail_template.get_recipient(emails, context)

    #     #if mail template is in plain-text
    #     if mail_template.template_type == 1:
    #         return send_mail(subject, body, sender, emails, fail_silently=not
    #         settings.DEBUG)

    #     #if mail template is in html
    #     elif mail_template.template_type == 2:
    #         msg = EmailMultiAlternatives(subject, body, sender, emails,
    #                                     alternatives=((body, 'text/html'),),
    #                                     bcc=bcc
    #                                     )
    #     #if mail template is an external file
    #     else:
    #         msg = ""

    #     if attachments:
    #         for name, content, mimetype in attachments:
    #             msg.attach(name, content, mimetype)
    #     return msg.send(fail_silently=not (settings.DEBUG or settings.TEST))



#EmailTemplate.send('expense_notification_to_admin', {
#    # context object that email template will be rendered with
#    'expense': expense_request,
#})

#invoice_pdf = invoice.pdf_file.pdf_file_data
#send_email(
#    # a string such as 'invoice_to_customer'
#    template_name,
#
#    # context that contains Customer, Invoice and other objects
#    ctx,
#
#    # list of receivers i.e. ['customer1@example.com', 'customer2@example.com]
#    emails=emails,
#
#    # attached PDF file of the invoice
#    attachments=[(invoice.reference, invoice_pdf, 'application/pdf')]
#)

#from celery import task
#from core.models import EmailTemplate

#@task
#def send_email(*args, **kwargs):
#    return EmailTemplate.send(*args, **kwargs)