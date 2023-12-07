import json
import logging
import os
import sys
import django

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print(project_path)
if project_path not in sys.path:
	sys.path.append(project_path)

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaaS_Boilerplate.settings')
django.setup()

import paho.mqtt.client as mqtt
from django_tenants.utils import tenant_context

# Import your Django models
from tenant.models import Client as Tenant

# MQTT settings
MQTT_BROKER = os.getenv("MQTT_BROKER", "64.227.130.161")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "/gvd/uplink"

# Configure logging
logging.basicConfig(level=logging.INFO)


def on_connect(client, userdata, flags, rc):
	logging.info("Connected with result code " + str(rc))
	client.subscribe(MQTT_TOPIC)


# Handle device-specific data processing
# This function should be implemented based on your specific requirements
def handle_device_data(tenant, message_dict):
	print(message_dict)


def on_message(client, userdata, msg):
	try:
		mqtt_message_str = msg.payload.decode('utf-8')
		message_dict = json.loads(mqtt_message_str)

		tenant_schema_name = message_dict.get('schema')
		print(message_dict)
		if tenant_schema_name:
			try:
				tenant = Tenant.objects.get(schema_name=tenant_schema_name)
				with tenant_context(tenant):
					handle_device_data(tenant, message_dict)
			except Tenant.DoesNotExist:
				logging.error(f"Tenant with schema {tenant_schema_name} does not exist.")
			except Exception as e:
				logging.error(f"Error processing message for tenant {tenant_schema_name}: {e}")
		else:
			logging.warning("Tenant schema name not provided in the message.")
	except json.JSONDecodeError as e:
		logging.error(f"JSON Decode Error: {e}")
	except Exception as e:
		logging.error(f"Unexpected error: {e}")


def main():
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message

	try:
		client.connect(MQTT_BROKER, MQTT_PORT, 60)
		client.loop_forever()
	except Exception as e:
		logging.error(f"Failed to connect to MQTT broker: {e}")


if __name__ == "__main__":
	main()
