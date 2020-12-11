from __future__ import unicode_literals

from django.db import models


class Ccy(models.Model):
    iso = models.CharField(max_length=3)
    alias = models.CharField(max_length=50, null=True, blank=True)
    ccyPeg = models.ForeignKey('self', on_delete=models.SET_NULL,
                               null=True, blank=True)
    
    desc = models.CharField(max_length=50, null=True, blank=True)
    id_AP = models.CharField(max_length=3, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'util_ccy'
        ordering=('iso',)

    def __str__(self):
        return self.iso

    
class CcyPair(models.Model):
    alias = models.CharField(max_length=6, null=True, blank=True)
    ccy1 = models.ForeignKey(Ccy, on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_ccy1')
    
    ccy2 = models.ForeignKey(Ccy, on_delete=models.CASCADE,
                             related_name='%(app_label)s_%(class)s_ccy2')
    
    desc = models.CharField(max_length=50, null=True, blank=True)
    id_AP = models.CharField(max_length=3, null=True, blank=True)
    
    class Meta:
        managed = True
        db_table = 'util_ccypair'
        unique_together = ('alias',)
        
    def __str__(self):
        return self.alias    