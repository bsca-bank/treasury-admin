# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from django.db import models
from django.utils import timezone
#
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, AbstractUser, Group
from django.contrib.contenttypes.models import ContentType
#
from django_pandas.managers import DataFrameManager
from django.utils.translation import gettext_lazy as _

from tiers.client.models import ClientCtrl
from util.fileStorage.models import FileStorage, FileStorageFolder
from util.workflow.abstracts import MixinFourEyesChecking



def upload_path_handler(instance, filename):
    ctype = ContentType.objects.get_for_model(instance)
    upload_dir = os.path.join('uploads',
                              '%s' % ctype.model,
                              '%s' % instance.pk,
                              )
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    return os.path.join(upload_dir, filename)  

class MeetingType(models.Model):

    level = models.IntegerField(default=0)
    #
    nature = models.CharField(max_length=50) 
    type_session = models.CharField(max_length=50, null=True, blank=True) 
    #
    name_fr = models.CharField(max_length=50, null=True, blank=True)
    name_cn = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=10)
    #
    parent_type = models.ForeignKey('self', 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)    
    #    
    def __str__(self):
        return u"%s <%s>" %(self.alias, self.type_session)

    class Meta:
        managed = True
        verbose_name = "Meeting Type" 
        verbose_name_plural = "Meeting Types"

class MeetingItemType(models.Model):

    level = models.IntegerField(default=0)

    nature = models.CharField(max_length=50, null=True, blank=True) 
    #
    name_fr = models.CharField(max_length=50, null=True, blank=True)
    name_cn = models.CharField(max_length=50, null=True, blank=True)
    #
    parent_type = models.ForeignKey('self', 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)    

    item_key = models.CharField(max_length=1, null=True, blank=True)

    #    
    def __str__(self):
        return u"%s | %s" %(self.nature, self.item_key)

    class Meta:
        managed = True
        verbose_name = "Meeting Item Type" 
        verbose_name_plural = "Meeting Item Types"


class MeetingUserType(models.Model):

    nature = models.CharField(max_length=50, null=True, blank=True) 
    #
    name_fr = models.CharField(max_length=50, null=True, blank=True)
    name_cn = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True)
    #
    parent_type = models.ForeignKey('self', 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)    

    #    
    def __str__(self):
        return u"%s | %s" %(self.nature, self.alias)

    class Meta:
        managed = True
        verbose_name = "Meeting User Type" 
        verbose_name_plural = "Meeting User Types"

#Create your models here.
class Meeting(models.Model):

    nature = models.ForeignKey(MeetingType, 
                            on_delete=models.CASCADE)    
    #
    order_no = models.IntegerField(default=0)
    #
    global_no = models.IntegerField(default=0)
    #
    name_fr = models.TextField(max_length=100, null=True, blank=True)
    name_cn = models.TextField(max_length=100, null=True, blank=True)
    #
    date_val = models.DateField(verbose_name="Date de Réunion",help_text="")  
    heure = models.TimeField(verbose_name="Heure", help_text="")  
    location = models.CharField(verbose_name="Lieu", max_length=50, null=True, blank=True)
    #
    acc_period = models.CharField(max_length=6, null=True, blank=True)
    #
    obs = models.TextField(max_length=1000, null=True, blank=True)

    @property
    def ref_meeting(self):
        yyyy = self.date_val.strftime("%Y")
        type_meeting = self.nature.alias
        order_no = "0" + str(self.order_no)
        outset = type_meeting + order_no + "/" + yyyy
        return outset
    
    @property
    def year(self):
        outset = self.date_val.year
        return outset
    #    
    def __str__(self):
        return u"%s" %(self.ref_meeting)


    class Meta:
        managed = True
        verbose_name = "Meeting" 
        verbose_name_plural = "Meetings"
        ordering = ['-date_val',]


