# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime

from django.db import models
from django.utils import timezone
#
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
#
from django_pandas.managers import DataFrameManager
from util.fileStorage.models import FileStorage, FileStorageFolder
from util.workflow.abstracts import MixinFourEyesChecking

#Create your models here.
class InternalFileFolder(FileStorageFolder):
 
    ref_id = models.CharField(max_length=10, blank=True, null=True,
                            verbose_name="Réf.ID",
                            help_text='Référence id interne')    

    group_disrib = models.ManyToManyField(Group, 
                            related_name='%(app_label)s_%(class)s_group_disrib',
                            verbose_name='group_disrib',
                            help_text='Champs de Circulation')
    #    
    def __str__(self):
        return u"%s | %s " %(self.id, self.folder_name)
    
    class Meta:
        managed = True
        db_table = 'internal_file_folder' 
        verbose_name = "Classeur Interne" 
        verbose_name_plural = "Classeurs Internes"    
        ordering = ('group_oper','type_folder','ref_id')   


class InternalFileStorage(FileStorage, MixinFourEyesChecking):

    date_recu = models.DateField(verbose_name="Date de réception",
                                help_text="Date de réception du document")  

    date_val = models.DateField(blank=True, null=True,
                                verbose_name="Date de limite",
                                help_text="Date de limite pour le traitement du document")  

    ref_id = models.CharField(max_length=15, blank=True, null=True,
                            verbose_name="Réf.ID",
                            help_text='Réf.ID interne')    

    file_folder = models.ForeignKey(InternalFileFolder, on_delete=models.SET_NULL, 
                                    blank=True, null=True,
                                    related_name='%(app_label)s_%(class)s_file_folder',
                                    verbose_name="File folder",
                                    help_text='Classeur de dossier')

    group_disrib = models.ForeignKey(Group, on_delete=models.SET_NULL, 
                            blank=True, null=True,
                            related_name='%(app_label)s_%(class)s_group_disrib',
                            verbose_name='group_disrib',
                            help_text='Champs de Circulation')
    #    
    def __str__(self):
        return u"%s | %s" %(self.id, self.type_file)
    
    def save(self, *args, **kwargs):
        ''' On save, update date_recu '''
        if not self.date_recu:
            self.date_recu = datetime.date.today()
        return super(InternalFileStorage, self).save(*args, **kwargs)

    class Meta:
        managed = True
        db_table = 'internal_file' 
        verbose_name = "Document Interne" 
        verbose_name_plural = "Documents Internes"    
        ordering = ('group_oper','type_file','ref_id')   
