from dal import autocomplete
from .models import TreasuryPosition
from .sygma.models import SygmaCtrl



class TreasuryPositionAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return TreasuryPosition.objects.none()
        qs = TreasuryPosition.objects.all()
        #key
        date_val = self.forwarded.get('date_val', None)
        corresp = self.forwarded.get('corresp', None)
        
        if date_val:
            
            #date format correction due to incompatible date format in the database
            import datetime 
            date_val = datetime.datetime.strptime(date_val, '%d/%m/%Y').strftime('%Y-%m-%d')            
            
            if corresp:
                qs = qs.filter(date_val=date_val, corresp=corresp)
            else:
                qs = qs.filter(date_val=date_val)

        #if self.q:
            #qs = qs.filter(ref_id__istartswith=self.q)
        return qs


class SygmaAutocomplete(autocomplete.Select2QuerySetView):
    
    def get_queryset(self):
        if not self.request.user.is_authenticated == True:
            return SygmaCtrl.objects.none()
        qs = SygmaCtrl.objects.all()
        #key
        date_val = self.forwarded.get('date_val', None)
        codtype = self.forwarded.get('codtype', None)
        
        #date format correction due to incompatible date format in the database
        if date_val:

            import datetime 
            date_val = datetime.datetime.strptime(date_val, '%d/%m/%Y').strftime('%Y-%m-%d')   

            if codtype:
                qs = qs.filter(date_val=date_val, codtype=codtype)
            else:    
                qs = qs.filter(date_val=date_val)
                
                
        if self.q:
            qs = qs.filter(ref_id__istartswith=self.q)
        return qs