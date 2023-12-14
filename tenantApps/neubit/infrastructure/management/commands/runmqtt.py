import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
	help = 'Starts the MQTT listener script'

	def handle(self, *args, **options):
		# Assuming mqtt.py is in the 'utility' folder
		script_path = os.path.join(os.path.dirname(__file__), '../../../../../utility/mqtt.py')
		os.system(f'python {script_path}')
