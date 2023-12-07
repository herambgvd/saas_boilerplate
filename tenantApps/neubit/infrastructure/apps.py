from django.apps import AppConfig


class InfrastructureConfig(AppConfig):
	default_auto_field = 'django.db.models.BigAutoField'
	name = 'tenantApps.neubit.infrastructure'

	def ready(self):
		import tenantApps.neubit.infrastructure.signals