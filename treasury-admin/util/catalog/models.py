# encoding: UTF-8
from __future__ import unicode_literals
from django.contrib.contenttypes.models import ContentType

from django.db import models


class CatalogTypeCommercial(models.Model):

    level = models.IntegerField(default=0)
    nature = models.CharField(max_length=50, null=True, blank=True)
    alias = models.CharField(max_length=50, null=True, blank=True) 
    id_AP = models.CharField(max_length=3, null=True, blank=True)
    #
    parent_type = models.ForeignKey('self', 
                            on_delete=models.SET_NULL, 
                            #limit_choices_to={'nature':0},
                            null=True, blank=True)

    chk_dom = models.BooleanField(default=True,
                                verbose_name="Dom",
                                help_text="Check here if a dom document needed")

    jour_dom = models.IntegerField(null=True, blank=True, help_text="Nb.de jour pour l'apurement")
    
    # COBAC
    code_oper = models.CharField(max_length=1, null=True, blank=True,
                                verbose_name="C_Oper",)

    code_nature = models.CharField(max_length=1, null=True, blank=True,
                                verbose_name="C_Nature",) 

    class Meta:
        managed = True
        db_table = 'util_catalog_type_comm'
        ordering = ('level','nature')
        verbose_name = "Contrôle de nomenclature commercial"
        verbose_name_plural = "Contrôle de nomenclature commercial" 
        
        
    def __str__(self):
        return u"%s / %s" %(self.id_AP, self.alias,)


class CatalogTypeProduct(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                    related_name='%(app_label)s_%(class)s_parent_type',  
                                    verbose_name="Parent Type",
                                    help_text="Parent model content type")

    child_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL,
                                    null=True, blank=True,
                                    related_name='%(app_label)s_%(class)s_child_type',  
                                    verbose_name="Child Type",
                                    help_text="Inline model content type")

    category_act = models.ForeignKey("CatalogTypeActivity", on_delete=models.CASCADE)

    category_l1 = models.CharField(max_length=50)
    category_l2 = models.CharField(max_length=50)
    code_product = models.CharField(max_length=10,verbose_name="Code Product") 

    class Meta:
        managed = True
        db_table = 'util_catalog_type_product'
        ordering = ('content_type','category_l1')
        verbose_name = "Contrôle de nomenclature produit"
        verbose_name_plural = "Contrôle de nomenclature produit" 

    def __str__(self):
        return u"%s | %s" %(self.category_l1, self.code_product,)    


class CatalogTypeTiers(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    category_l1 = models.CharField(max_length=100)
    category_l2 = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'util_catalog_type_tiers'

        verbose_name = "Contrôle de nomenclature tiers"
        verbose_name_plural = "Contrôle de nomenclature tiers" 

    def __str__(self):
        return u"%s | %s" %(self.category_l1, self.category_l2,)    


class CatalogTypeFile(models.Model):

    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, 
                                    null=True, blank=True)
                                    
    category_l1 = models.CharField(max_length=100)
    category_l2 = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'util_catalog_type_doc'

        verbose_name = "Contrôle de nomenclature document"
        verbose_name_plural = "Contrôle de nomenclature document" 

    def __str__(self):
        return u"%s" %(self.category_l1)

class CatalogTypeActivity(models.Model):

    category_l1 = models.CharField(max_length=50)
    alias = models.CharField(max_length=50) 

    class Meta:
        managed = True
        db_table = 'util_catalog_type_act'

        verbose_name = "Contrôle de nomenclature Activité"
        verbose_name_plural = "Contrôle de nomenclature Activité" 

    def __str__(self):
        return u"%s" %(self.alias)    


