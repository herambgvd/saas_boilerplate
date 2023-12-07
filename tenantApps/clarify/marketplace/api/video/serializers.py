from rest_framework import serializers

from tenantApps.clarify.marketplace.models import MarketplaceFiles


class MarketplaceFilesSerializer(serializers.ModelSerializer):
	class Meta:
		model = MarketplaceFiles
		fields = ['status']
