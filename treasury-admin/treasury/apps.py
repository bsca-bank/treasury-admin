from __future__ import unicode_literals

from django.apps import AppConfig

class TreasuryConfig(AppConfig):
  name = 'treasury'
  
  def ready(self):
    from treasury import signals # import your signals.py