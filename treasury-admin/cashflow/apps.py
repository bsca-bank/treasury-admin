from __future__ import unicode_literals

from django.apps import AppConfig

class CashFlowConfig(AppConfig):

    name = 'cashflow'

    def ready(self):
        from cashflow import signals # import your signals.py