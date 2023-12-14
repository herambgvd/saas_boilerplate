import json
import logging
import os
import sys

import django

project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
	sys.path.append(project_path)

# Set up the Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaaS_Boilerplate.settings')
django.setup()

import paho.mqtt.client as mqtt
from django_tenants.utils import tenant_context

# Import your Django models
from tenant.models import Client as Tenant
from tenantApps.neubit.infrastructure.models import IotDevice
from tenantApps.neubit.monitoring.models import AM319, GS301, EM400, VS121, EM300

# MQTT settings
MQTT_BROKER = os.getenv("MQTT_BROKER", "64.227.130.161")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "/gvd/uplink"

# Configure logging
logging.basicConfig(level=logging.INFO)


def on_connect(client, userdata, flags, rc):
	logging.info("Connected with result code " + str(rc))
	client.subscribe(MQTT_TOPIC)


############ Message Parsing Functions #########
def am319Parser(message_dict):
	if 'co2' in message_dict:
		print("CO2 Calling")
		device_name = IotDevice.objects.get(name=message_dict.get('deviceName'))
		device = AM319()
		device.selectIOT = device_name
		device.co2 = message_dict.get('co2')
		device.hcho = message_dict.get('hcho')
		device.humidity = message_dict.get('humidity')
		device.light_level = message_dict.get('light_level')
		device.pir_trigger = message_dict.get('pir_trigger')
		device.pm10 = message_dict.get('pm10')
		device.pm2_5 = message_dict.get('pm2_5')
		device.pressure = message_dict.get('pressure')
		device.temperature = message_dict.get('temperature')
		device.tvoc = message_dict.get('tvoc')
		device.save()
		print("AM319 Save")


def gs301Parser(message_dict):
	iot_device_instance = IotDevice.objects.get(
		name=message_dict.get('deviceName'))  # Replace 'some_id' with actual logic
	# Create a new instance of GS301
	gs301_instance = GS301(
		selectIOT=iot_device_instance,
		h2s=message_dict.get('h2s'),
		nh3=message_dict.get('nh3'),
		temperature=message_dict.get('temperature'),
		humidity=message_dict.get('humidity'),
	)

	# Save the instance to the database
	gs301_instance.save()
	print("GS301 Save")


def em400Parser(message_dict):
	iot_device_instance = IotDevice.objects.get(
		name=message_dict.get('deviceName'))  # Replace 'some_id' with actual logic
	# Create a new instance of EM400
	em400_instance = EM400(
		selectIOT=iot_device_instance,
		position=message_dict.get('position'),
		battery=message_dict.get('battery'),
		temperature=message_dict.get('temperature'),
	)
	em400_instance.save()
	print("EM400 Save")


def em300Parser(message_dict):
	iot_device_instance = IotDevice.objects.get(
		name=message_dict.get('deviceName'))  # Replace 'some_id' with actual logic
	# Create a new instance of EM300
	em300_instance = EM300(
		selectIOT=iot_device_instance,
		humidity=message_dict.get('humidity'),
		temperature=message_dict.get('temperature'),
	)
	em300_instance.save()
	print("EM300 Save")


def vs121Parser(message_dict):
	iot_device_instance = IotDevice.objects.get(
		name=message_dict.get('deviceName'))  # Replace 'some_id' with actual logic
	# Create a new instance of EM400
	vs121_instance = VS121(
		selectIOT=iot_device_instance,
		people_in=message_dict.get('people_in'),
		people_out=message_dict.get('people_out'),
	)
	vs121_instance.save()
	print("VS121 Save")


########### End Message Parser #################

# Handle device-specific data processing
# This function should be implemented based on your specific requirements
def handle_device_data(tenant, message_dict):
	print(message_dict)
	if message_dict.get('deviceName', '').startswith('GS301'):
		gs301Parser(message_dict)
	if message_dict.get('deviceName', '').startswith('EM400'):
		em400Parser(message_dict)
	if message_dict.get('deviceName', '').startswith('VS121'):
		vs121Parser(message_dict)
	if message_dict.get('deviceName', '').startswith('AM319'):
		am319Parser(message_dict)
	if message_dict.get('deviceName', '').startswith('EM300'):
		em300Parser(message_dict)


def on_message(client, userdata, msg):
	try:
		mqtt_message_str = msg.payload.decode('utf-8')
		message_dict = json.loads(mqtt_message_str)
		tenant_schema_name = message_dict.get('schema')
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
