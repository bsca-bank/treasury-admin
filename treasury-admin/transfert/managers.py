from .models import *

# First, define the Manager subclass.
class ProxyContentTypeManager(models.Manager):

    def get_queryset(self):
        ctype = ContentType.objects.get_for_model(self.model, for_concrete_model=False)
        type_product = CatalogTypeProduct.objects.get(content_type=ctype)
        return super().get_queryset().filter(type_product=type_product.id)
