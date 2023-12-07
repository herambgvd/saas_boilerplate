import json

import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import IotGateway, IotDevice


# @receiver(post_save, sender=NVR)
# def createNvrProfile(sender, instance, **kwargs):
# 	nvr = instance
# 	if nvr.selectManufacturer == "Hikvision":
# 		try:
# 			fetchData = Client('http://' + str(nvr.ipAddress) + ":" + str(nvr.port), nvr.username, nvr.password)
# 			if fetchData:
# 				deviceResponse = fetchData.System.deviceInfo(method='get')
# 				hddResponse = fetchData.ContentMgmt.Storage.hdd(method='get')
# 				NVR.objects.filter(id=nvr.id).update(status=True)
# 				NVR.objects.filter(id=nvr.id).update(deviceID=deviceResponse["DeviceInfo"]["deviceID"])
# 				NVR.objects.filter(id=nvr.id).update(macAddress=deviceResponse["DeviceInfo"]["macAddress"])
# 				NVR.objects.filter(id=nvr.id).update(modelNo=deviceResponse["DeviceInfo"]["model"])
# 				NVR.objects.filter(id=nvr.id).update(hddType='SATA')
# 				hddList = hddResponse['hddList']['hdd']
# 				if isinstance(hddList, dict):
# 					NVR.objects.filter(id=nvr.id).update(
# 						hddCapacity={hddList['id']: float(hddList['capacity']) / 1000000})
# 					NVR.objects.filter(id=nvr.id).update(
# 						freeHdd={hddList['id']: float(hddList['freeSpace']) / 1000000})
# 				if isinstance(hddList, list):
# 					capacity = {}
# 					freeCapacity = {}
# 					for hdd in hddList:
# 						capacity[hdd['id']] = float(hdd['capacity']) / 1000000
# 						freeCapacity[hdd['id']] = float(hdd['freeSpace']) / 1000000
# 					NVR.objects.filter(id=nvr.id).update(
# 						hddCapacity=capacity)
# 					NVR.objects.filter(id=nvr.id).update(
# 						freeHdd=freeCapacity)
# 		except ValueError:
# 			print("Connection not establish")
# 			NVR.objects.filter(id=nvr.id).update(status=False)
# 	return "Done"


@receiver(post_save, sender=IotGateway)
def fetch_devices(sender, instance, created, **kwargs):
	if created:  # Only run when a new IotGateway is created and fetchDevice is False
		BASE_URL = f"http://{instance.gatewayIp}/api/devices"  # Build BASE_URL using the instance's IP
		LIMIT = 100
		headers = {
			'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJsb3JhLWFwcC1zZXJ2ZXIiLCJleHAiOjE3MDIwMzY2MTUsImlzcyI6ImxvcmEtYXBwLXNlcnZlciIsIm5iZiI6MTcwMTk1MDIxNSwic3ViIjoidXNlciIsInVzZXJuYW1lIjoiYXBpdXNlciJ9.4ZdpA_k01KPld-KWjiHX7TZ_3_8u56KlDaBUNtrOOug'
		}
		url = f"{BASE_URL}?limit={LIMIT}"
		response = requests.get(url, headers=headers, verify=False)
		response_data = json.loads(response.content.decode())
		devices = response_data.get('devices', [])
		print(f"Fetched devices from API: {devices}")

		for device in devices:
			devEUI = device['devEUI']
			name = device['name']
			description = device['description']
			# Check if device already exists
			existing_device = IotDevice.objects.filter(devEUI=devEUI).first()
			if existing_device:
				# Update the existing device if needed
				existing_device.name = name
				existing_device.description = description
				existing_device.save()
			else:
				# Create a new device
				IotDevice.objects.create(selectBranch=instance.selectBranch, selectGateway=instance, devEUI=devEUI,
				                         name=name, description=description)
		# After fetching all devices, update fetchDevice to True
		instance.fetchDevice = True
		instance.save()
