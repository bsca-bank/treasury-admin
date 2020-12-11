from import_export import resources
from .models import *

class TrfDossierExecRsrc(resources.ModelResource):
  class Meta:
    model = TrfDossierExec
    exclude = ( 'id','nature','ref_id','statut','agenceID', 'statut_sys', 'ccy_code', 'operType', 'donneur', 
                'accDonneur', 'benef', 'accBenef', 'montant', 'montant_xaf', 
                'fxRate', 'date_val', 'date_exec', 'invoice', 'feeType', 
                'motif', 'uti', 'timestamp',
                'trfDossier','ctrl')
    
    skip_unchanged = False
    import_id_fields = ['apbkdopi_ptr']
    
    def before_import(self, dataset, dry_run):
      if dataset.headers:
        dataset.headers = [str(header).lower().strip() for header in dataset.headers]    