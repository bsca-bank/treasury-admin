# -*- coding: utf-8 -*-
from django.dispatch import Signal
from django.dispatch import receiver
#
from django.db.models.signals import pre_save, post_save, pre_delete
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

#from .calc import updateActTresor
from .models import CashFlowDetail