#Create your models here.
class MeetingItem(models.Model):

    nature = models.ForeignKey(MeetingItemType, 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)
    
    date_val = models.DateField(verbose_name="Date du Sujet",help_text="")  
    #
    order_no = models.IntegerField(default=0)
    #
    ref_no = models.TextField(max_length=3, null=True, blank=True)
    #
    #
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True, blank=True)
    #
    name_fr = models.TextField(max_length=300, null=True, blank=True)
    name_cn = models.TextField(max_length=300, null=True, blank=True)
    #
    file_fr = models.FileField(upload_to=upload_path_handler, 
                                #max_length=10,
                                null=True, blank=True, 
                                help_text="version final en Français")

    file_cn = models.FileField(upload_to=upload_path_handler, 
                               #max_length=10,
                               null=True, blank=True, 
                               help_text="version final en Chinois")
    #
    obs = models.TextField(max_length=1000, null=True, blank=True,
                            default="Respo/责任部门: ")

    @property
    def ref_item(self):
        ref_meeting = self.meeting.ref_meeting
        outset = ref_meeting + "_" + str(self.order_no)
        return outset

    @property
    def year(self):
        outset = self.date_val.year
        return outset
    #
    def __str__(self):
        return u"%s" %(self.ref_item)
  
    class Meta:
        managed = True
        verbose_name = "Meeting Item" 
        verbose_name_plural = "Meeting Items"
        unique_together = (('meeting','order_no',))


class MeetingUser(models.Model):
    #
    first_name = models.CharField(_('given name'), max_length=30, blank=True, help_text="Prénom")
    last_name = models.CharField(_('surname'), max_length=150, blank=True, help_text="Nom")
    alias = models.CharField(_('Name'), max_length=150, blank=True, help_text="Short name")
    
    GENDER_CHOICES = (
        (0, 'Femme'),        
        (1, 'Homme'),
    ) 
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1)
    date_birth = models.DateField(help_text="date de naissance")
    nationality = models.CharField(_('nationality'), max_length=50, blank=True)

    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    #
    nature = models.ForeignKey(MeetingUserType, 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)   
    # 
    #
    name_cn = models.CharField(max_length=50, null=True, blank=True)
    position = models.CharField(max_length=50, null=True, blank=True, help_text="Poste")
    #
    tel_fix = models.CharField(max_length=50, null=True, blank=True)
    tel_mobile = models.CharField(max_length=50, null=True, blank=True)
    no_passport = models.CharField(max_length=50, null=True, blank=True, help_text="Numéro du Passport")
    date_exp_passport = models.DateField(help_text="Date Exp. du Passport")
    
    #    
    def __str__(self):
        return u"%s | %s" %(self.id, self.nature)
  
    class Meta:
        managed = True
        verbose_name = "Meeting User" 
        verbose_name_plural = "Meeting User"     




from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
#
from util.catalog.models import CatalogTypeFile


class MeetingDoc(models.Model):
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
    nature = models.ForeignKey(CatalogTypeFile, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_nature',
                                    verbose_name="type_file",
                                    help_text='Type du document')   
    #
    parent_doc = models.ForeignKey('self', 
                            on_delete=models.SET_NULL, 
                            null=True, blank=True)    

    #
    meeting = models.ForeignKey(Meeting, on_delete=models.SET_NULL, null=True, blank=True)
    meeting_item = models.ForeignKey(MeetingItem, on_delete=models.SET_NULL, null=True, blank=True)
    meeting_user = models.ForeignKey(MeetingUser, on_delete=models.SET_NULL, null=True, blank=True)
    #
    name_fr = models.TextField(max_length=200, null=True, blank=True)
    name_cn = models.TextField(max_length=200, null=True, blank=True)
    #
    file_fr = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    file_cn = models.FileField(upload_to=upload_path_handler, null=True, blank=True)
    #
    obs = models.TextField(max_length=1000, null=True, blank=True)
    #    
    def __str__(self):
        return u"%s [%s] | %s | %s" %(self.meeting, self.meeting_item, self.name_fr, self.name_cn, )
  
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
            self.modified = timezone.now()
        else:
            self.modified = timezone.now()
        return super(MeetingDoc, self).save(*args, **kwargs)

    class Meta:
        managed = True
        verbose_name = "Meeting Doc" 
        verbose_name_plural = "Meeting Doc"     

