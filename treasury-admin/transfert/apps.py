from __future__ import unicode_literals

from django.apps import AppConfig

class TransfertConfig(AppConfig):

  name = 'transfert'

  def ready(self):
    from transfert import signals # import your signals.py