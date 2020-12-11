from import_export import resources
from .models import *

class CashFlowDetailRsrc(resources.ModelResource):
  class Meta:
    model = CashFlowDetail
    #exclude = ( 'id',)
    skip_unchanged = True
    #import_id_fields = ['id']
    widgets = {
      'date_val': {'format': '%Y-%m-%d'},
      'date_pay': {'format': '%Y-%m-%d'},
    }
    
    def before_import(self, dataset, dry_run):
      if dataset.headers:
        dataset.headers = [str(header).lower().strip() for header in dataset.headers]
        
      