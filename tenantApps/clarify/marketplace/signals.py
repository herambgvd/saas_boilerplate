import requests
from django.db.models.signals import post_save
from django.dispatch import receiver

from tenantApps.common.branch.models import ConfigManager
from .models import MarketplaceFiles


@receiver(post_save, sender=MarketplaceFiles)
def startProcessing(sender, instance, created, **kwargs):
	aiServer = ConfigManager.objects.get(configName="ANALYSE")
	if created:  # Check if a new record was created
		marketplace_video = instance
		tenant_name = getattr(instance, 'tenant_name', None)
		apiServer = aiServer.configValue + 'video/analysis/stream/'
		videoPath = '{}'.format(marketplace_video.fileName.url)
		weightPath = '{}'.format(marketplace_video.selectMarketplace.weights.url)
		print(marketplace_video)
		# Data to be sent in POST request
		data = {
			'video_id': str(marketplace_video.id),
			'video_url': str(videoPath),
			'model_path': str(weightPath),
			'topic_name': marketplace_video.name.replace(" ", "-"),
			'tenant_name': tenant_name
		}
		print(data)
		# Send POST request to inference server
		response = requests.post(apiServer, json=data)
		if response.status_code == 200:
			print('Successfully sent')
		else:
			print('Failed sent')
		return 'Processing Done'
