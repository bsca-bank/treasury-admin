from __future__ import unicode_literals

from django.apps import AppConfig

class TiersConfig(AppConfig):
    name = 'tiers'
    
    def ready(self):
        from tiers import signals # import your signals.py