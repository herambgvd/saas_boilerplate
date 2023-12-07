from django.apps import AppConfig


class MarketplaceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tenantApps.clarify.marketplace'

    def ready(self):
        import tenantApps.clarify.marketplace.signals
