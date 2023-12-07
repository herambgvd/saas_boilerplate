from tenantApps.neubit.infrastructure.models import IotDevice

from tenantApps.neubit.monitoring.models import AM319


# R718N3, VS330)


def r718n3Parser(message_dict):
	if 'data' in message_dict:
		if 'Current1' in message_dict['data']:
			print("Current Calling")
			print(message_dict['data'])
			device_name = IotDevice.objects.get(name="R718N325")
			device = R718N3()
			device.selectIOT = device_name
			device.current1 = message_dict['data'].get('Current1') / 1000
			device.current2 = message_dict['data'].get('Current2') / 1000
			device.current3 = message_dict['data'].get('Current3') / 1000
			device.multiplier = message_dict['data'].get('Multiplier1')
			device.volt = message_dict['data'].get('Volt')
			device.save()
			print("Current Save")
		else:
			print("No Current1")
	else:
		print("Packet not from this parser")


def am319Parses(message_dict):
	if 'name' in message_dict and message_dict['name'] == "AM319":
		if 'co2' in message_dict:
			print("CO2 Calling")
			print(message_dict)
			device_name = IotDevice.objects.get(name="AM319")
			print(device_name)
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
			print("AM319 CO2 Save")
